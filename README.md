configSerial
===========
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
    along with this program.  If not, see <http://www.gnu.org/licenses/

ConfigSerial is a helper module to encapsulate the configuration of a serial port using wxPython and pySerial.  It 
creates a configuration file that contains the configuration data.  The name of the configuration file can be specified 
on instantiation and it is stored in the users home directory by default.  It should be a hidden file so that means
that it will add a '.' to the front of the file name in Linux.  Windows will generate a registry key for each configuration key.
