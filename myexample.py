"""

Copyright (c) 2011, 2012, Regents of the University of California

All rights reserved.



Redistribution and use in source and binary forms, with or without

modification, are permitted provided that the following conditions 

are met:



 - Redistributions of source code must retain the above copyright

   notice, this list of conditions and the following disclaimer.

 - Redistributions in binary form must reproduce the above copyright

   notice, this list of conditions and the following disclaimer in the

   documentation and/or other materials provided with the

   distribution.



THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS

"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT

LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 

FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 

THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 

INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 

(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 

SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 

HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 

STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 

ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 

OF THE POSSIBILITY OF SUCH DAMAGE.

"""

"""

@author David Siap <dsiap@ucdavis.edu>

"""

"""

Driver for Labview socket

This is a driver that will listen to a LabView socket on (host,port)


@author Ming Xiao <minxiao@ucdavis.edu>

"""
import socket
import sys
import os

import smap.driver as driver
import smap.util as util
import smap.actuate as actuate
import subprocess

LUX_CONST = 360
TOL = 100

class FileActuator(actuate.BinaryActuator):
    """Example Binary Acutator which implements actuation by writing
    to a file
    """

    def setup(self, opts):
        actuate.BinaryActuator.setup(self, opts)
        self.file = os.path.expanduser(opts['filename'])

    def get_state(self, request):
        with open(self.file, 'r') as fp:
            return int(fp.read())

    def set_state(self, request, state):
        with open(self.file, 'w') as fp:
            fp.write(str(state))
        return state

class Labview_socket(driver.SmapDriver):
    def setup(self, opts):
        self.ports = []
        self.num_con = int(opts.get('num_con',0)) #get number of connections
        assert self.num_con > 0
        for i in range(self.num_con):
            port = int(opts.get('port%d'%i,0))
            assert port > 0
            self.ports.append(port)

        print '________________'
        print self.num_con, self.ports
        
	#port and host should be defined in configuration file
	#self.port = int(opts.get("port",8081)) #default port 8081
	self.host = opts.get('host','localhost') #default host localhost
	self.rate = int(opts.get("Rate", 2))#Can set the rate to whatever you want, in seconds
	self.timeout = float(self.rate)/self.num_con
        #add the timeseries
	for i in range(self.num_con):
            self.add_timeseries('/sensor%d'%i,'Lux',data_type='double')
        self.set_metadata('/', {
            'Instrument/Manufacturer' : 'Labview Datasocket',
            'Instrument/Model' : 'sensor'
            })
        #get the file to actuate on
        filename = opts.pop('Filename','/home/ubuntu/Desktop/test_file.txt')
        #add the actuator
        self.add_actuator('/point0', 'Switch Position',
                          FileActuator, setup={'filename': filename},
                          read_limit=1, write_limit=1)

    def start(self):
        util.periodicSequentialCall(self.read).start(self.rate)

    def read_port(self,port_idx):
        """
        Establishes a connection to self.host on port self.ports[port_idx].
        """
        assert port_idx >= 0
        assert port_idx < self.num_con
        #print 'hereeeee'
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print 'created socket'
            #s.settimeout(self.timeout)
            #s.settimeout(1)
            #print 'set timeout'
            print self.host, self.ports[port_idx]
            s.connect((str(self.host),self.ports[port_idx]))
            print 'Connected to %s on port %d'%(s.getpeername,self.ports[port_idx])
            data = s.recv(128)
            s.close()
            print 'Received %s'%repr(data)
            lux = float(data.strip()) * LUX_CONST
            self.add('/sensor%d'%port_idx,lux)
            print 'Added %f to /sensor%d'%(lux,port_idx)
            return lux
        except:
            print 'ERROR: sensor%d'%port_idx,sys.exc_info()[0]

    def set_state(self,point=0,state=1):
        """
        Sets the actuation point to the state
        state - either 0(off) or 1(on)
        point - index of the actuation point. 0 <= point < self.num_con
        """
        subprocess.call('curl -XPUT http://localhost:8080/data/ming-test0/point0?state=%d'%state,shell=True)
        pass

    def read(self):
        """
        Creates a connection to (self.host,self.port)
        Read value from port
        Add value to /sensor0
        Close connection
        """
        for i in range(self.num_con):
            self.read_port(i)
