#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# General MIDI Instrument List

# These are the instruments in the General MIDI Level 1 sound set.
# https://soundprogramming.net/file-formats/general-midi-instrument-list/

MIDI_GM1 = {
	# Piano:
	1: "Acoustic Grand Piano",
	2: "Bright Acoustic Piano",
	3: "Electric Grand Piano",
	4: "Honky-tonk Piano",
	5: "Electric Piano 1",
	6: "Electric Piano 2",
	7: "Harpsichord",
	8: "Clavinet",

	# Chromatic Percussion:
	9: "Celesta",
	10: "Glockenspiel",
	11: "Music Box",
	12: "Vibraphone",
	13: "Marimba",
	14: "Xylophone",
	15: "Tubular Bells",
	16: "Dulcimer",

	# Organ:
	17: "Drawbar Organ",
	18: "Percussive Organ",
	19: "Rock Organ",
	20: "Church Organ",
	21: "Reed Organ",
	22: "Accordion",
	23: "Harmonica",
	24: "Tango Accordion",

	# Guitar:
	25: "Acoustic Guitar (nylon)",
	26: "Acoustic Guitar (steel)",
	27: "Electric Guitar (jazz)",
	28: "Electric Guitar (clean)",
	29: "Electric Guitar (muted)",
	30: "Overdriven Guitar",
	31: "Distortion Guitar",
	32: "Guitar harmonics",

	# Bass:
	33: "Acoustic Bass",
	34: "Electric Bass (finger)",
	35: "Electric Bass (pick)",
	36: "Fretless Bass",
	37: "Slap Bass 1",
	38: "Slap Bass 2",
	39: "Synth Bass 1",
	40: "Synth Bass 2",

	# Strings:
	41: "Violin",
	42: "Viola",
	43: "Cello",
	44: "Contrabass",
	45: "Tremolo Strings",
	46: "Pizzicato Strings",
	47: "Orchestral Harp",
	48: "Timpani",

	# Strings (continued):
	49: "String Ensemble 1",
	50: "String Ensemble 2",
	51: "Synth Strings 1",
	52: "Synth Strings 2",
	53: "Choir Aahs",
	54: "Voice Oohs",
	55: "Synth Voice",
	56: "Orchestra Hit",

	# Brass:
	57: "Trumpet",
	58: "Trombone",
	59: "Tuba",
	60: "Muted Trumpet",
	61: "French Horn",
	62: "Brass Section",
	63: "Synth Brass 1",
	64: "Synth Brass 2",

	# Reed:
	65: "Soprano Sax",
	66: "Alto Sax",
	67: "Tenor Sax",
	68: "Baritone Sax",
	69: "Oboe",
	70: "English Horn",
	71: "Bassoon",
	72: "Clarinet",

	# Pipe:
	73: "Piccolo",
	74: "Flute",
	75: "Recorder",
	76: "Pan Flute",
	77: "Blown Bottle",
	78: "Shakuhachi",
	79: "Whistle",
	80: "Ocarina",

	# Synth Lead:
	81: "Lead 1 (square)",
	82: "Lead 2 (sawtooth)",
	83: "Lead 3 (calliope)",
	84: "Lead 4 (chiff)",
	85: "Lead 5 (charang)",
	86: "Lead 6 (voice)",
	87: "Lead 7 (fifths)",
	88: "Lead 8 (bass + lead)",

	# Synth Pad:
	89: "Pad 1 (new age)",
	90: "Pad 2 (warm)",
	91: "Pad 3 (polysynth)",
	92: "Pad 4 (choir)",
	93: "Pad 5 (bowed)",
	94: "Pad 6 (metallic)",
	95: "Pad 7 (halo)",
	96: "Pad 8 (sweep)",

	# Synth Effects:
	97: "FX 1 (rain)",
	98: "FX 2 (soundtrack)",
	99: "FX 3 (crystal)",
	100: "FX 4 (atmosphere)",
	101: "FX 5 (brightness)",
	102: "FX 6 (goblins)",
	103: "FX 7 (echoes)",
	104: "FX 8 (sci-fi)",

	# Ethnic:
	105: "Sitar",
	106: "Banjo",
	107: "Shamisen",
	108: "Koto",
	109: "Kalimba",
	110: "Bag pipe",
	111: "Fiddle",
	112: "Shanai",

	# Percussive:
	113: "Tinkle Bell",
	114: "Agogo",
	115: "Steel Drums",
	116: "Woodblock",
	117: "Taiko Drum",
	118: "Melodic Tom",
	119: "Synth Drum",
	120: "Reverse Cymbal",

	# Sound effects:
	121: "Guitar Fret Noise",
	122: "Breath Noise",
	123: "Seashore",
	124: "Bird Tweet",
	125: "Telephone Ring",
	126: "Helicopter",
	127: "Applause",
	128: "Gunshot",
}

