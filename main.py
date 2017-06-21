## -------------------------------------------------------------------------- ##
## Business   | Asesores y Consultores en Tecnología S.A. de C.V. ----------- ##
## Programmer | Dyanko Cisneros Mendoza
## Customer   | Human Quality
## Project    | VideoWall Room
## Version    | 0.1 --------------------------------------------------------- ##

## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface,
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface,
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait

print(Version())

## End ControlScript Import ----------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------
IPCP = ProcessorDevice('IPlink')
## End Device/Processor Definition ---------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------
TLP = UIDevice('TouchPanel')
## End Device/User Interface Definition ----------------------------------------
##
## Begin User Import -----------------------------------------------------------
## Instances of Python Extron modules------------------
## IP-controlled Modules declared:
import biam_dsp_TesiraSeries_v1_5_19_0    as DeviceA
import extr_sp_Quantum_Ultra610_v1_0_1_0  as DeviceB
## Serial-controlled Modules declared:
import deno_dvd_DBT3313UD_Series_v1_0_2_0 as DeviceC
## IR/Serial-controlled Modules declared:
## IP-controlled Devices declared:
Biamp   = DeviceA.EthernetClass('192.168.10.150', 23, Model='TesiraFORTE CI')
Quantum = DeviceB.EthernetClass('10.10.10.12', 23, Model='Quantum Ultra 610')
## Serial-controlled Devices declared:
Denon   = DeviceC.SerialClass(IPCP, 'COM1', Baud=9600, Model='DBT-3313UD')
##
## End User Import -------------------------------------------------------------
## Begin Communication Interface Definition ------------------------------------
## Instantiating ID GUI Buttons to variable names
## Page Index
BtnIndex    = Button(TLP, 1)
## Page Main
BtnVideo    = Button(TLP, 2)
BtnAudio    = Button(TLP, 3)
BtnBluRay   = Button(TLP, 4)
BtnStatus   = Button(TLP, 5)
BtnPowerOff = Button(TLP, 6)
LblMaster   = Label(TLP, 300)
## Page Video - Sources
BtnVHDMI   = Button(TLP, 11)
BtnVPS4    = Button(TLP, 12)
BtnVXbox   = Button(TLP, 13)
BtnVBluRay = Button(TLP, 14)
BtnVSky    = Button(TLP, 15)
BtnVRoku   = Button(TLP, 16)
BtnVPC     = Button(TLP, 17)
BtnVShare  = Button(TLP, 18)
## Page Video - Presets
BtnVP1     = Button(TLP, 21)
BtnVP2     = Button(TLP, 22)
BtnVP3     = Button(TLP, 23)
BtnVP4     = Button(TLP, 24)
BtnVP5     = Button(TLP, 25)
BtnVP6     = Button(TLP, 26)
BtnVP7     = Button(TLP, 27)
BtnVP8     = Button(TLP, 28)
## Page Video - Power
BtnVWPwr1 = Button(TLP, 30)
BtnVWPwr0 = Button(TLP, 31)
## Page Audio - Set
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
## Page Audio - A
BtnHDMI_A   = Button(TLP, 61)
BtnPS4_A    = Button(TLP, 62)
BtnXbox_A   = Button(TLP, 63)
BtnBluRay_A = Button(TLP, 64)
BtnSky_A    = Button(TLP, 65)
BtnRoku_A   = Button(TLP, 66)
BtnPC_A     = Button(TLP, 67)
BtnShare_A  = Button(TLP, 68)
## Page Audio - B
BtnHDMI_B   = Button(TLP, 71)
BtnPS4_B    = Button(TLP, 72)
BtnXbox_B   = Button(TLP, 73)
BtnBluRay_B = Button(TLP, 74)
BtnSky_B    = Button(TLP, 75)
BtnRoku_B   = Button(TLP, 76)
BtnPC_B     = Button(TLP, 77)
BtnShare_B  = Button(TLP, 78)
## Page Audio - C
BtnHDMI_C   = Button(TLP, 81)
BtnPS4_C    = Button(TLP, 82)
BtnXbox_C   = Button(TLP, 83)
BtnBluRay_C = Button(TLP, 84)
BtnSky_C    = Button(TLP, 85)
BtnRoku_C   = Button(TLP, 86)
BtnPC_C     = Button(TLP, 87)
BtnShare_C  = Button(TLP, 88)
## Page Audio - D
BtnHDMI_D   = Button(TLP, 91)
BtnPS4_D    = Button(TLP, 92)
BtnXbox_D   = Button(TLP, 93)
BtnBluRay_D = Button(TLP, 94)
BtnSky_D    = Button(TLP, 95)
BtnRoku_D   = Button(TLP, 96)
BtnPC_D     = Button(TLP, 97)
BtnShare_D  = Button(TLP, 98)
## Page Audio - E
BtnHDMI_E   = Button(TLP, 101)
BtnPS4_E    = Button(TLP, 102)
BtnXbox_E   = Button(TLP, 103)
BtnBluRay_E = Button(TLP, 104)
BtnSky_E    = Button(TLP, 105)
BtnRoku_E   = Button(TLP, 106)
BtnPC_E     = Button(TLP, 107)
BtnShare_E  = Button(TLP, 108)
## Page Bluray - Play
BtnBRPrev   = Button(TLP, 131)
BtnBRBack   = Button(TLP, 132)
BtnBRPause  = Button(TLP, 133)
BtnBRPlay   = Button(TLP, 134)
BtnBRStop   = Button(TLP, 135)
BtnBRRewi   = Button(TLP, 136)
BtnBRNext   = Button(TLP, 137)
## Page Bluray - Navigation
BtnBRUp     = Button(TLP, 138)
BtnBRLeft   = Button(TLP, 139)
BtnBRDown   = Button(TLP, 140)
BtnBRRight  = Button(TLP, 141)
BtnBREnter  = Button(TLP, 142)
## Page Bluray - Options
BtnBRPopup  = Button(TLP, 143)
BtnBRSetup  = Button(TLP, 144)
BtnBRInfo   = Button(TLP, 145)
BtnBRReturn = Button(TLP, 146)
BtnBRTray   = Button(TLP, 148)
BtnBRPower  = Button(TLP, 150)
LblBRDisk   = Label(TLP, 151)

