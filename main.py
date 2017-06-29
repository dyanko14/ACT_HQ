## -------------------------------------------------------------------------- ##
## Business   | Asesores y Consultores en Tecnología S.A. de C.V. ----------- ##
## Programmer | Dyanko Cisneros Mendoza
## Customer   | Human Quality
## Project    | VideoWall Room
## Version    | 0.1 --------------------------------------------------------- ##

## CONTROL SCRIPT IMPORT -------------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface,
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface,
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait

from gui import TLP, Btn, Btn_Page, Btn_Group, Btn_State, Lbl, Popup, Page
print(Version())

## PROCESOR DEFINITION ---------------------------------------------------------
IPCP = ProcessorDevice('IPlink')

## MODULE IMPORT ---------------------------------------------------------------
## Ethernet:
import biam_dsp_TesiraSeries_v1_5_20_0    as DeviceA
import extr_sp_Quantum_Ultra610_v1_0_1_0  as DeviceB
## RS-232
import deno_dvd_DBT3313UD_Series_v1_0_2_0 as DeviceC

## Ethernet:
Biamp   = DeviceA.EthernetClass('192.168.10.150', 23, Model='TesiraFORTE CI')
Quantum = DeviceB.EthernetClass('10.10.10.12', 23, Model='Quantum Ultra 610')
## RS-232:
Denon   = DeviceC.SerialClass(IPCP, 'COM1', Baud=9600, Model='DBT-3313UD')

## INITIALIZATE ----------------------------------------------------------------
## This is the last function that loads when starting the system
def Initialize():
    ## Opening a new connection Socket
    ## IP Sockets
    Biamp.Connect()
    Quantum.Connect()
    ## Serial Sockets
    Denon.Initialize()
    SubscribeDenon()
    UpdateDenon()

    ## Power Page Counter Variable
    global intPwrCount
    intPwrCount = 4
    
    ## Recursive Functions
    UpdateLoop()

    ## TouchPanel Functions
    Btn_Group['Mode'].SetCurrent(None)
    TLP.HidePopupGroup(2)
    TLP.ShowPage(Page['Index'])
    TLP.ShowPopup(Popup['Hi'])
    
    ## Notify to Console
    print("System Initialize")
    pass

## SUBSCRIBE FUNCTIONS ---------------------------------------------------------
def SubscribeBiamp():
    Biamp.SubscribeStatus('ConnectionStatus',None,Biamp_Parsing)
    Biamp.SubscribeStatus('SourceSelectorSourceSelection',{'Instance Tag':'SelectorA'},Biamp_Parsing)
    Biamp.SubscribeStatus('SourceSelectorSourceSelection',{'Instance Tag':'SelectorB'},Biamp_Parsing)
    Biamp.SubscribeStatus('SourceSelectorSourceSelection',{'Instance Tag':'SelectorC'},Biamp_Parsing)
    Biamp.SubscribeStatus('SourceSelectorSourceSelection',{'Instance Tag':'SelectorD'},Biamp_Parsing)
    Biamp.SubscribeStatus('SourceSelectorSourceSelection',{'Instance Tag':'SelectorE'},Biamp_Parsing)
    pass

def SubscribeQuantum():
    pass

def SubscribeDenon():
    Denon.SubscribeStatus('ConnectionStatus',None,Denon_Parsing)
    Denon.SubscribeStatus('CurrentChapterTrackNum',None,Denon_Parsing)
    Denon.SubscribeStatus('CurrentTitleAlbumNum',None,Denon_Parsing)
    Denon.SubscribeStatus('DiscTypeStatus',None,Denon_Parsing)
    Denon.SubscribeStatus('PlaybackStatus',None,Denon_Parsing)
    Denon.SubscribeStatus('Power',None,Denon_Parsing)
    pass

## UPDATE FUNCTIONS ------------------------------------------------------------
def UpdateBiamp():
    Biamp.Update('SourceSelectorSourceSelection',{'Instance Tag':'SelectorA'})
    Biamp.Update('SourceSelectorSourceSelection',{'Instance Tag':'SelectorB'})
    Biamp.Update('SourceSelectorSourceSelection',{'Instance Tag':'SelectorC'})
    Biamp.Update('SourceSelectorSourceSelection',{'Instance Tag':'SelectorD'})
    Biamp.Update('SourceSelectorSourceSelection',{'Instance Tag':'SelectorE'})
    pass

