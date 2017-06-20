from extronlib.interface import SerialInterface, EthernetClientInterface
from re import compile, search
from extronlib.system import Wait, ProgramLog


class DeviceClass:

    def __init__(self):

        self.Unidirectional = 'False'
        self.connectionCounter = 15
        self.DefaultResponseTimeout = 0.3
        self._compile_list = {}
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self._ReceiveBuffer = b''
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Debug = False
        self.Models = {}

        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'DeviceStatus': {'Status': {}},
            'Input': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'PresetRecall': {'Parameters': ['Canvas'], 'Status': {}},
            'PresetSave': {'Parameters': ['Canvas'], 'Status': {}},
            'WindowBorderStyle': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'WindowHorizontalShift': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'WindowHorizontalShiftStatus': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'WindowHorizontalSize': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'WindowHorizontalSizeStatus': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'WindowMute': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'WindowPriority': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'WindowPriorityStatus': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'WindowVerticalShift': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'WindowVerticalShiftStatus': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'WindowVerticalSize': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
            'WindowVerticalSizeStatus': {'Parameters': ['Window', 'Canvas'], 'Status': {}},
        }

        self.VerboseDisabled = True
        self.PasswdPromptCount = 0
        self.Authenticated = 'Not Needed'
        self.devicePassword = None

        if self.Unidirectional == 'False':
            self.AddMatchString(compile(b'(FAIL POWER|FAIL FAN)'), self.__MatchDeviceStatus, None)
            self.AddMatchString(compile(b'Grp([0-9]{2}) Win([0-9]{3}) In([0-9]{4})\r\n'), self.__MatchInput, None)
            self.AddMatchString(compile(b'WndwB([0-9]{2})\*([0-9]{3})\*([0-9]{3})\r\n'), self.__MatchWindowBorderStyle, None)
            self.AddMatchString(compile(b'HctrW([0-9]{2})\*([0-9]{3})\*([+-][0-9]{6})\r\n'), self.__MatchWindowHorizontalShiftStatus, None)
            self.AddMatchString(compile(b'HsizW([0-9]{2})\*([0-9]{3})\*([0-9]{6})\r\n'), self.__MatchWindowHorizontalSizeStatus, None)
            self.AddMatchString(compile(b'Vmt([0-9]{2})\*([0-9]{3})\*([0-1])\r\n'), self.__MatchWindowMute, None)
            self.AddMatchString(compile(b'WndwP([0-9]{2})\*([0-9]{3})\*([0-9]{1,3})\r\n'), self.__MatchWindowPriorityStatus, None)
            self.AddMatchString(compile(b'VctrW([0-9]{2})\*([0-9]{3})\*([+-][0-9]{6})\r\n'), self.__MatchWindowVerticalShiftStatus, None)
            self.AddMatchString(compile(b'VsizW([0-9]{2})\*([0-9]{3})\*([0-9]{6})\r\n'), self.__MatchWindowVerticalSizeStatus, None)

            self.AddMatchString(compile(b'E([0-3][0-9])\r\n'), self.__MatchErrors, None)

            self.AddMatchString(compile(b'Vrb3\r\n'), self.__MatchVerboseMode, None)

            if self.ConnectionType != 'Serial':
                self.AddMatchString(compile(b'Password:'), self.__MatchPassword, None)
                self.AddMatchString(compile(b'Login Administrator\r\n'), self.__MatchLoginAdmin, None)
                self.AddMatchString(compile(b'Login User\r\n'), self.__MatchLoginUser, None)

        self.lastHDCPSignalStatusUpdate = 0
        self.lastResolutionStatusUpdate = 0

    def SetPassword(self, value, qualifier):
        if self.devicePassword is not None:
            self.Send('{0}\r\n'.format(self.devicePassword))
        else:
            self.MissingCredentialsLog('Password')

    def __MatchPassword(self, match, tag):
        self.PasswdPromptCount += 1
        if self.PasswdPromptCount > 1:
            print('Log in failed. Please supply proper Admin password')
            self.Authenticated = 'None'
        else:
            self.SetPassword(None, None)

    def __MatchLoginAdmin(self, match, tag):

        self.Authenticated = 'Admin'
        self.PasswdPromptCount = 0

    def __MatchLoginUser(self, match, tag):

        self.Authenticated = 'User'
        self.PasswdPromptCount = 0
        print('Logged in as User. May have limited functionality.')

    def __MatchVerboseMode(self, match, qualifier):
        self.OnConnected()
        self.VerboseDisabled = False

    def __MatchDeviceStatus(self, match, tag):

        ValueStateValues = {
            'FAIL FAN': 'Chassis Fan Failure',
            'FAIL POWER': 'Power Supply Failure'
        }
        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('DeviceStatus', value, None)

    def SetInput(self, value, qualifier):

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])

        if 1 <= Window <= 999 and 1 <= int(value) <= 9999 and 1 <= Canvas <= 10:
            self.__SetHelper('Input', '{0}*{1}*{2}!'.format(Canvas, Window, value), value, qualifier)
        else:
            print('Invalid Command for SetInput')

    def UpdateInput(self, value, qualifier):

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])
        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__UpdateHelper('Input', '{0}*{1}!'.format(Canvas, Window), value, qualifier)
        else:
            print('Invalid Command for UpdateInput')

    def __MatchInput(self, match, qualifier):

        Canvas = str(int(match.group(1).decode()))
        Window = int(match.group(2).decode())
        value = int(match.group(3).decode())

        self.WriteStatus('Input', value, {'Canvas': Canvas, 'Window': Window})

    def SetPresetRecall(self, value, qualifier):

        window = qualifier['Canvas']
        if 1 <= int(window) <= 10 and 1 <= int(value) <= 128:
            self.__SetHelper('PresetRecall', '1*{0}*{1}.'.format(window, value), value, qualifier)
        else:
            print('Invalid Command for SetPresetRecall')

    def SetPresetSave(self, value, qualifier):

        window = qualifier['Canvas']
        if 1 <= int(window) <= 10 and 1 <= int(value) <= 128:
            self.__SetHelper('PresetSave', '1*{0}*{1},'.format(window, value), value, qualifier)
        else:
            print('Invalid Command for SetPresetSave')

    def SetWindowHorizontalShift(self, value, qualifier):

        WindowHorizontalShiftValues = {
            'Increment': '+',
            'Decrement': '-'
        }

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])

        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__SetHelper('WindowHorizontalShift', '\x1BW{0}*{1}{2}HCTR\r\n'.format(Canvas, Window, WindowHorizontalShiftValues[value]), value, qualifier)
        else:
            print('Invalid Command for SetWindowHorizontalShift')

    def UpdateWindowHorizontalShiftStatus(self, value, qualifier):

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])
        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__UpdateHelper('WindowHorizontalShiftStatus', '\x1BW{0}*{1}HCTR\r\n'.format(Canvas, Window), value, qualifier)
        else:
            print('Invalid Command for UpdateWindowHorizontalShiftStatus')

    def __MatchWindowHorizontalShiftStatus(self, match, tag):
        Canvas = str(int(match.group(1).decode()))
        Window = int(match.group(2).decode())
        value = int(match.group(3).decode())
        self.WriteStatus('WindowHorizontalShiftStatus', value, {'Canvas': Canvas, 'Window': Window})

    def SetWindowHorizontalSize(self, value, qualifier):

        WindowHorizontalSizeValues = {
            'Increment': '+',
            'Decrement': '-'
        }

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])

        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__SetHelper('WindowHorizontalSize', '\x1BW{0}*{1}{2}HSIZ\r\n'.format(Canvas, Window, WindowHorizontalSizeValues[value]), value, qualifier)
        else:
            print('Invalid Command for SetWindowHorizontalSize')

    def UpdateWindowHorizontalSizeStatus(self, value, qualifier):

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])
        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__UpdateHelper('WindowHorizontalSizeStatus', '\x1BW{0}*{1}HSIZ\r\n'.format(Canvas, Window), value, qualifier)
        else:
            print('Invalid Command for UpdateWindowHorizontalSizeStatus')

    def __MatchWindowHorizontalSizeStatus(self, match, tag):
        Canvas = str(int(match.group(1).decode()))
        Window = int(match.group(2).decode())
        value = int(match.group(3).decode())
        self.WriteStatus('WindowHorizontalSizeStatus', value, {'Canvas': Canvas, 'Window': Window})

    def SetWindowBorderStyle(self, value, qualifier):

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])

        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            if value == 'No Border':
                self.__SetHelper('WindowBorderStyle', '\x1BB{0}*{1}*0WNDW\r\n'.format(Canvas, Window), value, qualifier)
            else:
                if 0 < int(value) < 65:
                    self.__SetHelper('WindowBorderStyle', '\x1BB{0}*{1}*{2}WNDW\r\n'.format(Canvas, Window, value), value, qualifier)
        else:
            print('Invalid Command for SetWindowBorderStyle')

    def UpdateWindowBorderStyle(self, value, qualifier):

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])
        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__UpdateHelper('WindowBorderStyle', '\x1BB{0}*{1}WNDW\r\n'.format(Canvas, Window), value, qualifier)
        else:
            print('Invalid Command for UpdateWindowBorderStyle')

    def __MatchWindowBorderStyle(self, match, tag):

        Canvas = str(int(match.group(1).decode()))
        Window = int(match.group(2).decode())
        value = int(match.group(3).decode())
        if value == 0:
            self.WriteStatus('WindowBorderStyle', 'No Border', {'Canvas': Canvas, 'Window': Window})
        else:
            self.WriteStatus('WindowBorderStyle', value, {'Canvas': Canvas, 'Window': Window})

    def SetWindowMute(self, value, qualifier):

        ValueStateValues = {
            'Mute': '1B',
            'Unmute': '0B'
        }
        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])
        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__SetHelper('WindowMute', '{0}*{1}*{2}\r\n'.format(Canvas, Window, ValueStateValues[value]), value, qualifier)
        else:
            print('Invalid Command for SetWindowMute')

    def UpdateWindowMute(self, value, qualifier):

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])
        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__UpdateHelper('WindowMute', '{0}*{1}B\r\n'.format(Canvas, Window), value, qualifier)
        else:
            print('Invalid Command for UpdateWindowMute')

    def __MatchWindowMute(self, match, tag):

        ValueStateValues = {
            '1': 'Mute',
            '0': 'Unmute'
        }

        Canvas = str(int(match.group(1).decode()))
        Window = int(match.group(2).decode())
        value = ValueStateValues[match.group(3).decode()]
        self.WriteStatus('WindowMute', value, {'Canvas': Canvas, 'Window': Window})

    def SetWindowPriority(self, value, qualifier):

        ValueStateValues = {
            'Send to Back': '0',
            'Send Backward': '1',
            'Bring Forward': '2',
            'Bring to Front': '3'
        }

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])
        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__SetHelper('WindowPriority', '\x1BP{0}*{1}*{2}WNDW\r\n'.format(Canvas, Window, ValueStateValues[value]), value, qualifier)
        else:
            print('Invalid Command for SetWindowPriority')

    def UpdateWindowPriorityStatus(self, value, qualifier):

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])
        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__UpdateHelper('WindowPriorityStatus', '\x1BP{0}*{1}WNDW\r\n'.format(Canvas, Window), value, qualifier)
        else:
            print('Invalid Command for UpdateWindowPriorityStatus')

    def __MatchWindowPriorityStatus(self, match, tag):

        Canvas = str(int(match.group(1).decode()))
        Window = int(match.group(2).decode())
        value = int(match.group(3).decode())
        self.WriteStatus('WindowPriorityStatus', value, {'Canvas': Canvas, 'Window': Window})

    def SetWindowVerticalShift(self, value, qualifier):

        WindowVerticalShiftValues = {
            'Increment': '+',
            'Decrement': '-'
        }

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])

        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__SetHelper('WindowVerticalShift', '\x1BW{0}*{1}{2}VCTR\r\n'.format(Canvas, Window, WindowVerticalShiftValues[value]), value, qualifier)
        else:
            print('Invalid Command for SetWindowVerticalShift')

    def UpdateWindowVerticalShiftStatus(self, value, qualifier):

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])
        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__UpdateHelper('WindowVerticalShiftStatus', '\x1BW{0}*{1}VCTR\r\n'.format(Canvas, Window), value, qualifier)
        else:
            print('Invalid Command for UpdateWindowVerticalShiftStatus')

    def __MatchWindowVerticalShiftStatus(self, match, tag):
        Canvas = str(int(match.group(1).decode()))
        Window = int(match.group(2).decode())
        value = int(match.group(3).decode())
        self.WriteStatus('WindowVerticalShiftStatus', value, {'Canvas': Canvas, 'Window': Window})

    def SetWindowVerticalSize(self, value, qualifier):

        WindowVerticalSizeValues = {
            'Increment': '+',
            'Decrement': '-'
        }

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])

        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__SetHelper('WindowVerticalSize', '\x1BW{0}*{1}{2}VSIZ\r\n'.format(Canvas, Window, WindowVerticalSizeValues[value]), value, qualifier)
        else:
            print('Invalid Command for SetWindowVerticalSize')

    def UpdateWindowVerticalSizeStatus(self, value, qualifier):

        Window = qualifier['Window']
        Canvas = int(qualifier['Canvas'])
        if 1 <= Window <= 999 and 1 <= Canvas <= 10:
            self.__UpdateHelper('WindowVerticalSizeStatus', '\x1BW{0}*{1}VSIZ\r\n'.format(Canvas, Window), value, qualifier)
        else:
            print('Invalid Command for UpdateWindowVerticalSizeStatus')

    def __MatchWindowVerticalSizeStatus(self, match, tag):
        Canvas = str(int(match.group(1).decode()))
        Window = int(match.group(2).decode())
        value = int(match.group(3).decode())
        self.WriteStatus('WindowVerticalSizeStatus', value, {'Canvas': Canvas, 'Window': Window})

    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Debug = True
        if self.VerboseDisabled:
            @Wait(1)
            def SendVerbose():
                self.Send('w3cv\r\n')
                self.Send(commandstring)
        else:
            self.Send(commandstring)

    def __UpdateHelper(self, command, commandstring, value, qualifier):
        if self.initializationChk:
            self.OnConnected()
            self.initializationChk = False

        self.counter += 1
        if self.counter > self.connectionCounter and self.connectionFlag:
            self.OnDisconnected()

        if self.Authenticated in ['User', 'Admin', 'Not Needed']:
            if self.Unidirectional == 'True':
                print('Inappropriate Command ', command)
            else:
                if self.VerboseDisabled:
                    @Wait(1)
                    def SendVerbose():
                        self.Send('w3cv\r\n')
                        self.Send(commandstring)
                else:
                    self.Send(commandstring)
        else:
            print('Inappropriate Command ', command)

    def __MatchErrors(self, match, qualifier):

        DEVICE_ERROR_CODES = {
            '01': 'Invalid input number (too large)',
            '10': 'Invalid command',
            '11': 'Invalid preset number',
            '12': 'Invalid port number',
            '13': 'Invalid parameter',
            '14': 'Command not available for this configuration',
            '17': 'System timed out',
            '22': 'Busy',
            '24': 'Privilege violation',
            '25': 'Device not present',
            '26': 'Maximum number of connections exceeded',
            '27': 'Invalid event number',
            '28': 'Bad filename or file not found',
            '30': 'Hardware failure (followed by a colon [:] and a descriptor number)',
            '31': 'Attempt to break port pass-through when it has not been set',
            '32': 'Incorrect V-chip password'
        }
        ErrorCode = DEVICE_ERROR_CODES.get(match.group(1).decode(), 'Unknown error: ' + match.group(0).decode())
        print(ErrorCode)

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0
        self.WriteStatus('DeviceStatus', 'Normal', None)

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False
        self.VerboseDisabled = True

        if self.ConnectionType != 'Serial':
            self.Authenticated = 'Not Needed'
            self.PasswdPromptCount = 0


    ######################################################
    # RECOMMENDED not to modify the code below this point
    ######################################################
    # Send Control Commands
    def Set(self, command, value, qualifier=None):
        method = 'Set%s' % command
        if hasattr(self, method) and callable(getattr(self, method)):
            getattr(self, method)(value, qualifier)
        else:
            print(command, 'does not support Set.')
    # Send Update Commands

    def Update(self, command, qualifier=None):
        method = 'Update%s' % command
        if hasattr(self, method) and callable(getattr(self, method)):
            getattr(self, method)(None, qualifier)
        else:
            print(command, 'does not support Update.')

    # This method is to tie an specific command with a parameter to a call back method
    # when its value is updated. It sets how often the command will be query, if the command
    # have the update method.
    # If the command doesn't have the update feature then that command is only used for feedback
    def SubscribeStatus(self, command, qualifier, callback):
        Command = self.Commands.get(command)
        if Command:
            if command not in self.Subscription:
                self.Subscription[command] = {'method': {}}

            Subscribe = self.Subscription[command]
            Method = Subscribe['method']

            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        if Parameter in qualifier:
                            Method[qualifier[Parameter]] = {}
                            Method = Method[qualifier[Parameter]]
                        else:
                            return

            Method['callback'] = callback
            Method['qualifier'] = qualifier
        else:
            print(command, 'does not exist in the module')

    # This method is to check the command with new status have a callback method then trigger the callback
    def NewStatus(self, command, value, qualifier):
        if command in self.Subscription:
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
            Command = self.Commands[command]
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        break
            if 'callback' in Method and Method['callback']:
                Method['callback'](command, value, qualifier)

    # Save new status to the command
    def WriteStatus(self, command, value, qualifier=None):
        self.counter = 0
        if not self.connectionFlag:
            self.OnConnected()
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    if Parameter in qualifier:
                        Status[qualifier[Parameter]] = {}
                        Status = Status[qualifier[Parameter]]
                    else:
                        return
        try:
            if Status['Live'] != value:
                Status['Live'] = value
                self.NewStatus(command, value, qualifier)
        except:
            Status['Live'] = value
            self.NewStatus(command, value, qualifier)

    # Read the value from a command.
    def ReadStatus(self, command, qualifier=None):
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    return None
        try:
            return Status['Live']
        except:
            return None

    def __ReceiveData(self, interface, data):
        # handling incoming unsolicited data
        self._ReceiveBuffer += data
        # check incoming data if it matched any expected data from device module
        if self.CheckMatchedString() and len(self._ReceiveBuffer) > 10000:
            self._ReceiveBuffer = b''

    # Add regular expression so that it can be check on incoming data from device.
    def AddMatchString(self, regex_string, callback, arg):
        if regex_string not in self._compile_list:
            self._compile_list[regex_string] = {'callback': callback, 'para': arg}

    # Check incoming unsolicited data to see if it was matched with device expectancy.
    def CheckMatchedString(self):
        for regexString in self._compile_list:
            while True:
                result = search(regexString, self._ReceiveBuffer)
                if result:
                    self._compile_list[regexString]['callback'](result, self._compile_list[regexString]['para'])
                    self._ReceiveBuffer = self._ReceiveBuffer.replace(result.group(0), b'')
                else:
                    break
        return True


class SerialClass(SerialInterface, DeviceClass):

    def __init__(self, Host, Port, Baud=9600, Data=8, Parity='None', Stop=1, FlowControl='Off', CharDelay=0, Model=None):
        SerialInterface.__init__(self, Host, Port, Baud, Data, Parity, Stop, FlowControl, CharDelay)
        self.ConnectionType = 'Serial'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()


class EthernetClass(EthernetClientInterface, DeviceClass):

    def __init__(self, Hostname, IPPort, Protocol='TCP', ServicePort=0, Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort, Protocol, ServicePort)
        self.ConnectionType = 'Ethernet'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()