## Page Status
BtnLANBiamp = Button(TLP, 201)
BtnLANVWall = Button(TLP, 202)
BtnLANIPCP  = Button(TLP, 203)
Btn232Denon = Button(TLP, 204)
## Page PowerOff
BtnPowerAll = Button(TLP, 220, repeatTime = 1)
LblAllOff   = Label(TLP, 221)
LblCountAll = Label(TLP, 222)
## Button Grouping -------------------------------------------------------------
## Group Page Main
PageMain   = [BtnVideo, BtnAudio, BtnBluRay, BtnStatus, BtnPowerOff]
GroupMode  = MESet([BtnIndex, BtnVideo, BtnAudio, BtnBluRay, BtnStatus, BtnPowerOff])
## Group Page Video
PageVW     = [BtnVHDMI, BtnVPS4, BtnVXbox, BtnVBluRay, BtnVSky, BtnVRoku, BtnVPC, BtnVShare]
PageVWP    = [BtnVP1, BtnVP2, BtnVP3, BtnVP4, BtnVP5, BtnVP6, BtnVP7, BtnVP8]
PageVWPwr  = [BtnVWPwr1, BtnVWPwr0]
## Group Page Audio
PageAudio  = [BtnSetA, BtnSetB, BtnSetC, BtnSetD, BtnSetE]
PageAudioA = [BtnHDMI_A, BtnPS4_A, BtnXbox_A, BtnBluRay_A, BtnSky_A, BtnRoku_A, BtnPC_A, BtnShare_A]
PageAudioB = [BtnHDMI_B, BtnPS4_B, BtnXbox_B, BtnBluRay_B, BtnSky_B, BtnRoku_B, BtnPC_B, BtnShare_B]
PageAudioC = [BtnHDMI_C, BtnPS4_C, BtnXbox_C, BtnBluRay_C, BtnSky_C, BtnRoku_C, BtnPC_C, BtnShare_C]
PageAudioD = [BtnHDMI_D, BtnPS4_D, BtnXbox_D, BtnBluRay_D, BtnSky_D, BtnRoku_D, BtnPC_D, BtnShare_D]
PageAudioE = [BtnHDMI_E, BtnPS4_E, BtnXbox_E, BtnBluRay_E, BtnSky_E, BtnRoku_E, BtnPC_E, BtnShare_E]
GroupAudio = MESet([BtnSetA, BtnSetB, BtnSetC, BtnSetD, BtnSetE])
GroupSetA  = MESet(PageAudioA)
GroupSetB  = MESet(PageAudioB)
GroupSetC  = MESet(PageAudioC)
GroupSetD  = MESet(PageAudioD)
GroupSetE  = MESet(PageAudioE)
## Group Page BluRay
PageBRNav  = [BtnBRUp, BtnBRLeft, BtnBRDown, BtnBRRight, BtnBREnter]
PageBROpt  = [BtnBRPopup, BtnBRSetup, BtnBRInfo, BtnBRReturn, BtnBRTray, BtnBRPower]
PageBRPlay = [BtnBRPrev, BtnBRBack, BtnBRPause, BtnBRPlay, BtnBRStop, BtnBRRewi, BtnBRNext, BtnBRTray]
GroupPlay  = MESet(PageBRPlay)
## Group Button State List
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
## End Communication Interface Definition --------------------------------------