def UpdateQuantum():
    pass

def UpdateDenon():
    Denon.Update('CurrentChapterTrackNum')
    Denon.Update('CurrentTitleAlbumNum')
    Denon.Update('DiscTypeStatus')
    Denon.Update('PlaybackStatus')
    Denon.Update('Power')
    pass

## DATA PARSING FUNCTIONS ------------------------------------------------------
## These functions receive the data of the devices in real time
## Each function stores the parsed data in dictionaries and activate feedback
## Each function works with the subscription methods of the Python modules
def Biamp_Parsing(command,value,qualifier):
    ##
    if command == 'ConnectionStatus':
        print('Biamp Module Conex status: {}'.format(value))

        if value == 'Connected':
            Biamp_Data['ConexModule'] = True
            Btn['LANBiamp'].SetState(1)
        else:
            Biamp_Data['ConexModule'] = False
            Btn['LANBiamp'].SetState(0)
            ## TurnOff the Buttons Feedback
            Btn_Group['SetA'].SetCurrent(None)
            Btn_Group['SetB'].SetCurrent(None)
            Btn_Group['SetC'].SetCurrent(None)
            Btn_Group['SetD'].SetCurrent(None)
            Btn_Group['SetE'].SetCurrent(None)
            ## Disconnect the IP Socket
            Biamp.Disconnect()
    ##
    elif command == 'SourceSelectorSourceSelection':
        print(str(qualifier) + ' ' + str(value))
        ## The value is the active channel of active Source Selector Block

        ## This function TurnOff the buttons when No Source is detected in each Block
        if value == 'No Source':
            for item in ['SelectorA','SelectorB','SelectorC','SelectorD','SelectorE']:
                if qualifier['Instance Tag'] == item:
                    ## Ej: Turn Off the 'SetD' Group Buttons ('Set'+(item[8]))
                    Btn_Group['Set'+(item[8])].SetCurrent(None)
        else:
            value = int(value) ##The active channel is string type, now is integer
            value = value - 1  ##The first index of button list is 0 not 1
            ## Assign the value to Button Lists
            if qualifier['Instance Tag'] == 'SelectorA':
                Btn_Group['SetA'].SetCurrent(value)

            elif qualifier['Instance Tag'] == 'SelectorB':
                Btn_Group['SetB'].SetCurrent(value)

            elif qualifier['Instance Tag'] == 'SelectorC':
                Btn_Group['SetC'].SetCurrent(value)

            elif qualifier['Instance Tag'] == 'SelectorD':
                Btn_Group['SetD'].SetCurrent(value)

            elif qualifier['Instance Tag'] == 'SelectorE':
                Btn_Group['SetE'].SetCurrent(value)
    pass

def Quantum_Parsing(command,value,qualifier):
    ##
    if command == 'ConnectionStatus':
        print('Biamp Module Conex status: {}'.format(value))

        if value == 'Connected':
            Quantum_Data['ConexModule'] = True
            Btn['LANVWall'].SetState(1)

        elif value == 'Disconnected':
            Quantum_Data['ConexModule'] = False
            Btn['LANVWall'].SetState(0)
            ## Disconnect the IP Socket
            Quantum.Disconnect()
    ##
    elif command == 'DeviceStatus':
        print(value)
    pass

