import wave
import threading
import time
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
        bytesLeft = 32768;
        numRd = 0;
        values = []
        printout = "Receiving from "+self.device.hostname+"...\n"
        print (printout)
        filename = ("Recordings/"+self.device.hostname+"_"+self.dateAndTime+"_8ch.wav")
        out_sound = wave.open(filename, 'w')
        #f=open(filename,'wb+')
        # (num of channels, sampling width in bytes, sampling rate, num of frames, compression type, compression name)
        out_sound.setparams((1, 2, 16000, 1, 'NONE', 'not compressed'))
        expected_bytes = 32768 # 1 second
        totL = 0
        c=1
        
        while self.continue_recording:
            out_sound.writeframes(self.device.tcpConnection.recv(32768))
            self.seconds_recorded +=1
        out_sound.close()
        printout = self.device.hostname+" streamed for "+str(self.seconds_recorded//60)+" minutes "+str(self.seconds_recorded%60)+" seconds\n"

        print (printout)
            #file_buffer = self.device.tcpConnection.recv(4096) # it will not always receive the specified bytes
            #file_buffer_length = len(file_buffer)
            #if (file_buffer!=0):
            #    print(4096)
            #    print("filebuffer!=0")
            #    print(file_buffer)
            #if (file_buffer_length!=0):
            #    print(4096)
            #    print("file_buffer_length!=0")
            #    print(file_buffer)

            #if (self.device.tcpConnection.recv(1024)>0):
            #    print(1024)
            #    print(self.device.tcpConnection.recv(1024))
            ##while(bytesLeft!=0):
            #    file_buffer = self.device.tcpConnection.recv(bytesLeft)
            #    if(file_buffer ==0): break
            #    else:
            #        numRd += sys.getsizeof(file_buffer)
            #        if c==1: 
            #            data = file_buffer; 
            #            c=0
            #        else: 
            #            data += file_buffer
            #        bytesLeft -= sys.getsizeof(file_buffer)
            #        print("1")
            #        print(file_buffer)
            #bytes_received += file_buffer
            #print(bytes_received)
            #time.sleep(1)
            #leng = len(file_buffer)
            #totL += leng
            #if c==1:
            #    temp = file_buffer
            #    c=0
            #else:
            #    temp += file_buffer
            #if(totL>=32768):
            #    self.seconds_recorded +=1
            #    print(temp)
       
            
        #while bytes_received<expected_bytes:
        #    file_buffer = self.device.tcpConnection.recv(4096) # it will not always receive the specified bytes

        #    file_buffer_length = len(file_buffer)

        #    if file_buffer_length == 0:
        #        print self.device.hostname, "connection closed"
        #        break

        #    bytes_received += file_buffer_length

        #    if bytes_received>=expected_bytes:
        #        self.seconds_recorded +=1
        #        out_sound.writeframes(file_buffer)
        #        #print self.seconds_recorded, "seconds recorded\r",
        #        if self.continue_recording:
        #            bytes_received = bytes_received-expected_bytes                    
        #        else:
        #            file_buffer = file_buffer[0:file_buffer_length - (bytes_received-expected_bytes)]
        
            
        #out_sound.close()
        #printout = self.device.hostname+" streamed for "+str(self.seconds_recorded//60)+" minutes "+str(self.seconds_recorded%60)+" seconds\n"

        #print (printout)

        #bytes_received 
        #buff[32000]
        
        #i=True
        #c=True
        #while self.continue_recording:
        #    len = 32000
        #    while len > 0 and (self.device.tcpConnection.recv(4096) > 0 ) :
        #        dataRecieved = self.device.tcpConnection.recv(4096)
        #        #if (dataRecieved > 0):
        #        #    expected_bytes += sys.getsizeof(dataRecieved)
        #        #    bytes_received += dataRecieved
        #        #    continue
        #        if c==True:
        #            bytes_received = dataRecieved
        #        len =- sys.getsizeof(dataRecieved)
        #        c = False
        #        if c!=32000:
        #            bytes_received += dataRecieved
        #        self.seconds_recorded +=1
        #        #if ((dataRecieved == -1) and (errno == EAGAIN or errno == EWOULDBLOCK)):
        #        #    # Simple error just try again.
        #        #    continue
        #        #else: 
        #        #    break
        ##if len < 0:
        #filename = ("Recordings/"+self.device.hostname+"_"+self.dateAndTime+"_8ch.wav")
  
        #f.setparams((1, 2, 16000, 1, 'NONE', 'not compressed'))
        #f.write(bytes_received)
        #f.close()
        #out_sound.close()
        #printout = self.device.hostname+" streamed for "+str(self.seconds_recorded//60)+" minutes "+str(self.seconds_recorded%60)+" seconds\n"

        #print (printout)
        
        
        #while bytes_received<expected_bytes:
        #    file_buffer = self.device.tcpConnection.recv(4096) # it will not always receive the specified bytes

        #    file_buffer_length = len(file_buffer)

        #    if file_buffer_length == 0:
        #        print self.device.hostname, "connection closed"
        #        break

        #    bytes_received += file_buffer_length

        #    if bytes_received>=expected_bytes:
        #        self.seconds_recorded +=1
        #        #print self.seconds_recorded, "seconds recorded\r",
        #        if self.continue_recording:
        #            bytes_received = bytes_received-expected_bytes                    
        #        else:
        #            file_buffer = file_buffer[0:file_buffer_length - (bytes_received-expected_bytes)]
    
        #    out_sound.writeframes(file_buffer)
        #out_sound.close()
        #printout = self.device.hostname+" streamed for "+str(self.seconds_recorded//60)+" minutes "+str(self.seconds_recorded%60)+" seconds\n"

        #print (printout)