# This is the last function that loads when starting the system-----------------
def Initialize():
    ## Opening a new Connection Thread to all devices
    Biamp.Connect()
    Denon.Initialize()
    
    ## Power Page Counter Variable
    global PwrCount
    PwrCount = 0
    
    ## Biamp Subscribe Commands
    Biamp.SubscribeStatus('ConnectionStatus',None,Biamp_Parsing)
    Biamp.SubscribeStatus('SourceSelectorSourceSelection',{'Instance Tag':'SelectorA'},Biamp_Parsing)
    Biamp.SubscribeStatus('SourceSelectorSourceSelection',{'Instance Tag':'SelectorB'},Biamp_Parsing)
    Biamp.SubscribeStatus('SourceSelectorSourceSelection',{'Instance Tag':'SelectorC'},Biamp_Parsing)
    Biamp.SubscribeStatus('SourceSelectorSourceSelection',{'Instance Tag':'SelectorD'},Biamp_Parsing)
    Biamp.SubscribeStatus('SourceSelectorSourceSelection',{'Instance Tag':'SelectorE'},Biamp_Parsing)

    ## Quantum Subscribe Commands
    Quantum.SubscribeStatus('ConnectionStatus',None,Quantum_Parsing)
    Quantum.SubscribeStatus('DeviceStatus',None,Quantum_Parsing)

    ## Denon Subscribe Commands
    Denon.SubscribeStatus('ConnectionStatus',None,Denon_Parsing)
    Denon.SubscribeStatus('CurrentChapterTrackNum',None,Denon_Parsing)
    Denon.SubscribeStatus('CurrentTitleAlbumNum',None,Denon_Parsing)
    Denon.SubscribeStatus('DiscTypeStatus',None,Denon_Parsing)
    Denon.SubscribeStatus('PlaybackStatus',None,Denon_Parsing)
    Denon.SubscribeStatus('Power',None,Denon_Parsing)
    
    ## TouchPanel Functions
    GroupMode.SetCurrent(None)
    TLP.HidePopupGroup(2)
    TLP.ShowPage('Index')
    TLP.ShowPopup('Welcome')
    
    ## Update Data Dictionaries
    @Wait(5)
    def CheckData():
        DictionaryUpdate()
    
    ## Notify to Console
    print("System Initialize")
    pass

## Data Parsing Functions ------------------------------------------------------
## These functions receive the data of the devices in real time
## Each function stores the parsed data in dictionaries and activate feedback
## Each function works with the subscription methods of the Python modules

