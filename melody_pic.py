#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo
import math
import random
import os
import queue
import sys
import time

from MusicDefs import MusicDefs
from MusicScale import MusicScale
from GeneralMidi import MIDI_GM1_INSTRUMENT_NAMES, MIDI_PERCUSSION_NAMES
from SupportFunctions import hsv_to_rgb, lab_to_rgb, rgb_to_lab

SCALE_MAJOR_DIATONIC = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<11)

#PIANO_NOTE_NAMES = ['I', 'ii', 'II', 'iii', 'III', 'IV', 'v', 'V', 'vi', 'VI', 'vii', 'VII']
PIANO_NOTE_NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

NOTE_NAMES_BY_FIFTHS = [
    'Fo', 'Co', 'Go', 'Do', 'Ao', 'Eo', 'Bo',
    'Fb', 'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb',
    'F',  'C',  'G',  'D',  'A',  'E',  'B',
    'F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#',
    'Fx', 'Cx', 'Gx', 'Dx', 'Ax', 'Ex', 'Bx',
    'F&', 'C&', 'G&', 'D&', 'A&', 'E&', 'B&',
]

NOTE_MIDI_A4 = 69
NOTE_MIDI_C4 = 60

def seq_floats(start, stop, step=1):
    stop = stop - step;
    number = int(round((stop - start)/float(step)))

    if number > 1:
        return([start + step*i for i in range(number+1)])

    elif number == 1:
        return([start])

    else:
        return([])

fast = True

if fast:
    import OpenGL
    OpenGL.ERROR_CHECKING = False
    OpenGL.ERROR_LOGGING = False
    OpenGL.ERROR_ON_COPY = True
    OpenGL.STORE_POINTERS = False

