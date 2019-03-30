import threading
import audioStreamReceiver
import pimatrix
import time

from timeServer import TimeServer

deviceMan = pimatrix.deviceManager()
winPerfTimer = TimeServer()


def printMenu():
    print "\n"
    print "\tPC Controller for Matrix RPi\n"
    if deviceMan.numDevices == 0:
        print("\n\tNo device connected")
    else:
        print "\tDevice connected:", deviceMan.numDevices
    print "\t" + '=' * 30
    print "\n\t1. Discover devices"
    if deviceMan.numDevices > 0:
        print "\t2. Connected devices' detail"
        print "\t" + '-' * 30
        if not deviceMan.deviceBusy:
            print "\t3. Record to disk"
            print "\t4. Record over network"
        else:
            print "\t5. Stop all devices' current task"
        print "\t" + '-' * 30
        print "\t6. Disconnect from all devices"
        if not deviceMan.deviceBusy: 
            print "\t7. Shutdown all devices"
    print "\t0. Terminate"
    print "\n\t" + '=' * 30


while(True):
    printMenu()
    rawChoice = raw_input("\n\tChoice: ")
    if len(rawChoice) == 0:
        print("\n\tPlease choose from the menu")
        continue
    else:
        choice = int(rawChoice)

    if choice == 1:
        print "\n\tScanning......"
        deviceMan.discoverDevices()
        deviceMan.tabulateDevice()
        raw_input("\n\tPress Enter to continue...")     
    
    elif choice == 2:
        if deviceMan.numDevices > 0:
            deviceMan.tabulateDevice()
            raw_input("\n\tPress Enter to continue...")
        else:
            print("\n\tPlease choose from the menu")

    elif choice == 3:
        if deviceMan.numDevices > 0:
            digit = chr((int(time.clock()) + 2) % 10 + 48)
            deviceMan.sendCommand("rec2sd", digit) 
        else:
            print("\n\tPlease choose from the menu")

    elif choice == 4:
        if deviceMan.numDevices > 0:
            #deviceMan.cleanTcpBuffer()
            deviceMan.clean32768TcpBuffer()
            currentDateAndTime = time.strftime("%d%m%y_%H%M%S") 

            streamerList = [audioStreamReceiver.RecordingStream(device, currentDateAndTime) for device in deviceMan.deviceList]
            for streamer in streamerList:
                streamer.start()
                streamer.continue_recording = True
            digit = chr((int(time.clock()) + 2) % 10 + 48)
            deviceMan.sendCommand("rec2net", digit)
            raw_input("")
            for streamer in streamerList:
                streamer.continue_recording = False
            print "\tStopping......\n"
            for streamer in streamerList:
                streamer.join()
            deviceMan.sendCommand("stop")
            #deviceMan.clean32768TcpBuffer()
            print "\tStopped"
        else:
            print("\n\tPlease choose from the menu")

    elif choice == 5:
        if deviceMan.numDevices > 0:
            deviceMan.sendCommand("stop")
        else:
            print("\n\tPlease choose from the menu")

    elif choice == 6:
        if deviceMan.numDevices > 0:
            deviceMan.disconnectAll()
            print ("\n\tAll device disconnected")
        else:
            print("\n\tPlease choose from the menu")

    elif choice == 7:
        if deviceMan.numDevices > 0:
            yn = raw_input("\n\tShutdown all devices? (y/n): ")
            if  yn == "y":
                print ("\n\tShutting down now")
                deviceMan.sendCommand("shutdown")
            elif  yn == "n":
                print ("\n\n\tShutdown Cancelled")
            else:
                print ("\n\tError...\n\n\tIncorrect input")
                print ("\n\tTry again")
        else:
            print("\n\tPlease choose from the menu")

    elif choice == 0:
        deviceMan.disconnectAll()
        if deviceMan.numDevices > 0:
            print ("\n\tDisconnect from all device")
        break  

    else:
        print ("\n\tError...\n\tIncorrect input")
        print ("\n\tTry Again")
            
print "\n\n"
print '=' * 50
print '\t\tTerminated'
print '=' * 50
print "\n\n\tThank you for using PC Controller"
print "\tHave a nice day!\n"
winPerfTimer.stop()