## Data Parsing Functions - IP Controlled Devices ------------------------------
def Biamp_Parsing(command,value,qualifier):

    if command == 'ConnectionStatus':
        if value == 'Connected':
            Biamp_Data['Conex'] = 'Connected'
            BtnLANBiamp.SetState(1)
        elif value == 'Disconnected':
            Biamp_Data['Conex'] = 'Disconnected'
            BtnLANBiamp.SetState(0)

    elif command == 'SourceSelectorSourceSelection':
        print(qualifier)
        print(value)
        ## The value is the active channel of active Source Selector Block
        if value == 'No Source':
            if qualifier['Instance Tag'] == 'SelectorA':
                Biamp_Data['SelectorA'] = 'No Source' ##Store data in Dictionary
                GroupSetA.SetCurrent(None) ##Turn On-Off the active Source Button
            elif qualifier['Instance Tag'] == 'SelectorB':
                Biamp_Data['SelectorB'] = 'No Source' ##Store data in Dictionary
                GroupSetB.SetCurrent(None) ##Turn On-Off the active Source Button
            elif qualifier['Instance Tag'] == 'SelectorC':
                Biamp_Data['SelectorC'] = 'No Source' ##Store data in Dictionary
                GroupSetC.SetCurrent(None) ##Turn On-Off the active Source Button
            elif qualifier['Instance Tag'] == 'SelectorD':
                Biamp_Data['SelectorD'] = 'No Source' ##Store data in Dictionary
                GroupSetD.SetCurrent(None) ##Turn On-Off the active Source Button
            elif qualifier['Instance Tag'] == 'SelectorE':
                Biamp_Data['SelectorE'] = 'No Source' ##Store data in Dictionary
                GroupSetE.SetCurrent(None) ##Turn On-Off the active Source Button
        else:
            value = int(value) ##The active channel is string type, now is integer
            value = value - 1  ##The first index of button list is 0 not 1
            ## Assign the value to Button Lists
            if qualifier['Instance Tag'] == 'SelectorA':
                Biamp_Data['SelectorA'] = (value + 1) ##Store int data in Dictionary
                GroupSetA.SetCurrent(value) ##Turn On-Off the active Source Button
            elif qualifier['Instance Tag'] == 'SelectorB':
                Biamp_Data['SelectorB'] = (value + 1) ##Store int  data in Dictionary
                GroupSetB.SetCurrent(value) ##Turn On-Off the active Source Button
            elif qualifier['Instance Tag'] == 'SelectorC':
                Biamp_Data['SelectorC'] = (value + 1) ##Store int  data in Dictionary
                GroupSetC.SetCurrent(value) ##Turn On-Off the active Source Button
            elif qualifier['Instance Tag'] == 'SelectorD':
                Biamp_Data['SelectorD'] = (value + 1) ##Store int data in Dictionary
                GroupSetD.SetCurrent(value) ##Turn On-Off the active Source Button
            elif qualifier['Instance Tag'] == 'SelectorE':
                Biamp_Data['SelectorE'] = (value + 1) ##Store int data in Dictionary
                GroupSetE.SetCurrent(value) ##Turn On-Off the active Source Button
    pass

def Quantum_Parsing(command,value,qualifier):

    if command == 'ConnectionStatus':
        if value == 'Connected':
            Quantum_Data['Conex'] = 'Connected'
            BtnLANVWall.SetState(1)
        elif value == 'Disconnected':
            Quantum_Data['Conex'] = 'Disconnected'
            BtnLANVWall.SetState(0)

    elif command == 'DeviceStatus':
        Quantum_Data['DeviceStatus'] = value ##Store the value in Dictionary
        print('Parsing Quantum Device: ' + Quantum_Data['DeviceStatus'])
    
    pass

## Data Parsing Functions - Serial Controlled Devices --------------------------
def Denon_Parsing(command,value,qualifier):
    
    if command == 'ConnectionStatus':
        if value == 'Connected':
            Denon_Data['Conex'] = 'Connected' ##Store the value in Dictionary
            Btn232Denon.SetState(1)
        elif value == 'Disconnected':
            Denon_Data['Conex'] = 'Disconnected' ##Store the value in Dictionary
            Btn232Denon.SetState(0)

    elif command == 'CurrentChapterTrackNum':
        Denon_Data['Chapter'] = value ##Store the value in Dictionary
        ## Send the new data to GUI BluRay Label
        LblBRDisk.SetText(Denon_Data['DiscType'] + ' Title: ' + str(Denon_Data['Title']) + ' Chap: ' + str(Denon_Data['Chapter']))
        print('Parsing Denon Chapter: ' + str(Denon_Data['Chapter']))

    elif command == 'CurrentTitleAlbumNum':
        Denon_Data['Title'] = value ##Store the value in Dictionary
        ## Send the new data to GUI BluRay Label
        LblBRDisk.SetText(Denon_Data['DiscType'] + ' Title: ' + str(Denon_Data['Title']) + ' Chap: ' + str(Denon_Data['Chapter']))
        print('Parsing Denon Title:' + str(Denon_Data['Title']))

    elif command == 'DiscTypeStatus':
        Denon_Data['DiscType'] = value ##Store the value in Dictionary
        ## Send the new data to GUI BluRay Label
        LblBRDisk.SetText(Denon_Data['DiscType'] + ' Title: ' + str(Denon_Data['Title']) + ' Chap: ' + str(Denon_Data['Chapter']))
        print('Parsing Denon Disk:' + Denon_Data['DiscType'])
 
    elif command == 'PlaybackStatus':
        Denon_Data['PlaybackStatus'] = value ##Store the value in Dictionary
        print('Parsing Denon Play:' + Denon_Data['PlaybackStatus'])
        if value == 'Fast Reverse':
            GroupPlay.SetCurrent(BtnBRBack)
        elif value == 'Playing':
            GroupPlay.SetCurrent(BtnBRPlay)
        elif value == 'Paused':
            GroupPlay.SetCurrent(BtnBRPause)
        elif value == 'Stopped' or value == 'Resume Stop':
            GroupPlay.SetCurrent(BtnBRStop)
        elif value == 'Fast Forward':
            GroupPlay.SetCurrent(BtnBRRewi)
        elif value == 'Tray Opening':
            GroupPlay.SetCurrent(BtnBRTray)
        else:
            GroupPlay.SetCurrent(None)

    elif command == 'Power':
        Denon_Data['Power'] = value ##Store the value in Dictionary
        print('Parsing Denon Power:' + Denon_Data['Power'])
        if value == 'On':
            Denon_Data['Power'] = 'On'
            BtnBRPower.SetState(1)
        elif value == 'Off':
            Denon_Data['Power'] = 'Off'
            BtnBRPower.SetState(0)
    pass
