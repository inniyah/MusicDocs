from __future__ import print_function

import fluidsynth
import rtmidi
import mido
import time
import sys

from threading import Thread, Lock

from GeneralMidi import MIDI_GM1_INSTRUMENT_NAMES, MIDI_PERCUSSION_NAMES
from KeyFindingHMM import find_music_key, get_music_key_name, get_root_note_from_music_key, get_scale_from_music_key

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# See: The Cognition of Basic Musical Structures, by David Temperley, p. 180
# Basic primacy of the diatonic scale: all diatonic steps have higher values than chromatic ones
# All the diatonic degrees have a value of at least 3.5
# All the chromatic degrees have a value of 2.0, with the exception of vii
MUSIC_KEY_PROFILE_MAJOR = [ 5.0, 2.0, 3.5, 2.0, 4.5, 4.0, 2.0, 4.5, 2.0, 3.5, 1.5, 4.0 ] # Major scale
MUSIC_KEY_PROFILE_MINOR = [ 5.0, 2.0, 3.5, 4.5, 2.0, 4.0, 2.0, 4.5, 3.5, 2.0, 1.5, 4.0 ] # Harmonic minor scale

class FifoList():
    def __init__(self):
        self.data = {}
        self.nextin = 0
        self.nextout = 0
        self.lock = Lock()
    def append(self, data):
        try:
            self.lock.acquire()
            self.nextin += 1
            self.data[self.nextin] = data
        finally:
            self.lock.release()
    def pop(self):
        try:
            self.lock.acquire()
            self.nextout += 1
            result = self.data[self.nextout]
            del self.data[self.nextout]
        finally:
            self.lock.release()
        return result
    def peek(self):
        try:
            self.lock.acquire()
            result = self.data[self.nextout + 1] if self.data else None
        finally:
            self.lock.release()
        return result

class RandomSoundPlayer():
    def __init__(self, keyboard_handlers=None):
        self.keyboard_handlers = keyboard_handlers
        self.fs = fluidsynth.Synth()
        self.fs.start(driver="alsa")
        eprint("FluidSynth Started")
        self.sfid = self.fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
        self.fs.program_select(0, self.sfid, 0, 0)
    def __del__(self): # See:https://eli.thegreenplace.net/2009/06/12/safely-using-destructors-in-python/
        self.fs.delete()
        eprint("FluidSynth Closed")
        del self.fs
    def press(self, key, velocity=64, duration=0.5):
        self.fs.noteon(0, key + 19, velocity)
        if self.keyboard_handlers:
            for keyboard_handler in self.keyboard_handlers:
                keyboard_handler.press(key + 19, 1, True)
        time.sleep(duration)
        self.fs.noteoff(0, key + 19)
        if self.keyboard_handlers:
            for keyboard_handler in self.keyboard_handlers:
                keyboard_handler.press(key + 19, 1, False)
    @staticmethod
    def random_key(mean_key=44):
        x = random.gauss(mean_key, 10.0)
        if x < 1: x = 1
        elif x > 88: x = 88
        return int(round(x))
    @staticmethod
    def random_velocity():
        x = random.gauss(100.0, 10.0)
        if x < 1: x = 1
        elif x > 127: x = 127
        return int(round(x))
    @staticmethod
    def random_duration(self, mean_duration=2.0):
        x = random.gauss(mean_duration, 2.0)
        if x < 0.2: x = 0.2
        return x
    def random_play(self, num, mean_key, mean_duration):
        while num != 0:
            num -= 1
            key = self.random_key(mean_key)
            velocity = self.random_velocity()
            duration = self.random_duration(mean_duration)
            self.press(key, velocity, duration)
        #if self.keyboard_handler: self.keyboard_handler.show(False)

