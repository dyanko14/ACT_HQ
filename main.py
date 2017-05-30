## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface,
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface,
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait
import re

print(Version())

## End ControlScript Import ----------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------
IPCP    = ProcessorDevice('IPlink')
## End Device/Processor Definition ---------------------------------------------
##
## Begin User Import -----------------------------------------------------------
TLP     = UIDevice('TouchPanel')
#--
Denon   = SerialInterface(IPCP, 'COM1', Baud=9600)
LCDs    = SerialInterface(IPCP, 'COM2', Baud=9600, Data=8, Parity='None',
                          Stop=1, FlowControl='Off', CharDelay=0, Mode='RS232')
#--
Quantum = EthernetClientInterface('192.168.10.152', 23, 'TCP')
Tesira  = EthernetClientInterface('192.168.10.150', 22, 'SSH',
                                   Credentials=('default', ''))
## End User Import -------------------------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------
'''PANEL - ROOM .............................................................'''
## Index
BtnIndex    = Button(TLP, 1)
## Main
BtnVideo    = Button(TLP, 2)
BtnAudio    = Button(TLP, 3)
BtnBluRay   = Button(TLP, 4)
BtnStatus   = Button(TLP, 5)
BtnPowerOff = Button(TLP, 6)
LblMaster   = Label(TLP, 300)
## Video
BtnVWHDMI   = Button(TLP, 11)
BtnVWPS4    = Button(TLP, 12)
BtnVWXbox   = Button(TLP, 13)
BtnVWBluRay = Button(TLP, 14)
BtnVWSky    = Button(TLP, 15)
BtnVWRoku   = Button(TLP, 16)
BtnVWPC     = Button(TLP, 17)
BtnVWShare  = Button(TLP, 18)
## Video - Presets
BtnVWP1     = Button(TLP, 21)
BtnVWP2     = Button(TLP, 22)
BtnVWP3     = Button(TLP, 23)
BtnVWP4     = Button(TLP, 24)
BtnVWP5     = Button(TLP, 25)
BtnVWP6     = Button(TLP, 26)
BtnVWP7     = Button(TLP, 27)
BtnVWP8     = Button(TLP, 28)
## Video - Power
BtnVWPower1 = Button(TLP, 30)
BtnVWPower0 = Button(TLP, 31)
## Audio - Set
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
## Audio - B
BtnHDMI_A   = Button(TLP, 61)
BtnPS4_A    = Button(TLP, 62)
BtnXbox_A   = Button(TLP, 63)
BtnBluRay_A = Button(TLP, 64)
BtnSky_A    = Button(TLP, 65)
BtnRoku_A   = Button(TLP, 66)
BtnPC_A     = Button(TLP, 67)
BtnShare_A  = Button(TLP, 68)
## Audio - B
BtnHDMI_B   = Button(TLP, 71)
BtnPS4_B    = Button(TLP, 72)
BtnXbox_B   = Button(TLP, 73)
BtnBluRay_B = Button(TLP, 74)
BtnSky_B    = Button(TLP, 75)
BtnRoku_B   = Button(TLP, 76)
BtnPC_B     = Button(TLP, 77)
BtnShare_B  = Button(TLP, 78)
## Audio - C
BtnHDMI_C   = Button(TLP, 81)
BtnPS4_C    = Button(TLP, 82)
BtnXbox_C   = Button(TLP, 83)
BtnBluRay_C = Button(TLP, 84)
BtnSky_C    = Button(TLP, 85)
BtnRoku_C   = Button(TLP, 86)
BtnPC_C     = Button(TLP, 87)
BtnShare_C  = Button(TLP, 88)
## Audio - D
BtnHDMI_D   = Button(TLP, 91)
BtnPS4_D    = Button(TLP, 92)
BtnXbox_D   = Button(TLP, 93)
BtnBluRay_D = Button(TLP, 94)
BtnSky_D    = Button(TLP, 95)
BtnRoku_D   = Button(TLP, 96)
BtnPC_D     = Button(TLP, 97)
BtnShare_D  = Button(TLP, 98)
## Audio - E
BtnHDMI_E   = Button(TLP, 101)
BtnPS4_E    = Button(TLP, 102)
BtnXbox_E   = Button(TLP, 103)
BtnBluRay_E = Button(TLP, 104)
BtnSky_E    = Button(TLP, 105)
BtnRoku_E   = Button(TLP, 106)
BtnPC_E     = Button(TLP, 107)
BtnShare_E  = Button(TLP, 108)
## Bluray - Play
BtnBRPrev   = Button(TLP, 131)
BtnBRBack   = Button(TLP, 132)
BtnBRPause  = Button(TLP, 133)
BtnBRPlay   = Button(TLP, 134)
BtnBRStop   = Button(TLP, 135)
BtnBRRewi   = Button(TLP, 136)
BtnBRNext   = Button(TLP, 137)
## Bluray - Navigation
BtnBRUp     = Button(TLP, 138)
BtnBRLeft   = Button(TLP, 139)
BtnBRDown   = Button(TLP, 140)
BtnBRRight  = Button(TLP, 141)
BtnBREnter  = Button(TLP, 142)
## Bluray - Options
BtnBRPopup  = Button(TLP, 143)
BtnBRSetup  = Button(TLP, 144)
BtnBRInfo   = Button(TLP, 145)
BtnBRReturn = Button(TLP, 146)
BtnBRTray   = Button(TLP, 148)
BtnBRPower  = Button(TLP, 150)
## Status
BtnLANBiamp = Button(TLP, 201)
BtnLANVWall = Button(TLP, 202)
BtnLANIPCP  = Button(TLP, 203)
Btn232Denon = Button(TLP, 204)
## PowerOff
BtnAllOff   = Button(TLP, 220, holdTime = 3)
LblAllOff   = Label(TLP, 221)