def Denon_Parsing(command,value,qualifier):
    ##
    if command == 'ConnectionStatus':
        print('Denon Module Conex status: {}'.format(value))

        if value == 'Connected':
            Denon_Data['ConexModule'] = True
            Btn['232Denon'].SetState(1)

        elif value == 'Disconnected':
            Denon_Data['ConexModule'] = False
            Btn['232Denon'].SetState(0)
            ## TurnOff the Buttons Feedback
            Btn_Group['BR'].SetCurrent(None)
            Btn['BRPower'].SetState(0)
    ##
    elif command == 'CurrentChapterTrackNum':
        Denon_Data['Chapter'] = value 
        DenonLabel()
    ##
    elif command == 'CurrentTitleAlbumNum':
        Denon_Data['Title'] = value 
        DenonLabel()
    ##
    elif command == 'DiscTypeStatus':
        Denon_Data['DiscType'] = value 
        DenonLabel()
    ##
    elif command == 'PlaybackStatus':
        print('Bluray Playback Parsing: ' + value)
        Denon_Data['PlaybackStatus'] = value
        DenonLabel()
        if value == 'Fast Reverse':
            Btn_Group['BR'].SetCurrent(Btn['BRBack'])

        elif value == 'Playing':
            Btn_Group['BR'].SetCurrent(Btn['BRPlay'])

        elif value == 'Paused':
            Btn_Group['BR'].SetCurrent(Btn['BRPause'])

        elif value == 'Stopped' or value == 'Resume Stop':
            Btn_Group['BR'].SetCurrent(Btn['BRStop'])

        elif value == 'Fast Forward':
            Btn_Group['BR'].SetCurrent(Btn['BRRewi'])

        elif value == 'Tray Opening':
            Btn_Group['BR'].SetCurrent(Btn['BRTray'])

        else:
            Btn_Group['BR'].SetCurrent(None)
    ##
    elif command == 'Power':
        print('Bluray Power Parsing: ' + value)

        if value == 'On':
            Denon_Data['Power'] = True
            Btn['BRPower'].SetState(1)

        elif value == 'Off':
            Denon_Data['Power'] = False
            Btn['BRPower'].SetState(0)
    pass

def DenonLabel():
    ## This update the data of Bluray label in GUI
    Lbl['Bluray'].SetText(Denon_Data['DiscType'] +' Title: ' + 
                      str(Denon_Data['Title']) + ' Chap: ' +
                      str(Denon_Data['Chapter']))
    pass

## RECURSIVE FUNCTIONS -----------------------------------------------------------
## This functions report a 'Online' / 'Offline' status after to send the Connect() Method
## CAUTION: If you never make a Connect(), the Extron Module never will work with Subscriptions
@event(Biamp, 'Connected')
@event(Biamp, 'Disconnected')
def BiampConnectionHandler(interface, state):
    print('Biamp Conex Event: ' + state)
    if state == 'Connected':
        Btn['LANBiamp'].SetState(1)
        Biamp_Data['ConexEvent'] = True
        ## Send & Query Information
        SubscribeBiamp()
        UpdateBiamp()
    if state == 'Disconnected':
        Btn['LANBiamp'].SetState(0)
        Biamp_Data['ConexEvent'] = False
        Trying()
    pass

@event(Quantum, 'Connected')
@event(Quantum, 'Disconnected')
def QuantumConnectionHandler(interface, state):
    print('Quantum Conex Event: ' + state)
    if state == 'Connected':
        Btn['LANVWall'].SetState(1)
        Quantum_Data['ConexEvent'] = True
        ## Send & Query Information
        SubscribeQuantum()
        UpdateQuantum()
    if state == 'Disconnected':
        Btn['LANVWall'].SetState(0)
        Quantum_Data['ConexEvent'] = False
        Trying2()
    pass

## This functions try to make a Connect() 
## Help´s when the device was Off in the first Connect() method when the code starts
def Trying():
    if Biamp_Data['ConexEvent'] == False:
        print('Tryng to make a Connect() in Biamp')
        Biamp.Connect(4) ## Have 4 seconds to try to connect
        LoopTrying.Restart()
    pass
LoopTrying = Wait(5, Trying) ## Invoke a validate function every 5s

def Trying2():
    if Quantum_Data['ConexEvent'] == False:
        print('Tryng to make a Connect() in Quantum')
        Quantum.Connect(4) ## Have 4 seconds to try to connect
        LoopTrying2.Restart()
    pass
LoopTrying2 = Wait(5, Trying2) ## Invoke a validate function every 5s

def UpdateLoop():
    # This not affect any device
    # This return True / False when no response is received from Module
    # If in 5 times the data is not reported (connectionCounter = 5) from the Update Command
    # Generate 'Connected' / 'Disconnected'
    Biamp.Update('VerboseMode')
    Quantum.Update('Input',{'Window':1,'Canvas':'1'})
    Denon.Update('PlaybackStatus')
    loopUpdate.Restart()
