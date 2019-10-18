#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo
import math
import random
import os
import queue
import sys

from general_midi import MIDI_GM1_INSTRUMENT_NAMES, MIDI_PERCUSSION_NAMES

SCALE_MAJOR_DIATONIC = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<11)

NOTE_NAMES = ['I', 'ii', 'II', 'iii', 'III', 'IV', 'v', 'V', 'vi', 'VI', 'vii', 'VII']

FIFTHS_NAMES = [
    'Fb', 'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb',
    'F',  'C',  'G',  'D',  'A',  'E',  'B',
    'F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#',
    'Fx', 'Cx', 'Gx', 'Dx', 'Ax', 'Ex', 'Bx',
]

DIATONIC_SCALE_POS = [ 0, 7, 2, 9, 4, -1, 6, 1, 8, 3, 10, 5 ]

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

def hsv_to_rgb(hue, saturation=1., value=1.):
    h = float(hue)
    s = float(saturation)
    v = float(value)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    return r, g, b

def lab_to_rgb(l, a, b):
    y = (l + 16.) / 116.
    x = a / 500. + y
    z = y - b / 200.

    x = 0.95047 * ((x * x * x) if (x * x * x > 0.008856) else ((x - 16./116.) / 7.787))
    y = 1.00000 * ((y * y * y) if (y * y * y > 0.008856) else ((y - 16./116.) / 7.787))
    z = 1.08883 * ((z * z * z) if (z * z * z > 0.008856) else ((z - 16./116.) / 7.787))

    r = x *  3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y *  1.8758 + z *  0.0415
    b = x *  0.0557 + y * -0.2040 + z *  1.0570

    r = (1.055 * (r**(1./2.4)) - 0.055) if (r > 0.0031308) else (12.92 * r)
    g = (1.055 * (g**(1./2.4)) - 0.055) if (g > 0.0031308) else (12.92 * g)
    b = (1.055 * (b**(1./2.4)) - 0.055) if (b > 0.0031308) else (12.92 * b)

    return [ max(0., min(1., r)), max(0., min(1., g)), max(0., min(1., b)) ]

def rgb_to_lab(r, g, b):
    r = ((r + 0.055) / 1.055)**2.4 if (r > 0.04045) else (r / 12.92);
    g = ((g + 0.055) / 1.055)**2.4 if (g > 0.04045) else (g / 12.92);
    b = ((b + 0.055) / 1.055)**2.4 if (b > 0.04045) else (b / 12.92);

    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047;
    y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.00000;
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883;

    x = x**(1./3.) if (x > 0.008856) else (7.787 * x) + 16/116.0;
    y = y**(1./3.) if (y > 0.008856) else (7.787 * y) + 16/116.0;
    z = z**(1./3.) if (z > 0.008856) else (7.787 * z) + 16/116.0;

    return [(116. * y) - 16., 500. * (x - y), 200. * (y - z)]

class MelodyPic:
    def __init__(self, D, scale=SCALE_MAJOR_DIATONIC, tonic=0):
        self.ctx = None

        self.notes_in_scale = [(scale & 1<<(r%12) != 0) for r in range(tonic*7, tonic*7 + 12)]

        self.vstep = 14. * math.sqrt(5.)
        self.hstep = 14.

        min_height_chords = int(self.hstep * 27)

        self.width = 1280
        self.height = max(720, min_height_chords)

        self.root_note = 0
        self.note_names_base_pos = [0, -5, 2, -3, 4, 5, -6, 7, -4, 9, -2, 11][self.root_note]
        self.note_names = [FIFTHS_NAMES[8 + self.note_names_base_pos + p] for p in DIATONIC_SCALE_POS] 
        print(self.note_names)

        self.fifths_vpos_offset = 5

        self.notes_active = [ 0 ] * 128
        self.pitch_classes_active = [ 0 ] * 12

    def draw_circle_of_fifths(self):
        self.ctx.save()

        self.ctx.set_source_rgb(1, 0, 0)
        self.ctx.set_line_width(0.06)
        self.ctx.arc(0, 0, self.D * .4, 0, 2. * math.pi)

        self.ctx.set_line_width(0.04)
        self.ctx.stroke()

        self.ctx.restore()

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