#--
PageMain    = [BtnVideo, BtnAudio, BtnBluRay, BtnStatus, BtnPowerOff]
GroupModes  = MESet([BtnIndex, BtnVideo, BtnAudio, BtnBluRay, BtnStatus, BtnPowerOff])
#--
PageVW      = [BtnVWHDMI, BtnVWPS4, BtnVWXbox, BtnVWBluRay, BtnVWSky, BtnVWRoku, BtnVWPC, BtnVWShare]
PageVWP     = [BtnVWP1, BtnVWP2, BtnVWP3, BtnVWP4, BtnVWP5, BtnVWP6, BtnVWP7, BtnVWP8]
PageVWPower = [BtnVWPower1, BtnVWPower0]
#--
PageAudio   = [BtnSetA, BtnSetB, BtnSetC, BtnSetD, BtnSetE]
PageAudioA  = [BtnHDMI_A, BtnPS4_A, BtnXbox_A, BtnBluRay_A, BtnSky_A, BtnRoku_A, BtnPC_A, BtnShare_A]
PageAudioB  = [BtnHDMI_B, BtnPS4_B, BtnXbox_B, BtnBluRay_B, BtnSky_B, BtnRoku_B, BtnPC_B, BtnShare_B]
PageAudioC  = [BtnHDMI_C, BtnPS4_C, BtnXbox_C, BtnBluRay_C, BtnSky_C, BtnRoku_C, BtnPC_C, BtnShare_C]
PageAudioD  = [BtnHDMI_D, BtnPS4_D, BtnXbox_D, BtnBluRay_D, BtnSky_D, BtnRoku_D, BtnPC_D, BtnShare_D]
PageAudioE  = [BtnHDMI_E, BtnPS4_E, BtnXbox_E, BtnBluRay_E, BtnSky_E, BtnRoku_E, BtnPC_E, BtnShare_E]
#--
GroupAudio  = MESet([BtnSetA, BtnSetB, BtnSetC, BtnSetD, BtnSetE])
GroupSetA   = MESet(PageAudioA)
GroupSetB   = MESet(PageAudioB)
GroupSetC   = MESet(PageAudioC)
GroupSetD   = MESet(PageAudioD)
GroupSetE   = MESet(PageAudioE)
#--
PageBRNav   = [BtnBRUp, BtnBRLeft, BtnBRDown, BtnBRRight, BtnBREnter]
PageBROpt   = [BtnBRPopup, BtnBRSetup, BtnBRInfo, BtnBRReturn, BtnBRTray, BtnBRPower]
PageBRPlay  = [BtnBRPrev, BtnBRBack, BtnBRPause, BtnBRPlay, BtnBRStop, BtnBRRewi, BtnBRNext]
GroupPlay   = MESet(PageBRPlay)
#--
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']