## Data dictionaries -----------------------------------------------------------
## Each dictionary store the real time information of room devices
## Data dictionaries - IP Controlled Devices -----------------------------------
Biamp_Data = {
    'Conex'     : '',
    'SelectorA' : '',
    'SelectorB' : '',
    'SelectorC' : '',
    'SelectorD' : '',
    'SelectorE' : '',    
}
Quantum_Data = {
    'Conex'        : '',
    'DeviceStatus' : '',
}
## Data dictionaries - Serial Controlled Devices -------------------------------
Denon_Data = {
    'Conex'          : '',
    'Chapter'        : '',
    'DiscType'       : '',
    'PlaybackStatus' : '',
    'Power'          : '',
    'Title'          : '',
}

## Recursive functions ---------------------------------------------------------
def DictionaryUpdate():
    ##If any data dicionary are empty
    if Biamp_Data['SelectorA'] == '' or Biamp_Data['SelectorB'] == '' or \
       Biamp_Data['SelectorC'] == '' or Biamp_Data['SelectorD'] == ''or \
       Biamp_Data['SelectorE'] == '':
       ## Send Queries information to devices
       Biamp.Update('SourceSelectorSourceSelection',{'Instance Tag':'SelectorA'})
       Biamp.Update('SourceSelectorSourceSelection',{'Instance Tag':'SelectorB'})
       Biamp.Update('SourceSelectorSourceSelection',{'Instance Tag':'SelectorC'})
       Biamp.Update('SourceSelectorSourceSelection',{'Instance Tag':'SelectorD'})
       Biamp.Update('SourceSelectorSourceSelection',{'Instance Tag':'SelectorE'})
       ## Notify to Console
       print('-> Data Biamp SourceA: ' + str(Biamp_Data['SelectorA']))
       print('-> Data Biamp SourceB: ' + str(Biamp_Data['SelectorB']))
       print('-> Data Biamp SourceC: ' + str(Biamp_Data['SelectorC']))
       print('-> Data Biamp SourceD: ' + str(Biamp_Data['SelectorD']))
       print('-> Data Biamp SourceE: ' + str(Biamp_Data['SelectorE']))
    pass
       
    

## Event Definitions -----------------------------------------------------------
## This section define all actions that a user triggers through the buttons ----
## Page Index ------------------------------------------------------------------
@event(BtnIndex, 'Pressed')
def IndexEvents(button, state):
    TLP.HideAllPopups()
    TLP.ShowPage('Main')
    TLP.ShowPopup('Welcome')
    print('Touch Mode: %s' % 'Index')
    pass

