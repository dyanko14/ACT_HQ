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

print('Running Python File <|--Bluray')

def BlurayControl(IPCP, TLP, Denon):  
    '''>>Instantiated Buttons------------------------------------------------'''
    ## Mode of BluRay-------------
    BtnBRPrev   = Button(TLP, 131)
    BtnBRBack   = Button(TLP, 132)
    BtnBRPause  = Button(TLP, 133)
    BtnBRPlay   = Button(TLP, 134)
    BtnBRStop   = Button(TLP, 135)
    BtnBRRewi   = Button(TLP, 136)
    BtnBRNext   = Button(TLP, 137)
    ##--
    BtnBRUp     = Button(TLP, 138)
    BtnBRLeft   = Button(TLP, 139)
    BtnBRDown   = Button(TLP, 140)
    BtnBRRight  = Button(TLP, 141)
    BtnBREnter  = Button(TLP, 142)
    ##--
    BtnBRPopup  = Button(TLP, 143)
    BtnBRSetup  = Button(TLP, 144)
    BtnBRInfo   = Button(TLP, 145)
    BtnBRReturn = Button(TLP, 146)
    BtnBRTray   = Button(TLP, 148)
    BtnBRPower  = Button(TLP, 150)
    ##--
    Btn232Denon = Button(TLP, 204)
    ## Group Buttons Operation------
    PageBRNav   = [BtnBRUp, BtnBRLeft, BtnBRDown, BtnBRRight, BtnBREnter]
    PageBROpt   = [BtnBRPopup, BtnBRSetup, BtnBRInfo, BtnBRReturn, BtnBRTray, BtnBRPower]
    PageBRPlay  = [BtnBRPrev, BtnBRBack, BtnBRPause, BtnBRPlay, BtnBRStop, BtnBRRewi, BtnBRNext]
    GroupPlay   = MESet(PageBRPlay)
    ## Group Buttons Status
    ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
    
    '''>>Data Dictionarie ---------------------------------------------------'''
    Denon_Status = {
        'ConnectionStatus' : '',
        'Power'            : '',
        'PlaybackStatus'   : ''
    }

    '''>>Open Communications ------------------------------------------------'''
    Denon.Initialize()

    #Physical Ethernet Port Status
    def DenonAutoReconnect():
        Denon.Connect()       
        DenonReconnecttime.Restart()
    DenonReconnecttime = Wait(60,DenonAutoReconnect) #60s

    #Physical Ethernet Port Status
    @event(Denon, 'Online')
    @event(Denon, 'Offline')
    def DenonConnectionHandler(interface, state):
        if state == 'Online':
            Btn232Denon.SetState(1)          
            interface.StartKeepAlive(5, (b'PW?\r'))
        elif state == 'Offline':
            Btn232Denon.SetState(0)
            interface.StopKeepAlive()

    '''>>Data Parsing from Connected Devices --------------------------------'''
    @event(Denon, 'ReceiveData')
    def DenonDataHandler(interface, data):
        #print(data)
        pass
    
    def DenonRS232Status(command, value, qualifier):
        print(command + value)
        if value == 'Connected':
            Denon_Status['ConnectionStatus'] = 'Connected'
            Btn232Denon.SetState(1)
        if value == 'Disconnected':
            Denon_Status['ConnectionStatus'] = 'Disconnected'
            Btn232Denon.SetState(0)
    
    def DenonPowerStatus(command, value, qualifier):
        print(command + value)
        if value == 'On':
            Denon_Status['Power'] = 'On'
            BtnBRPower.SetState(1)
        if value == 'Off':
            Denon_Status['Power'] = 'Off'
            BtnBRPower.SetState(0)

    def DenonPlaybackStatus(command, value, qualifier):
        print(command + value)
        if value == 'Paused':
            Denon_Status['PlaybackStatus'] = 'Paused'
            GroupPlay.SetCurrent(BtnBRPause)
        elif value == 'Playing':
            Denon_Status['PlaybackStatus'] = 'Playing'
            GroupPlay.SetCurrent(BtnBRPlay)
        elif value == 'Stopped':
            Denon_Status['PlaybackStatus'] = 'Stopped'
            GroupPlay.SetCurrent(BtnBRStop)
        #--
        elif value == 'Fast Forward':
            Denon_Status['PlaybackStatus'] = 'Fast Forward'
            GroupPlay.SetCurrent(BtnBRRewi)
        elif value == 'Slow Forward':
            Denon_Status['PlaybackStatus'] = 'Fast Reverse'
            GroupPlay.SetCurrent(BtnBRBack)
        #--
        elif value == 'DVD Menus':
            Denon_Status['PlaybackStatus'] = 'DVD Menus'
        GroupPlay.SetCurrent(BtnBRPopup)
        
    def DenonChapterStatus(command, value, qualifier):
        print(command + value)
        
    def DenonDiskStatus(command, value, qualifier):
        print(command + value)
        
    Denon.SubscribeStatus('ConnectionStatus', None, DenonRS232Status)
    Denon.SubscribeStatus('Power', None, DenonPowerStatus)
    Denon.SubscribeStatus('PlaybackStatus', None, DenonPlaybackStatus)
    Denon.SubscribeStatus('CurrentChapterTrackNum', None, DenonChapterStatus)
    Denon.SubscribeStatus('DiscTypeStatus', None, DenonDiskStatus)
    
    '''>>User Button Events -------------------------------------------------'''
    @event(PageBRNav, ButtonEventList)
    def BRNavigationHandler(button, state):
        if button is BtnBRUp and state == 'Pressed':
            Denon.Set('MenuNavigation','Up')
            print("BluRay Button Pressed: %s" % 'Up')
        elif button is BtnBRLeft and state == 'Pressed':
            Denon.Set('MenuNavigation','Left')
            print("BluRay Button Pressed: %s" % 'Left')
        elif button is BtnBRDown and state == 'Pressed':
            Denon.Set('MenuNavigation','Down')
            print("BluRay Button Pressed: %s" % 'Down')
        elif button is BtnBRRight and state == 'Pressed':
            Denon.Set('MenuNavigation','Right')
            print("BluRay Button Pressed: %s" % 'Right')
        elif button is BtnBREnter and state == 'Pressed':
            Denon.Set('MenuNavigation','Enter')
            print("BluRay Button Pressed: %s" % 'Enter')
        pass
    
        @event(PageBROpt, ButtonEventList)
        def BROptionHandler(button, state):
            #--
            if button is BtnBRPopup and state == 'Pressed':
                Denon.Set('MenuCall','Top Menu')
                BtnBRPopup.SetState(1)
                print("BluRay Button Pressed: %s" % 'Menu')
            elif button is BtnBRPopup and state == 'Released':
                BtnBRPopup.SetState(0)
                print("BluRay Button Released: %s" % 'Menu')
            #--
            if button is BtnBRSetup and state == 'Pressed':
                Denon.Set('Function','Setup')
                BtnBRSetup.SetState(1)
                print("BluRay Button Pressed: %s" % 'Title')
            elif button is BtnBRSetup and state == 'Released':
                BtnBRSetup.SetState(0)
                print("BluRay Button Released: %s" % 'Title')
            #--
            if button is BtnBRInfo and state == 'Pressed':
                Denon.Set('Function','Display')
                BtnBRInfo.SetState(1)
                print("BluRay Button Pressed: %s" % 'Info')
            elif button is BtnBRInfo and state == 'Released':
                BtnBRInfo.SetState(0)
                print("BluRay Button Released: %s" % 'Info')
            #--
            if button is BtnBRReturn and state == 'Pressed':
                Denon.Set('MenuNavigation','Return')
                BtnBRReturn.SetState(1)
                print("BluRay Button Pressed: %s" % 'Return')
            elif button is BtnBRReturn and state == 'Released':
                BtnBRReturn.SetState(0)
                print("BluRay Button Released: %s" % 'Return')
            #--
            if button is BtnBRTray and state == 'Pressed':
                Denon.Set('Transport','Eject')
                BtnBRTray.SetState(1)
                print("BluRay Button Pressed: %s" % 'Tray')
            elif button is BtnBRTray and state == 'Released':
                BtnBRTray.SetState(0)
                print("BluRay Button Released: %s" % 'Tray')
            #--
            if button is BtnBRPower and state == 'Pressed':
                if Denon_Status['Power'] == 'On':
                    Denon.Set('Power','Off')
                elif Denon_Status['Power'] == 'Off':
                    Denon.Set('Power','On')
                print("BluRay Button Pressed: %s" % 'Power')
            #--
            pass
        
        @event(PageBRPlay, ButtonEventList)
        def BRPlayHandler(button, state):
            #--
            if button is BtnBRPrev and state == 'Pressed':
                Denon.Set('Transport','Previous')
                print("BluRay Button Pressed: %s" % 'Prev')
            #--
            if button is BtnBRBack and state == 'Pressed':
                Denon.Set('Transport','Rew')
                print("BluRay Button Pressed: %s" % 'Back')
            #--
            if button is BtnBRPause and state == 'Pressed':
                Denon.Set('Transport','Pause')
                print("BluRay Button Pressed: %s" % 'Pause')
            #--
            if button is BtnBRPlay and state == 'Pressed':
                Denon.Set('Transport','Play')
                print("BluRay Button Pressed: %s" % 'Play')
            #--
            if button is BtnBRStop and state == 'Pressed':
                Denon.Set('Transport','Stop')
                print("BluRay Button Pressed: %s" % 'Stop')
            #--
            if button is BtnBRRewi and state == 'Pressed':
                Denon.Set('Transport','FFwd')
                print("BluRay Button Pressed: %s" % 'Rewind')
            #--
            if button is BtnBRNext and state == 'Pressed':
                Denon.Set('Transport','Next')
                print("BluRay Button Pressed: %s" % 'Next')
            #--
            pass
    pass