loopUpdate = Wait(12, UpdateLoop) # Invoke a query function each 12s

## DATA DICTIONARIES -----------------------------------------------------------
## Each dictionary store the real time information of room devices
## Data dictionaries - IP Devices
Biamp_Data = {
    'ConexModule': None,
    'ConexEvent' : None,
}
Quantum_Data = {
    'ConexModule': None,
    'ConexEvent' : None,
}
## Data dictionaries - RS232 Devices
Denon_Data = {
    'Conex'          : None,
    'Chapter'        : '',
    'DiscType'       : '',
    'PlaybackStatus' : '',
    'Power'          : None,
    'Title'          : '',
}

## PAGE USER EVENTS ------------------------------------------------------------
## Page Index ------------------------------------------------------------------
@event(Btn['Index'], 'Pressed')
def IndexEvents(button, state):
    TLP.HideAllPopups()
    TLP.ShowPage(Page['Main'])
    TLP.ShowPopup(Popup['Hi'])
    print('Touch Mode: %s' % 'Index')
    pass

## Main Page -------------------------------------------------------------------
@event(Btn_Page['Main'], Btn_State['List'])
def MainEvents(button, state):

    if button is Btn['Video'] and state == 'Pressed':
        Lbl['Master'].SetText('Proyección de Video')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup(Popup['Video'])
        print('Touch Mode: %s' % 'VideoWall')

    elif button is Btn['Audio'] and state == 'Pressed':
        Lbl['Master'].SetText('Selección de Audio')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup(Popup['Audio'])
        print('Touch Mode: %s' % 'Audio')

    elif button is Btn['Bluray'] and state == 'Pressed':
        Lbl['Master'].SetText('Control de BluRay')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup(Popup['Bluray'])
        print('Touch Mode: %s' % 'BluRay')

    elif button is Btn['Status'] and state == 'Pressed':
        Lbl['Master'].SetText('Información de dispositivos')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup(Popup['Status'])
        print('Touch Mode: %s' % 'Status')

    elif button is Btn['Power'] and state == 'Pressed':
        Lbl['Master'].SetText('Apagado del Sistema')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup(Popup['Power'])
        print('Touch Mode: %s' % 'PowerOff')

    ##Turn On the feedbak of last pressed button
    Btn_Group['Mode'].SetCurrent(button)
    pass

## Video Page ------------------------------------------------------------------
@event(Btn_Page['VW'], Btn_State['List'])
def VideoSourcesEvents(button, state):
    
    if button is Btn['VHDMI'] and state == 'Pressed':
        Quantum.Set('PresetRecall','1',{'Canvas':'1'})
        print("Videowall Full: %s" % 'HDMI')
    
    elif button is Btn['VPS4'] and state == 'Pressed':
        Quantum.Set('PresetRecall','2',{'Canvas':'1'})
        print("Videowall Full: %s" % 'PS4')
    
    elif button is Btn['VXbox'] and state == 'Pressed':
        Quantum.Set('PresetRecall','3',{'Canvas':'1'})
        print("Videowall Full: %s" % 'Xbox')
    
    elif button is Btn['VBluray'] and state == 'Pressed':
        Quantum.Set('PresetRecall','4',{'Canvas':'1'})
        print("Videowall Full: %s" % 'Bluray')
        
    elif button is Btn['VSky'] and state == 'Pressed':
        Quantum.Set('PresetRecall','5',{'Canvas':'1'})
        print("Videowall Full: %s" % 'Sky')
    
    elif button is Btn['VRoku'] and state == 'Pressed':
        Quantum.Set('PresetRecall','6',{'Canvas':'1'})
        print("Videowall Full: %s" % 'Roku')
    
    elif button is Btn['VPC'] and state == 'Pressed':
        Quantum.Set('PresetRecall','7',{'Canvas':'1'})
        print("Videowall Full: %s" % 'PC')
    
    elif button is Btn['VShare'] and state == 'Pressed':
        Quantum.Set('PresetRecall','8',{'Canvas':'1'})
        print("Videowall Full: %s" % 'Share')
    pass