## End Device/User Interface Definition ----------------------------------------
##
## Begin Communication Interface Definition ------------------------------------
## End Communication Interface Definition --------------------------------------
def Initialize():
    Tesira.Connect()
    Denon.Initialize()
    #--
    TLP.ShowPage('Index')
    print("System Initialize")
    pass

## Data Dictionaries -----------------------------------------------------------
Biamp_status = {
    'Router'  : '',
    'Channel' : '',
}
Denon_Status = {
    'ConnectionStatus' : '',
    'Power'            : '',
    'PlaybackStatus'   : ''
}
## Data Parsing ----------------------------------------------------------------
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
#--
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

## Event Definitions -----------------------------------------------------------
'''PANEL - ROOM .............................................................'''
## Index Page ------------------------------------------------------------------
@event(BtnIndex, 'Pressed')
def ButtonObjectPressed(button, state):
    TLP.ShowPage('Main')
    print('Touch Mode: %s' % 'Index')
    pass

## Main Page -------------------------------------------------------------------
@event(PageMain, ButtonEventList)
def GroupModeHandler(button, state):
    #--
    GroupModes.SetCurrent(button)
    #--
    if button is BtnVideo and state == 'Pressed':
        LblMaster.SetText('Proyección de Video')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('VWall')
        print('Touch Mode: %s' % 'VideoWall')
    #--
    elif button is BtnAudio and state == 'Pressed':
        LblMaster.SetText('Selección de Audio')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('Audios')
        print('Touch Mode: %s' % 'Audio')
    #--
    elif button is BtnBluRay and state == 'Pressed':
        LblMaster.SetText('Control de BluRay')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('BR')
        print('Touch Mode: %s' % 'BluRay')
    #--
    elif button is BtnStatus and state == 'Pressed':
        LblMaster.SetText('Información de dispositivos')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('Status')
        print('Touch Mode: %s' % 'Status')
    #--
    elif button is BtnPowerOff and state == 'Pressed':
        LblMaster.SetText('Apagado del Sistema')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('x_PowerOff')
        print('Touch Mode: %s' % 'PowerOff')
    #--
    pass

## Video Page ------------------------------------------------------------------
@event(PageVW, ButtonEventList)
def VideoSourceHandler(button, state):
    if button is BtnVWHDMI and state == 'Pressed':
        print("Videowall Full: %s" % 'HDMI')
    elif button is BtnVWPS4 and state == 'Pressed':
        print("Videowall Full: %s" % 'PS4')
    elif button is BtnVWXbox and state == 'Pressed':
        print("Videowall Full: %s" % 'Xbox')
    elif button is BtnVWBluRay and state == 'Pressed':
        print("Videowall Full: %s" % 'Bluray')
    elif button is BtnVWSky and state == 'Pressed':
        print("Videowall Full: %s" % 'Sky')
    elif button is BtnVWRoku and state == 'Pressed':
        print("Videowall Full: %s" % 'Roku')
    elif button is BtnVWPC and state == 'Pressed':
        print("Videowall Full: %s" % 'PC')
    elif button is BtnVWShare and state == 'Pressed':
        print("Videowall Full: %s" % 'Share')
    pass
