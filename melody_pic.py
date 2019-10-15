#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo
import math
import os
import queue
import sys

SCALE_MAJOR_DIATONIC = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<11)


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

class MelodyPic:
    def __init__(self, D, scale=SCALE_MAJOR_DIATONIC, tonic=0):
        self.ctx = None

        self.notes = [(scale & 1<<(r%12) != 0) for r in range(tonic*7, tonic*7 + 12)]

        self.vstep = 14. * math.sqrt(5.)
        self.hstep = 14.
        self.width = 1200
        self.height = int(self.hstep * 27)

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
        x = self.hstep * (1 + n)
        y = self.height - self.hstep - ((n * 7 + 4) % 12) * self.vstep

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
        if is_pressed:
            self.ctx.arc(x, y, r + 2.0, 0, 2. * math.pi)
            self.ctx.set_line_width(6.0)
        else:
            self.ctx.arc(x, y, r, 0, 2. * math.pi)
            self.ctx.set_line_width(2.0)
        self.ctx.stroke()

        label = NOTE_NAMES[note]
        self.ctx.set_source_rgb(0.1, 0.1, 0.1)
        self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self.ctx.set_font_size(10)
        text_extents = self.ctx.text_extents(str(label))
        self.ctx.move_to(x - text_extents.width/2., y + text_extents.height/2.)
        self.ctx.show_text(str(label))

        self.ctx.restore()

    def draw_pitch_class(self, n):
        x = self.width + self.hstep * (n - 18)

        if ((n * 7 + 4) % 24) >= 12:
            return

        y = self.height - self.hstep - ((n * 7 + 4) % 12) * self.vstep

        R = [ 14, 10, 12, 10, 12, 12, 10, 14, 10, 12, 10, 12 ]
        r = R[n % 12]

        is_pressed = (self.pressed_classes[n % 12] != 0)

        self.ctx.save()

        if self.notes[n % 12]:
            color = self.get_color_from_note(n, 1.)
        else:
            color = self.get_color_from_note(n, .1)
        self.ctx.set_source_rgb(*color)
        self.ctx.arc(x, y, r, 0, 2. * math.pi)
        self.ctx.fill()

        if self.notes[n % 12] or is_pressed:
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

        label = NOTE_NAMES[n % 12]
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

        self.ctx.translate(0, 0)
        self.ctx.scale(1.0, 1.0)

        num_notes_in_screen = int(self.width / self.hstep) - 30

        # Horizontal lines
        for n in range(12):
            note = self.base_note + n
            y = self.height - self.hstep - ((n * 7 + 4) % 12) * self.vstep
            color = self.get_color_from_note(note, 1. if self.notes[note % 12] else 0.1)
            self.ctx.set_source_rgb(*color)
            self.ctx.move_to(0, y)
            self.ctx.line_to(self.width, y)
            self.ctx.stroke()

        # Vertical lines
        for n in range(num_notes_in_screen):
            note = self.base_note + n
            channel = self.pressed_notes[note].bit_length() - 1
            x = self.hstep * (1 + n)
            y = self.height - self.hstep - ((n * 7 + 4) % 12) * self.vstep
            if channel >= 0:
                self.ctx.set_source_rgb(*self.hsv_to_rgb(360. * ((channel*9)%16) / 16., 1.0, 0.6))
            else:
                self.ctx.set_source_rgb(0.8, 0.8, 0.8)
            self.ctx.move_to(x, self.height)
            self.ctx.line_to(x, y)
            self.ctx.stroke()

        # Notes
        for n in range(num_notes_in_screen):
            self.draw_note(n)

        # Pitch classes
        for n in range(-11, 18):
            self.draw_pitch_class(n)

    def press(self, num_key, channel, action=True):
        if action:
            self.pressed_notes[num_key] |= 1<<channel
            self.pressed_classes[num_key % 12] += 1
        else:
            self.pressed_notes[num_key] &= ~(1<<channel)
            self.pressed_classes[num_key % 12] -= 1

