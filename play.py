from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play
import play_midi
import os
import chord
import equal_temperament as et
from time import sleep
# from time import sleep
os.environ['TMP'] = '.'
os.environ['TEMP'] = '.'

def sleep_ms(ms):
    return sleep(ms/1000)

def play_frequency(frequency, duration=1000):

    
    # Generate a sine wave of the given frequency
    sine_wave = Sine(frequency,sample_rate=44100, bit_depth=16).to_audio_segment(duration=duration, volume=-20.0)#, channels=2)
    print(sine_wave.frame_rate, sine_wave.sample_width, sine_wave.channels, sine_wave.frame_count())
    # Play the sound
    try:
        play(sine_wave)
    except ValueError:
        print(f"Sample rate {sine_wave.frame_rate} not supported")
    
    # sine_wave.export('sine.wav', format='wav')

def play_chord(chord, octave=4, duration=1000):
    # Generate sounds of the frequencies of the notes in the chord
    sample_rate = 44100  # Set a valid sample rate
    sounds = [Sine(frequency, sample_rate=sample_rate, bit_depth=16).to_audio_segment(duration=duration, volume=-20.0) for frequency in chord.get_frequencies(octave)]
    output = sounds[0]
    for sound in sounds[1:]:
        output *= sound
    # Play the sounds

    play(output.fade_in(50).fade_out(250))

bpm = 120
beat = 6e4/bpm

# play_frequency(440, beat*4)
# with open('sine.wav', 'rb') as f:
#     zero = AudioSegment.from_wav(f)
#     play(zero)
#     print(zero.frame_rate)

# play_midi.play_midi_note(69, beat*4)

# play_chord(chord.Chord('A', chord.chord_types['major']), 3, beat*4)
# play_midi.play_midi_chord([et.note_name_to_midi(nn, 2) for nn in chord.Chord('A', chord.chord_types['major']).get_note_names()], beat*4)

chord_progression = [{'root':'D','quality':'major13','inversion':0,'octave':3,'beats':3.5,'rest_beats':0.5},
                     {'root':'D','quality':'major13','inversion':1,'octave':3,'beats':3.5,'rest_beats':0.5},
                     {'root':'D','quality':'major13','inversion':2,'octave':3,'beats':3.5,'rest_beats':0.5},
                     {'root':'D','quality':'major13','inversion':3,'octave':3,'beats':3.5,'rest_beats':0.5},
                     {'root':'D','quality':'major13','inversion':4,'octave':3,'beats':3.5,'rest_beats':0.5},
                     {'root':'D','quality':'major13','inversion':5,'octave':3,'beats':3.5,'rest_beats':0.5},
]
# , 'E', 'F#', 'A',
#                      'D', 'D', 'A', 'A',
                    #  'E', 'D', 'A', 'E'}

def play_chord_progression(chord_progression, gen='midi', bpm=120, time_signature=(4,4)):

    # Write something to test the sum of beats and rest_beats fits the time signature

    # beats = [chord['beats'] for chord in chord_progression]
    # rests = [chord['rest_beats'] for chord in chord_progression]
    # # print(beats)
    # pattern = [br for br in zip(beats, rests)]
    # pattern = list(sum(pattern, ())) # this is actual magic
    # print(pattern)
    # print(sum(pattern))
    # print(4 % 8)
    # print(8 % 4)
    # print(time_signature[0])
    # if time_signature[0] % sum(pattern) != 0:
    #     raise ValueError("Time signature must be divisible by pattern.")
    beat = 6e4/bpm
    for chord_dict in chord_progression:
        print(f"{chord_dict['root']}{chord_dict['quality']} in inversion {chord_dict['inversion']}")
        if gen == 'midi':
            play_midi.play_midi_chord([et.note_name_to_midi(nn_o[:-1], nn_o[-1]) for nn_o in chord.Chord(chord_dict['root'], quality=chord_dict['quality'], inversion=chord_dict['inversion'], octave=chord_dict['octave']).get_note_names()], beat*chord_dict['beats'])
        elif gen == 'audio':
            play_chord(chord.Chord(chord_dict['root'], chord_dict['quality']), chord_dict['octave'], beat*chord_dict['beats'])
        sleep_ms(beat*chord_dict['rest_beats'])
    # sleep(beat*pattern[-1])

# for chord_name in chord_progressing:
#     # play_chord(chord.Chord(chord_name, chord.chord_types['major']), 3, beat*4)
#     play_midi.play_midi_chord([et.note_name_to_midi(nn, 2) for nn in chord.Chord(chord_name, chord.chord_types['major']).get_note_names()], beat*1.5)
#     sleep(beat*.5/1000)
#     play_midi.play_midi_chord([et.note_name_to_midi(nn, 2) for nn in chord.Chord(chord_name, chord.chord_types['major']).get_note_names()], beat*0.25)
#     sleep(beat*.75/1000)
#     play_midi.play_midi_chord([et.note_name_to_midi(nn, 2) for nn in chord.Chord(chord_name, chord.chord_types['major']).get_note_names()], beat*0.25)
#     sleep(beat*.75/1000)

# print(chord.Chord('B', chord.chord_types['minor']).get_note_names())

play_chord_progression(chord_progression, gen='midi', bpm=120)