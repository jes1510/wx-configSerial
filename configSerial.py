'''
This is a helper module for configuring a serial port in WX
It saves the configuration in a configuration file.  

The actual port should be accessed through the 'Port' class
at port.ser.

Written by Jesse Merritt
www.github.com/jes1510
August 5 , 2012

   This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Depends on the following modules:
serial
wx
time
'''

import serial
import wx
import time

class configSerial(wx.Dialog):
    '''
    Serial port configuration tool for WX. 
    
    Keyword Arguments:
    parent: 	WX parent class 
    id: 		WX window ID
    port: 	Serial port configuration
    title: 	Optional window title  
    '''
    def __init__(self, parent, id, port, title = "Configure Serial Port"):	  
        self.parent= parent
        self.id = id
        self.port = port
        self.comError = 0;        
        self.ports = self.findPorts()			# Find the available ports
        if len(self.ports) < 1 :
            self.ports.append("No Ports Found")
        
        # Init the variables to known states
        self.baudRates = ['110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800', '38400', '56000', '57600', '115200']
        self.dataBitsList = ['5', '6', '7', '8']
        self.parityList = ['None', 'Even', 'Odd']
        self.stopBitsList = ['0', '1','2']
        self.flowControlList = ['None', 'Hardware', 'XONXOFF']
        self.flowControl = self.port.flowControl

        # Init to defaults
        self.portName = self.ports[0]	# Pick the first port
        self.baud = str(self.port.baud)		# default 9600
        self.dataBits = str(self.port.dataBits)		
        self.parity = str(self.port.parity)
        self.stopBit = str(self.port.stopBits)        
        self.timeout = str(self.port.timeout)

        #   Build the box
        wx.Dialog.__init__(self, self.parent, self.id, title, size=(225,325)) # second is vertical

        #   Vertical sizer with a bunch of horizontal sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)    
        sizer8 = wx.BoxSizer(wx.HORIZONTAL) 
  
        sizer.Add(sizer2, 0, wx.EXPAND)
        sizer.Add(sizer3, 0, wx.EXPAND)
        sizer.Add(sizer4, 0, wx.EXPAND)
        sizer.Add(sizer5, 0, wx.EXPAND)
        sizer.Add(sizer6, 0, wx.EXPAND)
        sizer.Add(sizer7, 0, wx.EXPAND)   
        sizer.Add(sizer8, 0, wx.EXPAND) 

        #   Drop downs and text
        st1 = sizer2.Add(wx.StaticText(self, -1, 'Port', style=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL), 1, wx.EXPAND)
        self.portsCombo = wx.ComboBox(self, -1, self.ports[0], size=(150, -1), choices=self.ports,style=wx.CB_READONLY)
        portsBox = sizer2.Add(self.portsCombo, 0, wx.ALL| wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)

        st2 = sizer3.Add(wx.StaticText(self, -1, 'Baud', style=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL ), 1, wx.EXPAND)
        self.baudCombo = wx.ComboBox(self, -1, self.baud, size=(150, -1), choices=self.baudRates,style=wx.CB_READONLY)
        baudBox = sizer3.Add(self.baudCombo, 0, wx.ALL| wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)

        st3 = sizer4.Add(wx.StaticText(self, -1, 'Data Bits', style=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL), 1, wx.EXPAND)
        self.bitsCombo = wx.ComboBox(self, -1, self.dataBits, size=(150, -1), choices=self.dataBitsList,style=wx.CB_READONLY)
        bitsBox = sizer4.Add(self.bitsCombo, 0, wx.ALL| wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)

        st4 = sizer5.Add(wx.StaticText(self, -1, 'Parity', style=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL), 1, wx.EXPAND)
        self.parityCombo = wx.ComboBox(self, -1, self.parity,  size=(150, -1), choices=self.parityList,style=wx.CB_READONLY)
        parityBox = sizer5.Add(self.parityCombo, 0, wx.ALL| wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)

        st5 = sizer6.Add(wx.StaticText(self, -1, 'Stop Bits', style=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL), 1, wx.EXPAND)
        self.stopCombo = wx.ComboBox(self, -1, self.stopBit, size=(150, -1), choices=self.stopBitsList,style=wx.CB_READONLY)
        stopBox = sizer6.Add(self.stopCombo, 0, wx.ALL| wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)

        st6 = sizer7.Add(wx.StaticText(self, -1, 'Flow Control', style=wx.ALIGN_RIGHT| wx.ALIGN_CENTER_VERTICAL), 1, wx.EXPAND)
        self.flowCombo = wx.ComboBox(self, -1, self.port.flowControl, size=(150, -1), choices=self.flowControlList,style=wx.CB_READONLY)
        flowBox = sizer7.Add(self.flowCombo, 0, wx.ALL| wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5) 
        
        st7 = sizer8.Add(wx.StaticText(self, -1, 'Timeout(mS)', style=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL), 1, wx.EXPAND)
        self.timeoutEntry = wx.TextCtrl(self, -1, self.timeout, size=(150, -1))
        timeoutBox = sizer8.Add(self.timeoutEntry, 0, wx.ALL| wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5) 

	# Button events
        doneButton = wx.Button(self, -1, 'Save Settings')
        cancelButton = wx.Button(self, -1, 'Cancel')
        sizer.Add(doneButton, 0, wx.ALL|wx.ALIGN_CENTER, 5)  
        sizer.Add(cancelButton, 0, wx.ALL|wx.ALIGN_CENTER, 5)  
        self.Bind(wx.EVT_BUTTON, self.done,doneButton)
        self.Bind(wx.EVT_BUTTON, self.cancel,cancelButton)  

        self.SetSizer(sizer)        
        #self.flowCombo.SetValue(self.port.flowControl)
         
        
    def showComError(self) :    
	'''
	Show a window with a COM error    
	'''
        dlg = wx.MessageDialog(self, "Could not open serial port!", 'Error!', wx.OK | wx.ICON_ERROR)  
        dlg.ShowModal()        
            
    def cancel(self, e) :
	'''
	Cancel
	'''
        self.Close(True)

    def done(self, e) :	
	'''
	Pass the serial configuration to the port class
	on a save.  Have it write the configuration to
	the config file
	
	Keyword Arguments:
	e: WX event (button press) 
	'''
        self.port.name = self.portsCombo.GetValue()
        self.port.baud = int(self.baudCombo.GetValue())
        self.port.dataBits = int(self.bitsCombo.GetValue())
        self.port.parity = self.parityCombo.GetValue()
        self.port.stopBit = int(self.stopCombo.GetValue())
        self.port.flowControl = self.flowCombo.GetValue()  
        self.port.timeout = float(self.timeoutEntry.GetValue()) 

        self.port.rtscts = 0
        self.port.xonxoff = 0

        if self.port.flowControl == "Hardware" :
            self.port.rtscts = 1
            self.port.xonxoff = 0
            
        if self.port.flowControl == "XONXOFF" :
            self.port.rtscts = 0
            self.port.xonxoff = 0

        if self.port.flowControl == "None" :
            self.port.rtscts = 0  
            self.port.xonxoff = 0
            
        if self.port.parity == 'None' :
	   self.parity = serial.PARITY_NONE 
	   
	if self.port.parity == 'Even' :
	   self.parity = serial.PARITY_EVEN
	   
	if self.port.parity == 'Odd' :
	   self.parity = serial.PARITY_ODD 	  
	

        if self.ports != "No Ports Found" :
           self.port.ser = serial.Serial(port= self.port.name, 
				baudrate= int(self.port.baud), 
				bytesize=int(self.port.dataBits), 
				parity= self.parity, 
				xonxoff = self.port.xonxoff,
				rtscts = self.port.rtscts,				
				timeout = int(self.port.timeout)/1000)
        
        self.Close(True)  
        self.port.saveOptions()

    def findPorts(self) :  
	'''
	Loop through all possible serial ports
	and append the name to a list.  Should
	be compatible with Windows or Linux
	'''    
        self.ports = []
        for i in range(64) :  #  Windows
            try :                
                s = serial.Serial("COM" + str(i))                
                s.close()
                self.ports.append("COM" + str(i))                
            except :
                pass
                
        if len(self.ports) > 0 : 
            return self.ports

        for i in range(64) :
            for k in ["/dev/ttyUSB", "/dev/ttyACM", "/dev/ttyS"] : # Linux
                try :		
                    s = serial.Serial(k+str(i))
                    s.close()                
                    self.ports.append(k+ str(i))

                except :
                    pass				
        return self.ports  
        