#--
@event(PageVWP, ButtonEventList)
def VideoPresetHandler(button, state):
    if button is BtnVWP1 and state == 'Pressed':
        print("Videowall Preset: %s" % '1')
    elif button is BtnVWP2 and state == 'Pressed':
        print("Videowall Preset: %s" % '2')
    elif button is BtnVWP3 and state == 'Pressed':
        print("Videowall Preset: %s" % '3')
    elif button is BtnVWP4 and state == 'Pressed':
        print("Videowall Preset: %s" % '4')
    elif button is BtnVWP5 and state == 'Pressed':
        print("Videowall Preset: %s" % '5')
    elif button is BtnVWP6 and state == 'Pressed':
        print("Videowall Preset: %s" % '6')
    elif button is BtnVWP7 and state == 'Pressed':
        print("Videowall Preset: %s" % '7')
    elif button is BtnVWP8 and state == 'Pressed':
        print("Videowall Preset: %s" % '8')
    pass
#--
@event(PageVWPower, ButtonEventList)
def VideoPowerHandler(button, state):
    if button is BtnVWPower1 and state == 'Pressed':
        print("Videowall: %s" % 'PwrOn')
    elif button is BtnVWPower0 and state == 'Pressed':
        print("Videowall: %s" % 'PwrOff')
    pass
pass

## Audio Page ------------------------------------------------------------------
@event(PageAudio, ButtonEventList)
def GroupAudioHandler(button, state):
    GroupAudio.SetCurrent(button)
    if button is BtnSetA and state == 'Pressed':
        TLP.ShowPopup('Audio_Sources_A')
        print("Audio Set: %s" % 'A')
    elif button is BtnSetB and state == 'Pressed':
        TLP.ShowPopup('Audio_Sources_B')
        print("Audio Set: %s" % 'B')
    elif button is BtnSetC and state == 'Pressed':
        TLP.ShowPopup('Audio_Sources_C')
        print("Audio Set: %s" % 'C')
    elif button is BtnSetD and state == 'Pressed':
        TLP.ShowPopup('Audio_Sources_D')
        print("Audio Set: %s" % 'D')
    elif button is BtnSetE and state == 'Pressed':
        TLP.ShowPopup('Audio_Sources_E')
        print("Audio Set: %s" % 'E')
    pass
#--
@event(PageAudioA, ButtonEventList)
def AudioSourceAHandler(button, state):
    if button is BtnHDMI_A and state == 'Pressed':
        Tesira.Send(b'SelectorA set sourceSelection 1\r')
        print("Audio on Set %s: %s" % ('A','HDMI'))
    elif button is BtnPS4_A and state == 'Pressed':
        Tesira.Send(b'SelectorA set sourceSelection 2\r')
        print("Audio on Set %s: %s" % ('A','PS4'))
    elif button is BtnXbox_A and state == 'Pressed':
        Tesira.Send(b'SelectorA set sourceSelection 3\r')
        print("Audio on Set %s: %s" % ('A','Xbox'))
    elif button is BtnBluRay_A and state == 'Pressed':
        Tesira.Send(b'SelectorA set sourceSelection 4\r')
        print("Audio on Set %s: %s" % ('A','Bluray'))
    elif button is BtnSky_A and state == 'Pressed':
        Tesira.Send(b'SelectorA set sourceSelection 5\r')
        print("Audio on Set %s: %s" % ('A','Sky'))
    elif button is BtnRoku_A and state == 'Pressed':
        Tesira.Send(b'SelectorA set sourceSelection 6\r')
        print("Audio on Set %s: %s" % ('A','Roku'))
    elif button is BtnPC_A and state == 'Pressed':
        Tesira.Send(b'SelectorA set sourceSelection 7\r')
        print("Audio on Set %s: %s" % ('A','PC'))
    elif button is BtnShare_A and state == 'Pressed':
        Tesira.Send(b'SelectorA set sourceSelection 8\r')
        print("Audio on Set %s: %s" % ('A','Share'))
    GroupSetA.SetCurrent(button)
    pass
