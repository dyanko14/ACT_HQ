"""--------------------------------------------------------------------------
 Business   | Asesores y Consultores en Tecnología S.A. de C.V.
 Programmer | Dyanko Cisneros Mendoza
 Customer   | Human Quality
 Project    | VideoWall Room
 Version    | 0.1 --------------------------------------------------------- """

## CONTROL SCRIPT IMPORT -------------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface, \
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface, \
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface, \
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait
from gui import TLP, BTN, BTNPAGE, BTNGROUP, BTNSTATE, LBL, POPUP, PAGE

## MODULE IMPORT ---------------------------------------------------------------
## IP:
import biam_dsp_TesiraSeries_v1_5_20_0    as DeviceA
import extr_sp_Quantum_Ultra610_v1_0_1_0  as DeviceB
## RS-232
import deno_dvd_DBT3313UD_Series_v1_0_2_0 as DeviceC

print(Version())

## PROCESOR DEFINITION ---------------------------------------------------------
IPCP = ProcessorDevice('IPlink')

## IP:
BIAMP = DeviceA.EthernetClass('192.168.10.150', 23, Model='TesiraFORTE CI')
QUANTUM = DeviceB.EthernetClass('10.10.10.12', 23, Model='Quantum Ultra 610')
## RS-232:
DENON = DeviceC.SerialClass(IPCP, 'COM1', Baud=9600, Model='DBT-3313UD')


## INITIALIZATE ----------------------------------------------------------------
def initialize():
    """This is the last function that loads when starting the system """
    ## OPEN CONNECTION SOCKETS
    ## IP
    BIAMP.Connect()
    QUANTUM.Connect()
    ## RS-232
    DENON.Initialize()
    subscribe_denon()
    update_denon()

    ## RECURSIVE FUNCTIONS
    update_loop_biamp()
    update_loop_quantum()
    update_loop_denon()

    ## POWER COUNTER VARIABLE
    global PWRCOUNT
    PWRCOUNT = 4 #Color Pwr Button Feedback 4=Too Much Red Button, 3=Red, 2=Slow Red, 1=Gray

    ## TOUCH PANEL FUNCTIONS
    BTNGROUP['Mode'].SetCurrent(None)
    TLP.HidePopupGroup(2)
    TLP.ShowPage(PAGE['Index'])
    TLP.ShowPopup(POPUP['Hi'])

    ## NOTIFY TO CONSOLE
    print("System Initialize")
    pass

## SUBSCRIBE FUNCTIONS ---------------------------------------------------------
def subscribe_biamp():
    """This send Subscribe Commands to Device"""
    BIAMP.SubscribeStatus('ConnectionStatus', None, biamp_parsing)
    BIAMP.SubscribeStatus('SourceSelectorSourceSelection', {'Instance Tag':'SelectorA'}, biamp_parsing)
    BIAMP.SubscribeStatus('SourceSelectorSourceSelection', {'Instance Tag':'SelectorB'}, biamp_parsing)
    BIAMP.SubscribeStatus('SourceSelectorSourceSelection', {'Instance Tag':'SelectorC'}, biamp_parsing)
    BIAMP.SubscribeStatus('SourceSelectorSourceSelection', {'Instance Tag':'SelectorD'}, biamp_parsing)
    BIAMP.SubscribeStatus('SourceSelectorSourceSelection', {'Instance Tag':'SelectorE'}, biamp_parsing)
    pass

def subscribe_quantum():
    """This send Subscribe Commands to Device"""
    pass

def subscribe_denon():
    """This send Subscribe Commands to Device"""
    DENON.SubscribeStatus('ConnectionStatus', None, denon_parsing)
    DENON.SubscribeStatus('CurrentChapterTrackNum', None, denon_parsing)
    DENON.SubscribeStatus('CurrentTitleAlbumNum', None, denon_parsing)
    DENON.SubscribeStatus('DiscTypeStatus', None, denon_parsing)
    DENON.SubscribeStatus('PlaybackStatus', None, denon_parsing)
    DENON.SubscribeStatus('Power', None, denon_parsing)
    pass

