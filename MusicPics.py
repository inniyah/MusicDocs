#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo
import math

SCALE_MAJOR_DIATONIC = (1<<0) + (1<<2) + (1<<4) + (1<<5) + (1<<7) + (1<<9) + (1<<11)
SCALE_MAJOR_MELODIC  = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<10)

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

    # Suspended triads
    [ [], (0, 2, 7),  "Sus2 Triad" ],
    [ [], (0, 5, 7),  "Sus4 Triad" ],
]

CHROMATIC_NOTES = ['C', 'Db/C#', 'D', 'Eb/D#', 'E', 'F', 'Gb/F#', 'G', 'Ab/G#', 'A', 'Bb/A#', 'B']

for chord_info in CHORDS_INFO:
    if not chord_info[0]:
        chord_info[0] = [0] * 12
        for i in range(0, 12):
            chord_mask = 0
            for num_note in chord_info[1]:
                chord_mask |= 1 << (i + num_note) % 12
            chord_info[0][i] = chord_mask

class HexagonalLayoutPic:
    def __init__(self, D, scale=SCALE_MAJOR_DIATONIC, h = 4):
        self.ctx = None

        self.notes = [(scale & 1<<r != 0) for r in range(12)]

        # diameter of hexagon in pixels
        self.D = D

        self.vnum = h * 2 + 1
        self.hnum = 13

        # vectorial distance to next hexagon in row
        self.shift_x = (math.sqrt(3)*D/2., 0)

        # vectorial distance to hexagon in next row
        self.shift_y = (math.sqrt(3)*D/4., 3*D/4.)

        # width of surface plus some border in pixels
        self.width = int((self.hnum + 2) * math.sqrt(3)*D/2. + 3*D/4.) + 1

        # height of surface plus some border in pixels
        self.height = int(self.vnum * 3*D/4. + 2*D) + 1

        self.field_colors = ((1, 0.5, 1), (0.5, 1, 1), (0.8, 0, 0.8), (0, 0.8, 0.8))

        self.hexagon_points = (
            ( math.sqrt(3)*D/4.,  D/4.),
            (                0.,  D/2.),
            (-math.sqrt(3)*D/4.,  D/4.),
            (-math.sqrt(3)*D/4., -D/4.),
            (                0., -D/2.),
            ( math.sqrt(3)*D/4., -D/4.)
        )

        for chord_signatures, chord_intervals, chord_name in CHORDS_INFO:
            for num_signature, chord_signature in enumerate(chord_signatures):
                if (scale & chord_signature) == chord_signature:
                    print("Chord: {} on {}".format(chord_name, CHROMATIC_NOTES[(num_signature) % 12]))

    def draw_hexagon(self, color, label):
        self.ctx.move_to(self.hexagon_points[0][0], self.hexagon_points[0][1])
        for pair in self.hexagon_points:
            self.ctx.line_to(pair[0], pair[1])
        self.ctx.close_path()
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.stroke_preserve()
        self.ctx.set_source_rgb(*self.field_colors[color])
        self.ctx.fill()

        text_extents = self.ctx.text_extents(str(label))
        self.ctx.move_to(-text_extents.width/2, text_extents.height/2)
        self.ctx.set_source_rgb(0.1, 0.1, 0.1)
        self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self.ctx.set_font_size(11)
        self.ctx.show_text(str(label))

    def draw_pic(self, ctx):
        self.ctx = ctx

        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

        self.ctx.translate(2. * math.sqrt(3) * self.D/4., self.D)

        ix_offset = int(self.hnum/2)
        iy_offset = int(self.vnum/2)
        for vpos in range(self.vnum):
            hexagons_in_line = self.hnum + (vpos%2)
            for hpos in range(hexagons_in_line):
                ix = int(hpos) - ix_offset
                iy = int(vpos) - iy_offset
                if vpos%2:
                    n = (int(ix * 7 - (iy+1)/2 + 9) % 12)
                else:
                    n = (int(ix * 7 - iy/2) % 12)
                self.ctx.translate(self.shift_x[0], self.shift_x[1])
                self.draw_hexagon(self.notes[n] + 2*(iy != 0), f"{n} ({ix},{iy})")
            self.ctx.translate(-hexagons_in_line * self.shift_x[0], -hexagons_in_line * self.shift_x[1])
            self.ctx.translate((2*(vpos%2) - 1) * self.shift_y[0], self.shift_y[1])

        self.ctx.set_source_rgb(0.1, 0.1, 0.1)
        self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self.ctx.set_font_size(13)
        self.ctx.move_to(20, 30)
        self.ctx.show_text("Hello, World!")

class PianoOctavePic:
    def __init__(self, width, height):
        self.ctx = None
        self.width = width
        self.height = height

    def white_key(self, pos):
        self.ctx.set_line_width(0.01)
        self.ctx.set_source_rgb(0.0, 0.0, 0.0)
        self.ctx.rectangle(pos, 0.0, 0.2, 1.0)
        self.ctx.stroke()
        self.ctx.set_source_rgb(1.0, 1.0, 1.0)
        self.ctx.rectangle(pos, 0.0, 0.2, 1.0)
        self.ctx.fill()

    def black_key(self, pos):
        self.ctx.set_line_width(0.01)
        self.ctx.set_source_rgb(0.0, 0.0, 0.0)
        self.ctx.rectangle(pos + 0.045, 0.0 , 0.1 , 0.6)
        self.ctx.fill()
        self.ctx.stroke()

    def draw_pic(self, ctx, scale=SCALE_MAJOR_DIATONIC):
        self.ctx = ctx

        notes = [(scale & 1<<r != 0) for r in range(12)]
        whites = [num for num, white in enumerate(notes) if white]
        blacks = [num for num, white in enumerate(notes) if not white]

        self.ctx.set_source_rgb(0.5, 0.5, 0.5)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()
 
        self.ctx.translate(20, 20)
        self.ctx.scale((self.width + 50) / 5, (self.height - 100) / 1.0)

        self.white_key(.1)
        self.white_key(.3)
        self.white_key(.5)
        self.white_key(.7)
        self.white_key(.9)
        self.white_key(1.1)
        self.white_key(1.3)

        self.black_key(.2)
        self.black_key(.4)
        self.black_key(.8)
        self.black_key(1.0)
        self.black_key(1.2)

def main():
    import ctypes
    import time

    from pyglet import app, clock, font, gl, image, window

    from MusicDefs import MusicDefs

    pic = PianoOctavePic(width=400, height=200)
    pic = HexagonalLayoutPic(D=100)

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
