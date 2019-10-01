#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo
import math
import queue

SCALE_MAJOR_DIATONIC = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<11)
SCALE_MAJOR_MELODIC  = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<10)

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
    [ [], ((0, 0, 0), (4, 0, -1), (8, 0, -2), (10, 2,  1)), "Augmented minor seventh Chord" ],
    [ [], ((0, 0, 0), (3, 1,  1), (6, 2,  2), (11, 1, -1)), "Diminished major seventh Chord" ],
    [ [], ((0, 0, 0), (4, 0, -1), (6, 2,  2), (10, 2,  1)), "Dominant seventh flat five Chord" ],
    [ [], ((0, 0, 0), (4, 0, -1), (6, 2,  2), (11, 1, -1)), "Major seventh flat five Chord" ],

    # Primary triads
    [ [], ((0, 0, 0), (4, 0, -1), (7, 1,  0)),  "Major Triad" ],
    [ [], ((0, 0, 0), (3, 1,  1), (7, 1,  0)),  "Minor Triad" ],
    [ [], ((0, 0, 0), (3, 1,  1), (6, 2,  2)),  "Diminished Triad" ],
    [ [], ((0, 0, 0), (4, 0, -1), (8, 0, -2)),  "Augmented Triad" ],

    # Suspended triads
    [ [], ((0, 0, 0), (2,  2, 0), (7, 1,  0)),  "Sus2 Triad" ],
    [ [], ((0, 0, 0), (5, -1, 0), (7, 1,  0)),  "Sus4 Triad" ],
]

CHROMATIC_NOTES = ['C', 'Db/C#', 'D', 'Eb/D#', 'E', 'F', 'Gb/F#', 'G', 'Ab/G#', 'A', 'Bb/A#', 'B']

for chord_info in CHORDS_INFO:
    if not chord_info[0]:
        chord_info[0] = [0] * 12
        for i in range(0, 12):
            chord_mask = 0
            for num_note, inc_x, inc_y in chord_info[1]:
                chord_mask |= 1 << (i + num_note) % 12
            chord_info[0][i] = chord_mask

class HexagonalLayoutPic:
    def __init__(self, D, scale=SCALE_MAJOR_DIATONIC, tonic=1, h = 4):
        self.ctx = None

        self.notes = [(scale & 1<<(r%12) != 0) for r in range(tonic*7, tonic*7 + 12)]

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
                    print("Chord: {} on {}: {}".format(chord_name, CHROMATIC_NOTES[(num_signature) % 12], chord_intervals))

        raw_chords = [
            [(0, 0, 0), (4, 0, -1), (7, 1,  0)], # Major triad
            [(0, 0, 0), (3, 1,  1), (7, 1,  0)], # Minor triad
            [(0, 0, 0), (4, 0, -1), (8, 0, -2)], # Augmented triad
            [(0, 0, 0), (3, 1,  1), (6, 2,  2)], # Diminished triad
        ]

        chords = []

        self.selected_notes = {}

        notes_set = set()
        for root_chord in raw_chords:
            if self.check_chord(root_chord):
                for base_n, base_x, base_y in root_chord:

                    for order in range(3):
                        for raw_chord in raw_chords:
                            real_chord = [( (base_n + n - raw_chord[order][0]) % 12,
                                             base_x + x - raw_chord[order][1],
                                             base_y + y - raw_chord[order][2]
                                          ) for (n, x, y) in (raw_chord*2)[order:order+3]]

                            if self.check_chord(real_chord):
                                print(f"{real_chord}")
                                for n, x, y in real_chord:
                                    self.selected_notes[(x, y)] = f"{n} ({x},{y})"
                                    notes_set.add((n, x, y))

        print(notes_set)

        print(chords)

        notes_queue = queue.Queue()
        for (x, y) in [(0, 0), (1, 0), (-1, 0), (0, -1), (-1, -1), (1, 1), (0, 1)]:
            n = self.get_note_from_coords(x, y)
            if self.notes[n]:
                #self.selected_notes[(x, y)] = n
                notes_queue.put((n, x, y))

        while not notes_queue.empty():
            try:
                n, x, y = notes_queue.get()
                #n, x, y = notes_queue.get(timeout=wait_timeout)
                #n, x, y = notes_queue.get_nowait()
            except queue.Empty:
                continue
            print(f"{n} ({x, y})")

    def check_chord(self, chord, note=(0,0,0)):
        base_note, base_x, base_y = note
        notes_in_scale = True
        for inc_note, inc_x, inc_y in chord:
            note_value = (base_note + self.get_note_from_coords(base_x + inc_x, base_y + inc_y) % 12)
            if not self.notes[note_value]:
                notes_in_scale = False
            #print(f"{inc_note}, {inc_x}, {inc_y}: {note_value} -> {self.notes[note_value]}")
        return notes_in_scale

    def get_note_from_coords(self, x, y):
            return (int(x * 7 - y * 4) % 12)

    def draw_hexagon(self, color, label):
        self.ctx.move_to(self.hexagon_points[0][0], self.hexagon_points[0][1])
        for pair in self.hexagon_points:
            self.ctx.line_to(pair[0], pair[1])
        self.ctx.close_path()
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.stroke_preserve()
        self.ctx.set_source_rgb(*color)
        self.ctx.fill()

        text_extents = self.ctx.text_extents(str(label))
        self.ctx.move_to(-text_extents.width/2, text_extents.height/2)
        self.ctx.set_source_rgb(0.1, 0.1, 0.1)
        self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self.ctx.set_font_size(11)
        self.ctx.show_text(str(label))

    def compass_to_rgb(self, h, s=1, v=1):
        h = float(h)
        s = float(s)
        v = float(v)
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
                iy = int(vpos) - iy_offset
                ix = int(hpos) - ix_offset + iy//2
                n = self.get_note_from_coords(ix, iy)

                self.ctx.translate(self.shift_x[0], self.shift_x[1])

                try:
                    color = self.compass_to_rgb(360. * n/12., 1.0)
                    label = self.selected_notes[(ix, iy)]
                except KeyError:
                    label = f"{n} ({ix},{iy})"
                    if self.notes[n]:
                        color = self.compass_to_rgb(360. * n/12., 0.2)
                    else:
                        color = self.compass_to_rgb(360. * n/12., 0.05)

                self.draw_hexagon(color, label)

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
