import wave
import numpy as np
from scipy.fft import fft

import wave
import numpy as np
from itertools import repeat
import multiprocessing as mp

import equal_temperament as et

import play_midi

def read_wav_file(file_path):
    """
    Read a WAV file and return the audio data as a numpy array.

    Parameters:
    file_path (str): The path to the WAV file.

    Returns:
    audio_array (numpy.ndarray): The audio data as a numpy array.
    sample_rate (int): The sample rate of the audio file.
    """

    with wave.open(file_path, 'rb') as wav_file:
        # Get audio properties
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()

        # Read audio data
        audio_data = wav_file.readframes(num_frames)

        # Convert audio data to numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        return audio_array, sample_rate

def calculate_bpm(audio_array, sample_rate, window_size=1024):
    # Calculate the energy of the signal over windows of time
    energy = np.array([np.sum(np.abs(audio_array[i:i+window_size]**2)) for i in range(0, len(audio_array), window_size)])

    # Identify peaks in the energy as beats
    beats = np.where(energy > np.mean(energy) + np.std(energy))[0]

    # Calculate BPM
    bpm = len(beats) / (len(audio_array) / sample_rate / 60)
    bpm = round(bpm)
    return bpm

def convert_to_notes(audio_array, sample_rate=44100):
    # Perform Fourier transform
    spectrum = fft(audio_array)
    # print(spectrum)
    
    # Find dominant frequency
    dominant_frequency_index = np.argmax(np.abs(spectrum))
    dominant_frequency = dominant_frequency_index * sample_rate / len(audio_array)
    # print(dominant_frequency)
    # exit()

    # Convert dominant frequency to note
    if dominant_frequency == 0:
        note = None
    else:
        note = et.frequency_to_note_name(dominant_frequency)

    return note

if __name__ == '__main__':
    # Example usage
    file_path = 'samples/eqt-chromo-sc.wav'
    audio_array, sample_rate = read_wav_file(file_path)

    bpm = calculate_bpm(audio_array, sample_rate)

    print('BPM:', bpm)

    chunk_size = bpm * len(audio_array) // (sample_rate*60)
    audio_array = audio_array[:len(audio_array) - len(audio_array) % chunk_size]
    audio_chunks = np.split(audio_array, len(audio_array) // chunk_size)
    # print(audio_chunks)
    beat_length = 60 / bpm * 1000

    # Create a pool of processes
    pool = mp.Pool(mp.cpu_count())

    notes = pool.starmap(convert_to_notes, zip(audio_chunks, repeat(sample_rate)))

    octaves = [int(note[-1]) if note is not None else None for note in notes]
    notes = [note[:-1] if note is not None else None for note in notes]
    
    print(f'notes: {notes}')
    print(octaves)

    melody = pool.starmap(et.note_name_to_midi, zip(notes, octaves))
    # midi_note = et.note_name_to_midi(notes[0][:-1],int(notes[0][-1])+2)
    # print(melody)
    for midi_note in melody:
        play_midi.play_midi_note(midi_note, beat_length)
    # print(f'midi_notes: {midi_notes}')

    # map(play_midi.play_midi_note, melody)
