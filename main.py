## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface,
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface,
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait
## End ControlScript Import ----------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------
IPCP    = ProcessorDevice('IPlink')
TLP     = UIDevice('TouchPanel')
#--
LCDs    = SerialInterface(IPCP, 'COM2', Baud=9600, Data=8, Parity='None',
                          Stop=1, FlowControl='Off', CharDelay=0, Mode='RS232')
#--
Quantum = EthernetClientInterface('192.168.10.152', 23, 'TCP')
Tesira  = EthernetClientInterface('192.168.10.150', 22, 'SSH',
                                   Credentials=('default', ''))
##
## End Device/Processor Definition ---------------------------------------------
##
## Begin User Import -----------------------------------------------------------
from Audio import AudioControl
from Video import VideoControl
from Bluray import BlurayControl
import deno_dvd_DBT3313UD_Series_v1_0_2_0 as DenonSerial
Denon = DenonSerial.SerialClass(IPCP, 'COM1', Baud=9600, Model='DBT-3313UD')
## End User Import -------------------------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------
BtnIndex    = Button(TLP, 1)
## Mode of Main Operation----
BtnVideo    = Button(TLP, 2)
BtnAudio    = Button(TLP, 3)
BtnBluRay   = Button(TLP, 4)
BtnStatus   = Button(TLP, 5)
BtnPowerOff = Button(TLP, 6)
## -------------------------
LblMaster   = Label(TLP, 300)
## Mode of Device Status-----

BtnLANVWall = Button(TLP, 202)
BtnLANIPCP  = Button(TLP, 203)

## Mode of Device Shutdown----
BtnAllOff   = Button(TLP, 220, holdTime = 3)
LblAllOff   = Label(TLP, 221)
## Group Buttons Operation------
PageMain    = [BtnVideo, BtnAudio, BtnBluRay, BtnStatus, BtnPowerOff]
## -----------
GroupModes  = MESet([BtnIndex, BtnVideo, BtnAudio, BtnBluRay, BtnStatus, BtnPowerOff])
## Group Buttons Status
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
## End Device/User Interface Definition ----------------------------------------
##
## Begin Communication Interface Definition ------------------------------------
## End Communication Interface Definition --------------------------------------
def Initialize():
    print(ProgramInfo)
    print("System Initialize")
    pass

## Event Definitions -----------------------------------------------------------
# Index Page -------------------------------------------------------------------
@event(BtnIndex, 'Pressed')
def ButtonObjectPressed(button, state):
    TLP.ShowPage('Main')
    pass

# Main Page --------------------------------------------------------------------
@event(PageMain, ButtonEventList)
def GroupModeHandler(button, state):
    #--
    GroupModes.SetCurrent(button)
    #--
    if button is BtnVideo and state == 'Pressed':
        LblMaster.SetText('Proyección de Video')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('VWall')
        print('Touch Mode: %s' % ('VideoWall'))
    #--
    elif button is BtnAudio and state == 'Pressed':
        LblMaster.SetText('Selección de Audio')
        TLP.ShowPopup('Audios')
        print('Touch Mode: %s' % ('Audio'))
    #--
    elif button is BtnBluRay and state == 'Pressed':
        #Denon.ReadStatus('Power')
        #Denon.ReadStatus('PlaybackStatus')
        #Denon.ReadStatus('CurrentChapterTrackNum')
        #Denon.ReadStatus('DiscTypeStatus')
        #--
        LblMaster.SetText('Control de BluRay')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('BR')
        print('Touch Mode: %s' % ('Bluray'))
    #--
    elif button is BtnStatus and state == 'Pressed':
        #Denon.ReadStatus('ConnectionStatus')
        #--
        LblMaster.SetText('Información de dispositivos')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('Status')
        print('Touch Mode: %s' % ('Status'))
    #--
    elif button is BtnPowerOff and state == 'Pressed':
        LblMaster.SetText('Apagado del Sistema')
        TLP.HidePopupGroup(2)
        TLP.ShowPopup('x_PowerOff')
        print('Touch Mode: %s' % ('PowerOff'))
    #--
    pass

# Power Page -------------------------------------------------------------------
@event(BtnAllOff, ButtonEventList)
def PowerSystemHandler(button, state):
    if state == 'Pressed':
        print("Button PowerOff Pressed")
    if state == 'Held':       
        Denon.Set('Power','Off')
        TLP.ShowPage('Index')
        print("Power System Held")
    pass

## End Events Definitions-------------------------------------------------------
ProgramInfo = '''
 Programer:  | Dyanko Cisneros Mendoza
 Business:   | GrupoACT
 Customer    | Human Quality Mty N.L.
 ----------  | -----------------------
 Library V:  | {0}
 Processor:  | {1}
 * PN:       | {2}
 * IP:       | {3}
 * MAC:      | {4}
 * Firmware: | {5}
 * SN:       | {6}
 * Memory:   | {7} Kbytes
'''.format(
    Version(),
    IPCP.ModelName,
    IPCP.PartNumber,
    IPCP.IPAddress,
    IPCP.MACAddress,
    IPCP.FirmwareVersion,
    IPCP.SerialNumber,
    IPCP.UserUsage)
    
## Begin SMD Popup ControlScript >>---------------------------------------------
AudioControl(IPCP, TLP, Tesira)
VideoControl(IPCP, TLP, Quantum)
BlurayControl(IPCP, TLP, Denon)

Initialize()