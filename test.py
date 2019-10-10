#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo
import math
import queue

SCALE_MAJOR_DIATONIC = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<11)
SCALE_MAJOR_MELODIC  = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<10)

#MAIN_TRIADS = [
#    [(0, 0, 0), (4, 0, -1), (7, 1,  0)], # Major triad
#    [(0, 0, 0), (3, 1,  1), (7, 1,  0)], # Minor triad
#    [(0, 0, 0), (4, 0, -1), (8, 0, -2)], # Augmented triad
#    [(0, 0, 0), (3, 1,  1), (6, 2,  2)], # Diminished triad
#]

CHORDS_INFO = [
    # Tertian seventh chords: constructed using a sequence of major thirds and/or minor thirds
    [ [], ((0, 0, 0), (4, 0, -1), (7, 1,  0), (11, 1, -1)), "Major seventh Chord" ],
    [ [], ((0, 0, 0), (3, 1,  1), (7, 1,  0), (10, 2,  1)), "Minor seventh Chord" ],
    [ [], ((0, 0, 0), (4, 0, -1), (7, 1,  0), (10, 2,  1)), "Dominant seventh Chord" ],
    [ [], ((0, 0, 0), (3, 1,  1), (6, 2,  2), (9,  3,  0)), "Diminished seventh Chord" ],
    [ [], ((0, 0, 0), (3, 1,  1), (6, 2,  2), (10, 2,  1)), "Half-diminished seventh Chord" ],
    [ [], ((0, 0, 0), (3, 1,  1), (7, 1,  0), (11, 1, -1)), "Minor major seventh Chord" ],
    [ [], ((0, 0, 0), (4, 0, -1), (8, 0, -2), (11, 1, -1)), "Augmented major seventh Chord" ],

    # Non-tertian seventh chords: constructed using augmented or diminished thirds
    #[ [], ((0, 0, 0), (4, 0, -1), (8, 0, -2), (10, 2, -2)), "Augmented minor seventh Chord" ],
    #[ [], ((0, 0, 0), (3, 1,  1), (6, 2,  2), (11, 1, -1)), "Diminished major seventh Chord" ],
    #[ [], ((0, 0, 0), (4, 0, -1), (6, 2, -1), (10, 2,  1)), "Dominant seventh flat five Chord" ],
    #[ [], ((0, 0, 0), (4, 0, -1), (6, 2,  2), (11, 1, -1)), "Major seventh flat five Chord" ],

    # Primary triads
    [ [], ((0, 0, 0), (4, 0, -1), (7, 1,  0)),  "Major Triad" ],
    [ [], ((0, 0, 0), (3, 1,  1), (7, 1,  0)),  "Minor Triad" ],
    [ [], ((0, 0, 0), (3, 1,  1), (6, 2,  2)),  "Diminished Triad" ],
    [ [], ((0, 0, 0), (4, 0, -1), (8, 0, -2)),  "Augmented Triad" ],

    # Suspended triads
    #[ [], ((0, 0, 0), (2,  2, 0), (7, 1,  0)),  "Sus2 Triad" ],
    #[ [], ((0, 0, 0), (5, -1, 0), (7, 1,  0)),  "Sus4 Triad" ],
]

NOTE_NAMES = ['I', 'ii', 'II', 'iii', 'III', 'IV', 'v', 'V', 'vi', 'VI', 'vii', 'VII']

def seq_floats(start, stop, step=1):
    stop = stop - step;
    number = int(round((stop - start)/float(step)))

    if number > 1:
        return([start + step*i for i in range(number+1)])

    elif number == 1:
        return([start])

    else:
        return([])

