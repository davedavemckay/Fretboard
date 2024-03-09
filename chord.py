from equal_temperament import equal_temperament as et

class Chord:
    def __init__(self, root, intervals=[]):
        self.root = root
        self.intervals = intervals

    def get_note_names(self):
        note_names = []
        for interval in self.intervals:
            note_names.append(et.interval_to_note_name(self.root, interval))
        return note_names
    
    def __str__(self) -> str:
        return f"Chord({self.root}, {self.intervals})"
    
    __repr__ = __str__

chord_types = {
    # Major
    'major':[1,3,5],
    'major6':[1,3,5,6],
    'major7':[1,3,5,7],
    'major9':[1,3,5,7,9],
    'major13':[1,3,5,7,9,13],
    # Minor
    'minor':[1,'b3',5],
    'minor6':[1,'b3',5,6],
    'minor7':[1,'b3',5,'b7'],
    'minor9':[1,'b3',5,'b7',9],
    'minor11':[1,'b3',5,'b7',9,11],
    'minor13':[1,'b3',5,'b7',9,13],
    # Diminished
    'diminished':[1,'b3','b5'],
    'diminished7':[1,'b3','b5','bb7'],
    'halfdiminished':[1,'b3','b5','b7'],
    # Augmented
    'augmented':[1,3,'#5'],
    'augmented7':[1,3,'#5','b7'],
    # Dominant
    'dominant7':[1,3,5,'b7'],
    'dominant9':[1,3,5,'b7',9],
    'dominant11':[1,3,5,'b7',9,11],
    # Suspended and Add
    'sus2':[1,2,5],
    'sus4':[1,4,5],
    'add9':[1,3,5,9],
}