#--
@event(PageAudioB, ButtonEventList)
def AudioSourceBHandler(button, state):
    if button is BtnHDMI_B and state == 'Pressed':
        Tesira.Send(b'SelectorB set sourceSelection 1\r')
        print("Audio on Set %s: %s" % ('B','HDMI'))
    elif button is BtnPS4_B and state == 'Pressed':
        Tesira.Send(b'SelectorB set sourceSelection 2\r')
        print("Audio on Set %s: %s" % ('B','PS4'))
    elif button is BtnXbox_B and state == 'Pressed':
        Tesira.Send(b'SelectorB set sourceSelection 3\r')
        print("Audio on Set %s: %s" % ('B','Xbox'))
    elif button is BtnBluRay_B and state == 'Pressed':
        Tesira.Send(b'SelectorB set sourceSelection 4\r')
        print("Audio on Set %s: %s" % ('B','Bluray'))
    elif button is BtnSky_B and state == 'Pressed':
        Tesira.Send(b'SelectorB set sourceSelection 5\r')
        print("Audio on Set %s: %s" % ('B','Sky'))
    elif button is BtnRoku_B and state == 'Pressed':
        Tesira.Send(b'SelectorB set sourceSelection 6\r')
        print("Audio on Set %s: %s" % ('B','Roku'))
    elif button is BtnPC_B and state == 'Pressed':
        Tesira.Send(b'SelectorB set sourceSelection 7\r')
        print("Audio on Set %s: %s" % ('B','PC'))
    elif button is BtnShare_B and state == 'Pressed':
        Tesira.Send(b'SelectorB set sourceSelection 8\r')
        print("Audio on Set %s: %s" % ('B','Share'))
    GroupSetB.SetCurrent(button)
    pass
#--
@event(PageAudioC, ButtonEventList)
def AudioSourceCHandler(button, state):
    if button is BtnHDMI_C and state == 'Pressed':
        Tesira.Send(b'SelectorC set sourceSelection 1\r')
        print("Audio on Set %s: %s" % ('C','HDMI'))
    elif button is BtnPS4_C and state == 'Pressed':
        Tesira.Send(b'SelectorC set sourceSelection 2\r')
        print("Audio on Set %s: %s" % ('C','PS4'))
    elif button is BtnXbox_C and state == 'Pressed':
        Tesira.Send(b'SelectorC set sourceSelection 3\r')
        print("Audio on Set %s: %s" % ('C','Xbox'))
    elif button is BtnBluRay_C and state == 'Pressed':
        Tesira.Send(b'SelectorC set sourceSelection 4\r')
        print("Audio on Set %s: %s" % ('C','Bluray'))
    elif button is BtnSky_C and state == 'Pressed':
        Tesira.Send(b'SelectorC set sourceSelection 5\r')
        print("Audio on Set %s: %s" % ('C','Sky'))
    elif button is BtnRoku_C and state == 'Pressed':
        Tesira.Send(b'SelectorC set sourceSelection 6\r')
        print("Audio on Set %s: %s" % ('C','Roku'))
    elif button is BtnPC_C and state == 'Pressed':
        Tesira.Send(b'SelectorC set sourceSelection 7\r')
        print("Audio on Set %s: %s" % ('C','PC'))
    elif button is BtnShare_C and state == 'Pressed':
        Tesira.Send(b'SelectorC set sourceSelection 8\r')
        print("Audio on Set %s: %s" % ('C','Share'))
    GroupSetC.SetCurrent(button)
    pass
