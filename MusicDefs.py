#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MusicDefs:
    INTVL_UNISON            = 1<<0  # Root Note / Tonic
    INTVL_MINOR_SECOND      = 1<<1  # 1 semitone
    INTVL_MAJOR_SECOND      = 1<<2  # 2 semitones / 1 tone
    INTVL_MINOR_THIRD       = 1<<3  # 3 semitones
    INTVL_MAJOR_THIRD       = 1<<4  # 4 semitones / 2 tones
    INTVL_PERF_FOURTH       = 1<<5  # 5 semitones
    INTVL_TRITONE           = 1<<6  # 6 semitones / 3 tones
    INTVL_PERF_FIFTH        = 1<<7  # 7 semitones
    INTVL_MINOR_SIXTH       = 1<<8  # 8 semitones / 4 tones
    INTVL_MAJOR_SIXTH       = 1<<9  # 9 semitones
    INTVL_MINOR_SEVENTH     = 1<<10 # 10 semitones / 5 tones
    INTVL_MAJOR_SEVENTH     = 1<<11 # 11 semitones
    INTVL_PERF_OCTAVE       = 1<<12 # 12 semitones / 6 tones

    NOTE_ROOT               = INTVL_UNISON
    INTVL_DIMINISHED_FIFTH  = INTVL_TRITONE      # 8 semitones / 4 tones
    INTVL_AUGMENTED_FIFTH   = INTVL_MINOR_SIXTH  # 8 semitones / 4 tones
    INTVL_MAJOR_NINTH       = INTVL_MAJOR_SECOND # 14 semitones / 7 tones
    INTVL_ELEVENTH          = INTVL_PERF_FOURTH  # 17 semitones
    INTVL_THIRTEENTH        = INTVL_PERF_FOURTH  # 17 semitones

    # Major chords sound happy and simple.
    TRIAD_MAJOR      = NOTE_ROOT + INTVL_MAJOR_THIRD + INTVL_PERF_FIFTH
    # Minor chords are considered to be sad, or ‘serious’.
    TRIAD_MINOR      = NOTE_ROOT + INTVL_MINOR_THIRD + INTVL_PERF_FIFTH
    # Diminished Chords sound tense and unpleasant.
    TRIAD_DIMINISHED = NOTE_ROOT + INTVL_MINOR_THIRD + INTVL_DIMINISHED_FIFTH
    # Augmented chords sound anxious and suspenseful.
    TRIAD_AUGMENTED  = NOTE_ROOT + INTVL_MAJOR_THIRD + INTVL_AUGMENTED_FIFTH

    TRIAD_INVERSION_NONE = 0
    # First inversion: the third of the chord is the bass note
    TRIAD_INVERSION_FIRST = 1
    # Second inversion: the fifth of the chord is the bass note
    TRIAD_INVERSION_SECOND= 2

    # When creating a chord you generally¹ stack thirds on top of each other and
    # name the chord after the number of steps from the root note to the highest added note.

    # The augmented triad does not belong to any tonality. It's one of the so-called "altered chords".
    # There are only 4 different augmented triad chords (taking inversions into account). The three chord
    # inversions have the same structure. Any of their notes can work as fundamental.
    # ①ne of the ways in which the augmented 5th chord is most used is to modulate to tonalities far away
    # from the initial one.
    # The augmented 5th chord works very well as a substitute for a dominant one, since it has a similar
    # loudness and contains the tension that is subsequently resolved with a tonic.

    CHORD_MAJOR      = TRIAD_MAJOR      # I + III + V
    CHORD_MINOR      = TRIAD_MINOR      # I + iii + V
    CHORD_DIMINISHED = TRIAD_DIMINISHED # I + iii + v
    CHORD_AUGMENTED  = TRIAD_AUGMENTED  # I + III + vi

    # Major seventh chords are considered to be thoughtful, soft.
    # Major seventh chords also sound “jazzy” because they’re commonly used in Jazz.
    CHORD_MAJOR_SEVENTH      = TRIAD_MAJOR      + INTVL_MAJOR_SEVENTH # I + III + V + VII
    # Dominant seventh chords are considered to be strong and restless.
    # Dominant seventh chords are commonly found in jazz and blues, as well as jazz
    # inspired r&b, hip hop, & EDM.
    CHORD_DOMINANT_SEVENTH   = TRIAD_MAJOR      + INTVL_MINOR_SEVENTH # I + III + V + vii
    # Minor seventh chords are considered to be moody, or contemplative.
    # If major chords are happy, and minor chords are sad, then minor seventh chords
    # are somewhere in between these two.
    CHORD_MINOR_SEVENTH      = TRIAD_MINOR      + INTVL_MINOR_SEVENTH # I + iii + V + vii
    # Semidiminished seventh
    CHORD_SEMIDIM_SEVENTH    = TRIAD_DIMINISHED + INTVL_MINOR_SEVENTH # I + iii + v + vii
    # Probably the most common use of the diminished seventh chord is like a bridge between two adjacent chords.
    # Another way you can use the diminished seventh chord is as a substitute for the dominant chord. In this case,
    # you would use the diminished seventh chord that is half a tone above the dominant chord.
    # It is composed of a diminished triad and a diminished seventh. Another way of looking at it is noticing that
    # it is formed entirely by minor third intervals.
    # There are only 3 diminished seventh chords. The rest are inversions or enharmonics of these 3 chords.
    # Both augmented fifth and diminished seventh are classified as symmetric chords.
    CHORD_DIMINISHED_SEVENTH = TRIAD_DIMINISHED + INTVL_MAJOR_SIXTH    # I + iii + v + VI
    CHORD_SEVENTH_MIN_VIIMAJ = TRIAD_MINOR      + INTVL_MAJOR_SEVENTH  # I + iii + V + VII
    CHORD_SEVENTH_AUG_VIIMAJ = TRIAD_AUGMENTED  + INTVL_MAJOR_SEVENTH  # I + III + vi + VII

    # So far every chord we’ve dealt with has been composed of a root, a third, and a fifth.
    # While the most common chords are built off this foundation, there are chords that don’t
    # follow this formula, such as suspended chords.
    # Sus2 Chords sound bright and nervous.
    CHORD_SUSPENDED_TWO = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_PERF_FIFTH
    # Sus4 Chords, like Sus2 chords, sound bright and nervous.
    CHORD_SUSPENDED_FOUR = NOTE_ROOT + INTVL_PERF_FIFTH + INTVL_PERF_FOURTH

    # So far, we’ve only discussed chords with intervals between 2 and 7.
    # There are also chords featuring voicings above a seventh, namely ninth, eleventh, and thirteenth chords.
    CHORD_DOMINANT_NINTH      = TRIAD_MAJOR + INTVL_MINOR_SEVENTH + INTVL_MAJOR_NINTH
    CHORD_MAJOR_ELEVENTH      = TRIAD_MAJOR + INTVL_MAJOR_SEVENTH + INTVL_MAJOR_NINTH + INTVL_ELEVENTH
    CHORD_DOMINANT_THIRTEENTH = TRIAD_MAJOR + INTVL_MAJOR_SEVENTH + INTVL_THIRTEENTH

    # Diatonic scales or modes: A set of 7 diatonic scales (or "modes") follow from a compact and natural set of definitions:
    # - The tonic and octave are both included
    # - There are 8 notes including the tonic and octave
    # - Steps larger than a whole step are forbidden
    # - There must be at least 2 whole steps separating each half step, including octave periodicity
    # We can define an infinite sequence of whole and half steps where the notes look like: o o oo o o oo o oo o o oo o oo o o oo

    # Lydian: Happy. Magic
    SCALE_HEPTA_LYDIAN     = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_TRITONE     + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH # ①-②-③-④⑤-⑥-⑦⑧
    # Ionian or major: Happy. Tension in V7
    SCALE_HEPTA_IONIAN     = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH # ①-②-③④-⑤-⑥-⑦⑧
    # Mixolydian: happy, but less bright. Epic (bVII)
    SCALE_HEPTA_MIXOLYDIAN = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MINOR_SEVENTH # ①-②-③④-⑤-⑥⑦-⑧
    # Dorian: Sad. Epic (bVII). I minor, IV major
    SCALE_HEPTA_DORIAN     = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MINOR_SEVENTH # ①-②③-④-⑤-⑥⑦-⑧
    # Aeolian or natural minor: Sad. Epic.
    SCALE_HEPTA_AEOLIAN    = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH # ①-②③-④-⑤⑥-⑦-⑧
    # Phrygian: dark, exotic, disturbing
    SCALE_HEPTA_PHRYGIAN   = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH # ①②-③-④-⑤⑥-⑦-⑧
    # Locrian: dissonant
    SCALE_HEPTA_LOCRIAN    = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_TRITONE    + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH # ①②-③-④⑤-⑥-⑦-⑧

    # Melodic modes: In the diatonic modes there must be at least 2 whole steps separating each half step. If we relax this condition and allow half steps to be
    # separated by only one whole step then another set of modes appears with the sequence: o o o oo oo o o o oo oo o o o oo oo o o o oo oo o

    # Lydian sharp V
    SCALE_HEPTA_LYDIAN_SHARP_FIFTH  = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_TRITONE     + INTVL_MINOR_SIXTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH # ①-②-③-④-⑤⑥-⑦⑧
    # Lydian/Mixolydian
    SCALE_HEPTA_LYDIAN_MIXOLYDIAN   = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_TRITONE     + INTVL_PERF_FIFTH  + INTVL_MAJOR_SIXTH + INTVL_MINOR_SEVENTH # ①-②-③-④⑤-⑥⑦-⑧
    # Melodic minor
    SCALE_HEPTA_MELODIC_MINOR       = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH  + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH # ①-②③-④-⑤-⑥-⑦⑧
    # Mixolydian/Aeolian
    SCALE_HEPTA_MIXOLYDIAN_AEOLIAN  = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH  + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH # ①-②-③④-⑤⑥-⑦-⑧
    # Dorian/Phrygian
    SCALE_HEPTA_DORIAN_PHRYGIAN     = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH  + INTVL_MAJOR_SIXTH + INTVL_MINOR_SEVENTH # ①②-③-④-⑤-⑥⑦-⑧
    # Aeolian/Locrian
    SCALE_HEPTA_AEOLIAN_LOCRIAN     = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_TRITONE     + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH # ①-②③-④⑤-⑥-⑦-⑧
    # Locrian flat IV
    SCALE_HEPTA_LOCRIAN_FLAT_FOURTH = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MINOR_THIRD + INTVL_MAJOR_THIRD + INTVL_TRITONE     + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH # ①②-③④-⑤-⑥-⑦-⑧

    # Major and minor heptatonic scales

    SCALE_MAJOR            = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH # ①-②-③④-⑤-⑥-⑦⑧ = Ionian
    SCALE_HARMONIC_MAJOR   = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MAJOR_SEVENTH # ①-②-③④-⑤⑥--⑦⑧
    SCALE_LOCRIAN_MAJOR    = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_TRITONE    + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH # ①-②-③④⑤-⑥-⑦-⑧
    SCALE_NATURAL_MINOR    = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH # ①-②③-④-⑤⑥-⑦-⑧ = Aeolian
    SCALE_HARMONIC_MINOR   = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MAJOR_SEVENTH # ①-②③-④-⑤⑥--⑦⑧
    SCALE_BACHIAN_MINOR    = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH # ①-②③-④-⑤-⑥-⑦⑧

    # Pentatonic scales

    SCALE_PENTA_MAJOR       = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FIFTH  + INTVL_MAJOR_SIXTH   # ①-②-③--⑤-⑥--⑧
    SCALE_PENTA_BLUES_MAJOR = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH  + INTVL_MAJOR_SIXTH   # ①-②---④⑤-⑥--⑧
    SCALE_PENTA_SUSPENDED   = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH  + INTVL_MINOR_SEVENTH # ①-②---④⑤--⑦-⑧
    SCALE_PENTA_MINOR       = NOTE_ROOT + INTVL_MINOR_THIRD  + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH  + INTVL_MINOR_SEVENTH # ①--③--④⑤--⑦-⑧
    SCALE_PENTA_BLUES_MINOR = NOTE_ROOT + INTVL_MINOR_THIRD  + INTVL_PERF_FOURTH + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH # ①--③--④-⑥-⑦-⑧

    # Other scales

    SCALE_NEAPOLITAN = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH
    SCALE_NEAPOLITAN_MINOR = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MAJOR_SEVENTH
    SCALE_BEBOP_DOMINANT = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MINOR_SEVENTH + INTVL_MAJOR_SEVENTH
    SCALE_BEBOP_MAJOR = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH
    SCALE_BEBOP_DORIAN = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MINOR_SEVENTH
    SCALE_BEBOP_DORIAN2 = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MINOR_SEVENTH + INTVL_MAJOR_SEVENTH
    SCALE_BEBOP_LOCRIAN = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_TRITONE + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH
    SCALE_BEBOP_MELODIC_MINOR = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH
    SCALE_BEBOP_HARMONIC_MINOR = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH + INTVL_MAJOR_SEVENTH
    SCALE_ARABIAN = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MAJOR_SEVENTH
    SCALE_AUGMENTED = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_TRITONE + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH
    SCALE_BLUES = NOTE_ROOT + INTVL_MAJOR_THIRD + INTVL_TRITONE + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH
    SCALE_DIMINISHED = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_TRITONE + INTVL_MINOR_SIXTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH
    SCALE_ENIGMATIC = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MAJOR_THIRD + INTVL_TRITONE + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH + INTVL_MAJOR_SEVENTH
    SCALE_JAPANESE = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SEVENTH
    SCALE_HUNGARIAN_MINOR = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_TRITONE + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MAJOR_SEVENTH
    SCALE_WHOLE = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_TRITONE + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH
    SCALE_CHROMATIC = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_TRITONE + \
                                  INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MAJOR_SIXTH + INTVL_MINOR_SEVENTH + INTVL_MAJOR_SEVENTH

    RATIO_INTVL_UNISON        = [  1,  1 ]
    RATIO_INTVL_MINOR_SECOND  = [ 16, 15 ]
    RATIO_INTVL_MAJOR_SECOND  = [  9,  8 ]
    RATIO_INTVL_MINOR_THIRD   = [  6,  5 ]
    RATIO_INTVL_MAJOR_THIRD   = [  5,  4 ]
    RATIO_INTVL_PERF_FOURTH   = [  4,  3 ]
    RATIO_INTVL_TRITONE       = [  7,  5 ]
    RATIO_INTVL_PERF_FIFTH    = [  3,  2 ]
    RATIO_INTVL_MINOR_SIXTH   = [  8,  5 ]
    RATIO_INTVL_MAJOR_SIXTH   = [  5,  3 ]
    RATIO_INTVL_MINOR_SEVENTH = [  9,  5 ]
    RATIO_INTVL_MAJOR_SEVENTH = [ 15,  8 ]
    RATIO_INTVL_PERF_OCTAVE   = [  2,  1 ]

    RATIO_TRIAD_MAJOR      = [  4,  5,  6 ]
    RATIO_TRIAD_MINOR      = [ 10, 12, 15 ]
    RATIO_TRIAD_DIMINISHED = [  5,  6,  7 ]
    RATIO_TRIAD_AUGMENTED  = [  5,  6,  8 ]

    RATIO_CHORD_MAJOR_SEVENTH      = [  8, 10, 12, 15 ]
    RATIO_CHORD_DOMINANT_SEVENTH   = [ 20, 25, 30, 36 ]
    RATIO_CHORD_MINOR_SEVENTH      = [ 10, 12, 15, 18 ]
    RATIO_CHORD_SEMIDIM_SEVENTH    = [  5,  6,  7,  9 ]
    RATIO_CHORD_DIMINISHED_SEVENTH = [ 15, 18, 21, 25 ]
    RATIO_CHORD_SEVENTH_MIN_VIIMAJ = [ 40, 48, 60, 75 ]
    RATIO_CHORD_SEVENTH_AUG_VIIMAJ = [ 40, 48, 64, 75 ]

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

def ks_key(X):
    '''Estimate the key from a pitch class distribution
    
    Parameters
    ----------
    X : np.ndarray, shape=(12,)
        Pitch-class energy distribution.  Need not be normalized
        
    Returns
    -------
    major : np.ndarray, shape=(12,)
    minor : np.ndarray, shape=(12,)
    
        For each key (C:maj, ..., B:maj) and (C:min, ..., B:min),
        the correlation score for `X` against that key.
    '''

    import numpy as np
    import scipy.linalg
    import scipy.stats

    X = scipy.stats.zscore(X)
    
    # Coefficients from Kumhansl and Schmuckler
    # as reported here: http://rnhart.net/articles/key-finding/
    major = np.asarray([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    major = scipy.stats.zscore(major)
    
    minor = np.asarray([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    minor = scipy.stats.zscore(minor)
    
    # Generate all rotations of major
    major = scipy.linalg.circulant(major)
    minor = scipy.linalg.circulant(minor)
    
    return major.T.dot(X), minor.T.dot(X)


def main():
    pass

if __name__ == '__main__':
    main()