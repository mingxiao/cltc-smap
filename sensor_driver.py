"""
smap driver to read via bluetooh from a arduino board and publish
data to smap archiver.
"""
import smap.driver as driver
import smap.util as util
import bluetooth

class sensor_driver(driver.SmapDriver):
    
    def setup(self,opts):
        self.addr = opts.get('bt_addr')
        self.port = opts.get('port')
        self.timeout = 1
        #connect to bluetooth
        try:
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.settimeout(timeout)
            self.sock.connect((self.addr,self.port))
        except:
            raise Exception('%s connection error at port %s'%(self.addr,self.port))
        self.rate = float(opts.get('Rate'))
        self.add_timeseries('/sensorX','LUX',data_type='double',milliseconds=True)

    def start(self):
        util.periodicSequentialCall(self.read).start(self.rate)

    def read(self,bytes_to_read=32):
        data = self.sock.recv(bytes_to_read)
        print data
        pass
