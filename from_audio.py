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

def convert_to_notes(audio_array):
    # Perform Fourier transform
    spectrum = fft(audio_array)

    # Find dominant frequency
    dominant_frequency = np.argmax(np.abs(spectrum))

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
    note = convert_to_notes(audio_array)
    bpm = calculate_bpm(audio_array, sample_rate)

    print('Note:', note)
    print('BPM:', bpm)

    chunk_size = bpm * len(audio_array) // (sample_rate*60)
    audio_array = audio_array[:len(audio_array) - len(audio_array) % chunk_size]
    audio_chunks = np.split(audio_array, len(audio_array) // chunk_size)
    beat_length = 60 / bpm

    # Create a pool of processes
    pool = mp.Pool(mp.cpu_count())

    notes = pool.map(convert_to_notes, audio_chunks)

    print(f'notes: {notes[:10]}')

    # notes = np.array([note for note in notes if note is not np.nan])

    beats = [beat_length for _ in range(len(notes))]
    print(f'beats: {beats[:10]}')
    # melody = zip([notes, beats])
    # print(melody)

    midi_notes = pool.starmap(et.note_name_to_midi, [notes, repeat(2)])

    print(f'midi_notes: {midi_notes}')

    # map(play_midi.play_midi_note, melody)
