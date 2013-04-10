import smap.driver as driver
import smap.util as util


class ms_socket(driver.SmapDriver):
    def setup(self,opts):
        self.counter = 0.0
        self.rate = float(opts.get('Rate'))
        self.add_timeseries('/sensorX','TMP',data_type='double',milliseconds=True)

    def start(self):
        util.periodicSequentialCall(self.read).start(self.rate)

    def read(self):
        self.add('/sensorX',self.counter)
        self.counter += 1.0