#    def draw_note(self, n):
#        note = n % 12
#        x = self.hstep * (1 + n)
#        y = self.height - self.hstep - (self.get_vpos_from_note(n) % 12) * self.vstep
#
#        R = [ 14, 10, 12, 10, 12, 12, 10, 14, 10, 12, 10, 12 ]
#        r = R[note]
#
#        is_pressed = (self.notes_active[n] != 0)
#
#        #self.ctx.save()
#
#        if self.notes_in_scale[note]:
#            color = self.get_color_from_note(note, 1.)
#        else:
#            color = self.get_color_from_note(note, .1)
#        self.ctx.set_source_rgb(*color)
#        self.ctx.arc(x, y, r, 0, 2. * math.pi)
#        self.ctx.fill()
#
#        if self.notes_in_scale[note] or is_pressed:
#            self.ctx.set_source_rgb(0.3, 0.3, 0.3)
#        else:
#            self.ctx.set_source_rgb(0.6, 0.6, 0.6)
#        if is_pressed:
#            self.ctx.arc(x, y, r + 2.0, 0, 2. * math.pi)
#            self.ctx.set_line_width(6.0)
#        else:
#            self.ctx.arc(x, y, r, 0, 2. * math.pi)
#            self.ctx.set_line_width(2.0)
#        self.ctx.stroke()
#
#        label = self.note_names[note]
#        self.ctx.set_source_rgb(0.1, 0.1, 0.1)
#        self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
#        self.ctx.set_font_size(10)
#        text_extents = self.ctx.text_extents(str(label))
#        self.ctx.move_to(x - text_extents.width/2., y + text_extents.height/2.)
#        self.ctx.show_text(str(label))
#
#        #self.ctx.restore()

    WHITE_KEYS = set([0, 2, 4, 5, 7, 9, 11])
    WHITE_KEY_WIDTH = 18.
    BLACK_KEY_WIDTH = WHITE_KEY_WIDTH * 7. / 12.
    OCTAVE_START = 2
    OCTAVE_END = 6 + 1

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
                self.ctx.set_source_rgb(1.0, 1.0, 0.9)
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

            label = NOTE_NAMES[n % 12]
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

            label = NOTE_NAMES[n % 12]
            self.ctx.set_source_rgb(1., 1., 1.)
            self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            self.ctx.set_font_size(6)
            text_extents = self.ctx.text_extents(str(label))
            self.ctx.move_to(press_x - text_extents.width/2., press_y + text_extents.height/2.)
            self.ctx.show_text(str(label))

    CHORDS_INFO = [
        [
            # Tertian seventh chords: constructed using a sequence of major thirds and/or minor thirds
            [ [], (0, 4, 7, 11), "Major 7th Chord" ],
            [ [], (0, 3, 7, 10), "Minor 7th Chord" ],
            [ [], (0, 4, 7, 10), "Dominant 7th Chord" ],
            [ [], (0, 3, 6,  9), "Diminished 7th Chord" ],
            [ [], (0, 3, 6, 10), "Half-diminished 7th Chord" ],
            [ [], (0, 3, 7, 11), "Minor major 7th Chord" ],
            [ [], (0, 4, 8, 11), "Augmented major 7th Chord" ],
        ],
        [
            # Primary triads
            [ [], (0, 4, 7),  "Major Triad" ],
            [ [], (0, 3, 7),  "Minor Triad" ],
            [ [], (0, 3, 6),  "Diminished Triad" ],
            [ [], (0, 4, 8),  "Augmented Triad" ],
        ],
        [
            # Suspended triads
            [ [], (0, 2, 7),  "Sus2 Triad" ],
            [ [], (0, 5, 7),  "Sus4 Triad" ],

            [ [], (0, 7, 9),  "6Sus Triad" ],
            [ [], (0, 7, 10), "7Sus Triad" ],
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

    def find_chords(self):
        chords_found = []

        pitch_classes = 0
        for num_note in range(0, 12):
            value = 1 << (num_note % 12)
            if self.pitch_classes_active[num_note] > 0:
                pitch_classes |= value

        for chords_list in self.CHORDS_INFO:
            for n in range(12):
                for chord_signatures, chord_intervals, chord_name in chords_list:
                    note = (self.root_note + n * 7) % 12
                    chord_signature = chord_signatures[note]
                    if (pitch_classes & chord_signature) == chord_signature:
                        chords_found.append((note % 12, chord_name, chord_intervals))
                        #print("Found: {} on {} ({:04x} - {:04x} -> {:04x})".format(chord_name, self.note_names[note % 12],
                        #    pitch_classes, chord_signature, pitch_classes & ~chord_signature))
                        pitch_classes &= ~chord_signature

        return chords_found

    def draw_chords(self):
        chords_found = self.find_chords()
        self.ctx.save()

        #print("{}".format(chords_found))
        for n in range(-13, 19):
            if (self.get_vpos_from_pitch_class(n) % 24) < 12:
                note = (self.root_note + n) % 12
                for chord_root, chord_name, chord_intervals in chords_found:
                    if note == chord_root % 12:
                        #print("Found: {} on {} ({})".format(chord_name, self.note_names[chord_root % 12], chord_intervals))
                        pitch_classes_in_chord = set()
                        for d in chord_intervals:
                            if (n + d) >= -13 and (n + d) < 19 and (self.get_vpos_from_pitch_class(n + d) % 24) < 12:
                                pitch_classes_in_chord.add(n + d)
                            if (n + d - 12) >= -13 and (n + d - 12) < 19 and (self.get_vpos_from_pitch_class(n + d - 12) % 24) < 12:
                                pitch_classes_in_chord.add(n + d - 12)

                        if len(pitch_classes_in_chord) == len(chord_intervals):
                            axis_lr = (sum(pitch_classes_in_chord) / len(pitch_classes_in_chord) - 11./3) / 13.5

                            vdif = [(((c * 7 + self.fifths_vpos_offset) % 12) - self.fifths_vpos_offset - c / 7.) * 7. / 24. for c in pitch_classes_in_chord]
                            axis_ud = sum(vdif) / len(vdif) * 3. / 5.

                            nmaj = [(1./(n+1) if (j - i) == 4 else 0.) for n, (i, j) in enumerate(zip(chord_intervals[:-1], chord_intervals[1:]))]
                            nmin = [(1./(n+1) if (j - i) == 3 else 0.) for n, (i, j) in enumerate(zip(chord_intervals[:-1], chord_intervals[1:]))]
                            axis_mm = 5. * (sum(nmaj) - sum(nmin) ) / len(chord_intervals)

                            chord_color = lab_to_rgb(75., (3 * axis_mm + axis_ud) * -20., axis_lr * 80.)

                            self.ctx.set_source_rgb(*chord_color)
                            self.ctx.set_line_width(50.0)
                            self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                            #print(pitch_classes_in_chord)
                            n1 = None
                            for n2 in sorted(pitch_classes_in_chord):
                                if not n1 is None:
                                    self.draw_pitch_line(n1, n2)
                                n1 = n2

        self.ctx.restore()

    def get_vpos_from_pitch_class(self, note):
        return note * 7 + self.fifths_vpos_offset

    def get_color_from_pitch(self, note, saturation=1., value=1.):
        if note == -1:
            return (0.9, 0.9, 0.9)
        return hsv_to_rgb(360. * ((note*7)%12)/12., saturation, value)

    def draw_pitch_line(self, n1, n2):
        x1 = self.width + self.hstep * (n1 - 19)
        y1 = self.height - self.hstep - (self.get_vpos_from_pitch_class(n1) % 12) * self.vstep
        x2 = self.width + self.hstep * (n2 - 19)
        y2 = self.height - self.hstep - (self.get_vpos_from_pitch_class(n2) % 12) * self.vstep

        #self.ctx.save()

        self.ctx.move_to(x1, y1)
        self.ctx.line_to(x2, y2)
        self.ctx.stroke()

        #self.ctx.restore()

    def draw_pitch_class(self, n):
        if (self.get_vpos_from_pitch_class(n) % 24) >= 12:
            return

        x = self.width + self.hstep * (n - 19)
        y = self.height - self.hstep - (self.get_vpos_from_pitch_class(n) % 12) * self.vstep

        R = [ 14, 10, 12, 10, 12, 12, 10, 14, 10, 12, 10, 12 ]
        r = R[n % 12]

        is_pressed = (self.pitch_classes_active[(self.root_note + n) % 12] != 0)

        #self.ctx.save()

        if self.notes_in_scale[n % 12]:
            color = self.get_color_from_note(n, 1.)
        else:
            color = self.get_color_from_note(n, .1)
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

        label = NOTE_NAMES[n % 12]
        #label = self.note_names[n % 12]
        self.ctx.set_source_rgb(0.1, 0.1, 0.1)
        self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self.ctx.set_font_size(10)
        text_extents = self.ctx.text_extents(str(label))
        self.ctx.move_to(x - text_extents.width/2., y + text_extents.height/2.)
        self.ctx.show_text(str(label))

        #self.ctx.restore()

    def draw_pitch_classes(self):
        # Pitch classes
        for n in range(-13, 19):
            c = 0
            for d in [3, 4, 7]:
                if d == 7 and c >= 0:
                    continue
                n2 = n - d
                if n2 >= -13 and (self.get_vpos_from_pitch_class(n) % 24) < 12 and (self.get_vpos_from_pitch_class(n2) % 24) < 12:
                    c += 1
                    if self.notes_in_scale[n % 12] and self.notes_in_scale[n2 % 12]:
                        self.ctx.set_source_rgb(0.4, 0.4, 0.4)
                        self.ctx.set_line_width(2.0)
                    else:
                        self.ctx.set_source_rgb(0.8, 0.8, 0.8)
                        self.ctx.set_line_width(1.0)

                    if self.pitch_classes_active[(n + self.root_note) % 12] > 0 and self.pitch_classes_active[(n2 + self.root_note) % 12] > 0:
                        self.ctx.set_source_rgb(0.4, 0.4, 0.4)
                        self.ctx.set_line_width(6.0)

                    self.draw_pitch_line(n, n2)

        # Pitch classes
        for n in range(-13, 19):
            self.draw_pitch_class(n)

    def draw_pic(self, ctx):
        self.ctx = ctx

        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

        self.ctx.translate(0, 0)
        self.ctx.scale(1.0, 1.0)

        self.draw_white_keys()
        self.draw_black_keys()

#        num_notes_in_screen = int(self.width / self.hstep) - 34

#        # Connection between fiths
#        for n in range(num_notes_in_screen - 1):
#            x = self.hstep * (1 + n)
#            y = self.height - self.hstep - (self.get_vpos_from_note(n) % 12) * self.vstep
#            x2 = self.hstep * (1 + (n+1))
#            y2 = self.height - self.hstep - (self.get_vpos_from_note(n+1) % 12) * self.vstep
#            self.ctx.set_source_rgb(0.95, 0.95, 0.95)
#            self.ctx.move_to(x, y)
#            self.ctx.line_to(x2, y2)
#            self.ctx.stroke()

#        # Horizontal lines
#        for n in range(12):
#            y = self.height - self.hstep - (self.get_vpos_from_note(n) % 12) * self.vstep
#            color = self.get_color_from_note(n, 1. if self.notes_in_scale[n % 12] else 0.2)
#            self.ctx.set_source_rgb(*color)
#            self.ctx.move_to(0, y)
#            self.ctx.line_to(self.width, y)
#            self.ctx.stroke()

#        # Vertical lines
#        base_note = NOTE_MIDI_C4 - 12 * 2 
#        for n in range(num_notes_in_screen):
#            note = base_note + n
#            channel = self.notes_active[note].bit_length() - 1
#            x = self.hstep * (1 + n)
#            y = self.height - self.hstep - (self.get_vpos_from_note(n) % 12) * self.vstep
#            if channel >= 0:
#                self.ctx.set_source_rgb(*hsv_to_rgb(360. * ((channel*9)%16) / 16., 1.0, 0.6))
#            else:
#                self.ctx.set_source_rgb(0.8, 0.8, 0.8)
#            self.ctx.move_to(x, self.height)
#            self.ctx.line_to(x, y)
#            self.ctx.stroke()

#        # Notes
#        for n in range(num_notes_in_screen):
#            self.draw_note(n)

        self.draw_chords()
        self.draw_pitch_classes()


    def press(self, num_key, channel, action=True, drums=False):
        if not drums:
            if action:
                self.notes_active[num_key] |= 1<<channel
                self.pitch_classes_active[num_key % 12] += 1
            else:
                self.notes_active[num_key] &= ~(1<<channel)
                self.pitch_classes_active[num_key % 12] -= 1

