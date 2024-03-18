from time import sleep
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
        num_channels = wav_file.getnchannels()

        # Read audio data
        audio_data = wav_file.readframes(num_frames)

        # Convert audio data to numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        # If stereo, convert to mono
        if num_channels == 2:
            audio_array = audio_array.reshape(-1, 2).mean(axis=1)

        return audio_array, sample_rate

def calculate_bpm(audio_array, sample_rate, window_size=512):
    # Calculate the energy of the signal over windows of time
    energy = np.array([np.sum(np.abs(audio_array[i:i+window_size]**2)) for i in range(0, len(audio_array), window_size)])

    # Identify peaks in the energy as beats
    beats = np.where(energy > np.mean(energy) + np.std(energy))[0]

    # print(len(beats),'beats detected')
    # print(len(audio_array) / sample_rate / 60)
    # Check if no beats are detected
    if len(beats) == 0:
        return 0

    # Calculate BPM
    bpm = len(beats) / (len(audio_array) / sample_rate / 60)
    bpm = round(bpm)
    return bpm

def audio_sample_length(audio_array, sample_rate):
    """
    Calculates the length of an audio sample in seconds.

    Args:
        audio_array (array-like): The audio sample as an array-like object.
        sample_rate (int): The sample rate of the audio sample.

    Returns:
        float: The length of the audio sample in seconds.
    """
    return len(audio_array) / sample_rate

def convert_to_notes(audio_array, sample_rate=44100):
    # Perform Fourier transform
    spectrum = fft(audio_array)
    # print(spectrum)
    
    # Find dominant frequency
    dominant_frequency_index = np.argmax(np.abs(spectrum))
    # print(dominant_frequency_index)
    # print(spectrum[dominant_frequency_index])
    dominant_frequency = dominant_frequency_index * sample_rate / len(audio_array)
    print(dominant_frequency)
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
    print(audio_sample_length(audio_array, sample_rate),'seconds')

    print('BPM:', bpm)
    # exit()
    chunk_size = bpm * len(audio_array) // (sample_rate*60)
    # print(len(audio_array))
    # print(bpm)
    # print(sample_rate)
    print(chunk_size)
    audio_array = audio_array[:len(audio_array) - len(audio_array) % chunk_size]
    # print(len(audio_array))
    # print(audio_array.shape)
    audio_chunks = np.split(audio_array, len(audio_array) // chunk_size)
    # print(len(audio_chunks))
    # print(audio_chunks[7])
    beat_length = 60 / bpm * 1000
    # print(beat_length)
    # print(convert_to_notes(audio_chunks[7], sample_rate))
    # exit()

    # Create a pool of processes
    pool = mp.Pool(mp.cpu_count())

    notes = pool.starmap(convert_to_notes, zip(audio_chunks, repeat(sample_rate)))
    octaves = [int(note[-1]) for note in notes if note is not None]
    notes = [note[:-1] for note in notes if note is not None]
    
    
    
    # print(f'notes: {notes}')
    # print(octaves)
    # exit()
    melody = pool.starmap(et.note_name_to_midi, zip(notes, octaves))
    # midi_note = et.note_name_to_midi(notes[0][:-1],int(notes[0][-1])+2)
    print(len(melody) * chunk_size / 1000 / 60)
    for midi_note in melody:
        if midi_note is not None:
            sleep_time = chunk_size / 1000 / 60
            sleep(sleep_time)
        else:
            play_midi.play_midi_note(midi_note, beat_length)
    # print(f'midi_notes: {midi_notes}')

    # map(play_midi.play_midi_note, melody)
