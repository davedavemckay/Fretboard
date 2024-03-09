from equal_temperament import equal_temperament as et

class GuitarString:
    """
    Represents a guitar string with various properties and methods.
    
    Attributes:
        tuning (str): The tuning note of the string.
        note (int): The distance of the tuning note from A4.
    """
    
    def __init__(self, tuning):
        """
        Initializes a new instance of the GuitarString class.
        
        Args:
            tuning (str): The tuning note of the string.
        
        Raises:
            ValueError: If the tuning note is invalid.
        """
        if tuning not in et.all_note_names:
            raise ValueError(f"Invalid tuning note {tuning}")
        self.tuning = tuning
        self.note = self.distance_from_A4()

    def note_name_at_fret(self, fret):
        """
        Calculates the note name at a given fret on the string.
        
        Args:
            fret (int): The fret number.
        
        Returns:
            str: The note name at the specified fret.
        
        Raises:
            ValueError: If the fret number is invalid.
        """
        if fret < 0:
            raise ValueError(f"Invalid fret {fret}")
        if fret == 0:
            return self.tuning
        index = (et.all_note_names.index(self.tuning) + fret) % len(et.note_names)
        octave = (et.all_note_names.index(self.tuning) + fret) // len(et.note_names)
        return f'{et.note_names[index]}{octave}'
    
    def distance_from_A4(self):
        """
        Calculates the distance of the tuning note from A4.
        
        Returns:
            int: The distance of the tuning note from A4.
        """
        return et.all_note_names.index(self.tuning) - et.all_note_names.index('A4')
    
    def frequency_at_fret(self, fret):
        """
        Calculates the frequency of the note at a given fret on the string.
        
        Args:
            fret (int): The fret number.
        
        Returns:
            float: The frequency of the note at the specified fret.
        """
        return et.A4 * (et.semitone ** (self.note + fret))
    
    def frequency(self):
        """
        Calculates the frequency of the open string.
        
        Returns:
            float: The frequency of the open string.
        """
        return et.A4 * (et.semitone ** self.note)
    
    def __str__(self):
        """
        Returns a string representation of the GuitarString object.
        
        Returns:
            str: The string representation of the GuitarString object.
        """
        return f"GuitarString({self.tuning})"
    
    def __repr__(self):
        """
        Returns a string representation of the GuitarString object.
        
        Returns:
            str: The string representation of the GuitarString object.
        """
        return f"GuitarString({self.tuning})"
    
    def __eq__(self, other):
        """
        Checks if two GuitarString objects are equal.
        
        Args:
            other (GuitarString): The other GuitarString object to compare.
        
        Returns:
            bool: True if the two objects are equal, False otherwise.
        """
        return self.tuning == other.tuning
    
    def __hash__(self):
        """
        Returns the hash value of the GuitarString object.
        
        Returns:
            int: The hash value of the GuitarString object.
        """
        return hash(self.tuning)
    
    def __lt__(self, other):
        """
        Checks if the current GuitarString object is less than the other GuitarString object.
        
        Args:
            other (GuitarString): The other GuitarString object to compare.
        
        Returns:
            bool: True if the current object is less than the other object, False otherwise.
        """
        return self.tuning < other.tuning
    
    def __le__(self, other):
        """
        Checks if the current GuitarString object is less than or equal to the other GuitarString object.
        
        Args:
            other (GuitarString): The other GuitarString object to compare.
        
        Returns:
            bool: True if the current object is less than or equal to the other object, False otherwise.
        """
        return self.tuning <= other.tuning
    
    def __gt__(self, other):
        """
        Checks if the current GuitarString object is greater than the other GuitarString object.
        
        Args:
            other (GuitarString): The other GuitarString object to compare.
        
        Returns:
            bool: True if the current object is greater than the other object, False otherwise.
        """
        return self.tuning > other.tuning
    
    def __ge__(self, other):
        """
        Checks if the current GuitarString object is greater than or equal to the other GuitarString object.
        
        Args:
            other (GuitarString): The other GuitarString object to compare.
        
        Returns:
            bool: True if the current object is greater than or equal to the other object, False otherwise.
        """
        return self.tuning >= other.tuning
    
    def __add__(self, other):
        """
        Adds two GuitarString objects together.
        
        Args:
            other (GuitarString): The other GuitarString object to add.
        
        Returns:
            str: The result of adding the two GuitarString objects.
        """
        return self.tuning + other.tuning
    
    def __sub__(self, other):
        """
        Subtracts one GuitarString object from another.
        
        Args:
            other (GuitarString): The other GuitarString object to subtract.
        
        Returns:
            str: The result of subtracting the two GuitarString objects.
        """
        return self.tuning - other.tuning