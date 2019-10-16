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

        self.notes_in_scale = [(scale & 1<<(r%12) != 0) for r in range(tonic*7, tonic*7 + 12)]

        self.vstep = 14. * math.sqrt(5.)
        self.hstep = 14.
        self.width = 1400
        self.height = int(self.hstep * 27)

        self.root_note = 0
        self.fifths_offset = 5
        self.notes_active = [ 0 ] * 128
        self.pitch_classes_active = [ 0 ] * 12

    def check_chord(self, chord, note=(0,0,0)):
        base_note, base_x, base_y = note
        notes_in_scale = True
        for inc_note, inc_x, inc_y in chord:
            note_value = (base_note + self.get_note_from_coords(base_x + inc_x, base_y + inc_y) % 12)
            if not self.notes_in_scale[note_value]:
                notes_in_scale = False
            #print(f"{inc_note}, {inc_x}, {inc_y}: {note_value} -> {self.notes_in_scale[note_value]}")
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

    def get_vpos_from_note(self, note):
        return note * 7 + self.fifths_offset

    def get_color_from_note(self, note, saturation=1., value=1.):
        if note == -1:
            return (0.9, 0.9, 0.9)
        return self.hsv_to_rgb(360. * ((note*7)%12)/12., saturation, value)

    def get_color_from_channel(self, channel, saturation=1., value=1.):
        if channel == -1:
            return (0.9, 0.9, 0.9)
        return self.hsv_to_rgb(360. * ((channel*17)%32)/32., saturation, value)

    def draw_note(self, n):
        note = n % 12
        x = self.hstep * (1 + n)
        y = self.height - self.hstep - (self.get_vpos_from_note(n) % 12) * self.vstep

        R = [ 14, 10, 12, 10, 12, 12, 10, 14, 10, 12, 10, 12 ]
        r = R[note]

        is_pressed = (self.notes_active[n] != 0)

        #self.ctx.save()

        if self.notes_in_scale[note]:
            color = self.get_color_from_note(note, 1.)
        else:
            color = self.get_color_from_note(note, .1)
        self.ctx.set_source_rgb(*color)
        self.ctx.arc(x, y, r, 0, 2. * math.pi)
        self.ctx.fill()

        if self.notes_in_scale[note] or is_pressed:
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

        #self.ctx.restore()

    WHITE_KEYS = set([0, 2, 4, 5, 7, 9, 11])
    WHITE_KEY_WIDTH = 18.
    BLACK_KEY_WIDTH = WHITE_KEY_WIDTH * 7. / 12.
    OCTAVE_START = 2 - 1
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
            self.ctx.fill_preserve()
            if (n % 12) == 0:
                self.ctx.set_source_rgb(0.0, 0.0, 0.0)
            else:
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

            if (n%12) in self.WHITE_KEYS:
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
            self.ctx.fill_preserve()
            self.ctx.set_source_rgb(0.5, 0.5, 0.5)
            self.ctx.set_line_width(1)
            self.ctx.stroke()

            press_x = (x1 + x2) / 2.
            press_y = self.height - 56
            press_r = self.BLACK_KEY_WIDTH / 2

            if is_pressed:
                color = self.get_color_from_channel(channel, 0.5)
                self.ctx.set_source_rgb(*color)
                self.ctx.arc(press_x, press_y, press_r, 0, 2. * math.pi)
                self.ctx.fill()

            label = NOTE_NAMES[n % 12]
            self.ctx.set_source_rgb(0., 0., 0.)
            self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            self.ctx.set_font_size(6)
            text_extents = self.ctx.text_extents(str(label))
            self.ctx.move_to(press_x - text_extents.width/2., press_y + text_extents.height/2.)
            self.ctx.show_text(str(label))

    def draw_chords(self):
        # Chords
        self.ctx.save()
        for n in range(-13, 19):
            for d in [3, 4]:
                n2 = n - d
                if n2 >= -13 and (self.get_vpos_from_pitch_class(n) % 24) < 12 and (self.get_vpos_from_pitch_class(n2) % 24) < 12:
                    if self.pitch_classes_active[(self.root_note + n) % 12] > 0 and self.pitch_classes_active[(self.root_note + n2) % 12] > 0:
                        self.ctx.set_source_rgb(0.7, 0.7, 0.7)

                        self.ctx.set_line_width(50.0)
                        self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)

                        self.draw_pitch_line(n, n2)
        self.ctx.restore()

    def get_vpos_from_pitch_class(self, note):
        return note * 7 + self.fifths_offset

    def get_color_from_pitch(self, note, saturation=1., value=1.):
        if note == -1:
            return (0.9, 0.9, 0.9)
        return self.hsv_to_rgb(360. * ((note*7)%12)/12., saturation, value)

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
            for d in [3, 4, 7]:
                n2 = n - d
                if n2 >= -13 and (self.get_vpos_from_pitch_class(n) % 24) < 12 and (self.get_vpos_from_pitch_class(n2) % 24) < 12:
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
#                self.ctx.set_source_rgb(*self.hsv_to_rgb(360. * ((channel*9)%16) / 16., 1.0, 0.6))
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


    def press(self, num_key, channel, action=True):
        if action:
            self.notes_active[num_key] |= 1<<channel
            self.pitch_classes_active[num_key % 12] += 1
        else:
            self.notes_active[num_key] &= ~(1<<channel)
            self.pitch_classes_active[num_key % 12] -= 1

