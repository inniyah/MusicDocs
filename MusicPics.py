#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo
import math

class HexagonalLayoutPic:
    def __init__(self, D, side_fields = 7):
        self.ctx = None

        # diameter of hexagon in pixels
        self.D = D

        #This is the number of the colored hexagons that make
        # up the overall board that is actually hexagon comprised of small, colored ones
        # number of fields along each side. Changing the vaue to 33 makes a lot of tiny
        # hexagons on each side of the board.
        self.side_fields = side_fields

        # vectorial distance to next hexagon in row
        self.shift_x = (math.sqrt(3)*D/2., 0)

        # vectorial distance to hexagon in next row
        self.shift_y = (math.sqrt(3)*D/4., 3*D/4.)

        # width of surface plus some border in pixels
        self.width = int((2*side_fields-1)*math.sqrt(3)*D/2.+3*D/4.)+1

        # height of surface plus some border in pixels
        self.height = int((2*side_fields-1)*3*D/4.+2*D)+1

        self.field_colors = ((1, 1, 1), (0, 0, 0), (1, 0, 0))

        self.p = (
            (math.sqrt(3)*D/4., D/4.),
            (0, D/2.),
            (-math.sqrt(3)*D/4., D/4.),
            (-math.sqrt(3)*D/4., -D/4.),
            (0, -D/2.),
            (math.sqrt(3)*D/4.,-D/4.)
        )

    def hexagon(self, color):
        for pair in self.p:
            self.ctx.line_to(pair[0], pair[1])
        self.ctx.close_path()
        self.ctx.set_source_rgb(0,0,0)
        self.ctx.stroke_preserve()
        self.ctx.set_source_rgb(*self.field_colors[color % 3])
        self.ctx.fill()

    def draw_hexa(self, ctx):
        self.ctx = ctx

        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

        fields_in_line = self.side_fields
        increment, decreasing = 1, 0
        self.ctx.translate((self.side_fields-1)*math.sqrt(3)*self.D/4., self.D)

        for j in range(2*self.side_fields-1):
            if fields_in_line > 2*self.side_fields-2:
                increment = -1
            for i in range(fields_in_line):
                self.ctx.translate(self.shift_x[0], self.shift_x[1])
                self.hexagon(i + j + decreasing)
            self.ctx.translate(-fields_in_line*self.shift_x[0], -fields_in_line*self.shift_x[1])
            self.ctx.translate(-increment*self.shift_y[0], self.shift_y[1])
            if increment == -1:
                decreasing += 1
            fields_in_line += increment

class PianoOctavePic:
    def __init__(self, width, height):
        self.ctx = None
        self.width = width
        self.height = height

    def white_key(self, pos):
        self.ctx.set_line_width(0.01)
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.rectangle(pos , 0,  .2,  1 )
        self.ctx.stroke()
        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(pos , 0,  .2,  1 )
        self.ctx.fill()

    def black_key(self, pos):
        self.ctx.set_line_width(0.01)
        self.ctx.set_source_rgb(0.0, 0.0, 0.0)
        self.ctx.rectangle(pos  , 0 , .1 , .6  )
        self.ctx.fill()
        self.ctx.stroke()

    def draw_piano(self, ctx):
        self.ctx = ctx

        self.ctx.set_source_rgb(0.5, 0.5, 0.5)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()
 
        self.ctx.translate(20, 20)
        self.ctx.scale((self.width + 50) / 5, (self.height - 100) / 1.0)
        self.white_key(.1)
        self.black_key(.2) 
        self.white_key(.3)
        self.black_key(.4) 
        self.white_key(.5)
        self.white_key(.7)
        self.black_key(.8) 
        self.white_key(.9)
        self.black_key(1.0) 
        self.white_key(1.1)
        self.black_key(1.2) 
        self.white_key(1.3)
        self.white_key(1.5) 
        self.black_key(1.6) 

def main():
    pass

if __name__ == '__main__':
    main()