## UPDATE FUNCTIONS ------------------------------------------------------------
def update_biamp():
    """This send Update Commands to Device"""
    BIAMP.Update('SourceSelectorSourceSelection', {'Instance Tag':'SelectorA'})
    BIAMP.Update('SourceSelectorSourceSelection', {'Instance Tag':'SelectorB'})
    BIAMP.Update('SourceSelectorSourceSelection', {'Instance Tag':'SelectorC'})
    BIAMP.Update('SourceSelectorSourceSelection', {'Instance Tag':'SelectorD'})
    BIAMP.Update('SourceSelectorSourceSelection', {'Instance Tag':'SelectorE'})
    pass

def update_quantum():
    """This send Update Commands to Device"""
    pass

def update_denon():
    """This send Update Commands to Device"""
    DENON.Update('CurrentChapterTrackNum')
    DENON.Update('CurrentTitleAlbumNum')
    DENON.Update('DiscTypeStatus')
    DENON.Update('PlaybackStatus')
    DENON.Update('Power')
    pass

## DATA PARSING FUNCTIONS ------------------------------------------------------
## These functions receive the data of the devices in real time
## Each function stores the parsed data in dictionaries and activate feedback
## Each function works with the subscription methods of the Python modules
def biamp_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device"""
    if command == 'ConnectionStatus':
        print('Biamp Module Conex status: {}'.format(value))

        if value == 'Connected':
            BIAMP_DATA['ConexModule'] = True
            BTN['LANBiamp'].SetState(1)
        else:
            BIAMP_DATA['ConexModule'] = False
            BTN['LANBiamp'].SetState(0)
            ## TurnOff the Buttons Feedback
            BTNGROUP['SetA'].SetCurrent(None)
            BTNGROUP['SetB'].SetCurrent(None)
            BTNGROUP['SetC'].SetCurrent(None)
            BTNGROUP['SetD'].SetCurrent(None)
            BTNGROUP['SetE'].SetCurrent(None)
            ## Disconnect the IP Socket
            BIAMP.Disconnect()

    elif command == 'SourceSelectorSourceSelection':
        print(str(qualifier) + ' ' + str(value))
        ## The value is the active channel of active Source Selector Block
        ## This function TurnOff the buttons when No Source is detected in each Block
        if value == 'No Source':
            for item in ['SelectorA', 'SelectorB', 'SelectorC', 'SelectorD', 'SelectorE']:
                if qualifier['Instance Tag'] == item:
                    ## Ej: Turn Off the 'SetD' Group Buttons ('Set'+(item[8]))
                    BTNGROUP['Set'+(item[8])].SetCurrent(None)
        else:
            value = int(value) ##The active channel is string type, now is integer
            value = value - 1  ##The first index of button list is 0 not 1
            ## Assign the value to Button Lists
            if qualifier['Instance Tag'] == 'SelectorA':
                BTNGROUP['SetA'].SetCurrent(value)

            elif qualifier['Instance Tag'] == 'SelectorB':
                BTNGROUP['SetB'].SetCurrent(value)

            elif qualifier['Instance Tag'] == 'SelectorC':
                BTNGROUP['SetC'].SetCurrent(value)

            elif qualifier['Instance Tag'] == 'SelectorD':
                BTNGROUP['SetD'].SetCurrent(value)

            elif qualifier['Instance Tag'] == 'SelectorE':
                BTNGROUP['SetE'].SetCurrent(value)
    pass

def quantum_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device"""
    if command == 'ConnectionStatus':
        print('Quantum Module Conex status: {}'.format(value))

        if value == 'Connected':
            QUANTUM_DATA['ConexModule'] = True
            BTN['LANVWall'].SetState(1)

        elif value == 'Disconnected':
            QUANTUM_DATA['ConexModule'] = False
            BTN['LANVWall'].SetState(0)
            ## Disconnect the IP Socket
            QUANTUM.Disconnect()

    elif command == 'DeviceStatus':
        print(value)
    pass