# General MIDI Level 2 Instrument List

# These are the instruments in the General MIDI Level 2 sound set.
# The first number listed is the patch number, and the second number is the bank number.
# https://soundprogramming.net/file-formats/general-midi-level-2-instrument-list/

MIDI_GM2 = {
	0: {
		# Piano:
		1	0	Acoustic Grand Piano
		2	0	Bright Acoustic Piano
		3	0	Electric Grand Piano
		4	0	Honky-tonk Piano
		5	0	Rhodes Piano
		6	0	Chorused Electric Piano
		7	0	Harpsichord
		8	0	Clavinet

		# Chromatic Percussion:
		9	0	Celesta
		10	0	Glockenspiel
		11	0	Music Box
		12	0	Vibraphone
		13	0	Marimba
		14	0	Xylophone
		15	0	Tubular Bells
		16	0	Dulcimer/Santur

		# Organ:
		17	0	Hammond Organ
		18	0	Percussive Organ
		19	0	Rock Organ
		20	0	Church Organ 1
		21	0	Reed Organ
		22	0	French Accordion
		23	0	Harmonica
		24	0	Bandoneon

		# Guitar:
		25	0	Nylon-String Guitar
		26	0	Steel-String Guitar
		27	0	Jazz Guitar
		28	0	Clean Electric Guitar
		29	0	Muted Electric Guitar
		30	0	Overdriven Guitar
		31	0	Distortion Guitar
		32	0	Guitar Harmonics

		# Bass:
		33	0	Acoustic Bass
		34	0	Fingered Bass
		35	0	Picked Bass
		36	0	Fretless Bass
		37	0	Slap Bass 1
		38	0	Slap Bass 2
		39	0	Synth Bass 1
		40	0	Synth Bass 2

		# Strings:
		41	0	Violin
		42	0	Viola
		43	0	Cello
		44	0	Contrabass
		45	0	Tremolo Strings
		46	0	Pizzicato Strings
		47	0	Harp
		48	0	Timpani

		# Orchestral Ensemble:
		49	0	String Ensemble
		50	0	Slow String Ensemble
		51	0	Synth Strings 1
		52	0	Synth Strings 2
		53	0	Choir Aahs
		54	0	Voice Oohs
		55	0	Synth Voice
		56	0	Orchestra Hit

		# Brass:
		57	0	Trumpet
		58	0	Trombone
		59	0	Tuba
		60	0	Muted Trumpet
		61	0	French Horn
		62	0	Brass Section
		63	0	Synth Brass 1
		64	0	Synth Brass 2

		# Reed:
		65	0	Soprano Sax
		66	0	Alto Sax
		67	0	Tenor Sax
		68	0	Baritone Sax
		69	0	Oboe
		70	0	English Horn
		71	0	Bassoon
		72	0	Clarinet

		# Wind:
		73	0	Piccolo
		74	0	Flute
		75	0	Recorder
		76	0	Pan Flute
		77	0	Blown Bottle
		78	0	Shakuhachi
		79	0	Whistle
		80	0	Ocarina

		# Synth Lead:
		81	0	Square Lead
		82	0	Saw Lead
		83	0	Synth Calliope
		84	0	Chiffer Lead
		85	0	Charang
		86	0	Solo Synth Vox
		87	0	5th Saw Wave
		88	0	Bass & Lead

		# Synth Pad:
		89	0	Fantasia Pad
		90	0	Warm Pad
		91	0	Polysynth Pad
		92	0	Space Voice Pad
		93	0	Bowed Glass Pad
		94	0	Metal Pad
		95	0	Halo Pad
		96	0	Sweep Pad

		# Synth Effects:
		97	0	Ice Rain
		98	0	Soundtrack
		99	0	Crystal
		100	0	Atmosphere
		101	0	Brightness
		102	0	Goblin
		103	0	Echo Drops
		104	0	Star Theme

		# Ethnic:
		105	0	Sitar
		106	0	Banjo
		107	0	Shamisen
		108	0	Koto
		109	0	Kalimba
		110	0	Bagpipe
		111	0	Fiddle
		112	0	Shanai

		# Percussive:
		113	0	Tinkle Bell
		114	0	Agogo
		115	0	Steel Drums
		116	0	Woodblock
		117	0	Taiko Drum
		118	0	Melodic Tom 1
		119	0	Synth Drum
		120	0	Reverse Cymbal

		# Sound effects:
		121	0	Guitar Fret Noise
		122	0	Breath Noise
		123	0	Seashore
		124	0	Bird Tweet
		125	0	Telephone 1
		126	0	Helicopter
		127	0	Applause
		128	0	Gun Shot
	},
	1: {
		# Piano:
		1	1	Wide Acoustic Grand
		2	1	Wide Bright Acoustic
		3	1	Wide Electric Grand
		4	1	Wide Honky-tonk	Variation
		5	1	Detuned Electric Piano 1
		6	1	Detuned Electric Piano 2
		7	1	Coupled Harpsichord
		8	1	Pulse Clavinet	Variation

		# Chromatic Percussion:
		12	1	Wet Vibraphone
		13	1	Wide Marimba
		15	1	Church Bells

		# Organ:
		17	1	Detuned Organ 1
		18	1	Detuned Organ 2
		20	1	Church Organ 2
		21	1	Puff Organ
		22	1	Italian Accordion

		# Guitar:
		25	1	Ukelele
		26	1	12-String Guitar
		27	1	Hawaiian Guitar
		28	1	Chorus Guitar
		29	1	Funk Guitar
		30	1	Guitar Pinch
		31	1	Feedback Guitar
		32	1	Guitar Feedback

		# Bass:
		34	1	Finger Slap
		39	1	Synth Bass 101
		40	1	Synth Bass 4

		# Strings:
		41	1	Slow Violin
		47	1	Yang Qin

		# Orchestral Ensemble:
		49	1	Orchestra Strings
		51	1	Synth Strings 3
		53	1	Choir Aahs 2
		54	1	Humming
		55	1	Analog Voice
		56	1	Bass Hit

		# Brass:
		57	1	Dark Trumpet
		58	1	Trombone 2
		60	1	Muted Trumpet 2
		61	1	French Horn 2
		62	1	Brass Section
		63	1	Synth Brass 3
		64	1	Synth Brass 4

		# Synth Lead:
		81	1	Square Wave
		82	1	Saw Wave
		85	1	Wire Lead
		88	1	Delayed Lead

		# Synth Pad:
		90	1	Sine Pad
		92	1	Itopia

		# Synth Effects:
		99	1	Synth Mallet
		103	1	Echo Bell

		# Ethnic:
		105	1	Sitar 2
		108	1	Taisho Koto

		# Percussive:
		116	1	Castanets
		117	1	Concert Bass Drum
		118	1	Melodic Tom 2
		119	1	808 Tom

		# Sound effects:
		121	1	Guitar Cut Noise
		122	1	Flute Key Click
		123	1	Rain
		124	1	Dog
		125	1	Telephone 2
		126	1	Car Engine
		127	1	Laughing
		128	1	Machine Gun
	},
	2: {
		# Piano:
		1	2	Dark Acoustic Grand
		5	2	Electric Piano 1
		6	2	Electric Piano 2
		7	2	Wide Harpsichord

		# Chromatic Percussion:
		15	2	Carillon

		# Organ:
		17	2	60's Organ 1
		18	2	Organ 5
		20	2	Church Organ 3

		# Guitar:
		25	2	Open Nylon Guitar
		26	2	Mandolin
		28	2	Mid Tone Guitar
		29	2	Funk Guitar 2
		31	2	Distortion Rtm Guitar

		# Bass:
		39	2	Synth Bass 3
		40	2	Rubber Bass

		# Orchestral Ensemble:
		49	2	60's Strings
		56	2	6th Hit

		# Brass:
		58	2	Bright Trombone
		63	2	Analog Brass 1
		64	2	Analog Brass 2

		# Synth Lead:
		81	2	Sine Wave
		82	2	Doctor Solo

		# Synth Effects:
		103	2	Echo Pan

		# Percussive:
		119	2	Electric Percussion

		# Sound effects:
		121	2	String Slap
		123	2	Thunder
		124	2	Horse Gallop
		125	2	Door Creaking
		126	2	Car Stop
		127	2	Screaming
		128	2	Lasergun
	},
	3: {
		# Piano:
		5	3	60's Electric Piano
		6	3	Electric Piano Legend
		7	3	Open Harpsichord

		# Organ:
		17	3	Organ 4

		# Guitar:
		25	3	Nylon Guitar 2
		26	3	Steel + Body
		29	3	Jazz Man

		# Bass:
		39	3	Clavi Bass
		40	3	Attack Pulse

		# Brass:
		63	3	Jump Brass

		# Synth Lead:
		82	3	Natural Lead

		# Sound effects:
		123	3	Wind
		124	3	Bird 2
		125	3	Door Closing
		126	3	Car Pass
		127	3	Punch
		128	3	Explosion
		123	4	Stream
		125	4	Scratch
		126	4	Car Crash
		127	4	Heart Beat
		123	5	Bubble
		125	5	Wind Chimes
		126	5	Siren
		127	5	Footsteps
		126	6	Train
		126	7	Jetplane
		126	8	Starship
		126	9	Burst Noise
	},
	4: {
		# Piano:
		6	4	Electric Piano Phase

		# Bass:
		39	4	Hammer

		# Synth Lead:
		82	4	Sequenced Saw

		# Sound effects:
		# Sound effects:
		123	4	Stream
		125	4	Scratch
		126	4	Car Crash
		127	4	Heart Beat
	},
	5: {
		# Sound effects:
		123	5	Bubble
		125	5	Wind Chimes
		126	5	Siren
		127	5	Footsteps
	},
	6:{
		# Sound effects:
		126	6	Train
	},
	7: {
		# Sound effects:
		126	7	Jetplane
	},
	8: {
		# Sound effects:
		126	8	Starship
	},
	9: {
		# Sound effects:
		126	9	Burst Noise
	}
}

