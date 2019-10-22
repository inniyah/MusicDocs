#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from MusicDefs import MusicDefs

class MusicScale():

    NAMES_BY_FIFTHS = [
        'Fo', 'Co', 'Go', 'Do', 'Ao', 'Eo', 'Bo',
        'Fb', 'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb',
        'F',  'C',  'G',  'D',  'A',  'E',  'B',
        'F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#',
        'Fx', 'Cx', 'Gx', 'Dx', 'Ax', 'Ex', 'Bx',
    ]

    DIATONIC_SCALE_POS = [ 0, 7-12 , 2, 9-12 , 4, -1, 6, 1, 8-12 , 3, 10-12 , 5 ]

    ENARMONIC_NOTE_NAMES = [ 'C', 'Db/C#','D', 'Eb/D#', 'E', 'F', 'Gb/F#', 'G', 'Ab/G#', 'A', 'Bb/A#', 'B'  ]

    def __init__(self, root_note):
        self.root_note = root_note
        self.enarmonic_names = [self.ENARMONIC_NOTE_NAMES[(self.root_note + p) % 12] for p in range(12)]

        self.note_names_base_pos = [0, -5, 2, -3, 4, -1, -6, 1, -4, 3, -2, 5][self.root_note]
        self.note_names = [self.NAMES_BY_FIFTHS[15 + self.note_names_base_pos + p] for p in self.DIATONIC_SCALE_POS]
        self.fifth_names = [self.NAMES_BY_FIFTHS[15 + self.note_names_base_pos + p] for p in range(12)]

    def getEnarmonicNoteNames(self):
        return self.enarmonic_names

    def getChromaticNoteNames(self):
        return self.note_names

    def getFifthNoteNames(self):
        return self.fifth_names

def main():
    scales = [MusicScale(n) for n in range(12)]
    for s in scales:
        print(s.getEnarmonicNoteNames())
    print("")

    for s in scales:
        print(s.getChromaticNoteNames())
    print("")

    for s in scales:
        print(s.getFifthNoteNames())
    print("")

if __name__ == '__main__':
    main()