def denon_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device"""
    if command == 'ConnectionStatus':
        print('Denon Module Conex status: {}'.format(value))

        if value == 'Connected':
            DENON_DATA['ConexModule'] = True
            BTN['232Denon'].SetState(1)

        elif value == 'Disconnected':
            DENON_DATA['ConexModule'] = False
            BTN['232Denon'].SetState(0)
            ## TurnOff the Buttons Feedback
            BTNGROUP['BR'].SetCurrent(None)
            BTN['BRPower'].SetState(0)

    elif command == 'CurrentChapterTrackNum':
        DENON_DATA['Chapter'] = value
        denon_label()

    elif command == 'CurrentTitleAlbumNum':
        DENON_DATA['Title'] = value
        denon_label()

    elif command == 'DiscTypeStatus':
        DENON_DATA['DiscType'] = value
        denon_label()

    elif command == 'PlaybackStatus':
        print('Bluray Playback Parsing: ' + value)
        DENON_DATA['PlaybackStatus'] = value
        denon_label()
        if value == 'Fast Reverse':
            BTNGROUP['BR'].SetCurrent(BTN['BRBack'])

        elif value == 'Playing':
            BTNGROUP['BR'].SetCurrent(BTN['BRPlay'])

        elif value == 'Paused':
            BTNGROUP['BR'].SetCurrent(BTN['BRPause'])

        elif value == 'Stopped' or value == 'Resume Stop':
            BTNGROUP['BR'].SetCurrent(BTN['BRStop'])

        elif value == 'Fast Forward':
            BTNGROUP['BR'].SetCurrent(BTN['BRRewi'])

        elif value == 'Tray Opening':
            BTNGROUP['BR'].SetCurrent(BTN['BRTray'])

        else:
            BTNGROUP['BR'].SetCurrent(None)

    elif command == 'Power':
        print('Bluray Power Parsing: ' + value)

        if value == 'On':
            DENON_DATA['Power'] = True
            BTN['BRPower'].SetState(1)

        elif value == 'Off':
            DENON_DATA['Power'] = False
            BTN['BRPower'].SetState(0)
    pass

def denon_label():
    """This update the data of Bluray label in GUI"""
    LBL['Bluray'].SetText(DENON_DATA['DiscType'] +' Title: ' + \
                      str(DENON_DATA['Title']) + ' Chap: ' + \
                      str(DENON_DATA['Chapter']))
    pass

## RECURSIVE FUNCTIONS -----------------------------------------------------------
## This functions report a 'Online' / 'Offline' status after to send the Connect() Method
## CAUTION: If you never make a Connect(), the Extron Module never will work with Subscriptions
@event(BIAMP, 'Connected')
@event(BIAMP, 'Disconnected')
def biamp_conex_event(interface, state):
    """BIAMP CONNECT() STATUS """
    print(str(interface) + ' Conex Event: ' + state)
    if state == 'Connected':
        BTN['LANBiamp'].SetState(1)
        BIAMP_DATA['ConexEvent'] = True
        ## Send & Query Information
        subscribe_biamp()
        update_biamp()
    if state == 'Disconnected':
        BTN['LANBiamp'].SetState(0)
        BIAMP_DATA['ConexEvent'] = False
        trying_biamp()
    pass

@event(QUANTUM, 'Connected')
@event(QUANTUM, 'Disconnected')
def quantum_conex_event(interface, state):
    """QUANTUM CONNECT() STATUS """
    print(str(interface) + ' Conex Event: ' + state)
    if state == 'Connected':
        BTN['LANVWall'].SetState(1)
        QUANTUM_DATA['ConexEvent'] = True
        ## Send & Query Information
        subscribe_quantum()
        update_quantum()
    if state == 'Disconnected':
        BTN['LANVWall'].SetState(0)
        QUANTUM_DATA['ConexEvent'] = False
        trying_quantum()
    pass

## This functions try to make a Connect()
## Help´s when the device was Off in the first Connect() method when the code starts
def trying_biamp():
    """Try to make a Connect() to device"""
    if BIAMP_DATA['ConexEvent'] == False:
        print('Tryng to make a Connect() in Biamp')
        BIAMP.Connect(4) ## Have 4 seconds to try to connect
        loop_trying_biamp.Restart()
    pass
loop_trying_biamp = Wait(5, trying_biamp)

def trying_quantum():
    """Try to make a Connect() to device"""
    if QUANTUM_DATA['ConexEvent'] == False:
        print('Tryng to make a Connect() in Quantum')
        QUANTUM.Connect(4) ## Have 4 seconds to try to connect
        loop_trying_quantum.Restart()
    pass
loop_trying_quantum = Wait(5, trying_quantum)

## RECURSIVE LOOP FUNCTIONS -----------------------------------------------------------
## This not affect any device
## This return True / False when no response is received from Mod
# ule
## If in 5 times the data is not reported (connectionCounter = 5) from the Update Command
## Generate 'Connected' / 'Disconnected'

def update_loop_biamp():
    """Continuos Update Commands to produce Module Connected / Disconnected"""
    BIAMP.Update('VerboseMode')
    loop_update_biamp.Restart()
loop_update_biamp = Wait(12, update_loop_biamp)

def update_loop_quantum():
    """Continuos Update Commands to produce Module Connected / Disconnected"""
    QUANTUM.Update('DeviceStatus')
    loop_update_quantum.Restart()
loop_update_quantum = Wait(12, update_loop_quantum)

def update_loop_denon():
    """Continuos Update Commands to produce Module Connected / Disconnected"""
    DENON.Update('PlaybackStatus')
    loop_update_denon.Restart()
loop_update_denon = Wait(12, update_loop_denon)

## DATA DICTIONARIES -----------------------------------------------------------
## Each dictionary store the real time information of room devices
## Data dictionaries - IP Devices
BIAMP_DATA = {
    'ConexModule': None,
    'ConexEvent' : None,
}
QUANTUM_DATA = {
    'ConexModule': None,
    'ConexEvent' : None,
}
## Data dictionaries - RS232 Devices
DENON_DATA = {
    'Conex'          : None,
    'Chapter'        : '',
    'DiscType'       : '',
    'PlaybackStatus' : '',
    'Power'          : None,
    'Title'          : '',
}

## PAGE USER EVENTS ------------------------------------------------------------
## Page Index ------------------------------------------------------------------
@event(BTN['Index'], 'Pressed')
def index_events(button, state):
    """User Actions: Touch Index Page"""

    TLP.HideAllPopups()
    TLP.ShowPage(PAGE['Main'])
    TLP.ShowPopup(POPUP['Hi'])
    print('Touch Mode: %s' % 'Index')
    pass

## Main Page -------------------------------------------------------------------
@event(BTNPAGE['Main'], BTNSTATE['List'])
def main_events(button, state):
    """User Actions: Touch Main Page"""

    if button is BTN['Video'] and state == 'Pressed':
        LBL['Master'].SetText('Proyección de Video')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup(POPUP['Video'])
        print('Touch Mode: %s' % 'VideoWall')

    elif button is BTN['Audio'] and state == 'Pressed':
        LBL['Master'].SetText('Selección de Audio')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup(POPUP['Audio'])
        print('Touch Mode: %s' % 'Audio')

    elif button is BTN['Bluray'] and state == 'Pressed':
        LBL['Master'].SetText('Control de BluRay')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup(POPUP['Bluray'])
        print('Touch Mode: %s' % 'BluRay')

    elif button is BTN['Status'] and state == 'Pressed':
        LBL['Master'].SetText('Información de dispositivos')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup(POPUP['Status'])
        print('Touch Mode: %s' % 'Status')

    elif button is BTN['Power'] and state == 'Pressed':
        LBL['Master'].SetText('Apagado del Sistema')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup(POPUP['Power'])
        print('Touch Mode: %s' % 'PowerOff')

    ##Turn On the feedbak of last pressed button
    BTNGROUP['Mode'].SetCurrent(button)
    pass

## Video Page ------------------------------------------------------------------
@event(BTNPAGE['VW'], BTNSTATE['List'])
def video_sources_events(button, state):
    """User Actions: Touch Video Page"""

    if button is BTN['VHDMI'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '1', {'Canvas':'1'})
        print("Videowall Full: %s" % 'HDMI')

    elif button is BTN['VPS4'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '2', {'Canvas':'1'})
        print("Videowall Full: %s" % 'PS4')

    elif button is BTN['VXbox'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '3', {'Canvas':'1'})
        print("Videowall Full: %s" % 'Xbox')

    elif button is BTN['VBluray'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '4', {'Canvas':'1'})
        print("Videowall Full: %s" % 'Bluray')

    elif button is BTN['VSky'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '5', {'Canvas':'1'})
        print("Videowall Full: %s" % 'Sky')

    elif button is BTN['VRoku'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '6', {'Canvas':'1'})
        print("Videowall Full: %s" % 'Roku')

    elif button is BTN['VPC'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '7', {'Canvas':'1'})
        print("Videowall Full: %s" % 'PC')

    elif button is BTN['VShare'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '8', {'Canvas':'1'})
        print("Videowall Full: %s" % 'Share')
    pass

@event(BTNPAGE['VWP'], BTNSTATE['List'])
def video_presets_events(button, state):
    """User Actions: Touch Video Presets Page"""

    if button is BTN['VP1'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '9', {'Canvas':'1'})
        print("Videowall Preset: %s" % '1')

    elif button is BTN['VP2'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '10', {'Canvas':'1'})
        print("Videowall Preset: %s" % '2')

    elif button is BTN['VP3'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '11', {'Canvas':'1'})
        print("Videowall Preset: %s" % '3')

    elif button is BTN['VP4'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '12', {'Canvas':'1'})
        print("Videowall Preset: %s" % '4')

    elif button is BTN['VP5'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '13', {'Canvas':'1'})
        print("Videowall Preset: %s" % '5')

    elif button is BTN['VP6'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '14', {'Canvas':'1'})
        print("Videowall Preset: %s" % '6')

    elif button is BTN['VP7'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '15', {'Canvas':'1'})
        print("Videowall Preset: %s" % '7')

    elif button is BTN['VP8'] and state == 'Pressed':
        QUANTUM.Set('PresetRecall', '16', {'Canvas':'1'})
        print("Videowall Preset: %s" % '8')
    pass

@event(BTNPAGE['VWPw'], BTNSTATE['List'])
def video_pwr_events(button, state):
    """User Actions: Touch Video Power Page"""

    if button is BTN['VWPwr1'] and state == 'Pressed':
        print("Videowall: %s" % 'PwrOn')

    elif button is BTN['VWPwr0'] and state == 'Pressed':
        print("Videowall: %s" % 'PwrOff')
    pass

## Audio Page ------------------------------------------------------------------
@event(BTNPAGE['Set'], BTNSTATE['List'])
def audio_set_events(button, state):
    """User Actions: Touch Audio Set Choice Page"""

    if button is BTN['SetA'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['AudioA'])
        print("Audio Set: %s" % 'A')

    elif button is BTN['SetB'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['AudioB'])
        print("Audio Set: %s" % 'B')

    elif button is BTN['SetC'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['AudioC'])
        print("Audio Set: %s" % 'C')

    elif button is BTN['SetD'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['AudioD'])
        print("Audio Set: %s" % 'D')

    elif button is BTN['SetE'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['AudioE'])
        print("Audio Set: %s" % 'E')

    ##Turn On the feedbak of last pressed button
    BTNGROUP['Set'].SetCurrent(button)
    pass

@event(BTNPAGE['SetA'], BTNSTATE['List'])
def audio_a_events(button, state):
    """User Actions: Touch Audio Set A Page"""

    if button is BTN['A_HDMI'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '1', {'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A', 'HDMI'))

    elif button is BTN['A_PS4'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '2', {'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A', 'PS4'))

    elif button is BTN['A_Xbox'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '3', {'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A', 'Xbox'))

    elif button is BTN['A_Bluray'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '4', {'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A', 'Bluray'))

    elif button is BTN['A_Sky'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '5', {'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A', 'Sky'))

    elif button is BTN['A_Roku'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '6', {'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A', 'Roku'))

    elif button is BTN['A_PC'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '7', {'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A', 'PC'))

    elif button is BTN['A_Share'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '8', {'Instance Tag':'SelectorA'})
        print("Audio on Set %s: %s" % ('A', 'Share'))
    pass

@event(BTNPAGE['SetB'], BTNSTATE['List'])
def audio_b_events(button, state):
    """User Actions: Touch Audio Set B Page"""

    if button is BTN['B_HDMI'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '1', {'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B', 'HDMI'))

    elif button is BTN['B_PS4'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '2', {'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B', 'PS4'))

    elif button is BTN['B_Xbox'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '3', {'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B', 'Xbox'))

    elif button is BTN['B_Bluray'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '4', {'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B', 'Bluray'))

    elif button is BTN['B_Sky'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '5', {'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B', 'Sky'))

    elif button is BTN['B_Roku'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '6', {'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B', 'Roku'))

    elif button is BTN['B_PC'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '7', {'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B', 'PC'))

    elif button is BTN['B_Share'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '8', {'Instance Tag':'SelectorB'})
        print("Audio on Set %s: %s" % ('B', 'Share'))
    pass

@event(BTNPAGE['SetC'], BTNSTATE['List'])
def audio_c_events(button, state):
    """User Actions: Touch Audio Set C Page"""

    if button is BTN['C_HDMI'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '1', {'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C', 'HDMI'))

    elif button is BTN['C_PS4'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '2', {'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C', 'PS4'))

    elif button is BTN['C_Xbox'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '3', {'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C', 'Xbox'))

    elif button is BTN['C_Bluray'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '4', {'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C', 'Bluray'))

    elif button is BTN['C_Sky'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '5', {'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C', 'Sky'))

    elif button is BTN['C_Roku'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '6', {'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C', 'Roku'))

    elif button is BTN['C_PC'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '7', {'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C', 'PC'))

    elif button is BTN['C_Share'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '8', {'Instance Tag':'SelectorC'})
        print("Audio on Set %s: %s" % ('C', 'Share'))
    pass

@event(BTNPAGE['SetD'], BTNSTATE['List'])
def audio_d_events(button, state):
    """User Actions: Touch Audio Set D Page"""

    if button is BTN['D_HDMI'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '1', {'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D', 'HDMI'))

    elif button is BTN['D_PS4'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '2', {'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D', 'PS4'))

    elif button is BTN['D_Xbox'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '3', {'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D', 'Xbox'))

    elif button is BTN['D_Bluray'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '4', {'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D', 'Bluray'))

    elif button is BTN['D_Sky'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '5', {'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D', 'Sky'))

    elif button is BTN['D_Roku'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '6', {'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D', 'Roku'))

    elif button is BTN['D_PC'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '7', {'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D', 'PC'))

    elif button is BTN['D_Share'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '8', {'Instance Tag':'SelectorD'})
        print("Audio on Set %s: %s" % ('D', 'Share'))
    pass

@event(BTNPAGE['SetE'], BTNSTATE['List'])
def audio_e_events(button, state):
    """User Actions: Touch Audio Set E Page"""

    if button is BTN['E_HDMI'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '1', {'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E', 'HDMI'))

    elif button is BTN['E_PS4'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '2', {'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E', 'PS4'))

    elif button is BTN['E_Xbox'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '3', {'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E', 'Xbox'))

    elif button is BTN['E_Bluray'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '4', {'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E', 'Bluray'))

    elif button is BTN['E_Sky'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '5', {'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E', 'Sky'))

    elif button is BTN['E_Roku'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '6', {'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E', 'Roku'))

    elif button is BTN['E_PC'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '7', {'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E', 'PC'))

    elif button is BTN['E_Share'] and state == 'Pressed':
        BIAMP.Set('SourceSelectorSourceSelection', '8', {'Instance Tag':'SelectorE'})
        print("Audio on Set %s: %s" % ('E', 'Share'))
    pass

## Bluray Page -----------------------------------------------------------------
@event(BTNPAGE['BRN'], BTNSTATE['List'])
def br_navigation_events(button, state):
    """User Actions: Touch BluRay Navigation Page"""

    if button is BTN['BRUp'] and state == 'Pressed':
        DENON.Set('MenuNavigation', 'Up')
        print("BluRay Pressed: %s" % 'Up')

    elif button is BTN['BRLeft'] and state == 'Pressed':
        DENON.Set('MenuNavigation', 'Left')
        print("BluRay Pressed: %s" % 'Left')

    elif button is BTN['BRDown'] and state == 'Pressed':
        DENON.Set('MenuNavigation', 'Down')
        print("BluRay Pressed: %s" % 'Down')

    elif button is BTN['BRRight'] and state == 'Pressed':
        DENON.Set('MenuNavigation', 'Right')
        print("BluRay Pressed: %s" % 'Right')

    elif button is BTN['BREnter'] and state == 'Pressed':
        DENON.Set('MenuNavigation', 'Enter')
        print("BluRay Pressed: %s" % 'Enter')
    pass

@event(BTNPAGE['BRO'], BTNSTATE['List'])
def br_option_events(button, state):
    """User Actions: Touch BluRay Options Page"""

    if button is BTN['BRPopup'] and state == 'Pressed':
        DENON.Set('MenuNavigation', 'Menu')
        BTN['BRPopup'].SetState(1)
        print("BluRay Pressed: %s" % 'Menu')
    else:
        BTN['BRPopup'].SetState(0)

    if button is BTN['BRSetup'] and state == 'Pressed':
        DENON.Set('Function', 'Setup')
        BTN['BRSetup'].SetState(1)
        print("BluRay Pressed: %s" % 'Title')
    else:
        BTN['BRSetup'].SetState(0)

    if button is BTN['BRInfo'] and state == 'Pressed':
        DENON.Set('Function', 'Display')
        BTN['BRInfo'].SetState(1)
        print("BluRay Pressed: %s" % 'Info')
    else:
        BTN['BRInfo'].SetState(0)

    if button is BTN['BRReturn'] and state == 'Pressed':
        DENON.Set('MenuNavigation', 'Return')
        BTN['BRReturn'].SetState(1)
        print("BluRay Pressed: %s" % 'Return')
    else:
        BTN['BRReturn'].SetState(0)

    if button is BTN['BRTray'] and state == 'Pressed':
        DENON.Set('Transport', 'Eject')
        print("BluRay Pressed: %s" % 'Tray')

    if button is BTN['BRPower'] and state == 'Pressed':
        print("BluRay Pressed: %s" % 'Power')
        if DENON_DATA['Power'] == True:
            DENON.Set('Power', 'Off')
        elif DENON_DATA['Power'] == False:
            DENON.Set('Power', 'On')
    pass

@event(BTNPAGE['BRP'], BTNSTATE['List'])
def br_play_events(button, state):
    """User Actions: Touch BluRay Playback Page"""

    if button is BTN['BRPrev'] and state == 'Pressed':
        DENON.Set('Transport', 'Previous')
        BTN['BRPrev'].SetState(1)
        print("BluRay Pressed: %s" % 'Prev')
    else:
        BTN['BRPrev'].SetState(0)

    if button is BTN['BRBack'] and state == 'Pressed':
        DENON.Set('Transport', 'Rew')
        print("BluRay Pressed: %s" % 'Back')

    if button is BTN['BRPause'] and state == 'Pressed':
        DENON.Set('Transport', 'Pause')
        print("BluRay Pressed: %s" % 'Pause')

    if button is BTN['BRPlay'] and state == 'Pressed':
        DENON.Set('Transport', 'Play')
        print("BluRay Pressed: %s" % 'Play')

    if button is BTN['BRStop'] and state == 'Pressed':
        DENON.Set('Transport', 'Stop')
        print("BluRay Pressed: %s" % 'Stop')

    if button is BTN['BRRewi'] and state == 'Pressed':
        DENON.Set('Transport', 'FFwd')
        print("BluRay Pressed: %s" % 'Rewind')

    if button is BTN['BRNext'] and state == 'Pressed':
        DENON.Set('Transport', 'Next')
        BTN['BRNext'].SetState(1)
        print("BluRay Pressed: %s" % 'Next')
    else:
        BTN['BRNext'].SetState(0)

    pass

## Status Page -----------------------------------------------------------------

## Power Page ------------------------------------------------------------------
@event(BTN['PowerAll'], BTNSTATE['List'])
def power_events(button, state):
    """User Actions: Touch PowerOff Page"""

    global PWRCOUNT
    ## If the user press the Power Button:
    ## Only Turn On the first state of button - Does not do any action
    if state == 'Pressed':
        BTN['PowerAll'].SetState(1)
        print('Button Pressed: %s' % 'PowerAll')

    ## If the user holds down the button:
    ## A variable is Decremented from 4 to 0 seconds
    ## In each new value, Turn On each visual state of the Power Button
    ## Whne the value is equal to 0, ShutDown all devices in the System
    elif state == 'Repeated':
        PWRCOUNT = PWRCOUNT - 1
        BTN['PowerAll'].SetState(PWRCOUNT)
        LBL['CountAll'].SetText(str(PWRCOUNT))
        print('Button Repeated: %s' % 'PowerAll')
        ## SHUTDOWN ALL DEVICES
        if PWRCOUNT == 0:
            TLP.ShowPage(PAGE['Index'])

    ## If the user release the Button:
    ## Clean the counter power data in GUI and delete the visual feedback
    elif state == 'Released':
        PWRCOUNT = 4
        BTN['PowerAll'].SetState(0)
        LBL['CountAll'].SetText('')
        print('Button Released: %s' % 'PowerAll')
    pass

## End Events Definitions-------------------------------------------------------
initialize()
