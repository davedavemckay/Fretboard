import equal_temperament as et

class Chord:
    def __init__(self, root, intervals=[], octave=4, quality=None, inversion=0):
        self.root = root
        if quality is None and len(intervals) == 0:
            raise ValueError("Either quality or intervals must be provided.")
        if len(intervals) == 0:
            self.intervals = chord_types[quality]
            self.quality=quality
        else:
            self.intervals = intervals
            self.quality = list(chord_types.keys())[list(chord_types.values()).index(intervals)]
        if inversion >= len(self.intervals):
            raise ValueError("Inversion cannot be greater than the number of notes in the chord.")
        self.inversion = inversion
        self.inverted_indices = []
        # print(self.intervals)
        # Take A minor chord as an example
        # A minor chord: A, C, E
        # A minor chord with first inversion: C, E, A
        # A minor chord with second inversion: E, A, C
        # A minor chord with third inversion: A, C, E - hence, the same as the original chord
        # if inversion == 0, self.intervals[inversion-1:] + self.intervals[:inversion-1] = self.intervals
        # if inversion == 1, self.intervals[inversion-1:] + self.intervals[:inversion-1] = self.intervals[1:] + self.intervals[:1] = [C, E, A]
        # if inversion == 2, self.intervals[inversion-1:] + self.intervals[:inversion-1] = self.intervals[2:] + self.intervals[:2] = [E, A, C]
        # if inversion == 3, self.intervals[inversion-1:] + self.intervals[:inversion-1] = self.intervals[3:] + self.intervals[:3] = [A, C, E]
        # hence if inversion >= 3, ValueError
        if self.inversion > 0:
            self.intervals = self.intervals[self.inversion:] + self.intervals[:self.inversion]
            # print(self.inversion)
            self.inverted_indices = [i for i in range(-1, -self.inversion - 1, -1)]  # -1, -2, -3, etc.
            # print(self.inverted_indices)
            # print(-self.inversion)
            # print([i for i in range(-1, -self.inversion - 1, -1)])
            # print(self.intervals[self.inversion:])
            # print(self.intervals[:self.inversion])
        elif self.inversion < 0:    
            raise ValueError("Inversion cannot be negative.")
        # print(self.intervals)
        self.intervals_without_accidentals = []
        self.intervals_in_octave = []
        self.intervals_without_accidentals_in_octave = []
        for interval in self.intervals:
            interval_in_octave = interval
            if type(interval) == int:
                interval = str(interval)
            if interval.startswith('b') or interval.startswith('#'):
                interval_without_accidental = int(interval[1:])
            else:
                interval_without_accidental = int(interval)
            interval_without_accidental_in_octave = interval_without_accidental
            if interval_without_accidental_in_octave > 7:
                interval_without_accidental_in_octave = interval_without_accidental % 7
                interval_in_octave = interval.replace(str(interval_without_accidental), str(interval_without_accidental_in_octave))
            self.intervals_without_accidentals.append(interval_without_accidental)
            self.intervals_in_octave.append(interval_in_octave)
            self.intervals_without_accidentals_in_octave.append(interval_without_accidental_in_octave)
            
        # Set up octaves
        # Input octave is the default octave - that of the lowest note in the chord (inversion)
        # If the interval is greater than 7, add 1 to the octave
        # If the interval is less than or equal to the previous interval, add 1 to the octave
        self.octaves = [octave for i in self.intervals]
        for i,interval in enumerate(self.intervals):
            if int(self.intervals_without_accidentals[i]) > 7:
                self.octaves[i] += 1
        for ii in self.inverted_indices:
            self.octaves[ii] += 1    
        print(self.intervals, self.octaves)


    def get_note_names(self):
        note_names = []
        for i, interval_in_octave in enumerate(self.intervals_in_octave):
            note_names.append(f'{et.interval_to_note_name(self.root, interval_in_octave)}{self.octaves[i]}')
        return note_names
    
    def get_frequencies(self):
        frequencies = []
        for note_name in enumerate(self.get_note_names()):
            frequencies.append(et.note_name_to_frequency(note_name[:-1], note_name[-1]))
        return frequencies
    
    def __str__(self) -> str:
        return f"Chord({self.root}, {self.intervals})"
    
    __repr__ = __str__

chord_types = {
    # Major
    'major':['1','3','5'],
    'major6':['1','3','5','6'],
    'major7':['1','3','5','7'],
    'major9':['1','3','5','7','9'],
    'major13':['1','3','5','7','9','13'],
    # Minor
    'minor':['1','b3','5'],
    'minor6':['1','b3','5','6'],
    'minor7':['1','b3','5','b7'],
    'minor9':['1','b3','5','b7','9'],
    'minor11':['1','b3','5','b7','9','11'],
    'minor13':['1','b3','5','b7','9','13'],
    # Diminished
    'diminished':['1','b3','b5'],
    'diminished7':['1','b3','b5','bb7'],
    'halfdiminished':['1','b3','b5','b7'],
    # Augmented
    'augmented':['1','3','#5'],
    'augmented7':['1','3','#5','b7'],
    # Dominant
    'dominant7':['1','3','5','b7'],
    'dominant9':['1','3','5','b7','9'],
    'dominant11':['1','3','5','b7','9','11'],
    # Suspended and Add
    'sus2':['1','2','5'],
    'sus4':['1','4','5'],
    'add9':['1','3','5','9'],
}