class MidiFileSoundPlayer():
    def __init__(self, filename, keyboard_handlers=None):
        self.keyboard_handlers = keyboard_handlers
        self.fs = fluidsynth.Synth()
        self.fs.start(driver="alsa")
        eprint("FluidSynth Started")
        self.sfid = self.fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
        for channel in range(0, 16):
            self.fs.program_select(channel, self.sfid, 0, 0)
        self.midi_file = mido.MidiFile(filename)
        eprint('Midi File: {}'.format(self.midi_file.filename))
        length = self.midi_file.length
        eprint('Song length: {} minutes, {} seconds'.format(int(length / 60), int(length % 60)))

        tempo = 500000
        ticks_per_beat = self.midi_file.ticks_per_beat
        time_signature_numerator = 4
        time_signature_denominator = 4
        clocks_per_click = 24

        count_ticks_in_total = 0
        count_ticks_in_beat = 0
        count_ticks_in_measure = 0
        num_bar = 1
        num_beat = 1
        current_beat_tick = 0
        pitch_classes_in_beat = 0

        # See: https://www.geeksforgeeks.org/python-find-the-closest-key-in-dictionary/
        self.chords_per_beat = {}

        scale_key = 0 # C
        scale_type = 0 # Major

        pitch_histogram_per_bar = []

        full_song = []

        pitch_histogram = [0] * 12
        self.instruments = set()
        for message in mido.midifiles.tracks.merge_tracks(self.midi_file.tracks):
            total_ticks_in_beat = ticks_per_beat * 4 / time_signature_denominator
            total_ticks_in_measure = ticks_per_beat * time_signature_numerator * 4 / time_signature_denominator
            time_of_measure = mido.midifiles.units.tick2second(total_ticks_in_measure, self.midi_file.ticks_per_beat, tempo)

            if isinstance(message, mido.Message):
                if message.type == 'note_on':
                    if message.channel != 9: # Exclude percussion 
                        pitch_histogram[message.note % 12] += 1
                        pitch_classes_in_beat |= 1 << (message.note % 12)
                elif message.type == 'note_off':
                    if message.channel != 9: # Exclude percussion 
                        pitch_histogram[message.note % 12] -= 1
                elif message.type == 'program_change':
                    self.instruments.add(message.program)

                count_ticks_in_total += message.time
                count_ticks_in_measure += message.time
                count_ticks_in_beat += message.time

            elif isinstance(message, mido.MetaMessage):
                if message.type == 'set_tempo':
                    tempo = message.tempo
                elif message.type == 'time_signature':
                    time_signature_numerator = message.numerator
                    time_signature_denominator = message.denominator
                    clocks_per_click = message.clocks_per_click
                    num_ticks = 0
                elif message.type == 'key_signature':
                    #music_key = message.key
                    eprint('Key signature changed to {}'.format(message.key))

            try:
                current_tick_in_song = full_song[count_ticks_in_total]
            except IndexError:
                full_song += [None] * (count_ticks_in_total - len(full_song) + 1)
                current_tick_in_song = []
                full_song[count_ticks_in_total] = current_tick_in_song

            while count_ticks_in_beat >= total_ticks_in_beat:
                num_beat += 1
                count_ticks_in_beat -= total_ticks_in_beat
                self.chords_per_beat[current_beat_tick] = pitch_classes_in_beat
                #current_tick_in_song[total_ticks_in_measure][2] = pitch_classes_in_beat
                eprint(f"beat@{count_ticks_in_total}: {num_beat}:{current_beat_tick} -> {pitch_classes_in_beat:#06x} = {pitch_classes_in_beat:>012b}")
                current_beat_tick = count_ticks_in_total
                pitch_classes_in_beat = sum([1 << (n % 12) if pitch_histogram[n] > 0 else 0 for n in range(12)])

            while count_ticks_in_measure >= total_ticks_in_measure:
                h = sum([1 << (n % 12) if pitch_histogram[n] > 0 else 0 for n in range(12)])
                pitch_histogram_per_bar.append(h)
                #current_tick_in_song[total_ticks_in_measure][1] = h
                eprint(f"Bar #{num_bar}: {pitch_histogram} ({time_of_measure:1f} s) -> {h:03x} ~ {h:012b}")
                num_bar += 1
                count_ticks_in_measure -= total_ticks_in_measure

        eprint(f"end@{count_ticks_in_total}: {num_beat}:{current_beat_tick} -> {pitch_classes_in_beat:#06x} = {pitch_classes_in_beat:>012b}")
        self.chords_per_beat[current_beat_tick] = pitch_classes_in_beat

        self.music_key_per_bar = find_music_key(pitch_histogram_per_bar)
        print(['{:03x}={}'.format(v, get_music_key_name(s)) for v, s in zip(pitch_histogram_per_bar, self.music_key_per_bar)])

        eprint(f"end: {pitch_histogram}")
        eprint([MIDI_GM1_INSTRUMENT_NAMES[i + 1] for i in self.instruments])

    def play(self):
        if self.midi_file.type == 2:
            # Can't merge tracks in type 2 (asynchronous) file
            return

        channel_programs = [0] * 16

        start_time = time.time() + 1.
        input_time = 0.0

        # The default tempo is 500000 microseconds per beat, which is 120 beats per minute (BPM)
        # You can use bpm2tempo() and tempo2bpm() to convert to and from beats per minute.
        # Note that tempo2bpm() may return a floating point number.
        tempo = 500000

        # Also called Pulses per Quarter note or PPQ. Typical values range from 96 to 480
        # You can use tick2second() and second2tick() to convert to and from seconds and ticks.
        # Note that integer rounding of the result might be necessary because MIDI files require ticks to be integers.
        ticks_per_beat = self.midi_file.ticks_per_beat

        # A Time Signature is two numbers, one on top of the other. The numerator describes the number of beats in a Bar,
        # while the denominator describes of what note value a beat is (ie, how many quarter notes there are in a beat).
        # If a time signature message is not present in a MIDI sequence, 4/4 signature is assumed.
        # 4/4 would be four quarter-notes per bar (MIDI default)
        # 4/2 would be four half-notes per bar (or 8 quarter notes)
        # 4/8 would be four eighth-notes per bar (or 2 quarter notes)
        # 2/4 would be two quarter-notes per bar
        time_signature_numerator = 4
        time_signature_denominator = 4

        # Metronome pulse in terms of the number of MIDI clock ticks per click
        # Assuming 24 MIDI clocks per quarter note, if the value of the sixth byte is 48, the metronome will click every
        # two quarter notes, or in other words, every half-note
        clocks_per_click = 24

        # Number of 32nd notes per beat. This byte is usually 8 as there is usually one quarter note per beat
        # and one quarter note contains eight 32nd notes.
        # It seems to be useless and unused in practice: https://www.midi.org/forum/473-smf-time-signature-confusion
        notated_32nd_notes_per_beat = 8

        count_ticks_in_total = 0
        count_ticks_in_beat = 0
        count_ticks_in_measure = 0
        num_bar = 1
        num_beat = 1

        pitch_classes_in_beat = self.chords_per_beat[0]
        music_key = self.music_key_per_bar[0]
        eprint(f"bar #1 (start) -> {get_music_key_name(music_key)}")
        if self.keyboard_handlers:
            for keyboard_handler in self.keyboard_handlers:
                keyboard_handler.change_root(get_root_note_from_music_key(music_key), get_scale_from_music_key(music_key))
                keyboard_handler.set_chord(pitch_classes_in_beat)

        eprint(f"beat@{count_ticks_in_total}: {num_beat} -> {pitch_classes_in_beat:#06x} = {pitch_classes_in_beat:>012b}")

        for message in mido.midifiles.tracks.merge_tracks(self.midi_file.tracks):
            total_ticks_in_beat = ticks_per_beat * 4 / time_signature_denominator
            total_ticks_in_measure = ticks_per_beat * time_signature_numerator * 4 / time_signature_denominator

            if message.time > 0:
                time_delta = mido.midifiles.units.tick2second(message.time, self.midi_file.ticks_per_beat, tempo)
            else:
                time_delta = 0

            input_time += time_delta
            playback_time = time.time() - start_time
            time_to_next_event = input_time - playback_time

            # Find bar:beat:subbeat

            if not isinstance(message, mido.MetaMessage):
                count_ticks_in_total += message.time
                count_ticks_in_measure += message.time
                count_ticks_in_beat += message.time

            while count_ticks_in_beat >= total_ticks_in_beat:
                num_beat += 1
                count_ticks_in_beat -= total_ticks_in_beat
                pitch_classes_in_beat = self.chords_per_beat[count_ticks_in_total]
                eprint(f"beat@{count_ticks_in_total}: {num_beat} -> {pitch_classes_in_beat:#06x} = {pitch_classes_in_beat:>012b}")
                for keyboard_handler in self.keyboard_handlers:
                    keyboard_handler.set_chord(pitch_classes_in_beat)

            while count_ticks_in_measure >= total_ticks_in_measure:
                try:
                    music_key = self.music_key_per_bar[num_bar-1]
                except IndexError:
                    music_key = None
                num_bar += 1
                count_ticks_in_measure -= total_ticks_in_measure
                if not music_key is None:
                    eprint(f"bar #{num_bar} -> {get_music_key_name(music_key)}")
                    if self.keyboard_handlers:
                        for keyboard_handler in self.keyboard_handlers:
                            keyboard_handler.change_root(get_root_note_from_music_key(music_key), get_scale_from_music_key(music_key))
                else:
                    eprint(f"bar #{num_bar}")

            if time_to_next_event > 0.0:
                time.sleep(time_to_next_event)

            current_timestamp = time.time_ns() / (10 ** 9) # Converted to floating-point seconds
            #sys.stdout.write(repr(message) + '\n')
            #sys.stdout.flush()
            if isinstance(message, mido.Message):
                if message.type == 'note_on':
                    self.fs.noteon(message.channel, message.note, message.velocity)
                    if self.keyboard_handlers:
                        for keyboard_handler in self.keyboard_handlers:
                            #self.last_notes.append((current_timestamp, message.note, message.channel, True))
                            keyboard_handler.press(message.note, message.channel, True, message.channel == 9)

                elif message.type == 'note_off':
                    self.fs.noteoff(message.channel, message.note)
                    if self.keyboard_handlers:
                        for keyboard_handler in self.keyboard_handlers:
                            #self.last_notes.append((current_timestamp, message.note, message.channel, False))
                            keyboard_handler.press(message.note, message.channel, False, message.channel == 9)

                elif message.type == 'control_change':
                    #eprint('Control {} for {} changed to {}'.format(message.control, message.channel, message.value))
                    pass

                elif message.type == 'program_change':
                    channel_programs[message.channel] = message.program
                    self.fs.program_select(message.channel, self.sfid, 0, message.program)
                    eprint('Program for {} changed to {} ("{}")'.format(message.channel, message.program, MIDI_GM1_INSTRUMENT_NAMES[message.program + 1]))

            elif isinstance(message, mido.MetaMessage):
                if message.type == 'set_tempo':
                    tempo = message.tempo
                    eprint('Tempo changed to {:.1f} BPM.'.format(mido.tempo2bpm(message.tempo)))
                elif message.type == 'time_signature':
                    time_signature_numerator = message.numerator
                    time_signature_denominator = message.denominator
                    clocks_per_click = message.clocks_per_click
                    notated_32nd_notes_per_beat = message.notated_32nd_notes_per_beat
                    num_ticks = 0
                    eprint(f'Time signature changed to {message.numerator}/{message.denominator}. Clocks per click: {message.clocks_per_click}, Notated 32nd Notes per_Beat: {message.notated_32nd_notes_per_beat}')
                elif message.type == 'key_signature':
                    eprint(f'Key signature changed to {message.key}')

        for keyboard_handler in self.keyboard_handlers:
            keyboard_handler.set_chord(0)

    def __del__(self): # See:https://eli.thegreenplace.net/2009/06/12/safely-using-destructors-in-python/
        self.fs.delete()
        eprint("FluidSynth Closed")
        del self.fs