class TestPic:
    def __init__(self, D, scale=SCALE_MAJOR_DIATONIC, tonic=0):
        self.ctx = None

        self.notes = [(scale & 1<<(r%12) != 0) for r in range(tonic*7, tonic*7 + 12)]

        self.width = 1200
        self.height = 800
        self.step = 30

    def check_chord(self, chord, note=(0,0,0)):
        base_note, base_x, base_y = note
        notes_in_scale = True
        for inc_note, inc_x, inc_y in chord:
            note_value = (base_note + self.get_note_from_coords(base_x + inc_x, base_y + inc_y) % 12)
            if not self.notes[note_value]:
                notes_in_scale = False
            #print(f"{inc_note}, {inc_x}, {inc_y}: {note_value} -> {self.notes[note_value]}")
        return notes_in_scale

    def get_note_from_coords(self, u, v):
        return (int(u * 7 + v * 4) % 12)

    def get_position_from_coords(self, u, v):
        x = 7 * u + 4 * v
        y = - 4 * v - u
        return (self.step * x / math.sqrt(5.), self.step * y)

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

    def draw_note(self, note, x, y):
        note = note % 12
        self.ctx.save()

        color = self.get_color_from_note(note, 1. if self.notes[note] else 0.1)
        self.ctx.set_source_rgb(*color)
        self.ctx.arc(x, y, 12, 0, 2. * math.pi)
        self.ctx.fill()

        self.ctx.set_source_rgb(0.3, 0.3, 0.3)
        self.ctx.arc(x, y, 12, 0, 2. * math.pi)
        self.ctx.set_line_width(2.0)
        self.ctx.stroke()

        label = NOTE_NAMES[note]
        self.ctx.set_source_rgb(0.1, 0.1, 0.1)
        self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self.ctx.set_font_size(10)
        text_extents = self.ctx.text_extents(str(label))
        self.ctx.move_to(x - text_extents.width/2., y + text_extents.height/2.)
        self.ctx.show_text(str(label))

        #sublabel = f"({note})"
        #text_extents = self.ctx.text_extents(str(sublabel))
        #self.ctx.move_to(x - text_extents.width/2., y + text_extents.height*3.5/2.)
        #self.ctx.set_font_size(10)
        #self.ctx.show_text(str(sublabel))

        self.ctx.restore()

    def draw_pic(self, ctx):
        self.ctx = ctx

        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

        self.ctx.translate(self.width // 2, self.height // 2)

#        for v in range(-3, 4):
#            for u in range(-2 - v//2 - 5, 3 - v // 2 + 5):
#                note = self.get_note_from_coords(u, v)
#                x, y = self.get_position_from_coords(u, v)
#                self.ctx.set_source_rgb(0.8, 0.8, 0.8)
#                self.ctx.move_to(self.width/2, y)
#                self.ctx.line_to(-self.width/2, y)
#                self.ctx.stroke()
#                self.ctx.move_to(x, self.height/2)
#                self.ctx.line_to(x, -self.height/2)
#                self.ctx.stroke()

        n = 3
        for y in seq_floats(0, self.height/2 + self.step, self.step):
                color = self.get_color_from_note(n, 1. if self.notes[n] else 0.05)
                self.ctx.set_source_rgb(*color)
                self.ctx.move_to(self.width/2, y)
                self.ctx.line_to(-self.width/2, y)

                color = self.get_color_from_note(11-n, 1. if self.notes[(11-n)%12] else 0.05)
                self.ctx.set_source_rgb(*color)
                self.ctx.move_to(self.width/2, -y)
                self.ctx.line_to(-self.width/2, -y)
                self.ctx.stroke()
                n = (n + 7) % 12

        for x in seq_floats(0, self.width/2 + self.step / math.sqrt(5.), self.step / math.sqrt(5.)):
                self.ctx.set_source_rgb(0.8, 0.8, 0.8)
                self.ctx.move_to(x, self.height/2)
                self.ctx.line_to(x, -self.height/2)
                self.ctx.move_to(-x, self.height/2)
                self.ctx.line_to(-x, -self.height/2)
                self.ctx.stroke()

        for v in range(-3, 4):
            for u in range(-2 - v//2 - 5, 3 - v // 2 + 5):
                note = self.get_note_from_coords(u, v)
                x, y = self.get_position_from_coords(u, v)
                #if v > 0:
                #    y += 10 * 27
                y = ((19 + y/self.step) % 24) * self.step - 11 * self.step
                self.draw_note(note, x, y)

        #self.ctx.set_source_rgb(0.1, 0.1, 0.1)
        #self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        #self.ctx.set_font_size(13)
        #self.ctx.move_to(20, 30)
        #self.ctx.show_text("Hello, World!")

def main():
    import ctypes
    import time

    from pyglet import app, clock, font, gl, image, window

    from MusicDefs import MusicDefs

    pic = TestPic(D=100, scale=SCALE_MAJOR_DIATONIC, tonic=1)

    window = window.Window(width=pic.width, height=pic.height)
    #ft = font.load('Arial', 24)
    #text = font.Text(ft, 'Hello World')

    # create data shared by ImageSurface and Texture
    data = (ctypes.c_ubyte * (pic.width * pic.height * 4))()
    stride = pic.width * 4
    surface = cairo.ImageSurface.create_for_data (data, cairo.FORMAT_ARGB32, pic.width, pic.height, stride); 
    texture = image.Texture.create_for_size(gl.GL_TEXTURE_2D, pic.width * pic.height, gl.GL_RGBA)

    def update_surface(dt, surface):
        ctx = cairo.Context(surface)
        pic.draw_pic(ctx)

    @window.event
    def on_draw():
        window.clear()

        gl.glEnable(gl.GL_TEXTURE_2D)

        gl.glBindTexture(gl.GL_TEXTURE_2D, texture.id)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, pic.width, pic.height, 0, gl.GL_BGRA, gl.GL_UNSIGNED_BYTE, data)

        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2f(0.0, 1.0)
        gl.glVertex2i(0, 0)
        gl.glTexCoord2f(1.0, 1.0)
        gl.glVertex2i(pic.width, 0)
        gl.glTexCoord2f(1.0, 0.0)
        gl.glVertex2i(pic.width, pic.height)
        gl.glTexCoord2f(0.0, 0.0)
        gl.glVertex2i(0, pic.height)
        gl.glEnd()

        #text.draw()

        #print('FPS: %f' % clock.get_fps())

    clock.schedule_interval(update_surface, 1/120.0, surface)
    app.run()

if __name__ == '__main__':
    main()
