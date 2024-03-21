import rtmidi
import time

midiout = rtmidi.MidiOut()

# check and get the ports which are open
available_ports = midiout.get_ports()

# let's print the list of ports and see if ours is among them
# print(available_ports)


# Attempt to open the port
if available_ports:
    midiout.open_port(1) # number here should match list index
print('MIDI port open', midiout.get_port_name(0))

# This is how you create a midi note, the specs are: [command, note, velocity]
# note_on = [0x90, 60, 112]
# note_off = [0x80, 60, 0]
# midiout.send_message(note_on)

# #Here you need to insert a short delay before turning the note off to make sure that the note_on signal was received
# time.sleep(1.1)
# midiout.send_message(note_off)

def play_note(note, duration=1):
    if note is None:
        return
    note_on = [0x90, note, 90]
    note_off = [0x80, note, 0]
    
    midiout.send_message(note_on)
    time.sleep(duration)
    midiout.send_message(note_off)

def play_chord(chord, duration=1):
    for note in chord:
        note_on = [0x90, note, 112]
        note_off = [0x80, note, 0]
        midiout.send_message(note_on)
    time.sleep(duration)
    for note in chord:
        note_off = [0x80, note, 0]
    midiout.send_message(note_off)

def play_melody(melody, duration=1):
    for i, note in enumerate(melody):
        if note is None:
            time.sleep(duration)
        else:
            if i == 0:
                play_note(note, duration)
            else:
                if note != melody[i-1]:
                    print(note)
                    play_note(note, duration)
                else:
                    time.sleep(duration)
    time.sleep(duration)

def play_chord_melody(melody, duration=1):
    for i, note_list in enumerate(melody):
        if note_list is None:
            time.sleep(duration)
        elif None in note_list:
            time.sleep(duration)
        else:
            if i == 0:
                play_chord(note_list, duration)
            else:
                if note_list != melody[i-1]:
                    # print(note)
                    play_chord(note_list, duration)
                else:
                    time.sleep(duration)
    time.sleep(duration)