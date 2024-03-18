import rtmidi
import time

midiout = rtmidi.MidiOut()

# check and get the ports which are open
available_ports = midiout.get_ports()

# let's print the list of ports and see if ours is among them
# print(available_ports)


# Attempt to open the port
if available_ports:
    midiout.open_port(0) # number here should match list index

# This is how you create a midi note, the specs are: [command, note, velocity]
# note_on = [0x90, 60, 112]
# note_off = [0x80, 60, 0]
# midiout.send_message(note_on)

# #Here you need to insert a short delay before turning the note off to make sure that the note_on signal was received
# time.sleep(1.1)
# midiout.send_message(note_off)

def play_midi_note(note, duration=1):
    if note is None:
        return
    note_on = [0x90, note, 112]
    note_off = [0x80, note, 0]
    midiout.send_message(note_on)
    time.sleep(duration/1)
    midiout.send_message(note_off)

def play_midi_chord(chord, duration=1):
    for note in chord:
        note_on = [0x90, note, 112]
        note_off = [0x80, note, 0]
        midiout.send_message(note_on)
    time.sleep(duration/1)
    for note in chord:
        note_off = [0x80, note, 0]
    midiout.send_message(note_off)

def play_melody(melody, duration=1):
    for i, note in enumerate(melody):
        if note is None:
            time.sleep(duration/1)
        else:
            if i == 0:
                play_midi_note(note, duration)
            else:
                if note != melody[i-1]:
                    play_midi_note(note, duration)
                else:
                    time.sleep(duration/1)
    time.sleep(duration/1)