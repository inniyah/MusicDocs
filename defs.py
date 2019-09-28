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

    # When creating a chord you generally¹ stack thirds on top of each other and
    # name the chord after the number of steps from the root note to the highest added note.

    # The augmented triad does not belong to any tonality. It's one of the so-called "altered chords".
    # There are only 4 different augmented triad chords (taking inversions into account). The three chord
    # inversions have the same structure. Any of their notes can work as fundamental.
    # One of the ways in which the augmented 5th chord is most used is to modulate to tonalities far away
    # from the initial one.
    # The augmented 5th chord works very well as a substitute for a dominant one, since it has a similar
    # loudness and contains the tension that is subsequently resolved with a tonic.

    CHORD_MAJOR      = TRIAD_MAJOR
    CHORD_MINOR      = TRIAD_MINOR
    CHORD_DIMINISHED = TRIAD_DIMINISHED
    CHORD_AUGMENTED  = TRIAD_AUGMENTED

    # Major seventh chords are considered to be thoughtful, soft.
    # Major seventh chords also sound “jazzy” because they’re commonly used in Jazz.
    CHORD_MAJOR_SEVENTH      = TRIAD_MAJOR      + INTVL_MAJOR_SEVENTH
    # Dominant seventh chords are considered to be strong and restless.
    # Dominant seventh chords are commonly found in jazz and blues, as well as jazz
    # inspired r&b, hip hop, & EDM.
    CHORD_DOMINANT_SEVENTH   = TRIAD_MAJOR      + INTVL_MINOR_SEVENTH
    # Minor seventh chords are considered to be moody, or contemplative.
    # If major chords are happy, and minor chords are sad, then minor seventh chords
    # are somewhere in between these two.
    CHORD_MINOR_SEVENTH      = TRIAD_MINOR      + INTVL_MAJOR_SEVENTH
    # Probably the most common use of the diminished seventh chord is like a bridge between two adjacent chords.
    # Another way you can use the diminished seventh chord is as a substitute for the dominant chord. In this case,
    # you would use the diminished seventh chord that is half a tone above the dominant chord.
    # It is composed of a diminished triad and a diminished seventh. Another way of looking at it is noticing that
    # it is formed entirely by minor third intervals.
    # There are only 3 diminished seventh chords. The rest are inversions or enharmonics of these 3 chords.
    # Both augmented fifth and diminished seventh are classified as symmetric chords.
    CHORD_DIMINISHED_SEVENTH = TRIAD_DIMINISHED + INTVL_MAJOR_SIXTH

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

    # Lydian: Happy. Magic
    SCALE_HEPTA_LYDIAN     = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_TRITONE     + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH
    # Ionian or major: Happy. Tension in V7
    SCALE_HEPTA_IONIAN     = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH
    # Mixolydian: happy, but less bright. Epic (bVII)
    SCALE_HEPTA_MIXOLYDIAN = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MINOR_SEVENTH
    # Dorian: Sad. Epic (bVII). I minor, IV major
    SCALE_HEPTA_DORIAN     = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MINOR_SEVENTH
    # Aeolian or natural minor: Sad. Epic.
    SCALE_HEPTA_AEOLIAN    = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH
    # Phrygian: dark, exotic, disturbing
    SCALE_HEPTA_PHRYGIAN   = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH
    # Locrian: dissonant
    SCALE_HEPTA_LOCRIAN    = NOTE_ROOT + INTVL_MINOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_TRITONE    + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH

    SCALE_MAJOR            = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH
    SCALE_HARMONIC_MAJOR   = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MAJOR_SEVENTH
    SCALE_LOCRIAN_MAJOR    = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FOURTH + INTVL_TRITONE    + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH
    SCALE_NATURAL_MINOR    = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH
    SCALE_HARMONIC_MINOR   = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MINOR_SIXTH + INTVL_MAJOR_SEVENTH
    SCALE_BACHIAN_MINOR    = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH + INTVL_MAJOR_SIXTH + INTVL_MAJOR_SEVENTH

    SCALE_PENTA_MAJOR       = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_MAJOR_THIRD + INTVL_PERF_FIFTH  + INTVL_MAJOR_SIXTH
    SCALE_PENTA_BLUES_MAJOR = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH  + INTVL_MAJOR_SIXTH
    SCALE_PENTA_SUSPENDED   = NOTE_ROOT + INTVL_MAJOR_SECOND + INTVL_PERF_FOURTH + INTVL_PERF_FIFTH  + INTVL_MINOR_SEVENTH
    SCALE_PENTA_MINOR       = NOTE_ROOT + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH  + INTVL_PERF_FIFTH  + INTVL_MINOR_SEVENTH
    SCALE_PENTA_BLUES_MINOR = NOTE_ROOT + INTVL_MINOR_THIRD + INTVL_PERF_FOURTH  + INTVL_MINOR_SIXTH + INTVL_MINOR_SEVENTH

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

def main():
    pass

if __name__ == '__main__':
    main()
