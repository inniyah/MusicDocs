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

    # Key Finding

    KEY_FINDING_KRUMHANSL_KESSLER = [ # Krumhansl-Kessler probe-tone profiles
    # Strong tendancy to identify the dominant key as the tonic
        [ 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88 ], # Major
        [ 6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17 ], # Minor
    ]

    KEY_FINDING_AARDEN_ESSEN = [ # Aarden-Essen continuity profiles
    # Weak tendancy to identify the subdominant key as the tonic
        [ 17.7661, 0.145624, 14.9265, 0.160186, 19.8049, 11.3587, 0.291248, 22.062, 0.145624, 8.15494, 0.232998, 4.95122 ], # Major
        [ 18.2648, 0.737619, 14.0499, 16.8599, 0.702494, 14.4362, 0.702494, 18.6161, 4.56621, 1.93186, 7.37619,  1.75623 ], # Minor
    ]

    KEY_FINDING_SIMPLE_PITCH = [ # Simple pitch profiles
    # Performs most consistently with large regions of music, becomes noiser with smaller regions of music.
        [ 2.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 2.0, 0.0, 1.0, 0.0, 1.0 ], # Major
        [ 2.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 2.0, 1.0, 0.0, 0.5, 0.5 ], # Minor
    ]

    KEY_FINDING_BELLMAN_BUDGE = [ # Bellman-Budge chord-based profiles
    # No particular tendancies for confusions with neighboring keys
        [ 16.80, 0.86, 12.95, 1.41, 13.49, 11.93, 1.25, 20.28, 1.80, 8.04, 0.62, 10.57 ], # Major
        [ 18.16, 0.69, 12.99, 13.34, 1.07, 11.15, 1.38, 21.07, 7.49, 1.53, 0.92, 10.21 ], # Minor
    ]

    KEY_FINDING_TEMPERLEY_KOSTKA_PAYNE = [ # Temperley-Kostka-Payne chord-based profiles
    # Strong tendency to identify the relative major as the tonic in minor keys. Well-balanced for major keys
        [ 0.748, 0.060, 0.488, 0.082, 0.670, 0.460, 0.096, 0.715, 0.104, 0.366, 0.057, 0.400 ], # Major
        [ 0.712, 0.084, 0.474, 0.618, 0.049, 0.460, 0.105, 0.747, 0.404, 0.067, 0.133, 0.330 ], # Minor
    ]

    # Reference Web Pages:
    # Key-finding algorithm: http://rnhart.net/articles/key-finding/
    # keycor manpage: http://extras.humdrum.org/man/keycor/

    # Bibliography:
    # Aarden, Bret. Dynamic Melodic Expectancy. Ph.D. dissertation. School of Music, Ohio State University; 2003.
    # Bellman, Héctor. "About the determination of key of a musical excerpt" in Proceedings of Computer Music Modeling and Retrieval (CMMR): Pisa, Italy; 2005. pp. 187-203.
    # Gabura, James A. "Music style analysis by computer" in Lincoln, Harry B., ed., The Computer and Music. Cornell University Press: Ithaca, New York; 1970.
    # Krumhansl, Carol. Cognitive Foundations of Musical Pitch. Oxford Psychology Series No. 17. Oxford University Press: New York; 1990. pp. 37, 81-96.
    # Sapp, Craig Stuart. "Key-Profile Comparisons in Key-Finding by Correlation." International Conference on Music Perception and Cognition (ICMPC 10); 2008, Sapporo, Japan.
    # Temperley, David. Music and Probability. MIT Press: Cambridge, Mass.; 2007. p. 85. 

    # See: https://www.extremraym.com/en/downloads/reascripts-midi-key-finder/
    # See: https://labs.la.utexas.edu/gilden/files/2016/04/temperley-maai.pdf
    # See: http://people.bu.edu/jyust/amsAthens2016.pdf
    # See: http://davidtemperley.com/kp-stats/
    # See: https://github.com/dharasim/MCR/wiki
    # See: https://musicinformationretrieval.wordpress.com/2017/01/20/symbolic-chord-detection-2/

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