@event(Btn_Page['VWP'], Btn_State['List'])
def VideoPresetsEvents(button, state):
    
    if button is Btn['VP1'] and state == 'Pressed':
        Quantum.Set('PresetRecall','9',{'Canvas':'1'})
        print("Videowall Preset: %s" % '1')
    
    elif button is Btn['VP2'] and state == 'Pressed':
        Quantum.Set('PresetRecall','10',{'Canvas':'1'})
        print("Videowall Preset: %s" % '2')
    
    elif button is Btn['VP3'] and state == 'Pressed':
        Quantum.Set('PresetRecall','11',{'Canvas':'1'})
        print("Videowall Preset: %s" % '3')
    
    elif button is Btn['VP4'] and state == 'Pressed':
        Quantum.Set('PresetRecall','12',{'Canvas':'1'})
        print("Videowall Preset: %s" % '4')
    
    elif button is Btn['VP5'] and state == 'Pressed':
        Quantum.Set('PresetRecall','13',{'Canvas':'1'})
        print("Videowall Preset: %s" % '5')
    
    elif button is Btn['VP6'] and state == 'Pressed':
        Quantum.Set('PresetRecall','14',{'Canvas':'1'})
        print("Videowall Preset: %s" % '6')
    
    elif button is Btn['VP7'] and state == 'Pressed':
        Quantum.Set('PresetRecall','15',{'Canvas':'1'})
        print("Videowall Preset: %s" % '7')
    
    elif button is Btn['VP8'] and state == 'Pressed':
        Quantum.Set('PresetRecall','16',{'Canvas':'1'})
        print("Videowall Preset: %s" % '8')
    pass

@event(Btn_Page['VWPw'], Btn_State['List'])
def VideoPwrEvents(button, state):
    
    if button is Btn['VWPwr1'] and state == 'Pressed':
        print("Videowall: %s" % 'PwrOn')
    
    elif button is Btn['VWPwr0'] and state == 'Pressed':
        print("Videowall: %s" % 'PwrOff')
    pass

## Audio Page ------------------------------------------------------------------
@event(Btn_Page['Set'], Btn_State['List'])
def AudioSetEvents(button, state):
    
    if button is Btn['SetA'] and state == 'Pressed':
        TLP.ShowPopup(Popup['AudioA'])
        print("Audio Set: %s" % 'A')
    
    elif button is Btn['SetB'] and state == 'Pressed':
        TLP.ShowPopup(Popup['AudioB'])
        print("Audio Set: %s" % 'B')
    
    elif button is Btn['SetC'] and state == 'Pressed':
        TLP.ShowPopup(Popup['AudioC'])
        print("Audio Set: %s" % 'C')
    
    elif button is Btn['SetD'] and state == 'Pressed':
        TLP.ShowPopup(Popup['AudioD'])
        print("Audio Set: %s" % 'D')
    
    elif button is Btn['SetE'] and state == 'Pressed':
        TLP.ShowPopup(Popup['AudioE'])
        print("Audio Set: %s" % 'E')
    
    ##Turn On the feedbak of last pressed button
    Btn_Group['Set'].SetCurrent(button)
    pass

