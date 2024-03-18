import equal_temperament as et

class Scale:
    def __init__(self, root, intervals=[], octave=4):
        self.root = root
        self.intervals = intervals
        self.octave = octave

    def get_notes(self):
        notes = [self.root]
        current_note = self.root
        for interval in self.intervals:
            current_note += interval
            notes.append(current_note)
        return notes

    def get_intervals(self):
        return self.intervals

scales = {
    # Major scales and modes
    'major':['1','2','3','4','5','6','7'],
    'ionian':['1','2','3','4','5','6','7'],
    'dorian':['1','2','b3','4','5','6','b7'],
    'phrygian':['1','b2','b3','4','5','b6','b7'],
    'lydian':['1','2','3','#4','5','6','7'],
    'mixolydian':['1','2','3','4','5','6','b7'],
    'aeolian':['1','2','b3','4','5','b6','b7'],
    'locrian':['1','b2','b3','4','b5','b6','b7'],
    # Minor scales and modes
    # Natural minor
    'minor':['1','2','b3','4','5','b6','b7'],
    'aeolian':['1','2','b3','4','5','b6','b7'],
    # Harmonic minor
    'harmonic_minor':['1','2','b3','4','5','b6','7'],
    'aeoloan_#7':['1','2','b3','4','5','b6','7'],
    'locrian_n6':['1','b2','b3','4','b5','6','b7'],
    'ionian_#5':['1','2','3','4','#5','6','7'],
    'dorian_#4':['1','2','b3','#4','5','6','b7'],
    'phyrigian_dom':['1','b2','3','4','5','b6','b7'],
    'lydian_#2':['1','#2','3','#4','5','6','7'],
    'super_locrian_bb7':['1','b2','b3','b4','b5','b6','bb7'],
    # Melodic minor
    'melodic_minor':['1','2','b3','4','5','6','7'],
    'dorian_b2':['1','b2','b3','4','5','6','b7'],
    'lydian_#5':['1','2','3','#4','#5','6','7'],
    'lydian_b7':['1','2','3','#4','5','6','b7'],
    'mixolydian_b6':['1','2','3','4','5','b6','b7'],
    'aeolian_b5':['1','2','b3','4','b5','b6','b7'],
    'super_locrian':['1','b2','b3','b4','b5','b6','b7'],
}