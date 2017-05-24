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

print('Running Python File <|--Audio')

def AudioControl(IPCP, TLP, Tesira):
    '''>>Instantiated Buttons------------------------------------------------'''
    ## Audio Set Selection   
    BtnSetA     = Button(TLP, 41)
    BtnSetB     = Button(TLP, 42)
    BtnSetC     = Button(TLP, 43)
    BtnSetD     = Button(TLP, 44)
    BtnSetE     = Button(TLP, 45)
    LblSetA     = Label(TLP, 51)
    LblSetB     = Label(TLP, 52)
    LblSetC     = Label(TLP, 53)
    LblSetD     = Label(TLP, 54)
    LblSetE     = Label(TLP, 55)
    ## Audio Source Selection
    BtnHDMI_A   = Button(TLP, 61)
    BtnPS4_A    = Button(TLP, 62)
    BtnXbox_A   = Button(TLP, 63)
    BtnBluRay_A = Button(TLP, 64)
    BtnSky_A    = Button(TLP, 65)
    BtnRoku_A   = Button(TLP, 66)
    BtnPC_A     = Button(TLP, 67)
    BtnShare_A  = Button(TLP, 68)
    ## Audio Source Selection
    BtnHDMI_B   = Button(TLP, 71)
    BtnPS4_B    = Button(TLP, 72)
    BtnXbox_B   = Button(TLP, 73)
    BtnBluRay_B = Button(TLP, 74)
    BtnSky_B    = Button(TLP, 75)
    BtnRoku_B   = Button(TLP, 76)
    BtnPC_B     = Button(TLP, 77)
    BtnShare_B  = Button(TLP, 78)
    ## Audio Source Selection
    BtnHDMI_C   = Button(TLP, 81)
    BtnPS4_C    = Button(TLP, 82)
    BtnXbox_C   = Button(TLP, 83)
    BtnBluRay_C = Button(TLP, 84)
    BtnSky_C    = Button(TLP, 85)
    BtnRoku_C   = Button(TLP, 86)
    BtnPC_C     = Button(TLP, 87)
    BtnShare_C  = Button(TLP, 88)
    ## Audio Source Selection
    BtnHDMI_D   = Button(TLP, 91)
    BtnPS4_D    = Button(TLP, 92)
    BtnXbox_D   = Button(TLP, 93)
    BtnBluRay_D = Button(TLP, 94)
    BtnSky_D    = Button(TLP, 95)
    BtnRoku_D   = Button(TLP, 96)
    BtnPC_D     = Button(TLP, 97)
    BtnShare_D  = Button(TLP, 98)
    ## Audio Source Selection
    BtnHDMI_E   = Button(TLP, 101)
    BtnPS4_E    = Button(TLP, 102)
    BtnXbox_E   = Button(TLP, 103)
    BtnBluRay_E = Button(TLP, 104)
    BtnSky_E    = Button(TLP, 105)
    BtnRoku_E   = Button(TLP, 106)
    BtnPC_E     = Button(TLP, 107)
    BtnShare_E  = Button(TLP, 108)
    ##-
    BtnLANBiamp = Button(TLP, 201)
    ## Group Buttons Operation------
    PageAudio   = [BtnSetA, BtnSetB, BtnSetC, BtnSetD, BtnSetE]
    PageAudioA  = [BtnHDMI_A, BtnPS4_A, BtnXbox_A, BtnBluRay_A, BtnSky_A, BtnRoku_A, BtnPC_A, BtnShare_A]
    PageAudioB  = [BtnHDMI_B, BtnPS4_B, BtnXbox_B, BtnBluRay_B, BtnSky_B, BtnRoku_B, BtnPC_B, BtnShare_B]
    PageAudioC  = [BtnHDMI_C, BtnPS4_C, BtnXbox_C, BtnBluRay_C, BtnSky_C, BtnRoku_C, BtnPC_C, BtnShare_C]
    PageAudioD  = [BtnHDMI_D, BtnPS4_D, BtnXbox_D, BtnBluRay_D, BtnSky_D, BtnRoku_D, BtnPC_D, BtnShare_D]
    PageAudioE  = [BtnHDMI_E, BtnPS4_E, BtnXbox_E, BtnBluRay_E, BtnSky_E, BtnRoku_E, BtnPC_E, BtnShare_E]
    ## -----------
    GroupAudio  = MESet([BtnSetA, BtnSetB, BtnSetC, BtnSetD, BtnSetE])
    GroupSetA   = MESet(PageAudioA)
    GroupSetB   = MESet(PageAudioB)
    GroupSetC   = MESet(PageAudioC)
    GroupSetD   = MESet(PageAudioD)
    GroupSetE   = MESet(PageAudioE)
    ## -----------
    ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']

    '''>>Data Dictionarie ---------------------------------------------------'''
    Biamp_status = {
        'Router'  : '',
        'Channel' : '',
    }

    '''>>Open Communications ------------------------------------------------'''
    Tesira.Connect()

    #Physical Ethernet Port Status
    def TesiraAutoReconnect():
        Tesira.Connect()       
        Reconnecttime.Restart()
    Reconnecttime = Wait(60,TesiraAutoReconnect) #60s
    
    #Physical Ethernet Port Status
    @event(Tesira, 'Connected')
    @event(Tesira, 'Disconnected')
    def TesiraConnectionHandler(interface, state):
        if state == 'Connected':
            #print('Tesira', state)
            BtnLANBiamp.SetState(1)
            '''>>Device Subscription ----------------------------------------'''
            Tesira.Send(b'SelectorA subscribe sourceSelection RouteA 50\r')
            Tesira.Send(b'SelectorB subscribe sourceSelection RouteB 50\r')
            Tesira.Send(b'SelectorC subscribe sourceSelection RouteC 50\r')
            Tesira.Send(b'SelectorD subscribe sourceSelection RouteD 50\r')
            Tesira.Send(b'SelectorE subscribe sourceSelection RouteE 50\r')
            #--            
            interface.StartKeepAlive(5, (b'DEVICE get hostname\r'))
        elif state == 'Disconnected':
            #print('Tesira', state)
            BtnLANBiamp.SetState(0)
            interface.StopKeepAlive()

    '''>>Data Parsing from Connected Devices --------------------------------'''
    @event(Tesira, 'ReceiveData')
    def TesiraParser(interface, data):
        #>>Find and Clean the data to a valid format '''
        if data.rfind(b'\r\n') > 0:
            Position = data.rfind(b'\r')
            CurrentResponse = data[:Position]
            data = data[Position+2:]
            CurrentResponse = (CurrentResponse.decode()).replace('\"','')

            #>>Evaluate the clean data with RegEx '''
            if CurrentResponse[0] == '!':
                ResponsePattern = re.compile(
                                  '! publishToken:Route([A-E]) value:([0-8])'
                                  )
                MatchObject = ResponsePattern.search(CurrentResponse)
                if MatchObject:
                    Biamp_status['Router']  = MatchObject.group(1)      #[A-E] in Dictionary
                    Biamp_status['Channel'] = int(MatchObject.group(2)) #[0-8] in Dictionary
                    print('Tesira Selector: {0} Channel: {1}'.format(Biamp_status['Router'], Biamp_status['Channel']))
                    '''Biamp GUI Feedback Function'''
                    TesiraStatus(Biamp_status['Router'], Biamp_status['Channel'])
        pass
        
    '''>>Data Parsing to GUI from Connected Devices -------------------------'''
    def TesiraStatus(Selector, Channel):
        if Selector == 'A' and Channel == 0:
            for item in PageAudioA:
                item.SetState(0)
        elif Selector == 'B' and Channel == 0:
            for item in PageAudioB:
                item.SetState(0)
        elif Selector == 'C' and Channel == 0:
            for item in PageAudioC:
                item.SetState(0)
        elif Selector == 'D' and Channel == 0:
            for item in PageAudioD:
                item.SetState(0)
        elif Selector == 'E' and Channel == 0:
            for item in PageAudioE:
                item.SetState(0)
        else:
            Channel = Channel - 1 #Buttons List begin with 0 index
            GroupSetA.SetCurrent(PageAudioA[Channel])
            GroupSetB.SetCurrent(PageAudioB[Channel])
            GroupSetC.SetCurrent(PageAudioC[Channel])
            GroupSetD.SetCurrent(PageAudioD[Channel])
            GroupSetE.SetCurrent(PageAudioE[Channel])
        pass

    '''>>User Button Events -------------------------------------------------'''
    @event(PageAudio, ButtonEventList)
    def GroupAudioHandler(button, state):
        GroupAudio.SetCurrent(button)
        if button is BtnSetA and state == 'Pressed':
            TLP.ShowPopup('Audio_Sources_A')
            print("Audio Source Selector: %s" % 'A')
        elif button is BtnSetB and state == 'Pressed':
            TLP.ShowPopup('Audio_Sources_B')
            print("Audio Source Selector: %s" % 'B')
        elif button is BtnSetC and state == 'Pressed':
            TLP.ShowPopup('Audio_Sources_C')
            print("Audio Source Selector: %s" % 'C')
        elif button is BtnSetD and state == 'Pressed':
            TLP.ShowPopup('Audio_Sources_D')
            print("Audio Source Selector: %s" % 'D')
        elif button is BtnSetE and state == 'Pressed':
            TLP.ShowPopup('Audio_Sources_E')
            print("Audio Source Selector: %s" % 'E')
        pass
    
    @event(PageAudioA, ButtonEventList)
    def AudioSourceAHandler(button, state):
        if button is BtnHDMI_A and state == 'Pressed':
            Tesira.Send(b'SelectorA set sourceSelection 1\r')
            print("Audio listen in Selector %s: %s" % ('A','HDMI'))
        elif button is BtnPS4_A and state == 'Pressed':
            Tesira.Send(b'SelectorA set sourceSelection 2\r')
            print("Audio listen in Selector %s: %s" % ('A','PS4'))
        elif button is BtnXbox_A and state == 'Pressed':
            Tesira.Send(b'SelectorA set sourceSelection 3\r')
            print("Audio listen in Selector %s: %s" % ('A','Xbox'))
        elif button is BtnBluRay_A and state == 'Pressed':
            Tesira.Send(b'SelectorA set sourceSelection 4\r')
            print("Audio listen in Selector %s: %s" % ('A','Bluray'))
        elif button is BtnSky_A and state == 'Pressed':
            Tesira.Send(b'SelectorA set sourceSelection 5\r')
            print("Audio listen in Selector %s: %s" % ('A','Sky'))
        elif button is BtnRoku_A and state == 'Pressed':
            Tesira.Send(b'SelectorA set sourceSelection 6\r')
            print("Audio listen in Selector %s: %s" % ('A','Roku'))
        elif button is BtnPC_A and state == 'Pressed':
            Tesira.Send(b'SelectorA set sourceSelection 7\r')
            print("Audio listen in Selector %s: %s" % ('A','PC'))
        elif button is BtnShare_A and state == 'Pressed':
            Tesira.Send(b'SelectorA set sourceSelection 8\r')
            print("Audio listen in Selector %s: %s" % ('A','ClickShare'))
        GroupSetA.SetCurrent(button)
        pass
        
    @event(PageAudioB, ButtonEventList)
    def AudioSourceBHandler(button, state):
        if button is BtnHDMI_B and state == 'Pressed':
            Tesira.Send(b'SelectorB set sourceSelection 1\r')
            print("Audio listen in Selector %s: %s" % ('B','HDMI'))
        elif button is BtnPS4_B and state == 'Pressed':
            Tesira.Send(b'SelectorB set sourceSelection 2\r')
            print("Audio listen in Selector %s: %s" % ('B','PS4'))
        elif button is BtnXbox_B and state == 'Pressed':
            Tesira.Send(b'SelectorB set sourceSelection 3\r')
            print("Audio listen in Selector %s: %s" % ('B','Xbox'))
        elif button is BtnBluRay_B and state == 'Pressed':
            Tesira.Send(b'SelectorB set sourceSelection 4\r')
            print("Audio listen in Selector %s: %s" % ('B','Bluray'))
        elif button is BtnSky_B and state == 'Pressed':
            Tesira.Send(b'SelectorB set sourceSelection 5\r')
            print("Audio listen in Selector %s: %s" % ('B','Sky'))
        elif button is BtnRoku_B and state == 'Pressed':
            Tesira.Send(b'SelectorB set sourceSelection 6\r')
            print("Audio listen in Selector %s: %s" % ('B','Roku'))
        elif button is BtnPC_B and state == 'Pressed':
            Tesira.Send(b'SelectorB set sourceSelection 7\r')
            print("Audio listen in Selector %s: %s" % ('B','PC'))
        elif button is BtnShare_B and state == 'Pressed':
            Tesira.Send(b'SelectorB set sourceSelection 8\r')
            print("Audio listen in Selector %s: %s" % ('B','ClickShare'))
        GroupSetB.SetCurrent(button)
        pass
    
    @event(PageAudioC, ButtonEventList)
    def AudioSourceCHandler(button, state):
        if button is BtnHDMI_C and state == 'Pressed':
            Tesira.Send(b'SelectorC set sourceSelection 1\r')
            print("Audio listen in Selector %s: %s" % ('C','HDMI'))
        elif button is BtnPS4_C and state == 'Pressed':
            Tesira.Send(b'SelectorC set sourceSelection 2\r')
            print("Audio listen in Selector %s: %s" % ('C','PS4'))
        elif button is BtnXbox_C and state == 'Pressed':
            Tesira.Send(b'SelectorC set sourceSelection 3\r')
            print("Audio listen in Selector %s: %s" % ('C','Xbox'))
        elif button is BtnBluRay_C and state == 'Pressed':
            Tesira.Send(b'SelectorC set sourceSelection 4\r')
            print("Audio listen in Selector %s: %s" % ('C','Bluray'))
        elif button is BtnSky_C and state == 'Pressed':
            Tesira.Send(b'SelectorC set sourceSelection 5\r')
            print("Audio listen in Selector %s: %s" % ('C','Sky'))
        elif button is BtnRoku_C and state == 'Pressed':
            Tesira.Send(b'SelectorC set sourceSelection 6\r')
            print("Audio listen in Selector %s: %s" % ('C','Roku'))
        elif button is BtnPC_C and state == 'Pressed':
            Tesira.Send(b'SelectorC set sourceSelection 7\r')
            print("Audio listen in Selector %s: %s" % ('C','PC'))
        elif button is BtnShare_C and state == 'Pressed':
            Tesira.Send(b'SelectorC set sourceSelection 8\r')
            print("Audio listen in Selector %s: %s" % ('C','ClickShare'))
        GroupSetC.SetCurrent(button)
        pass
        
    @event(PageAudioD, ButtonEventList)
    def AudioSourceDHandler(button, state):
        if button is BtnHDMI_D and state == 'Pressed':
            Tesira.Send(b'SelectorD set sourceSelection 1\r')
            print("Audio listen in Selector %s: %s" % ('D','HDMI'))
        elif button is BtnPS4_D and state == 'Pressed':
            Tesira.Send(b'SelectorD set sourceSelection 2\r')
            print("Audio listen in Selector %s: %s" % ('D','PS4'))
        elif button is BtnXbox_D and state == 'Pressed':
            Tesira.Send(b'SelectorD set sourceSelection 3\r')
            print("Audio listen in Selector %s: %s" % ('D','Xbox'))
        elif button is BtnBluRay_D and state == 'Pressed':
            Tesira.Send(b'SelectorD set sourceSelection 4\r')
            print("Audio listen in Selector %s: %s" % ('D','Bluray'))
        elif button is BtnSky_D and state == 'Pressed':
            Tesira.Send(b'SelectorD set sourceSelection 5\r')
            print("Audio listen in Selector %s: %s" % ('D','Sky')) 
        elif button is BtnRoku_D and state == 'Pressed':
            Tesira.Send(b'SelectorD set sourceSelection 6\r')
            print("Audio listen in Selector %s: %s" % ('D','Roku'))
        elif button is BtnPC_D and state == 'Pressed':
            Tesira.Send(b'SelectorD set sourceSelection 7\r')
            print("Audio listen in Selector %s: %s" % ('D','PC'))
        elif button is BtnShare_D and state == 'Pressed':
            Tesira.Send(b'SelectorD set sourceSelection 8\r')
            print("Audio listen in Selector %s: %s" % ('D','ClickShare'))
        GroupSetD.SetCurrent(button)
        pass
    
    @event(PageAudioE, ButtonEventList)
    def AudioSourceEHandler(button, state):
        if button is BtnHDMI_E and state == 'Pressed':
            Tesira.Send(b'SelectorE set sourceSelection 1\r')
            print("Audio listen in Selector %s: %s" % ('E','HDMI'))
        elif button is BtnPS4_E and state == 'Pressed':
            Tesira.Send(b'SelectorE set sourceSelection 2\r')
            print("Audio listen in Selector %s: %s" % ('E','PS4'))
        elif button is BtnXbox_E and state == 'Pressed':
            Tesira.Send(b'SelectorE set sourceSelection 3\r')
            print("Audio listen in Selector %s: %s" % ('E','Xbox'))
        elif button is BtnBluRay_E and state == 'Pressed':
            Tesira.Send(b'SelectorE set sourceSelection 4\r')
            print("Audio listen in Selector %s: %s" % ('E','Bluray'))
        elif button is BtnSky_E and state == 'Pressed':
            Tesira.Send(b'SelectorE set sourceSelection 5\r')
            print("Audio listen in Selector %s: %s" % ('E','Sky'))
        elif button is BtnRoku_E and state == 'Pressed':
            Tesira.Send(b'SelectorE set sourceSelection 6\r')
            print("Audio listen in Selector %s: %s" % ('E','Roku'))
        elif button is BtnPC_E and state == 'Pressed':
            Tesira.Send(b'SelectorE set sourceSelection 7\r')
            print("Audio listen in Selector %s: %s" % ('E','PC'))
        elif button is BtnShare_E and state == 'Pressed':
            Tesira.Send(b'SelectorE set sourceSelection 8\r')
            print("Audio listen in Selector %s: %s" % ('E','ClickShare'))
        GroupSetE.SetCurrent(button)
        pass
    pass