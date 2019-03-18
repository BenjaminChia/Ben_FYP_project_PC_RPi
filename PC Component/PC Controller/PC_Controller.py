import threading
import audioStreamReceiver
import pimatrix
import time
#import transcriptReceiver
from timeServer import TimeServer


deviceMan = pimatrix.deviceManager()
winPerfTimer = TimeServer()


def printMenu():
    print "\n"
    print "Welcome to Pi-Matrix Management Console"
    print "Device connected:", deviceMan.numDevices, "\n"
    print "1. Discover devices"
    if deviceMan.numDevices > 0:
        print "2. Connected devices' detail"
        print "----------------------------"
        if not deviceMan.deviceBusy:
            print "3. Record to disk"
            print "4. Record over network"
        else:
            print "5. Stop all devices' current task"
        print "----------------------"
        print "6. Disconnect from all devices"
        print "7. Shutdown all devices"
    print "0. terminate"


while(True):
    printMenu()
    rawChoice = raw_input("Choice: ");
    if len(rawChoice) == 0:
        choice = 1
    else:
        choice = int(rawChoice)

    if choice == 1:
        print "Scanning......"
        deviceMan.discoverDevices()
        deviceMan.tabulateDevice()
        raw_input("Press Enter to continue...")     
    
    elif choice == 2:
        deviceMan.tabulateDevice()
        raw_input("Press Enter to continue...")

    elif choice == 3:
        digit = chr((int(time.clock())+2)%10+48)
        #deviceMan.sendCommand("rec2sd") 
        deviceMan.sendCommand("rec2sd", digit)  

    elif choice == 4:
        #deviceMan.cleanTcpBuffer()
        deviceMan.clean32768TcpBuffer()
        currentDateAndTime = time.strftime("%Y%m%d_%H%M%S", time.localtime())

        streamerList = [audioStreamReceiver.RecordingStream(device, currentDateAndTime) for device in deviceMan.deviceList]
        for streamer in streamerList:
            streamer.start()
            streamer.continue_recording = True
        digit = chr((int(time.clock())+2)%10+48)
        deviceMan.sendCommand("rec2net", digit)
        raw_input("Press Enter to stop recording...")
        for streamer in streamerList:
            streamer.continue_recording = False
        #deviceMan.clean32768TcpBuffer()
        #deviceMan.sendCommand("stop")
        print "Stopping......\n"
        for streamer in streamerList:
            streamer.join()
        deviceMan.sendCommand("stop")
        deviceMan.clean32768TcpBuffer()
        #deviceMan.sendCommand("stop")

    elif choice == 5:
        deviceMan.sendCommand("stop")

    elif choice == 6:
        deviceMan.disconnectAll()
        #break

    elif choice == 0:

        break    


    elif choice == 7:
        yn = raw_input("Shutdown all devices? (y/n)")
        if  yn == "y":
            print ("shutting down now")
            deviceMan.sendCommand("shutdown")
            break
        elif  yn == "n":
            print ("shutdown cancelled")
        else:
            print ("incorrect input")
            print ("try again later")
            

print '=' * 50
print '\t\tTerminated'
print '=' * 50
print "\n\nThank you for using PC Controller"
print "Have a nice day!\n"
winPerfTimer.stop()