import wave
import threading
import sys
import socket

class RecordingStream(threading.Thread):
    def __init__(self, device, dateAndTime):
        threading.Thread.__init__(self)
        self.seconds_recorded = 0
        self.continue_recording = False
        self.device = device     
        self.dateAndTime = dateAndTime

    def run(self):
        print "\n\n"
        print '=' * 50
        printout = "\t Receiving from " + self.device.hostname + "...\n"
        print (printout)
        print '=' * 50
        filename = ("Recordings/" + self.device.hostname + "_" + self.dateAndTime + "_beamed.wav")
        out_sound = wave.open(filename, 'w')
        # (num of channels, sampling width in bytes, sampling rate, num of frames, compression type, compression name)
        out_sound.setparams((1, 2, 16000, 1, 'NONE', 'not compressed'))
        #expected_bytes/second = 32768 
        while self.continue_recording:
            out_sound.writeframes(self.device.tcpConnection.recv(32768))
            self.seconds_recorded +=1
            printout = "\n\t" + self.device.hostname + " streaming for " + str(self.seconds_recorded // 60) + " minutes " + str(self.seconds_recorded % 60) + " seconds"
            print (printout)
            print "\t Press Enter to stop recording...\n"
        
        out_sound.close()
        printout = "\n\n\t" + self.device.hostname + " streamed for " + str(self.seconds_recorded // 60) + " minutes " + str(self.seconds_recorded % 60) + " seconds\n"
        print (printout)
        print "\tRecording saved in " + filename + "\n"