class RtMidiSoundPlayer():
    def __init__(self, keyboard_handlers=None):
        self.keyboard_handlers = keyboard_handlers
        self.fs = fluidsynth.Synth()
        self.fs.start(driver="alsa")
        eprint("FluidSynth Started")
        self.sfid = self.fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
        #self.sfid = self.fs.sfload("OmegaGMGS2.sf2")
        #self.sfid = self.fs.sfload("GeneralUser GS 1.471/GeneralUser GS v1.471.sf2")
        #self.sfid = self.fs.sfload("fonts/Compifont_13082016.sf2")
        self.fs.program_select(0, self.sfid, 0, 0)

        self.pitch_classes_active = [ 0 ] * 12
        self.pitch_classes_in_chord = 0

        self.midi_in = rtmidi.MidiIn()
        available_ports = self.midi_in.get_ports()
        if available_ports:
            midi_port_num = 1
            try:
                self.midi_in_port = self.midi_in.open_port(midi_port_num)
            except rtmidi.InvalidPortError:
                eprint("Failed to open MIDI input")
                self.midi_in_port = None
                return
            eprint("Using MIDI input Interface {}: '{}'".format(midi_port_num, available_ports[midi_port_num]))
        else:
            eprint("Creating virtual MIDI input.")
            self.midi_in_port = self.midi_in.open_virtual_port("midi_driving_in")

        self.midi_in.set_callback(self.midi_received)

    def __del__(self): # See:https://eli.thegreenplace.net/2009/06/12/safely-using-destructors-in-python/
        self.fs.delete()
        eprint("FluidSynth Closed")
        del self.fs

    def midi_received(self, midi_event, data=None):
        current_timestamp = time.time_ns() / (10 ** 9) # Converted to floating-point seconds
        midi_msg, delta_time = midi_event
        if len(midi_msg) > 2:
            pressed = (midi_msg[2] != 0)
            note = midi_msg[1]
            pitch_class = midi_msg[1] % 12
            octave = midi_msg[1] // 12
            channel = 16

            if pressed:
                self.pitch_classes_active[note % 12] += 1
                self.pitch_classes_in_chord |= 1 << (note % 12)
            else:
                self.pitch_classes_active[note % 12] -= 1
                if self.pitch_classes_active[note % 12] == 0:
                    self.pitch_classes_in_chord &= ~(1 << (note % 12))

            #eprint("%s" % ((pressed, note, octave, pitch_class),))

            if pressed: # A note was hit
                if self.keyboard_handlers:
                    for keyboard_handler in self.keyboard_handlers:
                        keyboard_handler.press(midi_msg[1], channel, True)
                        keyboard_handler.set_chord(self.pitch_classes_in_chord)
                        #keyboard_handler.change_root(midi_msg[1])

            else: # A note was released
                if self.keyboard_handlers:
                    for keyboard_handler in self.keyboard_handlers:
                        keyboard_handler.press(midi_msg[1], channel, False)
                        keyboard_handler.set_chord(self.pitch_classes_in_chord)
                        #pass
