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

    def __init__(self, A4=440.0):
        self.A4 = A4
        self.semitone = 2 ** (1/12)
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.all_note_names = [f'{note_name}{octave}' for octave in range(0, 9) for note_name in self.note_names]
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
            11:['7']}

    def interval_to_note_name(self, root, interval):
        """
        Returns the note name that is a given interval away from the root note.
        Intervals are based on the Major scale, thus 1,2,3,4,5,6,7 follow the semitone pattern:
        0,2,4,5,7,9,11,12

        Args:
            root (str): The root note name.
            interval (int): The interval in semitones.

        Returns:
            str: The note name that is a given interval away from the root note.
        """
        if type(interval) == int:
            interval = str(interval)
        if interval.startswith('bb'):
            interval = self.intervals[(self.intervals.index(interval[-1])-2) % len(self.intervals)]
        return self.note_names[(self.note_names.index(root) + self.intervals.index(interval)) % len(self.note_names)]
    
equal_temperament = EqualTemperament()