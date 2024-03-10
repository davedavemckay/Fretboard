from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os
# from time import sleep
os.environ['TMP'] = '.'
os.environ['TEMP'] = '.'

def play_frequency(frequency, duration=1000):
    # Generate sound of given frequency
    sound = AudioSegment.silent(duration=duration)
    sound = sound._spawn(sound.raw_data, overrides={'sample_rate': 44100})
    sound = sound.set_frame_rate(frequency)
    
    # Export to a temporary file and play it
    _, temp_path = tempfile.mkstemp()
    sound.export(temp_path, format="wav")
    
    with open(temp_path, 'rb') as f:
        play(AudioSegment.from_wav(f))
    
    # Delete the temporary file
    # os.remove(temp_path)

def play_chord(chord, octave=4, duration=1000):
    # Generate sounds of the frequencies of the notes in the chord
    sounds = [AudioSegment.silent(duration=duration)._spawn(AudioSegment.silent(duration=duration).raw_data, overrides={'frame_rate': AudioSegment.silent(duration=duration).frame_rate}).set_frame_rate(frequency) for frequency in chord.get_frequencies(chord, octave)]
    # Play the sounds
    play(sum(sounds))

play_frequency(440)