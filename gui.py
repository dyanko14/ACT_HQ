""" --------------------------------------------------------------------------
 Business   | Asesores y Consultores en Tecnología S.A. de C.V.
 Programmer | Dyanko Cisneros Mendoza
 Customer   | Human Quality
 Project    | VideoWall Room
 Version    | 0.1 --------------------------------------------------------- """

## CONTROL SCRIPT IMPORT -------------------------------------------------------
from extronlib.device import UIDevice
from extronlib.ui import Button, Label
from extronlib.system import MESet

# UI Device
TLP = UIDevice('TouchPanel')

# UI Buttons
BTN = {
    ## Index
    'Index'   : Button(TLP, 1),
    ## Main
    'Video'   : Button(TLP, 2),
    'Audio'   : Button(TLP, 3),
    'Bluray'  : Button(TLP, 4),
    'Status'  : Button(TLP, 5),
    'Power'   : Button(TLP, 6),
    ## Video Full
    'VHDMI'   : Button(TLP, 11),
    'VPS4'    : Button(TLP, 12),
    'VXbox'   : Button(TLP, 13),
    'VBluray' : Button(TLP, 14),
    'VSky'    : Button(TLP, 15),
    'VRoku'   : Button(TLP, 16),
    'VPC'     : Button(TLP, 17),
    'VShare'  : Button(TLP, 18),
    ## Video Presets
    'VP1'     : Button(TLP, 21),
    'VP2'     : Button(TLP, 22),
    'VP3'     : Button(TLP, 23),
    'VP4'     : Button(TLP, 24),
    'VP5'     : Button(TLP, 25),
    'VP6'     : Button(TLP, 26),
    'VP7'     : Button(TLP, 27),
    'VP8'     : Button(TLP, 28),
    ## Video Power
    'VWPwr1'  : Button(TLP, 30),
    'VWPwr0'  : Button(TLP, 31),
    ## Audio Set
    'SetA'    : Button(TLP, 41),
    'SetB'    : Button(TLP, 42),
    'SetC'    : Button(TLP, 43),
    'SetD'    : Button(TLP, 44),
    'SetE'    : Button(TLP, 45),
    ## Audio Set A
    'A_HDMI'  : Button(TLP, 61),
    'A_PS4'   : Button(TLP, 62),
    'A_Xbox'  : Button(TLP, 63),
    'A_Bluray': Button(TLP, 64),
    'A_Sky'   : Button(TLP, 65),
    'A_Roku'  : Button(TLP, 66),
    'A_PC'    : Button(TLP, 67),
    'A_Share' : Button(TLP, 68),
    ## Audio Set B
    'B_HDMI'  : Button(TLP, 71),
    'B_PS4'   : Button(TLP, 72),
    'B_Xbox'  : Button(TLP, 73),
    'B_Bluray': Button(TLP, 74),
    'B_Sky'   : Button(TLP, 75),
    'B_Roku'  : Button(TLP, 76),
    'B_PC'    : Button(TLP, 77),
    'B_Share' : Button(TLP, 78),
    ## Audio Set C
    'C_HDMI'  : Button(TLP, 81),
    'C_PS4'   : Button(TLP, 82),
    'C_Xbox'  : Button(TLP, 83),
    'C_Bluray': Button(TLP, 84),
    'C_Sky'   : Button(TLP, 85),
    'C_Roku'  : Button(TLP, 86),
    'C_PC'    : Button(TLP, 87),
    'C_Share' : Button(TLP, 88),
    ## Audio Set D
    'D_HDMI'  : Button(TLP, 91),
    'D_PS4'   : Button(TLP, 92),
    'D_Xbox'  : Button(TLP, 93),
    'D_Bluray': Button(TLP, 94),
    'D_Sky'   : Button(TLP, 95),
    'D_Roku'  : Button(TLP, 96),
    'D_PC'    : Button(TLP, 97),
    'D_Share' : Button(TLP, 98),
    ## Audio Set E
    'E_HDMI'  : Button(TLP, 101),
    'E_PS4'   : Button(TLP, 102),
    'E_Xbox'  : Button(TLP, 103),
    'E_Bluray': Button(TLP, 104),
    'E_Sky'   : Button(TLP, 105),
    'E_Roku'  : Button(TLP, 106),
    'E_PC'    : Button(TLP, 107),
    'E_Share' : Button(TLP, 108),
    ## Bluray Play
    'BRPrev'  : Button(TLP, 131),
    'BRBack'  : Button(TLP, 132),
    'BRPause' : Button(TLP, 133),
    'BRPlay'  : Button(TLP, 134),
    'BRStop'  : Button(TLP, 135),
    'BRRewi'  : Button(TLP, 136),
    'BRNext'  : Button(TLP, 137),
    ## Bluray Navigation
    'BRUp'    : Button(TLP, 138),
    'BRLeft'  : Button(TLP, 139),
    'BRDown'  : Button(TLP, 140),
    'BRRight' : Button(TLP, 141),
    'BREnter' : Button(TLP, 142),
    ## Bluray Options
    'BRPopup' : Button(TLP, 143),
    'BRSetup' : Button(TLP, 144),
    'BRInfo'  : Button(TLP, 145),
    'BRReturn': Button(TLP, 146),
    'BRTray'  : Button(TLP, 148),
    'BRPower' : Button(TLP, 150),
    ## Status
    'LANBiamp': Button(TLP, 201),
    'LANVWall': Button(TLP, 202),
    'LANIPCP' : Button(TLP, 203),
    '232Denon': Button(TLP, 204),
    ## PowerOff
    'PowerAll': Button(TLP, 220, repeatTime=1),
}

