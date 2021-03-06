#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo
import math
import os
import queue
import sys

SCALE_MAJOR_DIATONIC = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<11)

CHORDS_INFO = [
    # Tertian seventh chords: constructed using a sequence of major thirds and/or minor thirds
    [ [], (0, 4, 7, 11), "Major seventh Chord" ],
    [ [], (0, 3, 7, 10), "Minor seventh Chord" ],
    [ [], (0, 4, 7, 10), "Dominant seventh Chord" ],
    [ [], (0, 3, 6,  9), "Diminished seventh Chord" ],
    [ [], (0, 3, 6, 10), "Half-diminished seventh Chord" ],
    [ [], (0, 3, 7, 11), "Minor major seventh Chord" ],
    [ [], (0, 4, 8, 11), "Augmented major seventh Chord" ],

    # Non-tertian seventh chords: constructed using augmented or diminished thirds
    [ [], (0, 4, 8, 10), "Augmented minor seventh Chord" ],
    [ [], (0, 3, 6, 11), "Diminished major seventh Chord" ],
    [ [], (0, 4, 6, 10), "Dominant seventh flat five Chord" ],
    [ [], (0, 4, 6, 11), "Major seventh flat five Chord" ],

    # Primary triads
    [ [], (0, 4, 7),  "Major Triad" ],
    [ [], (0, 3, 7),  "Minor Triad" ],
    [ [], (0, 3, 6),  "Diminished Triad" ],
    [ [], (0, 4, 8),  "Augmented Triad" ],

#    # Suspended triads
    [ [], (0, 2, 7),  "Sus2 Triad" ],
    [ [], (0, 5, 7),  "Sus4 Triad" ],
]

for chord_info in CHORDS_INFO:
    if not chord_info[0]:
        chord_info[0] = [0] * 12
        for i in range(0, 12):
            chord_mask = 0
            for num_note in chord_info[1]:
                chord_mask |= 1 << (i + num_note) % 12
            chord_info[0][i] = chord_mask

NOTE_NAMES = ['I', 'ii', 'II', 'iii', 'III', 'IV', 'v', 'V', 'vi', 'VI', 'vii', 'VII']

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

class TestPic:
    def __init__(self, D, scale=SCALE_MAJOR_DIATONIC, tonic=0):
        self.ctx = None

        self.notes = [(scale & 1<<(r%12) != 0) for r in range(tonic*7, tonic*7 + 12)]

        for chord_signatures, chord_intervals, chord_name in CHORDS_INFO:
            for num_signature, chord_signature in enumerate(chord_signatures):
                if (scale & chord_signature) == chord_signature:
                    print("Chord: {} on {}".format(chord_name, NOTE_NAMES[(num_signature) % 12]))

        self.width = 1200
        self.height = 800
        self.vstep = 14. * math.sqrt(5.)
        self.hstep = 14.

        self.base_note = NOTE_MIDI_C4 - 12 * 2
        self.pressed_notes = [ 0 ] * 128
        self.pressed_classes = [ 0 ] * 12

    def check_chord(self, chord, note=(0,0,0)):
        base_note, base_x, base_y = note
        notes_in_scale = True
        for inc_note, inc_x, inc_y in chord:
            note_value = (base_note + self.get_note_from_coords(base_x + inc_x, base_y + inc_y) % 12)
            if not self.notes[note_value]:
                notes_in_scale = False
            #print(f"{inc_note}, {inc_x}, {inc_y}: {note_value} -> {self.notes[note_value]}")
        return notes_in_scale

    def draw_circle_of_fifths(self):
        self.ctx.save()

        self.ctx.set_source_rgb(1, 0, 0)
        self.ctx.set_line_width(0.06)
        self.ctx.arc(0, 0, self.D * .4, 0, 2. * math.pi)

        self.ctx.set_line_width(0.04)
        self.ctx.stroke()

        self.ctx.restore()

    def hsv_to_rgb(self, hue, saturation=1., value=1.):
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

    def get_color_from_note(self, note, saturation=1., value=1.):
        if note == -1:
            return (0.9, 0.9, 0.9)
        return self.hsv_to_rgb(360. * ((note*7)%12)/12., saturation, value)

    def draw_note(self, n):
        note = (self.base_note + n) % 12
        x = self.hstep * (1 + n) - self.width / 2.
        y = self.height / 2 - self.hstep - ((n * 7 + 4) % 24) * self.vstep

        R = [ 14, 10, 12, 10, 12, 12, 10, 14, 10, 12, 10, 12 ]
        r = R[note]

        is_pressed = (self.pressed_notes[self.base_note + n] != 0)

        self.ctx.save()

        if self.notes[note]:
            color = self.get_color_from_note(note, 1.)
        else:
            color = self.get_color_from_note(note, .1)
        self.ctx.set_source_rgb(*color)
        self.ctx.arc(x, y, r, 0, 2. * math.pi)
        self.ctx.fill()

        if self.notes[note] or is_pressed:
            self.ctx.set_source_rgb(0.3, 0.3, 0.3)
        else:
            self.ctx.set_source_rgb(0.6, 0.6, 0.6)
        self.ctx.arc(x, y, r, 0, 2. * math.pi)
        if is_pressed:
            self.ctx.set_line_width(4.0)
        else:
            self.ctx.set_line_width(2.0)
        self.ctx.stroke()

        if self.pressed_classes[note] != 0:
            self.ctx.set_line_width(4.0)
            self.ctx.arc(x, y, r + 4, 0, 2. * math.pi)
            self.ctx.stroke()

        label = NOTE_NAMES[note]
        self.ctx.set_source_rgb(0.1, 0.1, 0.1)
        self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self.ctx.set_font_size(10)
        text_extents = self.ctx.text_extents(str(label))
        self.ctx.move_to(x - text_extents.width/2., y + text_extents.height/2.)
        self.ctx.show_text(str(label))

        self.ctx.restore()

    def draw_pic(self, ctx):
        self.ctx = ctx

        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

        self.ctx.translate(self.width // 2, self.height // 2)
        self.ctx.scale(1.0, 1.0)

        # Vertical lines
        for n in range(24):
            note = self.base_note + n
            y = self.height / 2 - self.hstep - ((n * 7 + 4) % 24) * self.vstep
            color = self.get_color_from_note(note, 1. if self.notes[note % 12] else 0.1)
            self.ctx.set_source_rgb(*color)
            self.ctx.move_to(self.width/2, y)
            self.ctx.line_to(-self.width/2, y)
            self.ctx.stroke()

        # Horizontal lines
        for n in range(int(self.width / self.hstep) - 1):
            note = self.base_note + n
            channel = self.pressed_notes[note].bit_length() - 1
            x = self.hstep * (1 + n) - self.width / 2.
            if channel >= 0:
                self.ctx.set_source_rgb(*self.hsv_to_rgb(360. * ((channel*9)%16) / 16., 1.0, 0.6))
            else:
                self.ctx.set_source_rgb(0.8, 0.8, 0.8)
            self.ctx.move_to(x, self.height/2)
            self.ctx.line_to(x, -self.height/2)
            self.ctx.stroke()

        # Notes
        for n in range(int(self.width / self.hstep) - 1):
            self.draw_note(n)

    def press(self, num_key, channel, action=True):
        if action:
            self.pressed_notes[num_key] |= 1<<channel
            self.pressed_classes[num_key % 12] += 1
        else:
            self.pressed_notes[num_key] &= ~(1<<channel)
            self.pressed_classes[num_key % 12] -= 1