class MelodyPic:
    def __init__(self, D, scale=SCALE_MAJOR_DIATONIC, tonic=0):
        self.ctx = None

        self.notes_in_scale = [(scale & 1<<(r%12) != 0) for r in range(tonic*7, tonic*7 + 12)]

        self.vstep = 10. * math.sqrt(5.)
        self.hstep = 10.

        min_height_chords = int(self.hstep * 27)

        self.width = 1280
        self.height = max(720, min_height_chords)

        self.change_root(0)

        self.fifths_vpos_offset = 5
        self.pitch_class_lower_limit = -13
        self.pitch_class_upper_limit = 19

        self.notes_active = [ 0 ] * 128
        self.pitch_classes_active = [ 0 ] * 12

        self.chord_pitch_classes = 0
        self.chords_found = []

        self.current_song = {}
        self.current_tick = 0
        self.current_tick_time = time.time()
        self.current_secs_per_tick = 1e10

        self.note_radius = [14.] * 12

    def get_vpos_from_note(self, note):
        return note * 7 + self.fifths_vpos_offset

    def get_color_from_note(self, note, saturation=1., value=1.):
        if note == -1:
            return (0.9, 0.9, 0.9)
        return hsv_to_rgb(360. * ((note*7)%12)/12., saturation, value)

    def get_color_from_channel(self, channel, saturation=1., value=1.):
        if channel == -1:
            return (0.9, 0.9, 0.9)
        return hsv_to_rgb(360. * ((channel*17)%32)/32., saturation, value)

    WHITE_KEYS = set([0, 2, 4, 5, 7, 9, 11])
    WHITE_KEY_WIDTH = 18.
    BLACK_KEY_WIDTH = WHITE_KEY_WIDTH * 7. / 12.
    OCTAVE_START = 2
    OCTAVE_END = 6 + 1

    def draw_time_lines(self):
        self.ctx.save()

        base_tick = self.current_tick + (time.time() - self.current_tick_time) / self.current_secs_per_tick

        y_min = 20
        y_max = self.height - 100 - 20

        pos = 0
        for n in range(12 * self.OCTAVE_START, 12 * (self.OCTAVE_END + 1)): # Octaves 2 to 5
            x = 9 + (pos + 0.5) * self.BLACK_KEY_WIDTH
            pos += 1

            self.ctx.move_to(x, y_min)
            self.ctx.set_source_rgb(0.5, 0.5, 0.5)
            self.ctx.line_to(x, y_max)
            self.ctx.stroke()

        x_min = 9 + 0.5 * self.BLACK_KEY_WIDTH
        x_max = 9 + (12*(self.OCTAVE_END - self.OCTAVE_START + 1) - 0.5) * self.BLACK_KEY_WIDTH

        n_ticks = 2000

        for t in range(n_ticks):
            try:
                if not self.current_song[int(base_tick + t)][0] is None:
                    y = y_max - t * (y_max - y_min) / n_ticks
                    self.ctx.move_to(x_min, y)
                    self.ctx.set_source_rgb(0.5, 0.5, 0.5)
                    self.ctx.line_to(x_max, y)
                    self.ctx.stroke()
            except (IndexError, KeyError):
                pass

        notes = []
        for a in self.notes_active:
            if a:
                v = [y_max if (a & 1<<c != 0) else None for c in range(16)]
            else:
                v = [ None ] * 16
            notes.append(v)

        for t in range(n_ticks):
            try:
                tick_data = self.current_song[int(base_tick + t)]
            except (IndexError, KeyError):
                continue
            y = y_max - t * (y_max - y_min) / n_ticks
            for (n_channel, n_note, n_program) in tick_data[3]:
                if notes[n_note][n_channel] is None:
                    notes[n_note][n_channel] = y
            for (n_channel, n_note) in tick_data[4]:
                if notes[n_note][n_channel] and n_note > self.OCTAVE_START * 12 and n_note < self.OCTAVE_END * 12:
                    x = 9 + ((n_note - self.OCTAVE_START * 12) + 0.5) * self.BLACK_KEY_WIDTH
                    self.ctx.move_to(x, notes[n_note][n_channel])
                    self.ctx.set_line_width(self.BLACK_KEY_WIDTH - 4)
                    self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                    color = self.get_color_from_channel(n_channel, 0.8)
                    self.ctx.set_source_rgba(*color, 0.5)
                    self.ctx.line_to(x, y)
                    self.ctx.stroke()
                notes[n_note][n_channel] = None

        self.ctx.restore()

    def draw_white_keys(self):
        pos = 0
        for n in range(12 * self.OCTAVE_START, 12 * (self.OCTAVE_END + 1)): # Octaves 2 to 5
            if not (n%12) in self.WHITE_KEYS:
                continue

            x1 = 9 + (pos) * self.WHITE_KEY_WIDTH
            x2 = 9 + (pos + 1) * self.WHITE_KEY_WIDTH
            pos += 1

            is_pressed = (self.notes_active[n] != 0)
            channel = self.notes_active[n].bit_length() - 1
            color = (1., 1., 1.)
            self.ctx.move_to(x1, self.height - 2)
            self.ctx.line_to(x2, self.height - 2)
            self.ctx.line_to(x2, self.height - 100)
            self.ctx.line_to(x1, self.height - 100)
            self.ctx.close_path()
            self.ctx.set_source_rgb(*color)
            if (n % 12) == self.root_note:
                self.ctx.set_source_rgb(1.0, 1.0, 0.8)
            self.ctx.fill_preserve()
            self.ctx.set_source_rgb(0.5, 0.5, 0.5)
            self.ctx.set_line_width(1)
            self.ctx.stroke()

            press_x = (x1 + x2) / 2.
            press_y = self.height - 10
            press_r = self.WHITE_KEY_WIDTH / 2

            if is_pressed:
                color = self.get_color_from_channel(channel, 0.5)
                self.ctx.set_source_rgb(*color)
                self.ctx.arc(press_x, press_y, press_r, 0, 2. * math.pi)
                self.ctx.fill()

            label = PIANO_NOTE_NAMES[n % 12]
            self.ctx.set_source_rgb(0., 0., 0.)
            self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            self.ctx.set_font_size(8)
            text_extents = self.ctx.text_extents(str(label))
            self.ctx.move_to(press_x - text_extents.width/2., press_y + text_extents.height/2.)
            self.ctx.show_text(str(label))

    def draw_black_keys(self):
        pos = 0
        for n in range(12 * self.OCTAVE_START, 12 * (self.OCTAVE_END + 1)): # Octaves 2 to 5
            x1 = 9 + (pos) * self.BLACK_KEY_WIDTH
            x2 = 9 + (pos + 1) * self.BLACK_KEY_WIDTH
            pos += 1

            if (n % 12) in self.WHITE_KEYS:
                continue

            is_pressed = (self.notes_active[n] != 0)
            channel = self.notes_active[n].bit_length() - 1
            color = (0., 0., 0.)
            self.ctx.move_to(x1, self.height - 50)
            self.ctx.line_to(x2, self.height - 50)
            self.ctx.line_to(x2, self.height - 100)
            self.ctx.line_to(x1, self.height - 100)
            self.ctx.close_path()
            self.ctx.set_source_rgb(*color)
            if (n % 12) == self.root_note:
                self.ctx.set_source_rgb(0., 0., 0.5)
            self.ctx.fill_preserve()
            self.ctx.set_source_rgb(0.5, 0.5, 0.5)
            self.ctx.set_line_width(1)
            self.ctx.stroke()

            press_x = (x1 + x2) / 2.
            press_y = self.height - 56
            press_r = self.BLACK_KEY_WIDTH / 2

            if is_pressed:
                color = self.get_color_from_channel(channel, 1.0, 0.5)
                self.ctx.set_source_rgb(*color)
                self.ctx.arc(press_x, press_y, press_r, 0, 2. * math.pi)
                self.ctx.fill()

            label = PIANO_NOTE_NAMES[n % 12]
            self.ctx.set_source_rgb(1., 1., 1.)
            self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            self.ctx.set_font_size(6)
            text_extents = self.ctx.text_extents(str(label))
            self.ctx.move_to(press_x - text_extents.width/2., press_y + text_extents.height/2.)
            self.ctx.show_text(str(label))

    CHORDS_INFO = [
        [
            # Nineth chords
            [ [], [0, 4, 7, 11, 14], "Major 9th Chord" ],
            [ [], [0, 4, 7, 10, 14], "Dominant 9th Chord" ],
            [ [], [0, 3, 7, 10, 14], "Minor 9th Chord" ],

            [ [], [0, 4, 7, 10, 15], "Major 7#9 Chord" ],
            [ [], [0, 4, 7, 10, 13], "Major 7b9 Chord" ],
            [ [], [0, 4, 7, 14],     "Major add9 Chord" ],
            [ [], [0, 3, 7, 14],     "Minor m(add9) Chord" ],

            # Tertian seventh chords: constructed using a sequence of major thirds and/or minor thirds
            [ [], [0, 4, 7, 11], "Major 7th Chord" ],
            [ [], [0, 3, 7, 10], "Minor 7th Chord" ],
            [ [], [0, 4, 7, 10], "Dominant 7th Chord" ],
            [ [], [0, 3, 6,  9], "Diminished 7th Chord" ],
            [ [], [0, 3, 6, 10], "Half-diminished 7th Chord" ],
            [ [], [0, 3, 7, 11], "Minor major 7th Chord" ],
            [ [], [0, 4, 8, 11], "Augmented major 7th Chord" ],
        ],
        [
            # Primary triads
            [ [], [0, 4, 7],  "Major Triad" ],
            [ [], [0, 3, 7],  "Minor Triad" ],
            [ [], [0, 3, 6],  "Diminished Triad" ],
            [ [], [0, 4, 8],  "Augmented Triad" ],
        ],
        [
            # Suspended triads
            [ [], [0, 2, 7],  "Sus2 Triad" ],
            [ [], [0, 5, 7],  "Sus4 Triad" ],

            [ [], [0, 7, 9],  "6Sus Triad" ],
            [ [], [0, 7, 10], "7Sus Triad" ],
        ],
    ]

    for chords_list in CHORDS_INFO:
        for chord_info in chords_list:
            if not chord_info[0]:
                chord_info[0] = [0] * 12
                for i in range(0, 12):
                    chord_mask = 0
                    for num_note in chord_info[1]:
                        chord_mask |= 1 << (i + num_note) % 12
                    chord_info[0][i] = chord_mask

    def check_chord(self, chord, note=(0,0,0)):
        base_note, base_x, base_y = note
        notes_in_scale = True
        for inc_note, inc_x, inc_y in chord:
            note_value = (base_note + self.get_note_from_coords(base_x + inc_x, base_y + inc_y) % 12)
            if not self.notes_in_scale[note_value]:
                notes_in_scale = False
            #print(f"{inc_note}, {inc_x}, {inc_y}: {note_value} -> {self.notes_in_scale[note_value]}")
        return notes_in_scale

    def get_chord_color(self, chord_root, chord_intervals):
        axis_lr = (sum(chord_intervals) / len(chord_intervals) - 11./3) / 13.5

        vdif = [(((c * 7) % 12) - c / 7.) * 7. / 24. for c in chord_intervals]
        axis_ud = sum(vdif) / len(vdif) * 3. / 5.

        nmaj = [(1./(n+1) if (j - i) == 4 else 0.) for n, (i, j) in enumerate(zip(chord_intervals[:-1], chord_intervals[1:]))]
        nmin = [(1./(n+1) if (j - i) == 3 else 0.) for n, (i, j) in enumerate(zip(chord_intervals[:-1], chord_intervals[1:]))]
        axis_mm = 5. * (sum(nmaj) - sum(nmin) ) / len(chord_intervals)

        chord_color = lab_to_rgb(75., (3 * axis_mm + axis_ud) * -20., axis_lr * 80.)
        return chord_color

    def get_vpos_from_pitch_class(self, note):
        return note * 7 + self.fifths_vpos_offset

    def draw_pitch_line(self, n1, n2):
        x1 = self.width + self.hstep * (n1 - self.pitch_class_upper_limit)
        y1 = self.height - self.hstep - (self.get_vpos_from_pitch_class(n1) % 24) * self.vstep
        x2 = self.width + self.hstep * (n2 - self.pitch_class_upper_limit)
        y2 = self.height - self.hstep - (self.get_vpos_from_pitch_class(n2) % 24) * self.vstep

        self.ctx.move_to(x1, y1)
        self.ctx.line_to(x2, y2)
        self.ctx.stroke()

    def draw_pitch_class_chords(self):
        self.ctx.save()

        for rel_note in range(self.pitch_class_lower_limit, self.pitch_class_upper_limit):
            if (self.get_vpos_from_pitch_class(rel_note) % 24) < 12:
                abs_pitch_class = (self.root_note + rel_note) % 12
                for chord_signature, chord_root, chord_name, chord_intervals in self.chords_found:
                    if abs_pitch_class == chord_root % 12:
                        #print("Found: {} on {} ({})".format(chord_name, self.note_names[chord_root % 12], chord_intervals))

                        pitch_classes_in_chord = set()
                        for d in chord_intervals:
                            for i in [-12, 0, 12]:
                                n = rel_note + d + i
                                if n >= self.pitch_class_lower_limit and n < self.pitch_class_upper_limit and (self.get_vpos_from_pitch_class(n) % 24) < 12:
                                    pitch_classes_in_chord.add(n)

                        #print(sorted(pitch_classes_in_chord))

                        if len(pitch_classes_in_chord) >= len(chord_intervals):
                            chord_color = self.get_chord_color(chord_root, chord_intervals)
                            self.ctx.set_source_rgb(*chord_color)
                            self.ctx.set_line_width(50.0)
                            self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)

                            n1 = None
                            for n2 in sorted(pitch_classes_in_chord):
                                if not n1 is None:
                                    self.draw_pitch_line(n1, n2)
                                n1 = n2

        self.ctx.restore()

    def get_color_from_pitch(self, note, saturation=1., value=1.):
        if note == -1:
            return (0.9, 0.9, 0.9)
        return hsv_to_rgb(360. * ((note*7)%12)/12., saturation, value)

    def is_pitch_class_visible(self, n):
        return n >= self.pitch_class_lower_limit and n < self.pitch_class_upper_limit and (self.get_vpos_from_pitch_class(n) % 24) < 18

    def get_pitch_class_label(self, n):
        return NOTE_NAMES_BY_FIFTHS[15 + ((n + self.root_note) * 7 + 7) % 24 - 7]

    def draw_pitch_class_note(self, n):
        if not self.is_pitch_class_visible(n):
            return

        x = self.width + self.hstep * (n - self.pitch_class_upper_limit)
        y = self.height - self.hstep - (self.get_vpos_from_pitch_class(n) % 24) * self.vstep

        r = self.note_radius[n % 12]

        is_pressed = (self.pitch_classes_active[(self.root_note + n) % 12] != 0)

        #self.ctx.save()

        if self.notes_in_scale[n % 12]:
            color = self.get_color_from_note((self.root_note + n) % 12, 1.)
        else:
            color = self.get_color_from_note((self.root_note + n) % 12, .1)
        self.ctx.set_source_rgb(*color)
        self.ctx.arc(x, y, r, 0, 2. * math.pi)
        self.ctx.fill()

        if self.notes_in_scale[n % 12] or is_pressed:
            self.ctx.set_source_rgb(0.3, 0.3, 0.3)
        else:
            self.ctx.set_source_rgb(0.6, 0.6, 0.6)
        if is_pressed:
            self.ctx.arc(x, y, r + 2.0, 0, 2. * math.pi)
            self.ctx.set_line_width(6.0)
        else:
            self.ctx.arc(x, y, r, 0, 2. * math.pi)
            self.ctx.set_line_width(2.0)
        self.ctx.stroke()
 
        if not (n % 12):
            self.ctx.set_source_rgb(0., 0., 0.)
            self.ctx.arc(x, y, r + 8., 0, 2. * math.pi)
            self.ctx.set_line_width(1.0)
            self.ctx.stroke()

        label = self.get_pitch_class_label(n)
        self.ctx.set_source_rgb(0.1, 0.1, 0.1)
        self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self.ctx.set_font_size(self.note_radius[n % 12] + 2)
        text_extents = self.ctx.text_extents(str(label))
        self.ctx.move_to(x - text_extents.width/2., y + text_extents.height/2.)
        self.ctx.show_text(str(label))

        #self.ctx.restore()

    def draw_pitch_class_notes(self):
        for n in range(self.pitch_class_lower_limit, self.pitch_class_upper_limit):
            self.draw_pitch_class_note(n)

    def draw_pitch_class_lines(self):
        for n in range(self.pitch_class_lower_limit, self.pitch_class_upper_limit):
            for d in [3, 4]:
                m = n - d
                if self.is_pitch_class_visible(n) and self.is_pitch_class_visible(m):
                    if self.notes_in_scale[n % 12] and self.notes_in_scale[m % 12]:
                        self.ctx.set_source_rgb(0.4, 0.4, 0.4)
                        self.ctx.set_line_width(2.0)
                    else:
                        self.ctx.set_source_rgb(0.8, 0.8, 0.8)
                        self.ctx.set_line_width(1.0)
                    self.draw_pitch_line(n, m)

        self.ctx.set_source_rgb(0.3, 0.3, 0.3)
        self.ctx.set_line_width(6.0)
        for n in range(self.pitch_class_lower_limit, self.pitch_class_upper_limit):
            if self.pitch_classes_active[(n + self.root_note) % 12] > 0 and self.is_pitch_class_visible(n):
                draw_fifth = True
                for d in [3, 4]:
                    if self.pitch_classes_active[(n + self.root_note - d) % 12] > 0 and self.is_pitch_class_visible(n - d):
                        self.draw_pitch_line(n, n - d)
                        draw_fifth = False
                if draw_fifth and self.pitch_classes_active[(n + self.root_note - 7) % 12] > 0 and self.is_pitch_class_visible(n - 7):
                    self.draw_pitch_line(n, n - 7)

    def draw_circle_of_fifths(self):
        self.ctx.save()

        cx = self.width - 32 * self.hstep / 2
        cy = (self.height - 2 * self.hstep - 16 * self.vstep) / 2

        cr = min(self.width - cx, cy) - 30

        nx = [cx + cr * math.sin(2. * math.pi * ((n * 7) % 12) / 12.) for n in range(12)]
        ny = [cy - cr * math.cos(2. * math.pi * ((n * 7) % 12) / 12.) for n in range(12)]

        for n1 in range(12):
            for n_inc in [3, 4, 5, 7]:
                n2 = (n1 + n_inc) % 12
                self.ctx.set_source_rgb(0.9, 0.9, 0.9)
                self.ctx.set_line_width(1.0)
                self.ctx.move_to(nx[n1], ny[n1])
                self.ctx.line_to(nx[n2], ny[n2])
                self.ctx.stroke()


        self.ctx.save()
        for chord_signature, chord_root, chord_name, chord_intervals in self.chords_found:
            if chord_intervals:
                chord_color = self.get_chord_color(chord_root, chord_intervals)
                self.ctx.set_source_rgb(*chord_color)
                self.ctx.set_line_width(50.0)
                self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                n1 = chord_root
                for d in chord_intervals + [chord_intervals[0]]:
                    n2 = (chord_root + d) % 12
                    self.ctx.move_to(nx[n1], ny[n1])
                    self.ctx.line_to(nx[n2], ny[n2])
                    self.ctx.stroke()
                    n1 = n2
        self.ctx.restore()


        for n1 in range(12):
            for n_inc in [3, 4]:
                n2 = (n1 + n_inc) % 12
                notes_in_scale = (self.notes_in_scale[n1] and self.notes_in_scale[n2])
                if notes_in_scale:
                    self.ctx.set_source_rgb(0.5, 0.5, 0.5)
                    self.ctx.set_line_width(2.0)
                    self.ctx.move_to(nx[n1], ny[n1])
                    self.ctx.line_to(nx[n2], ny[n2])
                    self.ctx.stroke()

        for n1 in range(12):
            for n_inc in [3, 4]:
                n2 = (n1 + n_inc) % 12
                notes_pressed = (self.pitch_classes_active[n1] > 0 and self.pitch_classes_active[n2] > 0)
                if notes_pressed:
                    self.ctx.set_source_rgb(0.3, 0.3, 0.3)
                    self.ctx.set_line_width(6.0)
                    self.ctx.move_to(nx[n1], ny[n1])
                    self.ctx.line_to(nx[n2], ny[n2])
                    self.ctx.stroke()


        for n in range(12):
            is_pressed = (self.pitch_classes_active[n % 12] != 0)

            if self.notes_in_scale[n % 12]:
                color = self.get_color_from_note(n % 12, 1.)
            else:
                color = self.get_color_from_note(n % 12, .1)

            self.ctx.set_source_rgb(*color)
            self.ctx.arc(nx[n], ny[n], self.note_radius[n], 0, 2. * math.pi)
            self.ctx.fill()

            if is_pressed:
                self.ctx.set_line_width(6.0)
            else:
                self.ctx.set_line_width(2.0)

            #self.ctx.move_to(x + self.note_radius[n], y)
            self.ctx.set_source_rgb(0.3, 0.3, 0.3)
            self.ctx.arc(nx[n], ny[n], self.note_radius[n], 0, 2. * math.pi)
            self.ctx.stroke()

            if (n % 12 == self.root_note):
                self.ctx.set_source_rgb(0., 0., 0.)
                self.ctx.arc(nx[n], ny[n], self.note_radius[n] + 6., 0, 2. * math.pi)
                self.ctx.set_line_width(1.0)
                self.ctx.stroke()

            label = PIANO_NOTE_NAMES[n % 12]
            self.ctx.set_source_rgb(0.1, 0.1, 0.1)
            self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            self.ctx.set_font_size(self.note_radius[n] + 2)
            text_extents = self.ctx.text_extents(str(label))
            self.ctx.move_to(nx[n] - text_extents.width/2., ny[n] + text_extents.height/2.)
            self.ctx.show_text(str(label))

        self.ctx.restore()

    def draw_pic(self, ctx):
        self.ctx = ctx

        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

        self.ctx.translate(0, 0)
        self.ctx.scale(1.0, 1.0)

        self.draw_white_keys()
        self.draw_black_keys()

        self.draw_time_lines()

        self.draw_pitch_class_chords()
        self.draw_pitch_class_lines()
        self.draw_pitch_class_notes()

        self.draw_circle_of_fifths()

    def press(self, num_key, channel, action=True, drums=False):
        if not drums:
            if action:
                self.notes_active[num_key] |= 1<<channel
                self.pitch_classes_active[num_key % 12] += 1
            else:
                self.notes_active[num_key] &= ~(1<<channel)
                self.pitch_classes_active[num_key % 12] -= 1

    def combine_chords(self, chords):
        if not chords:
            return chords

        combined_chords = []

        #for chord_signature, chord_root, chord_name, chord_intervals in chords:
        #    print(f"<<< Individual: {chord_signature:03x} ~ {chord_signature:012b}: {chord_root} {chord_name} {chord_intervals}")

        while chords:
            combined_signature, combined_root, combined_name, combined_intervals = chords.pop(0)
            print(f"Starting: {combined_signature:03x} ~ {combined_signature:012b}: {combined_root} {combined_name} {combined_intervals}")
            combined_intervals = set(combined_intervals)
            pending_chords = []
            while chords:
                if (combined_signature & chords[0][0]) == chords[0][0]:
                    print(f"Discarding: {chords[0][0]:03x} ~ {chords[0][0]:012b}: {chords[0][1]} {chords[0][2]} {chords[0][3]}")
                    chords.pop(0)
                elif (combined_signature & chords[0][0]) != 0:
                    chord_signature, chord_root, chord_name, chord_intervals = chords.pop(0)
                    print(f"Combining: {chord_signature:03x} ~ {chord_signature:012b}: {chord_root} {chord_name} {chord_intervals}")
                    combined_signature |= chord_signature
                    combined_intervals |= set([i + ((chord_root - combined_root) % 12) for i in chord_intervals])
                    combined_name += f" + {chord_name} on {chord_root}"
                else:
                    pending_chords.append(chords.pop(0))
            combined_chords.append((combined_signature, combined_root, combined_name, sorted(combined_intervals)))
            print(f"Final: {combined_signature:03x} ~ {combined_signature:012b}: {combined_root} {combined_name} {sorted(combined_intervals)}")
            chords = pending_chords

        for combined_signature, combined_root, combined_name, combined_intervals in combined_chords:
            print(f" >>> Combined: {combined_signature:03x} ~ {combined_signature:012b}: {combined_root} {combined_name} {combined_intervals}")
        return combined_chords

    def find_chords(self):
        chords_found = []

        #pitch_classes = 0
        #for num_note in range(0, 12):
        #    value = 1 << (num_note % 12)
        #    if self.pitch_classes_active[num_note] > 0:
        #        pitch_classes |= value

        pitch_classes = self.chord_pitch_classes
        comp_chord_signature = 0

        for chords_list in self.CHORDS_INFO:
            for n in range(12):
                for chord_signatures, chord_intervals, chord_name in chords_list:
                    note = (self.root_note + n * 7) % 12
                    chord_signature = chord_signatures[note]
                    if (pitch_classes & chord_signature) == chord_signature:
                        chords_found.append((chord_signature, note % 12, chord_name, chord_intervals))
                        #print("Found: {} on {} ({:012b} - {:012b} -> {:012b})".format(chord_name, self.note_names[note % 12],
                        #    pitch_classes, chord_signature, pitch_classes & ~chord_signature))
                        comp_chord_signature |= chord_signature
                        #pitch_classes &= ~chord_signature

        return self.combine_chords(chords_found)

    def set_tick(self, tick, secs_per_tick):
        self.current_tick = tick
        #self.current_secs_per_tick = secs_per_tick
        self.current_tick_time = time.time()

    def set_chord(self, chord=0):
        print(f"Pitch class histogram: {chord:#06x} = {chord:>012b}")

        self.chord_pitch_classes = chord
        self.chords_found = self.find_chords()
        print("{}".format(self.chords_found))

        self.note_radius = [12. if i else 10. for i in self.notes_in_scale]
        for chord_signature, chord_root, chord_name, chord_intervals in self.chords_found:
            if chord_intervals:
                self.note_radius[chord_root] = 24.

    def change_root(self, num_key, scale=None):
        self.root_note = (num_key % 12)
        self.scale = MusicScale(self.root_note)
        self.note_names = self.scale.getChromaticNoteNames()
        self.note_names_aug = self.scale.getChromaticAugmentedNoteNames()
        print(f"Root change: {self.note_names} , {self.note_names_aug}")

        if not scale is None:
            scale = ((scale << 12 | scale) >> ((12-num_key) % 12)) & 0xFFF
            self.notes_in_scale = [(scale & 1<<(r%12) != 0) for r in range(12)]
            print(f"{scale:03x} ~ {scale:012b} -> {self.notes_in_scale}")
            self.note_radius = [12. if i else 10. for i in self.notes_in_scale]
        else:
            self.note_radius = [12.] * 12

    def set_song_score(self, song):
        #print(song)
        self.current_song = song