#--
@event(PageAudioD, ButtonEventList)
def AudioSourceDHandler(button, state):
    if button is BtnHDMI_D and state == 'Pressed':
        Tesira.Send(b'SelectorD set sourceSelection 1\r')
        print("Audio on Set %s: %s" % ('D','HDMI'))
    elif button is BtnPS4_D and state == 'Pressed':
        Tesira.Send(b'SelectorD set sourceSelection 2\r')
        print("Audio on Set %s: %s" % ('D','PS4'))
    elif button is BtnXbox_D and state == 'Pressed':
        Tesira.Send(b'SelectorD set sourceSelection 3\r')
        print("Audio on Set %s: %s" % ('D','Xbox'))
    elif button is BtnBluRay_D and state == 'Pressed':
        Tesira.Send(b'SelectorD set sourceSelection 4\r')
        print("Audio on Set %s: %s" % ('D','Bluray'))
    elif button is BtnSky_D and state == 'Pressed':
        Tesira.Send(b'SelectorD set sourceSelection 5\r')
        print("Audio on Set %s: %s" % ('D','Sky')) 
    elif button is BtnRoku_D and state == 'Pressed':
        Tesira.Send(b'SelectorD set sourceSelection 6\r')
        print("Audio on Set %s: %s" % ('D','Roku'))
    elif button is BtnPC_D and state == 'Pressed':
        Tesira.Send(b'SelectorD set sourceSelection 7\r')
        print("Audio on Set %s: %s" % ('D','PC'))
    elif button is BtnShare_D and state == 'Pressed':
        Tesira.Send(b'SelectorD set sourceSelection 8\r')
        print("Audio on Set %s: %s" % ('D','Share'))
    GroupSetD.SetCurrent(button)
    pass
#--
@event(PageAudioE, ButtonEventList)
def AudioSourceEHandler(button, state):
    if button is BtnHDMI_E and state == 'Pressed':
        Tesira.Send(b'SelectorE set sourceSelection 1\r')
        print("Audio on Set %s: %s" % ('E','HDMI'))
    elif button is BtnPS4_E and state == 'Pressed':
        Tesira.Send(b'SelectorE set sourceSelection 2\r')
        print("Audio on Set %s: %s" % ('E','PS4'))
    elif button is BtnXbox_E and state == 'Pressed':
        Tesira.Send(b'SelectorE set sourceSelection 3\r')
        print("Audio on Set %s: %s" % ('E','Xbox'))
    elif button is BtnBluRay_E and state == 'Pressed':
        Tesira.Send(b'SelectorE set sourceSelection 4\r')
        print("Audio on Set %s: %s" % ('E','Bluray'))
    elif button is BtnSky_E and state == 'Pressed':
        Tesira.Send(b'SelectorE set sourceSelection 5\r')
        print("Audio on Set %s: %s" % ('E','Sky'))
    elif button is BtnRoku_E and state == 'Pressed':
        Tesira.Send(b'SelectorE set sourceSelection 6\r')
        print("Audio on Set %s: %s" % ('E','Roku'))
    elif button is BtnPC_E and state == 'Pressed':
        Tesira.Send(b'SelectorE set sourceSelection 7\r')
        print("Audio on Set %s: %s" % ('E','PC'))
    elif button is BtnShare_E and state == 'Pressed':
        Tesira.Send(b'SelectorE set sourceSelection 8\r')
        print("Audio on Set %s: %s" % ('E','Share'))
    GroupSetE.SetCurrent(button)
    pass
## Bluray Page -----------------------------------------------------------------
@event(PageBRNav, ButtonEventList)
def BRNavigationHandler(button, state):
    if button is BtnBRUp and state == 'Pressed':
        #Denon.Set('MenuNavigation','Up')
        print("BluRay Pressed: %s" % 'Up')
    elif button is BtnBRLeft and state == 'Pressed':
        #Denon.Set('MenuNavigation','Left')
        print("BluRay Pressed: %s" % 'Left')
    elif button is BtnBRDown and state == 'Pressed':
        #Denon.Set('MenuNavigation','Down')
        print("BluRay Pressed: %s" % 'Down')
    elif button is BtnBRRight and state == 'Pressed':
        #Denon.Set('MenuNavigation','Right')
        print("BluRay Pressed: %s" % 'Right')
    elif button is BtnBREnter and state == 'Pressed':
        #Denon.Set('MenuNavigation','Enter')
        print("BluRay Pressed: %s" % 'Enter')
    pass