## Main Page -------------------------------------------------------------------
@event(PageMain, ButtonEventList)
def MainEvents(button, state):

    if button is BtnVideo and state == 'Pressed':
        LblMaster.SetText('Proyección de Video')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('VWall')
        print('Touch Mode: %s' % 'VideoWall')

    elif button is BtnAudio and state == 'Pressed':
        LblMaster.SetText('Selección de Audio')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('Audios')
        print('Touch Mode: %s' % 'Audio')

    elif button is BtnBluRay and state == 'Pressed':
        LblBRDisk.SetText(Denon_Data['DiscType'] + ' Title: ' + str(Denon_Data['Title']) + ' Chap: ' + str(Denon_Data['Chapter']))
        LblMaster.SetText('Control de BluRay')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('BR')
        print('Touch Mode: %s' % 'BluRay')

    elif button is BtnStatus and state == 'Pressed':
        LblMaster.SetText('Información de dispositivos')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('Status')
        print('Touch Mode: %s' % 'Status')

    elif button is BtnPowerOff and state == 'Pressed':
        LblMaster.SetText('Apagado del Sistema')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('x_PowerOff')
        print('Touch Mode: %s' % 'PowerOff')

    ##Turn On the feedbak of last pressed button
    GroupMode.SetCurrent(button)
    pass

## Video Page ------------------------------------------------------------------
@event(PageVW, ButtonEventList)
def VideoSourcesEvents(button, state):
    if button is BtnVHDMI and state == 'Pressed':
        Quantum.Set('PresetRecall','1',{'Canvas':'1'})
        print("Videowall Full: %s" % 'HDMI')
    elif button is BtnVPS4 and state == 'Pressed':
        Quantum.Set('PresetRecall','2',{'Canvas':'1'})
        print("Videowall Full: %s" % 'PS4')
    elif button is BtnVXbox and state == 'Pressed':
        Quantum.Set('PresetRecall','3',{'Canvas':'1'})
        print("Videowall Full: %s" % 'Xbox')
    elif button is BtnVBluRay and state == 'Pressed':
        Quantum.Set('PresetRecall','4',{'Canvas':'1'})
        print("Videowall Full: %s" % 'Bluray')
    elif button is BtnVSky and state == 'Pressed':
        Quantum.Set('PresetRecall','5',{'Canvas':'1'})
        print("Videowall Full: %s" % 'Sky')
    elif button is BtnVRoku and state == 'Pressed':
        Quantum.Set('PresetRecall','6',{'Canvas':'1'})
        print("Videowall Full: %s" % 'Roku')
    elif button is BtnVPC and state == 'Pressed':
        Quantum.Set('PresetRecall','7',{'Canvas':'1'})
        print("Videowall Full: %s" % 'PC')
    elif button is BtnVShare and state == 'Pressed':
        Quantum.Set('PresetRecall','8',{'Canvas':'1'})
        print("Videowall Full: %s" % 'Share')
    pass

@event(PageVWP, ButtonEventList)
def VideoPresetsEvents(button, state):
    if button is BtnVP1 and state == 'Pressed':
        Quantum.Set('PresetRecall','9',{'Canvas':'1'})
        print("Videowall Preset: %s" % '1')
    elif button is BtnVP2 and state == 'Pressed':
        Quantum.Set('PresetRecall','10',{'Canvas':'1'})
        print("Videowall Preset: %s" % '2')
    elif button is BtnVP3 and state == 'Pressed':
        Quantum.Set('PresetRecall','11',{'Canvas':'1'})
        print("Videowall Preset: %s" % '3')
    elif button is BtnVP4 and state == 'Pressed':
        Quantum.Set('PresetRecall','12',{'Canvas':'1'})
        print("Videowall Preset: %s" % '4')
    elif button is BtnVP5 and state == 'Pressed':
        Quantum.Set('PresetRecall','13',{'Canvas':'1'})
        print("Videowall Preset: %s" % '5')
    elif button is BtnVP6 and state == 'Pressed':
        Quantum.Set('PresetRecall','14',{'Canvas':'1'})
        print("Videowall Preset: %s" % '6')
    elif button is BtnVP7 and state == 'Pressed':
        Quantum.Set('PresetRecall','15',{'Canvas':'1'})
        print("Videowall Preset: %s" % '7')
    elif button is BtnVP8 and state == 'Pressed':
        Quantum.Set('PresetRecall','16',{'Canvas':'1'})
        print("Videowall Preset: %s" % '8')
    pass

@event(PageVWPwr, ButtonEventList)
def VideoPowerEvents(button, state):
    if button is BtnVWPwr1 and state == 'Pressed':
        print("Videowall: %s" % 'PwrOn')
    elif button is BtnVWPwr0 and state == 'Pressed':
        print("Videowall: %s" % 'PwrOff')
    pass