@event(Btn_Page['SetA'], Btn_State['List'])
def AudioAEvents(button, state):
    
    if button is Btn['A_HDMI'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','1',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','HDMI'))
    
    elif button is Btn['A_PS4'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','2',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','PS4'))
    
    elif button is Btn['A_Xbox'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','3',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','Xbox'))
    
    elif button is Btn['A_Bluray'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','4',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','Bluray'))
    
    elif button is Btn['A_Sky'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','5',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','Sky'))
    
    elif button is Btn['A_Roku'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','6',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','Roku'))
    
    elif button is Btn['A_PC'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','7',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','PC'))
    
    elif button is Btn['A_Share'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','8',{'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A','Share'))
    pass

@event(Btn_Page['SetB'], Btn_State['List'])
def AudioBEvents(button, state):
    
    if button is Btn['B_HDMI'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','1',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','HDMI'))
    
    elif button is Btn['B_PS4'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','2',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','PS4'))
    
    elif button is Btn['B_Xbox'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','3',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','Xbox'))
    
    elif button is Btn['B_Bluray'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','4',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','Bluray'))
    
    elif button is Btn['B_Sky'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','5',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','Sky'))
    
    elif button is Btn['B_Roku'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','6',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','Roku'))
    
    elif button is Btn['B_PC'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','7',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','PC'))
    
    elif button is Btn['B_Share'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','8',{'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B','Share'))
    pass
    
@event(Btn_Page['SetC'], Btn_State['List'])
def AudioCEvents(button, state):
    
    if button is Btn['C_HDMI'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','1',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','HDMI'))
    
    elif button is Btn['C_PS4'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','2',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','PS4'))
    
    elif button is Btn['C_Xbox'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','3',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','Xbox'))
    
    elif button is Btn['C_Bluray'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','4',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','Bluray'))
    
    elif button is Btn['C_Sky'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','5',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','Sky'))
    
    elif button is Btn['C_Roku'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','6',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','Roku'))
    
    elif button is Btn['C_PC'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','7',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','PC'))
    
    elif button is Btn['C_Share'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','8',{'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C','Share'))
    pass

@event(Btn_Page['SetD'], Btn_State['List'])
def AudioDEvents(button, state):
    
    if button is Btn['D_HDMI'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','1',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','HDMI'))
    
    elif button is Btn['D_PS4'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','2',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','PS4'))
    
    elif button is Btn['D_Xbox'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','3',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','Xbox'))
    
    elif button is Btn['D_Bluray'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','4',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','Bluray'))
    
    elif button is Btn['D_Sky'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','5',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','Sky'))
    
    elif button is Btn['D_Roku'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','6',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','Roku'))
    
    elif button is Btn['D_PC'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','7',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','PC'))
    
    elif button is Btn['D_Share'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','8',{'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D','Share'))
    pass

@event(Btn_Page['SetE'], Btn_State['List'])
def AudioEEvents(button, state):
    
    if button is Btn['E_HDMI'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','1',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','HDMI'))
    
    elif button is Btn['E_PS4'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','2',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','PS4'))
    
    elif button is Btn['E_Xbox'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','3',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','Xbox'))
    
    elif button is Btn['E_Bluray'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','4',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','Bluray'))
    
    elif button is Btn['E_Sky'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','5',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','Sky'))
    
    elif button is Btn['E_Roku'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','6',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','Roku'))
    
    elif button is Btn['E_PC'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','7',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','PC'))
    
    elif button is Btn['E_Share'] and state == 'Pressed':
        Biamp.Set('SourceSelectorSourceSelection','8',{'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E','Share'))
    pass

## Bluray Page -----------------------------------------------------------------
@event(Btn_Page['BRN'], Btn_State['List'])
def BRNavigationEvents(button, state):
    
    if button is Btn['BRUp'] and state == 'Pressed':
        Denon.Set('MenuNavigation','Up')
        print("BluRay Pressed: %s" % 'Up')
        
    elif button is Btn['BRLeft'] and state == 'Pressed':
        Denon.Set('MenuNavigation','Left')
        print("BluRay Pressed: %s" % 'Left')
    
    elif button is Btn['BRDown'] and state == 'Pressed':
        Denon.Set('MenuNavigation','Down')
        print("BluRay Pressed: %s" % 'Down')
    
    elif button is Btn['BRRight'] and state == 'Pressed':
        Denon.Set('MenuNavigation','Right')
        print("BluRay Pressed: %s" % 'Right')
    
    elif button is Btn['BREnter'] and state == 'Pressed':
        Denon.Set('MenuNavigation','Enter')
        print("BluRay Pressed: %s" % 'Enter')
    pass

