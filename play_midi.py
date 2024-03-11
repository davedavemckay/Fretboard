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

def play_midi_note(note, duration=1000):
    note_on = [0x90, note, 112]
    note_off = [0x80, note, 0]
    midiout.send_message(note_on)
    time.sleep(duration/1000)
    midiout.send_message(note_off)

def play_midi_chord(chord, duration=1000):
    for note in chord:
        note_on = [0x90, note, 112]
        note_off = [0x80, note, 0]
        midiout.send_message(note_on)
    time.sleep(duration/1000)
    for note in chord:
        note_off = [0x80, note, 0]
    midiout.send_message(note_off)