pass

## Audio Page ------------------------------------------------------------------
@event(PageAudio, ButtonEventList)
def AudioSetEvents(button, state):
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
    ##Turn On the feedbak of last pressed button
    GroupAudio.SetCurrent(button)
    pass

@event(PageAudioA, ButtonEventList)
def AudioAEvents(button, state):
    if button is BtnHDMI_A and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','1',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','HDMI'))
    elif button is BtnPS4_A and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','2',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','PS4'))
    elif button is BtnXbox_A and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','3',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','Xbox'))
    elif button is BtnBluRay_A and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','4',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','Bluray'))
    elif button is BtnSky_A and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','5',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','Sky'))
    elif button is BtnRoku_A and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','6',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','Roku'))
    elif button is BtnPC_A and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','7',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','PC'))
    elif button is BtnShare_A and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','8',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','Share'))
    pass

@event(PageAudioB, ButtonEventList)
def AudioBEvents(button, state):
    if button is BtnHDMI_B and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','1',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','HDMI'))
    elif button is BtnPS4_B and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','2',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','PS4'))
    elif button is BtnXbox_B and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','3',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','Xbox'))
    elif button is BtnBluRay_B and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','4',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','Bluray'))
    elif button is BtnSky_B and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','5',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','Sky'))
    elif button is BtnRoku_B and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','6',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','Roku'))
    elif button is BtnPC_B and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','7',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','PC'))
    elif button is BtnShare_B and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','8',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','Share'))
    pass

@event(PageAudioC, ButtonEventList)
def AudioCEvents(button, state):
    if button is BtnHDMI_C and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','1',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','HDMI'))
    elif button is BtnPS4_C and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','2',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','PS4'))
    elif button is BtnXbox_C and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','3',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','Xbox'))
    elif button is BtnBluRay_C and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','4',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','Bluray'))
    elif button is BtnSky_C and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','5',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','Sky'))
    elif button is BtnRoku_C and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','6',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','Roku'))
    elif button is BtnPC_C and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','7',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','PC'))
    elif button is BtnShare_C and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','8',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','Share'))
    pass

@event(PageAudioD, ButtonEventList)
def AudioDEvents(button, state):
    if button is BtnHDMI_D and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','1',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','HDMI'))
    elif button is BtnPS4_D and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','2',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','PS4'))
    elif button is BtnXbox_D and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','3',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','Xbox'))
    elif button is BtnBluRay_D and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','4',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','Bluray'))
    elif button is BtnSky_D and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','5',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','Sky')) 
    elif button is BtnRoku_D and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','6',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','Roku'))
    elif button is BtnPC_D and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','7',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','PC'))
    elif button is BtnShare_D and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','8',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','Share'))
    pass

@event(PageAudioE, ButtonEventList)
def AudioEEvents(button, state):
    if button is BtnHDMI_E and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','1',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','HDMI'))
    elif button is BtnPS4_E and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','2',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','PS4'))
    elif button is BtnXbox_E and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','3',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','Xbox'))
    elif button is BtnBluRay_E and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','4',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','Bluray'))
    elif button is BtnSky_E and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','5',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','Sky'))
    elif button is BtnRoku_E and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','6',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','Roku'))
    elif button is BtnPC_E and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','7',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','PC'))
    elif button is BtnShare_E and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','8',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','Share'))
    pass

## Bluray Page -----------------------------------------------------------------
@event(PageBRNav, ButtonEventList)
def BRNavigationEvents(button, state):
    if button is BtnBRUp and state == 'Pressed':
        Denon.Set('MenuNavigation','Up')
        print("BluRay Pressed: %s" % 'Up')
        
    elif button is BtnBRLeft and state == 'Pressed':
        Denon.Set('MenuNavigation','Left')
        print("BluRay Pressed: %s" % 'Left')
    
    elif button is BtnBRDown and state == 'Pressed':
        Denon.Set('MenuNavigation','Down')
        print("BluRay Pressed: %s" % 'Down')
    
    elif button is BtnBRRight and state == 'Pressed':
        Denon.Set('MenuNavigation','Right')
        print("BluRay Pressed: %s" % 'Right')
    
    elif button is BtnBREnter and state == 'Pressed':
        Denon.Set('MenuNavigation','Enter')
        print("BluRay Pressed: %s" % 'Enter')
    pass

