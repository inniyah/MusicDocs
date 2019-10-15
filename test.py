#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo
import math
import os
import queue
import sys

from melody_pic import MelodyPic
from midi_sources import MidiFileSoundPlayer, RtMidiSoundPlayer
from threading import Thread, Lock

SCALE_MAJOR_DIATONIC = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<11)
SCALE_MAJOR_MELODIC  = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<10)

class Chords():
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

#        # Suspended triads
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

def main():
    import ctypes
    import time
    import pyglet

    from MusicDefs import MusicDefs

    pic = MelodyPic(D=100, scale=SCALE_MAJOR_DIATONIC, tonic=1)

    window = pyglet.window.Window(width=pic.width, height=pic.height, resizable=True)
    #ft = font.load('Arial', 24)
    #text = font.Text(ft, 'Hello World')

    # create data shared by ImageSurface and Texture
    data = (ctypes.c_ubyte * (pic.width * pic.height * 4))()
    stride = pic.width * 4
    surface = cairo.ImageSurface.create_for_data (data, cairo.FORMAT_ARGB32, pic.width, pic.height, stride); 
    texture = pyglet.image.Texture.create_for_size(pyglet.gl.GL_TEXTURE_2D, pic.width * pic.height, pyglet.gl.GL_RGBA)

    def update(dt, surface):
        ctx = cairo.Context(surface)

        ctx.save()
        pic.draw_pic(ctx)
        ctx.restore()


    @window.event
    def on_resize(width, height):
        pass

    def keyboard(c):
        if c == 'q':
            sys.exit(0)

    @window.event
    def on_key_press(symbol, modifiers):
        keyboard(chr(symbol))

    LEFT, MIDDLE, RIGHT = range(3)

    BUTTONS = {
        pyglet.window.mouse.LEFT:   LEFT,
        pyglet.window.mouse.MIDDLE: MIDDLE,
        pyglet.window.mouse.RIGHT:  RIGHT,
    }

    def mouse_button(button, pressed, x, y):
        pass

    def mouse_move(x1, y1, drag):
        pass

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        mouse_button(BUTTONS[button], True, x, window.height-y)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        mouse_button(BUTTONS[button], False, x, window.height-y)

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        mouse_move(x, window.height-y, False)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        mouse_move(x, window.height-y, True)

    @window.event
    def on_draw():
        window.clear()

        pyglet.gl.glEnable(pyglet.gl.GL_TEXTURE_2D)

        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, texture.id)
        pyglet.gl.glTexImage2D(pyglet.gl.GL_TEXTURE_2D, 0, pyglet.gl.GL_RGBA,
            pic.width, pic.height, 0, pyglet.gl.GL_BGRA, pyglet.gl.GL_UNSIGNED_BYTE, data)

        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glTexCoord2f(0.0, 1.0)
        pyglet.gl.glVertex2i(0, 0)
        pyglet.gl.glTexCoord2f(1.0, 1.0)
        pyglet.gl.glVertex2i(pic.width, 0)
        pyglet.gl.glTexCoord2f(1.0, 0.0)
        pyglet.gl.glVertex2i(pic.width, pic.height)
        pyglet.gl.glTexCoord2f(0.0, 0.0)
        pyglet.gl.glVertex2i(0, pic.height)
        pyglet.gl.glEnd()

        #text.draw()

        #print('FPS: %f' % clock.get_fps())

    midi_filename = 'Hallelujah.mid'
    #midi_filename = 'HotelCalifornia.mid'
    if not midi_filename is None:
        midi_file_player = MidiFileSoundPlayer(midi_filename, [pic])
        midi_thread = Thread(target = midi_file_player.play)
        midi_thread.start()
    else:
        midi_file_player = None
        midi_thread = None

    midi_input = RtMidiSoundPlayer([pic])

    pyglet.clock.schedule_interval(update, 1/120.0, surface)
    pyglet.app.run()

    pyglet.clock.schedule_interval(update, 0, surface) # Specifying an interval of 0 prevents the function from being called again

    if midi_thread:
        midi_thread.join()
        print("All threads finished")

if __name__ == '__main__':
    main()