# UI Page Buttons
BTNPAGE = {
    'Main': [BTN['Video'], BTN['Audio'], BTN['Bluray'], BTN['Status'], BTN['Power']],

    'VW'  : [BTN['VHDMI'], BTN['VPS4'], BTN['VXbox'], BTN['VBluray'],
             BTN['VSky'], BTN['VRoku'], BTN['VPC'], BTN['VShare']],

    'VWP' : [BTN['VP1'], BTN['VP2'], BTN['VP3'], BTN['VP4'],
             BTN['VP5'], BTN['VP6'], BTN['VP7'], BTN['VP8']],

    'VWPw': [BTN['VWPwr1'], BTN['VWPwr0']],

    'Set' : [BTN['SetA'], BTN['SetB'], BTN['SetC'], BTN['SetD'], BTN['SetE']],

    'SetA': [BTN['A_HDMI'], BTN['A_PS4'], BTN['A_Xbox'], BTN['A_Bluray'],
             BTN['A_Sky'], BTN['A_Roku'], BTN['A_PC'], BTN['A_Share']],

    'SetB': [BTN['B_HDMI'], BTN['B_PS4'], BTN['B_Xbox'], BTN['B_Bluray'],
             BTN['B_Sky'], BTN['B_Roku'], BTN['B_PC'], BTN['B_Share']],

    'SetC': [BTN['C_HDMI'], BTN['C_PS4'], BTN['C_Xbox'], BTN['C_Bluray'],
             BTN['C_Sky'], BTN['C_Roku'], BTN['C_PC'], BTN['C_Share']],

    'SetD': [BTN['D_HDMI'], BTN['D_PS4'], BTN['D_Xbox'], BTN['D_Bluray'],
             BTN['D_Sky'], BTN['D_Roku'], BTN['D_PC'], BTN['D_Share']],

    'SetE': [BTN['E_HDMI'], BTN['E_PS4'], BTN['E_Xbox'], BTN['E_Bluray'],
             BTN['E_Sky'], BTN['E_Roku'], BTN['E_PC'], BTN['E_Share']],

    'BRN' : [BTN['BRUp'], BTN['BRLeft'], BTN['BRDown'], BTN['BRRight'], BTN['BREnter']],

    'BRO' : [BTN['BRPopup'], BTN['BRSetup'], BTN['BRInfo'], BTN['BRReturn'],
             BTN['BRTray'], BTN['BRPower']],

    'BRP' : [BTN['BRPrev'], BTN['BRBack'], BTN['BRPause'], BTN['BRPlay'],
             BTN['BRStop'], BTN['BRRewi'], BTN['BRNext']],
}

# UI Group Page Buttons
BTNGROUP = {
    'Mode': MESet(BTNPAGE['Main']),

    'Set' : MESet(BTNPAGE['Set']),

    'SetA': MESet(BTNPAGE['SetA']),

    'SetB': MESet(BTNPAGE['SetB']),

    'SetC': MESet(BTNPAGE['SetC']),

    'SetD': MESet(BTNPAGE['SetD']),

    'SetE': MESet(BTNPAGE['SetE']),

    'BR'  : MESet(BTNPAGE['BRP']),
}

# UI Button states
BTNSTATE = {
    'List' : ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
}

# UI Labels
LBL = {
    'Master': Label(TLP, 300),
    ## Audio
    'SetA'  : Label(TLP, 51),
    'SetB'  : Label(TLP, 52),
    'SetC'  : Label(TLP, 53),
    'SetD'  : Label(TLP, 54),
    'SetE'  : Label(TLP, 55),
    ## BluRay
    'Bluray': Label(TLP, 151),
    ## Power
    'AllOff'   : Label(TLP, 221),
    'CountAll' : Label(TLP, 222),
}

POPUP = {
    'Index'  : 'Index',
    'Main'   : 'Main',
    'Video'  : 'VWall',
    'Audio'  : 'Audios',
    'AudioA' : 'Audio_Sources_A',
    'AudioB' : 'Audio_Sources_B',
    'AudioC' : 'Audio_Sources_C',
    'AudioD' : 'Audio_Sources_D',
    'AudioE' : 'Audio_Sources_E',
    'Bluray' : 'BR',
    'Status' : 'Status',
    'Hi'     : 'Welcome',
    'Power'  : 'x_PowerOff',
}

PAGE = {
    'Index'  : 'Index',
    'Main'   : 'Main',
}
