import math
class EqualTemperament:
    """
    Represents an equal temperament scale.

    Attributes:
        A4 (float): The frequency of the A4 note in Hz. Default is 440.0.
        semitone (float): The ratio of frequencies between adjacent semitones.
        note_names (list): The names of the 12 notes in an octave.
        all_note_names (list): The names of all notes in the equal temperament scale (over 10 octaves from C0 to C9).

    Methods:
        interval_to_note_name(root, interval): Returns the note name that is a given interval away from the root note.
    """

    def __init__(self, A4=440):
        self.A4 = A4
        self.semitone = 2 ** (1/12)
        self.notes = {
            0:['C','B#'], 
            1:['C#','Db'], 
            2:['D','C##'], 
            3:['D#','Eb'], 
            4:['E','Fb','D##'], 
            5:['F','E#'], 
            6:['F#','Gb'], 
            7:['G','F##'], 
            8:['G#','Ab'], 
            9:['A','G##'], 
            10:['A#','Bb'], 
            11:['B','Cb','A##'],
        }
        self.notes_list = [item for _,sublist in self.notes.items() for item in sublist]
        self.all_note_names = [f'{note_name[0]}{octave}' for octave in range(0, 9) for note_name in self.notes.values()]
        self.intervals = {
            0:['1'],
            1:['b2'],
            2:['2'],
            3:['b3'],
            4:['3'],
            5:['4'],
            6:['#4','b5'],
            7:['5'],
            8:['#5','b6'],
            9:['6','bb7'],
            10:['#6','b7'],
            11:['7'],
        }

et = EqualTemperament()
    
def note_name_to_frequency(note_name, octave):
    """
    Calculate the frequency of a note in equal temperament.

    Parameters:
    - note_name (str): The name of the note (e.g., 'A', 'C', 'D')
    - octave (int): The octave number of the note

    Returns:
    - float: The frequency of the note in Hertz
    """
    note = et.all_note_names.index(f'{note_name}{octave}') - et.all_note_names.index('A4')
    return round(et.A4 * (et.semitone ** note))

def interval_to_note_name(root, interval):
    """
    Returns the note name that is a given interval away from the root note.
    Intervals are based on the Major scale, thus 1,2,3,4,5,6,7 follow the semitone pattern:
    0,2,4,5,7,9,11,12

    Args:
        root (str): The root note name.
        interval (str or int): The interval in semitones.

    Returns:
        str: The note name that is a given interval away from the root note.
    """
    # print(interval, et.intervals.items())
    interval_index = next(key for key, value in et.intervals.items() if interval in value)
    root_index = next((index for index, names in et.notes.items() if root in names), None)
    if root_index is not None:
        return et.note_names[(root_index + interval_index) % len(et.note_names)][0]
    else:
        return None

def note_name_to_midi_number(note_name):
    """
    Calculate the MIDI number of a note.

    Parameters:
    - note_name (str): The name of the note (e.g., 'A1', 'C1', 'D2')

    Returns:
    - int: The MIDI number of the note
    """
    if note_name is None:
        return None
    if not note_name[-1].isdigit():
        return None
    if note_name[:-1] not in et.notes_list:
        return None
    # print(note_name)
    note = note_name[:-1]
    octave = note_name[-1]
    return et.all_note_names.index(f'{note}{octave}') + 21 # MIDI number of A0 is 21

def midi_number_to_note_name(midi_number):
    """
    Calculate the note name of a given MIDI number.

    Parameters:
    - midi_number (int): The MIDI number of the note

    Returns:
    - str: The name of the note (e.g., 'A', 'C', 'D')
    """
    if midi_number < 21 or midi_number > 108:
        return None
    return et.all_note_names[midi_number - 21]

def frequency(note_name, octave):
    """
    Calculate the frequency of a note in equal temperament.

    Parameters:
    - note_name (str): The name of the note (e.g., 'A', 'C', 'D')
    - octave (int): The octave number of the note

    Returns:
    - float: The frequency of the note in Hertz
    """
    note = et.all_note_names.index(f'{note_name}{octave}') - et.all_note_names.index('A4')
    return round(et.A4 * (et.semitone ** note))

def frequency_at_fret(tuning, fret):
    """
    Calculates the frequency of the note at a given fret on the string.
    
    Args:
        tuning (str): The tuning note of the string.
        fret (int): The fret number.
    
    Returns:
        float: The frequency of the note at the specified fret.
    """
    return round(et.frequency(tuning[:-1], int(tuning[-1])) * (et.semitone ** fret))

def frequency_to_note_name(frequency):
    """
    Calculate the note name of a given frequency in equal temperament.

    Parameters:
    - frequency (float): The frequency of the note in Hertz

    Returns:
    - str: The name of the note (e.g., 'A', 'C', 'D')
    """
    if frequency <= 0:
        return None
    note = round(12 * math.log2(frequency / et.A4))
    # print(len(et.all_note_names), (note + et.all_note_names.index('A4')) % len(et.all_note_names))
    return et.all_note_names[(note + et.all_note_names.index('A4')) % len(et.all_note_names)]

def transpose(note_name,semitones):
    """
    Transpose a note by a given number of semitones.
    Make use of midi numbering to transpose notes.

    Args:
        note_name (str): The name of the note (e.g., 'A', 'C', 'D')
        semitones (int): The number of semitones to transpose the note.

    Returns:
        str: The name of the transposed note (e.g., 'A', 'C', 'D')
    """
    if note_name is None:
        return None
    return midi_number_to_note_name(note_name_to_midi_number(note_name) + semitones)