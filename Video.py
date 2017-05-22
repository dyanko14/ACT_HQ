## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface,
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface,
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait
# External Module Import--------------------------------------------------------
import time #To handle time in LAN/RS232 Connections
import re   #To handle data with Regular Expressions

print('Running Python File <|--Extron Quantum')
print('Running Python File <|--LG Display')

def VideoControl(IPCP, TLP, Quantum):
    '''>>Opening of Communications ------------------------------------------'''
    Quantum.Connect()
    
    '''>>Instantiated Buttons------------------------------------------------'''
    ## Mode of VideoWall
    BtnVWHDMI   = Button(TLP, 11)
    BtnVWPS4    = Button(TLP, 12)
    BtnVWXbox   = Button(TLP, 13)
    BtnVWBluRay = Button(TLP, 14)
    BtnVWSky    = Button(TLP, 15)
    BtnVWRoku   = Button(TLP, 16)
    BtnVWPC     = Button(TLP, 17)
    BtnVWShare  = Button(TLP, 18)
    ## Presets of Videowall
    BtnVWP1     = Button(TLP, 21)
    BtnVWP2     = Button(TLP, 22)
    BtnVWP3     = Button(TLP, 23)
    BtnVWP4     = Button(TLP, 24)
    BtnVWP5     = Button(TLP, 25)
    BtnVWP6     = Button(TLP, 26)
    BtnVWP7     = Button(TLP, 27)
    BtnVWP8     = Button(TLP, 28)
    ## Power of Videowall
    BtnVWPower1 = Button(TLP, 30)
    BtnVWPower0 = Button(TLP, 31)
    ## Group Buttons Operation------
    PageVW      = [BtnVWHDMI, BtnVWPS4, BtnVWXbox, BtnVWBluRay, BtnVWSky, BtnVWRoku, BtnVWPC, BtnVWShare]
    PageVWP     = [BtnVWP1, BtnVWP2, BtnVWP3, BtnVWP4, BtnVWP5, BtnVWP6, BtnVWP7, BtnVWP8]
    PageVWPower = [BtnVWPower1, BtnVWPower0]
    ## Group Buttons Status
    ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
    
    '''>>Data Parsing from Connected Devices --------------------------------'''
    
    '''>>Data Parsing to GUI from Connected Devices -------------------------'''
    
    '''>>Dictionaries of Data -----------------------------------------------'''
    Quantum_Command = {
        'Preset1'  : '1*01*01\r',
        'Preset2'  : '1*01*02\r',
        'Preset3'  : '1*01*03\r',
        'Preset4'  : '1*01*04\r',
        'Preset5'  : '1*01*05\r',
        'Preset6'  : '1*01*06\r',
        'Preset7'  : '1*01*07\r',
        'Preset8'  : '1*01*08\r',
        'Preset9'  : '1*01*09\r',
        'Preset10' : '1*01*10\r',
        'Preset11' : '1*01*11\r',
        'Preset12' : '1*01*12\r',
        'Preset13' : '1*01*13\r',
        'Preset14' : '1*01*14\r',
        'Preset15' : '1*01*15\r',
    }

    '''>>User Button Events -------------------------------------------------'''
    @event(PageVW, ButtonEventList)
    def VideoSourceHandler(button, state):
        #--
        if button is BtnVWHDMI and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset1'])
            print("Video Full in Videowall: %s" % 'HDMI')
        #--
        elif button is BtnVWPS4 and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset2'])
            print("Video Full in Videowall: %s" % 'PS4')
        #--
        elif button is BtnVWXbox and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset3'])
            print("Video Full in Videowall: %s" % 'Xbox')
        #--
        elif button is BtnVWBluRay and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset4'])
            print("Video Full in Videowall: %s" % 'Bluray')
        #--
        elif button is BtnVWSky and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset5'])
            print("Video Full in Videowall: %s" % 'Sky')
        #--
        elif button is BtnVWRoku and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset6'])
            print("Video Full in Videowall: %s" % 'Roku')
        #--
        elif button is BtnVWPC and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset7'])
            print("Video Full in Videowall: %s" % 'PC')
        #--
        elif button is BtnVWShare and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset8'])
            print("Video Full in Videowall: %s" % 'ClickShare')
        #--
        pass

    @event(PageVWP, ButtonEventList)
    def VideoPresetHandler(button, state):
        #--
        if button is BtnVWP1 and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset9'])
            print("Video Preset in Videowall: %s" % '1')
        #--
        elif button is BtnVWP2 and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset10'])
            print("Video Preset in Videowall: %s" % '2')
        #--
        elif button is BtnVWP3 and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset11'])
            print("Video Preset in Videowall: %s" % '3')
        #--
        elif button is BtnVWP4 and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset12'])
            print("Video Preset in Videowall: %s" % '4')
        #--
        elif button is BtnVWP5 and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset13'])
            print("Video Preset in Videowall: %s" % '5')
        #--
        elif button is BtnVWP6 and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset14'])
            print("Video Preset in Videowall: %s" % '6')
        #--
        elif button is BtnVWP7 and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset15'])
            print("Video Preset in Videowall: %s" % '7')
        #--
        elif button is BtnVWP8 and state == 'Pressed':
            Quantum.Send(Quantum_Command['Preset16'])
            print("Video Preset in Videowall: %s" % '8')
        #--
        pass

    @event(PageVWPower, ButtonEventList)
    def VideoPowerHandler(button, state):
        #--
        if button is BtnVWPower1 and state == 'Pressed':
            print("Video Display in Videowall: %s" % 'Powered On')
        #--
        elif button is BtnVWPower0 and state == 'Pressed':
            print("Video Display in Videowall: %s" % 'Powered Off')
        #--
        pass

    pass
