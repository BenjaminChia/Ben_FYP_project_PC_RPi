#!/usr/bin/env python3
"""Create a recording with arbitrary duration.

PySoundFile (https://github.com/bastibe/PySoundFile/) has to be installed!

"""

import argparse
import tempfile
import queue
import sys
import time


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args()




def printMenu():

    print('_' * 50)
    print("\n")
    print ("Welcome to Recorder Management Console")
    print('_' * 50)
    print ("\n1. List Devices")
    print ("\n2. Recorder microphone")
    print("\n3. Terminate\n")
    #print ("3. stop record microphone")


while True:
    try:
        import sounddevice as sd
        import soundfile as sf
        import numpy  # Make sure NumPy is loaded before it is used in the callback

        assert numpy  # avoid "imported but unused" message (W0611)
        printMenu()
        rawChoice = input("\nChoice: ")
        choice = int(rawChoice)

        if choice == 1:
            print(sd.query_devices())
            input("\nEnter to continue")
        if choice == 2:
            try:
                if args.samplerate is None:
                    device_info = sd.query_devices(args.device, 'input')
                    # soundfile expects an int, sounddevice provides a float:
                    args.samplerate = 16000 #int(device_info['default_samplerate'])

                rawnumdevice = input("Num of devices: ")
                numdevice = int(rawnumdevice)
                chosendevice = [None] * numdevice
                filename = [None] * numdevice
                for i in range(numdevice):
                    print("Device ", i+1)
                    rawchosendevice = input("choose your device: ")
                    chosendevice[i] = int(rawchosendevice)
                    namef = (sd.query_devices(chosendevice[i], 'input')['name'])
                    filename[i]= time.strftime("%d%m%Y_%H%M") + ' Device'+str(i+1)+'_'+namef+'.wav'
                q = queue.Queue()

                def callback(indata, frames, time, status):
                    """This is called (from a separate thread) for each audio block."""
                    if status:
                        print(status, file=sys.stderr)
                    q.put(indata.copy())

                if numdevice == 1:
                    with sf.SoundFile(filename[0], mode='x', samplerate=args.samplerate,
                                      channels=args.channels, subtype=args.subtype) as file:
                        with sd.InputStream(samplerate=args.samplerate, device=chosendevice[0],
                                            channels=args.channels, callback=callback):
                            print("\n")
                            print('#' * 80)
                            print('press Ctrl+C to stop the recording')
                            print('#' * 80)

                            while True:
                                file.write(q.get())

                if numdevice == 2:
                    with sf.SoundFile(filename[0], mode='x', samplerate=args.samplerate,
                                      channels=args.channels, subtype=args.subtype) as file:
                        with sf.SoundFile(filename[1], mode='x', samplerate=args.samplerate,
                                          channels=args.channels, subtype=args.subtype) as file1:
                            with sd.InputStream(samplerate=args.samplerate, device=chosendevice[0],
                                            channels=args.channels, callback=callback):
                                with sd.InputStream(samplerate=args.samplerate, device=chosendevice[1],
                                                    channels=args.channels, callback=callback):
                                    print("\n")
                                    print('#' * 80)
                                    print('press Ctrl+C to stop the recording')
                                    print('#' * 80)

                                    while True:
                                        file.write(q.get())
                                        file1.write(q.get())
                if numdevice == 3:
                    with sf.SoundFile(filename[0], mode='x', samplerate=args.samplerate,
                                      channels=args.channels, subtype=args.subtype) as file:
                        with sf.SoundFile(filename[1], mode='x', samplerate=args.samplerate,
                                          channels=args.channels, subtype=args.subtype) as file1:
                            with sf.SoundFile(filename[2], mode='x', samplerate=args.samplerate,
                                              channels=args.channels, subtype=args.subtype) as file2:
                                with sd.InputStream(samplerate=args.samplerate, device=chosendevice[0],
                                                    channels=args.channels, callback=callback):
                                    with sd.InputStream(samplerate=args.samplerate, device=chosendevice[1],
                                                        channels=args.channels, callback=callback):
                                        with sd.InputStream(samplerate=args.samplerate, device=chosendevice[2],
                                                            channels=args.channels, callback=callback):
                                            print("\n")
                                            print('#' * 80)
                                            print('\t\tCtrl+C to stop the recording')
                                            print('#' * 80)

                                            while True:
                                                file.write(q.get())
                                                file1.write(q.get())
                                                file2.write(q.get())
            except KeyboardInterrupt:
                for i in range(numdevice):
                    print("\nDevice ", i+1)
                    print('Recording finished: ' + repr(filename[i]))

        if choice == 3:
            print('=' * 50)
            print('\t\tTerminated')
            print('=' * 50)
            break

    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

