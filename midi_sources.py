from __future__ import print_function

import fluidsynth
import rtmidi
import mido
import time
import sys

from threading import Thread, Lock

from GeneralMidi import MIDI_GM1_INSTRUMENT_NAMES, MIDI_PERCUSSION_NAMES

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

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

        eprint('Ticks per Beat: {}'.format(self.midi_file.ticks_per_beat))

        self.pitch_histograms = []
        self.instruments = set()
        eprint('Tracks:')
        for i, track in enumerate(self.midi_file.tracks):
            num_ticks = 0
            pitch_histogram = [0] * 12
            eprint('  {:2d}: {!r} ({} messages)'.format(i, track.name.strip(), len(track)))
            for message in track:
                if isinstance(message, mido.Message):
                    if message.type == 'note_on':
                        pitch_histogram[message.note % 12] += 1
                        #eprint(message)
                        pass
                    elif message.type == 'note_off':
                        #eprint(message)
                        pass
                    elif message.type == 'program_change':
                        self.instruments.add(message.program)

                if not isinstance(message, mido.MetaMessage):
                    num_ticks += message.time

            self.pitch_histograms.append(pitch_histogram)
        eprint(self.pitch_histograms)
        eprint([MIDI_GM1_INSTRUMENT_NAMES[i + 1] for i in self.instruments])

        #self.last_notes = FifoList()

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
        notated_32nd_notes_per_beat = 8

        num_ticks = 0
        num_bar = 1
        num_beat = 1

        for message in mido.midifiles.tracks.merge_tracks(self.midi_file.tracks):
            ticks_in_measure = ticks_per_beat * time_signature_numerator * notated_32nd_notes_per_beat / time_signature_denominator / 2

            if message.time > 0:
                time_delta = mido.midifiles.units.tick2second(message.time, self.midi_file.ticks_per_beat, tempo)
            else:
                time_delta = 0

            input_time += time_delta
            playback_time = time.time() - start_time
            time_to_next_event = input_time - playback_time

            # Find bar:beat:subbeat

            if time_to_next_event > 0.0:
                time.sleep(time_to_next_event)

            if not isinstance(message, mido.MetaMessage):
                num_ticks += message.time

            while num_ticks >= ticks_in_measure:
                num_bar += 1
                num_ticks -= ticks_in_measure
                eprint(f"{num_bar}")

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
                    eprint('Control {} for {} changed to {}'.format(message.control, message.channel, message.value))

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
                    eprint('Time signature changed to {}/{}. Clocks per click: {}'.format(message.numerator, message.denominator, message.clocks_per_click))
                elif message.type == 'key_signature':
                    eprint('Key signature changed to {}'.format(message.key))

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
        self.fs.program_select(0, self.sfid, 0, 0)

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

            #eprint("%s" % ((pressed, note, octave, pitch_class),))

            if pressed: # A note was hit
                if self.keyboard_handlers:
                    for keyboard_handler in self.keyboard_handlers:
                        keyboard_handler.press(midi_msg[1], 16, True)
                        #keyboard_handler.change_root(midi_msg[1])

            else: # A note was released
                if self.keyboard_handlers:
                    for keyboard_handler in self.keyboard_handlers:
                        keyboard_handler.press(midi_msg[1], 16, False)
