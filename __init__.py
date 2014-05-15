from Inst import Instrument
import sys
import signal
#import time
import rtmidi


def ctl_C_pressed(signal , frame):
    print("Cleaning mess...")

    sys.exit(0)
    

def MCallback(msg , data):
    msgbit = format(msg[0][0],'02X')[0] #Select the first bit in hex string form
    if msgbit is '9':
        print("DBG: MCallback(): NoteOn Recieved")
        trump.noteOn(msg[0][1])
    elif msgbit is '8':
        print("DBG: MCallback(): NoteOff Recieved")
        trump.noteOff(msg[0][1])
    else: print("DBG: MCallback(): Unknown Msg Recieved. Ignore")

signal.signal(signal.SIGINT, ctl_C_pressed)  
print("Simple MIDI Robotics Controller")
print("Ponkaza Works. All rights stolen")
print("")
not2bit_Amaj={"A":0b110 , "B":0b010 , "Csh":0b110 , "D":0b100 , "E":0b000 , "Fsh":0b101 , "Gsh":0b100} #A major t
#not2bit_Bflmaj={"Bb":0b100 , "C":0b000 , "D":0b100 , "Eb":0b010 , "F":0b100 , "G":0b000 , "A":0b110 , "Bb":0b100} #Trompeta en escala B bemol
not2bit_Bflmaj={"As3":0b100 , "C4":0b000 , "D4":0b100 , "Ds4":0b010 , "F4":0b100 , "G4":0b000 , "A4":0b110 , "As4":0b100 , "C5":0b000}
trump = Instrument(not2bit_Bflmaj , 3 , False , 0)
print("Initializing MIDI Connection")
midiIn = rtmidi.MidiIn(rtapi = rtmidi.API_LINUX_ALSA , name = "Ponkaza Robotic Musical Interface" )
print("Openning Virtual Port")
midiIn.open_virtual_port(name = "Input")
#TODO: Iniciar multimidicast desde aqui
midiIn.set_callback(MCallback)
print("OK. Waiting for MIDI Data")


while True:
    #signal.pause()
    raw_input()