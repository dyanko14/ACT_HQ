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
from gui import TLP, Btn, Btn_Page, Btn_Group, Lbl
## End ControlScript Import ----------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------
IPCP = ProcessorDevice('IPlink')
## End Device/Processor Definition ---------------------------------------------

## Begin User Import -----------------------------------------------------------
## Instances of Python Extron modules------------------
## Ethernet:
import biam_dsp_TesiraSeries_v1_5_19_0    as DeviceA
import extr_sp_Quantum_Ultra610_v1_0_1_0  as DeviceB
## RS-232
import deno_dvd_DBT3313UD_Series_v1_0_2_0 as DeviceC
## IR/Serial-controlled Modules declared:
## Ethernet:
Biamp   = DeviceA.EthernetClass('192.168.10.150', 23, Model='TesiraFORTE CI')
Quantum = DeviceB.EthernetClass('10.10.10.12', 23, Model='Quantum Ultra 610')
## RS-232:
Denon   = DeviceC.SerialClass(IPCP, 'COM1', Baud=9600, Model='DBT-3313UD')
## End User Import -------------------------------------------------------------
## Begin Communication Interface Definition ------------------------------------
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
    PwrCount = 4
    
    ## TouchPanel Functions
    Btn_Group['Mode'].SetCurrent(None)
    TLP.HidePopupGroup(2)
    TLP.ShowPage('Index')
    TLP.ShowPopup('Welcome')
    
    ## Notify to Console
    print("System Initialize")
    pass

## Page Index ------------------------------------------------------------------
@event(Btn['Index'], 'Pressed')
def IndexEvents(button, state):
    TLP.HideAllPopups()
    TLP.ShowPage('Main')
    TLP.ShowPopup('Welcome')
    print('Touch Mode: %s' % 'Index')
    pass

## Main Page -------------------------------------------------------------------
@event(Btn_Page['Main'], ButtonEventList)
def MainEvents(button, state):

    if button is Btn['Video'] and state == 'Pressed':
        Lbl['Master'].SetText('Proyección de Video')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('VWall')
        print('Touch Mode: %s' % 'VideoWall')

    elif button is Btn['Audio'] and state == 'Pressed':
        Lbl['Master'].SetText('Selección de Audio')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('Audios')
        print('Touch Mode: %s' % 'Audio')

    elif button is Btn['Bluray'] and state == 'Pressed':
        Lbl['Master'].SetText('Control de BluRay')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('BR')
        print('Touch Mode: %s' % 'BluRay')

    elif button is Btn['Status'] and state == 'Pressed':
        Lbl['Master'].SetText('Información de dispositivos')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('Status')
        print('Touch Mode: %s' % 'Status')

    elif button is Btn['Power'] and state == 'Pressed':
        Lbl['Master'].SetText('Apagado del Sistema')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('x_PowerOff')
        print('Touch Mode: %s' % 'PowerOff')

    ##Turn On the feedbak of last pressed button
    Btn_Group['Mode'].SetCurrent(button)
    pass

## Video Page ------------------------------------------------------------------
@event(Btn_Page['VW'], ButtonEventList)
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

@event(Btn_Page['VWP'], ButtonEventList)
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

@event(Btn_Page['VWPw'], ButtonEventList)
def VideoPwrEvents(button, state):
    
    if button is Btn['VWPwr1'] and state == 'Pressed':
        print("Videowall: %s" % 'PwrOn')
    
    elif button is Btn['VWPwr0'] and state == 'Pressed':
        print("Videowall: %s" % 'PwrOff')
    pass

## Audio Page ------------------------------------------------------------------
@event(Btn_Page['Set'], ButtonEventList)
def AudioSetEvents(button, state):
    
    if button is Btn['SetA'] and state == 'Pressed':
        TLP.ShowPopup('Audio_Sources_A')
        print("Audio Set: %s" % 'A')
    
    elif button is Btn['SetB'] and state == 'Pressed':
        TLP.ShowPopup('Audio_Sources_B')
        print("Audio Set: %s" % 'B')
    
    elif button is Btn['SetC'] and state == 'Pressed':
        TLP.ShowPopup('Audio_Sources_C')
        print("Audio Set: %s" % 'C')
    
    elif button is Btn['SetD'] and state == 'Pressed':
        TLP.ShowPopup('Audio_Sources_D')
        print("Audio Set: %s" % 'D')
    
    elif button is Btn['SetE'] and state == 'Pressed':
        TLP.ShowPopup('Audio_Sources_E')
        print("Audio Set: %s" % 'E')
    
    ##Turn On the feedbak of last pressed button
    Btn_Group['Set'].SetCurrent(button)
    pass

@event(Btn_Page['SetA'], ButtonEventList)
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

@event(Btn_Page['SetB'], ButtonEventList)
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
    
@event(Btn_Page['SetC'], ButtonEventList)
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

@event(Btn_Page['SetD'], ButtonEventList)
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

@event(Btn_Page['SetE'], ButtonEventList)
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
@event(Btn_Page['BRN'], ButtonEventList)
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

@event(Btn_Page['BRO'], ButtonEventList)
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
        if Denon_Data['Power'] == 'On':
            Denon.Set('Power','Off')
        elif Denon_Data['Power'] == 'Off':
            Denon.Set('Power','On')
    pass
    
@event(Btn_Page['BRP'], ButtonEventList)
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
@event(Btn['PowerAll'], ButtonEventList)
def PowerEvents(button, state):   
    global PwrCount
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
        PwrCount = PwrCount - 1
        Btn['PowerAll'].SetState(PwrCount)
        Lbl['CountAll'].SetText(str(PwrCount))
        print('Button Repeated: %s' % 'PowerAll')
        ## Shutdown routine
        if PwrCount == 0:
            TLP.ShowPage('Index')
    ## If the user release the Button:
    ## Clean the counter power data in GUI and delete the visual feedback
    elif state == 'Released':
        PwrCount = 4
        Btn['PowerAll'].SetState(0)
        Lbl['CountAll'].SetText('')
        print('Button Released: %s' % 'PowerAll')
    pass

## End Events Definitions-------------------------------------------------------
Initialize()