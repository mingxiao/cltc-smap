"""
smap driver to read via bluetooh from a arduino board and publish
data to smap archiver.
"""
import smap.driver as driver
import smap.util as util
import bluetooth
import re

class sensor_driver(driver.SmapDriver):
    def parse_reading(self,data):
        """
        @param data - string of data

        Returns a number if a reading is found otherwise return -1
        """
        pat =re.compile('([1-9][0-9]*)')
        datum = data.split('\n')
        #print datum
        for d in datum:
            m = pat.search(d)
            if m is not None:
                return float(m.group(1))
        return float(-1)
    
    def setup(self,opts):
        self.addr = opts.get('bt_addr')
        self.port = int(opts.get('port'))
        self.timeout = 4
        #connect to bluetooth
        try:
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.addr,self.port))
        except Exception,e:
            print 'Exception: %s' %e
            #raise Exception('%s connection error at port %s'%(self.addr,self.port))
        self.rate = float(opts.get('Rate'))
        self.add_timeseries('/sensorX','LUX',data_type='double',milliseconds=True)

    def start(self):
        util.periodicSequentialCall(self.read).start(self.rate)

    def read(self,bytes_to_read=256):
        reading = self.sock.recv(bytes_to_read)
        #we can read in data, now to parse it to make sure we have a number to read
        #print 'READ',reading
        data = self.parse_reading(reading)
        print 'Parse',data
        self.add('/sensorX',data)
        pass
