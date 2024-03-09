import guitar_string as gs

class Fretboard:
    def __init__(self, tuning):
        self.strings = []
        for i in range(0, len(tuning),2):
            self.strings.append(gs.GuitarString(tuning[i]+tuning[i+1]))
    
    def __str__(self):
        return f"Fretboard({self.strings})"