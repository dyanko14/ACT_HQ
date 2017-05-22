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
    ## Group Buttons Status
    ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
    
    '''>>Dictionaries of Data -----------------------------------------------'''
    Denon_Command = {
        # Power
        'PowerOn'  : (b'KYPW ON\r'),
        'PowerOff' : (b'KYPW OF\r'),
        # Navigation
        'NavUp'    : (b'KYCR UP\r'),
        'NavDown'  : (b'KYCR DW\r'),
        'NavLeft'  : (b'KYCR LT\r'),
        'NavRight' : (b'KYCR RT\r'),
        'NavEnter' : (b'KYENTER\r'),
        # Reproduction
        'RepPlay'  : (b'KYPLAY\r'),
        'RepPause' : (b'KYPAUS\r'),
        'RepStop'  : (b'KYSTOP\r'),
        'RepFwd'   : (b'KYSK FW\r'),
        'RepRev'   : (b'KYSK RV\r'),
        'RepSfwd'  : (b'KYSE FW\r'),
        'RepSrev'  : (b'KYSE RV\r'),
        # Options
        'OptPopup' : (b'KYPMENU\r'),
        'OptSetup' : (b'KYSETUP\r'),
        'OptInfo'  : (b'KYDISP\r'),
        'OptReturn': (b'KYRETURN\r'),
        'Eject'    : (b'KYTY EJ\r'),
        # Colors
        'Red'      : (b'KYC RED\r'),
        'Green'    : (b'KYC GRN\r'),
        'Blue'     : (b'KYC BLU\r'),
        'Yellow'   : (b'KYC YEL\r'),
        # Query Status
        '?Power'   : (b'PW?\r'),
        '?Play'    : (b'PS?\r')
    }

    '''>>Opening of Communications ------------------------------------------'''
    Denon.Initialize()


    '''>>Data Parsing from Connected Devices --------------------------------'''


    '''>>User Button Events -------------------------------------------------'''
    @event(PageBRNav, ButtonEventList)
    def BRNavigationHandler(button, state):
        #--
        if button is BtnBRUp and state == 'Pressed':
            Denon.Send(Denon_Command['NavUp'])
            print("BluRay Navigation {0} Button Pressed".format('Up'))
        #--
        elif button is BtnBRLeft and state == 'Pressed':
            Denon.Send(Denon_Command['NavLeft'])
            print("BluRay Navigation {0} Button Pressed".format('Left'))
        #--
        elif button is BtnBRDown and state == 'Pressed':
            Denon.Send(Denon_Command['NavDown'])
            print("BluRay Navigation {0} Button Pressed".format('Down'))
        #--
        elif button is BtnBRRight and state == 'Pressed':
            Denon.Send(Denon_Command['NavRight'])
            print("BluRay Navigation {0} Button Pressed".format('Right'))
        #--
        elif button is BtnBREnter and state == 'Pressed':
            Denon.Send(Denon_Command['NavEnter'])
            print("BluRay Navigation {0} Button Pressed".format('Enter'))
        #--
        pass
    
        @event(PageBROpt, ButtonEventList)
        def BROptionHandler(button, state):
            #--
            if button is BtnBRPopup and state == 'Pressed':
                Denon.Send(Denon_Command['OptPopup'])
                BtnBRPopup.SetState(1)
                print("BluRay Option {0} Button Pressed".format('Menu'))
            elif button is BtnBRPopup and state == 'Released':
                BtnBRPopup.SetState(0)
                print("BluRay Option {0} Button Released".format('Menu'))
            #--
            if button is BtnBRSetup and state == 'Pressed':
                Denon.Send(Denon_Command['OptSetup'])
                BtnBRSetup.SetState(1)
                print("BluRay Option {0} Button Pressed".format('Title'))
            elif button is BtnBRSetup and state == 'Released':
                BtnBRSetup.SetState(0)
                print("BluRay Option {0} Button Released".format('Title'))
            #--
            if button is BtnBRInfo and state == 'Pressed':
                Denon.Send(Denon_Command['OptInfo'])
                BtnBRInfo.SetState(1)
                print("BluRay Option {0} Button Pressed".format('Info'))
            elif button is BtnBRInfo and state == 'Released':
                BtnBRInfo.SetState(0)
                print("BluRay Option {0} Button Released".format('Info'))
            #--
            if button is BtnBRReturn and state == 'Pressed':
                Denon.Send(Denon_Command['OptReturn'])
                BtnBRReturn.SetState(1)
                print("BluRay Option {0} Button Pressed".format('Return'))
            elif button is BtnBRReturn and state == 'Released':
                BtnBRReturn.SetState(0)
                print("BluRay Option {0} Button Released".format('Return'))
            #--
            if button is BtnBRTray and state == 'Pressed':
                Denon.Send(Denon_Command['Eject'])
                BtnBRTray.SetState(1)
                print("BluRay Option {0} Button Pressed".format('Tray'))
            elif button is BtnBRTray and state == 'Released':
                BtnBRTray.SetState(0)
                print("BluRay Option {0} Button Released".format('Tray'))
            #--
            if button is BtnBRPower and state == 'Pressed':                
                print("BluRay Option {0} Button Pressed".format('Power'))
            #--
            pass
        
        @event(PageBRPlay, ButtonEventList)
        def BRPlayHandler(button, state):
            #--
            if button is BtnBRPrev and state == 'Pressed':
                Denon.Send(Denon_Command['RepRev'])
                BtnBRPrev.SetState(1)
                print("BluRay {0} Button Pressed".format('Prev'))
            elif button is BtnBRPrev and state == 'Released':
                BtnBRPrev.SetState(0)
                print("BluRay {0} Button Released".format('Prev'))
            #--
            if button is BtnBRBack and state == 'Pressed':
                BtnBRBack.SetState(1)
                Denon.Send(Denon_Command['RepSrev'])
                print("BluRay {0} Button Pressed".format('Back'))
            elif button is BtnBRBack and state == 'Released':
                BtnBRBack.SetState(0)
                print("BluRay {0} Button Released".format('Back'))
            #--
            if button is BtnBRPause and state == 'Pressed':
                Denon.Send(Denon_Command['RepPause'])
                print("BluRay {0} Button Pressed".format('Pause'))
            
            if button is BtnBRPlay and state == 'Pressed':
                Denon.Send(Denon_Command['RepPlay'])
                print("BluRay {0} Button Pressed".format('Play'))
            #--
            if button is BtnBRStop and state == 'Pressed':
                Denon.Send(Denon_Command['RepStop'])
                print("BluRay {0} Button Pressed".format('Stop'))
            #--
            if button is BtnBRRewi and state == 'Pressed':
                BtnBRRewi.SetState(1)
                Denon.Send(Denon_Command['RepSfwd'])
                print("BluRay {0} Button Pressed".format('Rewind'))
            elif button is BtnBRRewi and state == 'Released':
                BtnBRRewi.SetState(0)
                print("BluRay {0} Button Released".format('Rewind'))
            #--
            if button is BtnBRNext and state == 'Pressed':
                BtnBRNext.SetState(1)
                Denon.Send(Denon_Command['RepFwd'])
                print("BluRay {0} Button Pressed".format('Next'))
            elif button is BtnBRNext and state == 'Released':
                BtnBRNext.SetState(0)
                print("BluRay {0} Button Released".format('Next'))
            #--
            pass
    pass