class Port(wx.Dialog) :		
    '''
    Class to encapsulate the port and config attributes.
    Also manages writing and reading data from the 
    config file
    
    keyword arguments:
    wx.Dialog:  wx parent 
    filename:  filename to use for config file  
    '''
    def __init__(self, filename) : 
        self.name = '/dev/ttyACM0'		# Serial port name
        self.baud = 9600		        # Baud rate
        self.dataBits = 8			# data bits 
        self.parity = 'NONE'			# Whether or not to use parity
        self.stopBits = 1			# Number of stop bits
        self.timeout = 1000			# Serial port timeout in seconds
        self.xonxoff = 0			# XONXOFF flow control, 0=off, 1=on
        self.rtscts = 0			        # Hardware flow control.  0=off, 1=on
        self.configFile = wx.Config(filename)	# Configfile name.  Default location is home
        self.ser =  serial.Serial()     	# Serial port instance  
        self.flowControl = 'None'		# No flow control
	
        if self.configFile.Exists('port'):	# If the config file exists then load configuration
            self.name = self.configFile.Read('port')
            self.baud = self.configFile.ReadInt('baud') 
            self.dataBits = self.configFile.ReadInt('dataBits')
            self.parity = self.configFile.Read('parity')
            self.stopBits = self.configFile.ReadInt('stopBits')            
            self.timeout = self.configFile.ReadInt('timeout')	
            self.rtscts = self.configFile.ReadInt('rtscts')
            self.xonxoff = self.configFile.ReadInt('xonxoff')
            self.flowControl = self.configFile.Read('flowControl')
		
        else:
            self.saveOptions()	# create a default file if one doesn't exist

	  
    def saveOptions(self) :
        self.configFile.Write("port", self.name)        
        self.configFile.WriteInt("baud", self.baud)
        self.configFile.WriteInt("dataBits", self.dataBits)
        self.configFile.Write("parity", self.parity)
        self.configFile.WriteInt("stopBits", self.stopBits)
        self.configFile.WriteInt("timeout", self.timeout)
        self.configFile.WriteInt("rtscts", self.rtscts)
        self.configFile.WriteInt("xonxoff", self.xonxoff)
        self.configFile.Write("flowControl", self.flowControl)
        self.configFile.Flush()       
        