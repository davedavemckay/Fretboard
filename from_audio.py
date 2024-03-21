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
    # if dominant_frequency > 0:
    #     print(dominant_frequency)
    # exit()

    # Convert dominant frequency to note
    note = et.frequency_to_note_name(dominant_frequency)

    return note


def convert_to_multinotes(audio_array, sample_rate=44100, max_notes=3):
    """
    Converts an audio array into a list of note names.
    The number simultaneously playing notes to extract (such as in a chord) is determined by the max_notes parameter.

    Parameters:
    - audio_array (array-like): The input audio array.
    - sample_rate (int, optional): The sample rate of the audio. Default is 44100.
    - max_notes (int, optional): The maximum number of notes to extract. Default is 3.

    Returns:
    - notes (list): A list of note names extracted from the audio.

    """
    # Perform Fourier transform
    spectrum = fft(audio_array)
    spectrum = [abs(x.real) for x in spectrum]
    spectrum_stack = list(spectrum)
    # print(spectrum)
    frequency_indices = []
    unique_frequency_indices = []
    while len(unique_frequency_indices) < max_notes:
        # Find dominant frequency
        if len(spectrum_stack) == 0:
            continue
        frequency_indices.append(spectrum_stack.pop(np.argmax(np.abs(spectrum_stack))))
        unique_frequency_indices = list(set(frequency_indices))
    

    # Get the maximum magnitude
    max_magnitude = np.max(np.abs(spectrum))

    # Remove any frequencies with magnitude less than 10% of the maximum frequency
    print('ufi',unique_frequency_indices)
    unique_frequency_indices = [i for i in unique_frequency_indices if i == 0 or np.abs(spectrum.index(i)) >= 0.1 * max_magnitude]

    # Convert frequency indices to frequencies
    dominant_frequencies = [unique_frequency * sample_rate / len(audio_array) for unique_frequency in unique_frequency_indices]
    # if dominant_frequency > 0:
    #     print(dominant_frequency)
    # exit()

    # Convert dominant frequency to note
    notes = [et.frequency_to_note_name(dominant_frequency) for dominant_frequency in dominant_frequencies]

    return notes

def max_fft_count(audio_array):
    # Perform Fourier transform
    spectrum = fft(audio_array)

    return np.max(np.abs(spectrum).real)

if __name__ == '__main__':
    # Example usage
    file_path = 'samples/eqt-chromo-sc.wav'
    audio_array, sample_rate = read_wav_file(file_path)

    bpm = 60#calculate_bpm(audio_array, sample_rate)
    bps = bpm / 60
    beats = len(audio_array) / sample_rate * bps
    print(audio_sample_length(audio_array, sample_rate),'seconds')

    print('BPM:', bpm)
    print('BPS:', bps)
    print('Sample rate:', sample_rate)
    print('Audio array length:', len(audio_array), 'samples')
    # exit()
    chunk_size = int(len(audio_array) / beats / 16)
    # print(len(audio_array))
    # print(bpm)
    # print(sample_rate)
    print('chunk size',chunk_size,'samples')
    print('chunk size',chunk_size/sample_rate,'seconds')
    audio_array = audio_array[:len(audio_array) - len(audio_array) % chunk_size]
    print(len(audio_array))
    # print(audio_array.shape)
    audio_chunks = np.split(audio_array, len(audio_array) // chunk_size)
    print('num chunks',len(audio_chunks))
    # print(audio_chunks[7])
    # print(beat_length)
    # print(convert_to_notes(audio_chunks[7], sample_rate))
    # exit()

    # Create a pool of processes
    pool = mp.Pool(mp.cpu_count())

    max_counts = pool.map(max_fft_count, audio_chunks)
    normalisation_factor = max(max_counts)
    # exit()

    audio_chunks = [audio_chunk / normalisation_factor for audio_chunk in audio_chunks]

    notes = pool.starmap(convert_to_notes, zip(audio_chunks, repeat(sample_rate)))
    
    print(f'notes: {notes}')
    # exit()
    melody = pool.map(et.note_name_to_midi_number, notes)
    # midi_note = et.note_name_to_midi(notes[0][:-1],int(notes[0][-1])+2)
    print(melody)
    print(len(melody))
    print(len(melody) * chunk_size/sample_rate + chunk_size/sample_rate)
    sleep_time = chunk_size/sample_rate
    # for midi_note in melody:
    #     if midi_note is not None:
            
    #         sleep(sleep_time)
    #     else:
    #         play_midi.play_midi_note(midi_note, chunk_size/sample_rate)
    # sleep(sleep_time)
    # play_midi.play_melody(melody, chunk_size/sample_rate)
    print(chunk_size/sample_rate)
    # print(f'midi_notes: {midi_notes}')

    # map(play_midi.play_midi_note, melody)
    # play_midi.play_midi_note(89,beat_length)

    octave_down = pool.starmap(et.transpose, zip(notes, repeat(-12)))
    print(octave_down)
    octave_down_melody = pool.map(et.note_name_to_midi_number, octave_down)
    # play_midi.play_melody(octave_down_melody, chunk_size/sample_rate)

    multinotes = pool.starmap(convert_to_multinotes, zip(audio_chunks, repeat(sample_rate), repeat(3)))
    print(f'multinotes: {multinotes}')
    chord_melody = pool.map(et.note_name_to_midi_number, multinotes)
    print(f'chord melody: {chord_melody}')
    play_midi.play_chord_melody(chord_melody, chunk_size/sample_rate)
