from pydub import AudioSegment
from pydub.playback import play

def play_frequency(frequency, duration=1000):
    # Generate sound of given frequency
    sound = AudioSegment.silent(duration=duration)
    sound = sound._spawn(sound.raw_data, overrides={'frame_rate': sound.frame_rate})
    sound = sound.set_frame_rate(frequency)
    # Play the sound
    play(sound)

def play_chord(chord, octave=4, duration=1000):
    # Generate sounds of the frequencies of the notes in the chord
    sounds = [AudioSegment.silent(duration=duration)._spawn(AudioSegment.silent(duration=duration).raw_data, overrides={'frame_rate': AudioSegment.silent(duration=duration).frame_rate}).set_frame_rate(frequency) for frequency in get_frequencies(chord, octave)]
    # Play the sounds
    play(sum(sounds))

play_frequency(440)