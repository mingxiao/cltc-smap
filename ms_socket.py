import smap.driver as driver
import smap.util as util
import bluetooth

class ms_socket(driver.SmapDriver):
    def setup(self,opts):
        self.addr = opts.get('bt_addr')
        self.port = int(opts.get('port'))
        print self.addr,self.port
        self.timeout = 5
        #connect to bluetooth
        try:
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.addr,self.port))
        except Exception, e:
            print 'exception: %s'%e
            #raise Exception('%s connection error at port %s'%(self.addr,self.port))
        self.rate = float(opts.get('Rate'))
        self.add_timeseries('/arduino','LUX',data_type='double',milliseconds=True)

    def start(self):
        util.periodicSequentialCall(self.read).start(self.rate)

    def read(self,bytes_to_read=32):
        print 'READING...'
        data = self.sock.recv(bytes_to_read)
        print 'DATA', data
        self.add('/arduino',20.0)
        