@event(Btn_Page['BRO'], Btn_State['List'])
def BROptionEvents(button, state):

    if button is Btn['BRPopup'] and state == 'Pressed':
        Denon.Set('MenuNavigation','Menu')
        Btn['BRPopup'].SetState(1)
        print("BluRay Pressed: %s" % 'Menu')
    else:
        Btn['BRPopup'].SetState(0)

    if button is Btn['BRSetup'] and state == 'Pressed':
        Denon.Set('Function','Setup')
        Btn['BRSetup'].SetState(1)
        print("BluRay Pressed: %s" % 'Title')
    else:
        Btn['BRSetup'].SetState(0)

    if button is Btn['BRInfo'] and state == 'Pressed':
        Denon.Set('Function','Display')
        Btn['BRInfo'].SetState(1)
        print("BluRay Pressed: %s" % 'Info')
    else:
        Btn['BRInfo'].SetState(0)

    if button is Btn['BRReturn'] and state == 'Pressed':
        Denon.Set('MenuNavigation','Return')
        Btn['BRReturn'].SetState(1)
        print("BluRay Pressed: %s" % 'Return')
    else:
        Btn['BRReturn'].SetState(0)

    if button is Btn['BRTray'] and state == 'Pressed':
        Denon.Set('Transport','Eject')
        print("BluRay Pressed: %s" % 'Tray')

    if button is Btn['BRPower'] and state == 'Pressed':
        print("BluRay Pressed: %s" % 'Power')
        if Denon_Data['Power'] == True:
            Denon.Set('Power','Off')
        elif Denon_Data['Power'] == False:
            Denon.Set('Power','On')
    pass
    
@event(Btn_Page['BRP'], Btn_State['List'])
def BRPlayEvents(button, state):

    if button is Btn['BRPrev'] and state == 'Pressed':
        Denon.Set('Transport','Previous')
        Btn['BRPrev'].SetState(1)
        print("BluRay Pressed: %s" % 'Prev')
    else:
        Btn['BRPrev'].SetState(0)

    if button is Btn['BRBack'] and state == 'Pressed':
        Denon.Set('Transport','Rew')
        print("BluRay Pressed: %s" % 'Back')

    if button is Btn['BRPause'] and state == 'Pressed':
        Denon.Set('Transport','Pause')
        print("BluRay Pressed: %s" % 'Pause')

    if button is Btn['BRPlay'] and state == 'Pressed':
        Denon.Set('Transport','Play')
        print("BluRay Pressed: %s" % 'Play')

    if button is Btn['BRStop'] and state == 'Pressed':
        Denon.Set('Transport','Stop')
        print("BluRay Pressed: %s" % 'Stop')

    if button is Btn['BRRewi'] and state == 'Pressed':
        Denon.Set('Transport','FFwd')
        print("BluRay Pressed: %s" % 'Rewind')

    if button is Btn['BRNext'] and state == 'Pressed':
        Denon.Set('Transport','Next')
        Btn['BRNext'].SetState(1)
        print("BluRay Pressed: %s" % 'Next')
    else:
        Btn['BRNext'].SetState(0)

    pass

## Status Page -----------------------------------------------------------------

## Power Page ------------------------------------------------------------------
@event(Btn['PowerAll'], Btn_State['List'])
def PowerEvents(button, state):   
    global intPwrCount
    ## If the user press the Power Button:
    ## Only Turn On the first state of button - Does not do any action
    if state == 'Pressed':
        Btn['PowerAll'].SetState(1)
        print('Button Pressed: %s' % 'PowerAll')
    ## If the user holds down the button:
    ## A variable is incremented up to 4 seconds
    ## In each new value, Turn On each visual state of the Power Button
    ## Whne the value is equal to 4, ShutDown all devices in the System
    elif state == 'Repeated':
        intPwrCount = intPwrCount - 1
        Btn['PowerAll'].SetState(intPwrCount)
        Lbl['CountAll'].SetText(str(intPwrCount))
        print('Button Repeated: %s' % 'PowerAll')
        ## Shutdown routine
        if intPwrCount == 0:
            TLP.ShowPage(Page['Index'])
    ## If the user release the Button:
    ## Clean the counter power data in GUI and delete the visual feedback
    elif state == 'Released':
        intPwrCount = 4
        Btn['PowerAll'].SetState(0)
        Lbl['CountAll'].SetText('')
        print('Button Released: %s' % 'PowerAll')
    pass

## End Events Definitions-------------------------------------------------------
Initialize()