# General MIDI Drum Note Numbers

# General MIDI Drums (Channel 10): The numbers listed correspond to the MIDI note number for that drum sound.
# Drum sounds added in General MIDI Level 2 are tagged with (GM2). 
# https://soundprogramming.net/file-formats/general-midi-drum-note-numbers/

MIDI_DRUM = {
	27: High Q (GM2)
	28: Slap (GM2)
	29: Scratch Push (GM2)
	30: Scratch Pull (GM2)
	31: Sticks (GM2)
	32: Square Click (GM2)
	33: Metronome Click (GM2)
	34: Metronome Bell (GM2)
	35: Bass Drum 2
	36: Bass Drum 1
	37: Side Stick
	38: Snare Drum 1
	39: Hand Clap
	40: Snare Drum 2
	41: Low Tom 2
	42: Closed Hi-hat
	43: Low Tom 1
	44: Pedal Hi-hat
	45: Mid Tom 2
	46: Open Hi-hat
	47: Mid Tom 1
	48: High Tom 2
	49: Crash Cymbal 1
	50: High Tom 1
	51: Ride Cymbal 1
	52: Chinese Cymbal
	53: Ride Bell
	54: Tambourine
	55: Splash Cymbal
	56: Cowbell
	57: Crash Cymbal 2
	58: Vibra Slap
	59: Ride Cymbal 2
	60v High Bongo
	61: Low Bongo
	62: Mute High Conga
	63: Open High Conga
	64: Low Conga
	65: High Timbale
	66: Low Timbale
	67: High Agogo
	68: Low Agogo
	69: Cabasa
	70: Maracas
	71: Short Whistle
	72: Long Whistle
	73: Short Guiro
	74: Long Guiro
	75: Claves
	76: High Wood Block
	77: Low Wood Block
	78: Mute Cuica
	79: Open Cuica
	80: Mute Triangle
	81: Open Triangle
	82: Shaker (GM2)
	83: Jingle Bell (GM2)
	84: Belltree (GM2)
	85: Castanets (GM2)
	86: Mute Surdo (GM2)
	87: Open Surdo (GM2)
}