#--
@event(PageBROpt, ButtonEventList)
def BROptionHandler(button, state):
    #--
    if button is BtnBRPopup and state == 'Pressed':
        #Denon.Set('MenuCall','Top Menu')
        BtnBRPopup.SetState(1)
        print("BluRay Pressed: %s" % 'Menu')
    elif button is BtnBRPopup and state == 'Released':
        BtnBRPopup.SetState(0)
        print("BluRay Released: %s" % 'Menu')
    #--
    if button is BtnBRSetup and state == 'Pressed':
        #Denon.Set('Function','Setup')
        BtnBRSetup.SetState(1)
        print("BluRay Pressed: %s" % 'Title')
    elif button is BtnBRSetup and state == 'Released':
        BtnBRSetup.SetState(0)
        print("BluRay Released: %s" % 'Title')
    #--
    if button is BtnBRInfo and state == 'Pressed':
        #Denon.Set('Function','Display')
        BtnBRInfo.SetState(1)
        print("BluRay Pressed: %s" % 'Info')
    elif button is BtnBRInfo and state == 'Released':
        BtnBRInfo.SetState(0)
        print("BluRay Released: %s" % 'Info')
    #--
    if button is BtnBRReturn and state == 'Pressed':
        #Denon.Set('MenuNavigation','Return')
        BtnBRReturn.SetState(1)
        print("BluRay Pressed: %s" % 'Return')
    elif button is BtnBRReturn and state == 'Released':
        BtnBRReturn.SetState(0)
        print("BluRay Released: %s" % 'Return')
    #--
    if button is BtnBRTray and state == 'Pressed':
        #Denon.Set('Transport','Eject')
        BtnBRTray.SetState(1)
        print("BluRay Pressed: %s" % 'Tray')
    elif button is BtnBRTray and state == 'Released':
        BtnBRTray.SetState(0)
        print("BluRay Released: %s" % 'Tray')
    #--
    if button is BtnBRPower and state == 'Pressed':
        print("BluRay Pressed: %s" % 'Power')
    #--
    pass
#--
@event(PageBRPlay, ButtonEventList)
def BRPlayHandler(button, state):
    #--
    if button is BtnBRPrev and state == 'Pressed':
        #Denon.Set('Transport','Previous')
        print("BluRay Pressed: %s" % 'Prev')
    #--
    if button is BtnBRBack and state == 'Pressed':
        #Denon.Set('Transport','Rew')
        print("BluRay Pressed: %s" % 'Back')
    #--
    if button is BtnBRPause and state == 'Pressed':
        #Denon.Set('Transport','Pause')
        print("BluRay Pressed: %s" % 'Pause')
    #--
    if button is BtnBRPlay and state == 'Pressed':
        #Denon.Set('Transport','Play')
        print("BluRay Pressed: %s" % 'Play')
    #--
    if button is BtnBRStop and state == 'Pressed':
        #Denon.Set('Transport','Stop')
        print("BluRay Pressed: %s" % 'Stop')
    #--
    if button is BtnBRRewi and state == 'Pressed':
        #Denon.Set('Transport','FFwd')
        print("BluRay Pressed: %s" % 'Rewind')
    #--
    if button is BtnBRNext and state == 'Pressed':
        #Denon.Set('Transport','Next')
        print("BluRay Pressed: %s" % 'Next')
    #--
    pass
## Status Page -----------------------------------------------------------------
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
## Power Page ------------------------------------------------------------------
@event(BtnAllOff, ButtonEventList)
def PowerSystemHandler(button, state):
    if state == 'Pressed':
        print("Button PowerOff Pressed")
    if state == 'Held':       
        #Denon.Set('Power','Off')
        TLP.ShowPage('Index')
        print("Power System Held")
    pass

## End Events Definitions-------------------------------------------------------
Initialize()