@event(PageBROpt, ButtonEventList)
def BROptionEvents(button, state):

    if button is BtnBRPopup and state == 'Pressed':
        Denon.Set('MenuNavigation','Menu')
        BtnBRPopup.SetState(1)
        print("BluRay Pressed: %s" % 'Menu')
    else:
        BtnBRPopup.SetState(0)

    if button is BtnBRSetup and state == 'Pressed':
        Denon.Set('Function','Setup')
        BtnBRSetup.SetState(1)
        print("BluRay Pressed: %s" % 'Title')
    else:
        BtnBRSetup.SetState(0)

    if button is BtnBRInfo and state == 'Pressed':
        Denon.Set('Function','Display')
        BtnBRInfo.SetState(1)
        print("BluRay Pressed: %s" % 'Info')
    else:
        BtnBRInfo.SetState(0)

    if button is BtnBRReturn and state == 'Pressed':
        Denon.Set('MenuNavigation','Return')
        BtnBRReturn.SetState(1)
        print("BluRay Pressed: %s" % 'Return')
    else:
        BtnBRReturn.SetState(0)

    if button is BtnBRTray and state == 'Pressed':
        Denon.Set('Transport','Eject')
        print("BluRay Pressed: %s" % 'Tray')

    if button is BtnBRPower and state == 'Pressed':
        print("BluRay Pressed: %s" % 'Power')
        if Denon_Data['Power'] == 'On':
            BtnBRPower.SetState(0)
            Denon.Set('Power','Off')
        elif Denon_Data['Power'] == 'Off':
            BtnBRPower.State(1)
            Denon.Set('Power','On')
    pass

@event(PageBRPlay, ButtonEventList)
def BRPlayEvents(button, state):

    if button is BtnBRPrev and state == 'Pressed':
        Denon.Set('Transport','Previous')
        BtnBRPrev.SetState(1)
        print("BluRay Pressed: %s" % 'Prev')
    else:
        BtnBRPrev.SetState(0)

    if button is BtnBRBack and state == 'Pressed':
        Denon.Set('Transport','Rew')
        print("BluRay Pressed: %s" % 'Back')

    if button is BtnBRPause and state == 'Pressed':
        Denon.Set('Transport','Pause')
        print("BluRay Pressed: %s" % 'Pause')

    if button is BtnBRPlay and state == 'Pressed':
        Denon.Set('Transport','Play')
        print("BluRay Pressed: %s" % 'Play')

    if button is BtnBRStop and state == 'Pressed':
        Denon.Set('Transport','Stop')
        print("BluRay Pressed: %s" % 'Stop')

    if button is BtnBRRewi and state == 'Pressed':
        Denon.Set('Transport','FFwd')
        print("BluRay Pressed: %s" % 'Rewind')

    if button is BtnBRNext and state == 'Pressed':
        Denon.Set('Transport','Next')
        BtnBRNext.SetState(1)
        print("BluRay Pressed: %s" % 'Next')
    else:
        BtnBRNext.SetState(0)

    pass

## Status Page -----------------------------------------------------------------

## Power Page ------------------------------------------------------------------
@event(BtnPowerAll, ButtonEventList)
def PowerEvents(button, state):   
    global PwrCount
    ## If the user press the Power Button:
    ## Only Turn On the first state of button - Does not do any action
    if state == 'Pressed':
        BtnPowerAll.SetState(1)
        print('Button Pressed: %s' % 'PowerAll')
    ## If the user holds down the button:
    ## A variable is incremented up to 4 seconds
    ## In each new value, Turn On each visual state of the Power Button
    ## Whne the value is equal to 4, ShutDown all devices in the System
    elif state == 'Repeated':
        PwrCount = PwrCount + 1
        BtnPowerAll.SetState(PwrCount)
        LblCountAll.SetText(str(PwrCount))
        print('Button Repeated: %s' % 'PowerAll')
        ## Shutdown routine
        if PwrCount == 4:
            Denon.Set('Power','Off')
            Denon_Data['Power'] = 'Off'
            TLP.ShowPage('Index')
    ## If the user release the Button:
    ## Clean the counter power data in GUI and delete the visual feedback
    elif state == 'Released':
        PwrCount = 0
        BtnPowerAll.SetState(0)
        LblCountAll.SetText('')
        print('Button Released: %s' % 'PowerAll')
    pass

## End Events Definitions-------------------------------------------------------
Initialize()