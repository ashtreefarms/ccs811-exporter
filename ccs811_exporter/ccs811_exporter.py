"""ccs811_exporter.py: A Prometheus exporter for the CCS811 sensor"""

from Adafruit_CCS811 import Adafruit_CCS811
import logging
from prometheus_client import Counter, Gauge
from time import sleep

METRICS = {
    # Gauges
    'eco2': ('ccs811_eco2_ppm', "Current CCS811 eCO2 level"),
    'temp': ('ccs811_temperature_celsius', "Current CCS811 temperature"),
    'tvoc': ('ccs811_tvoc_ppb', "Current CCS811 TVOC level"),
    
    # Counters
    'io_errors': ('ccs811_io_errors_total', "Total CCS811 I/O errors"),
    'io_reads': ('ccs811_io_reads_total', "Total CCS811 I/O reads")
}
WAIT_DELAY = 0.1

logger = logging.getLogger(__name__)


class CCS811Exporter:
    @staticmethod
    def gauge(info, labels=None):
        if labels is None:
            labels = {}
        label_keys = list(labels.keys())
        label_values = [labels[k] for k in label_keys]
        gauge = Gauge(info[0], info[1], label_keys)
        if len(label_values):
            gauge = gauge.labels(*label_values)
        return gauge
    
    @staticmethod
    def counter(info, labels=None):
        if labels is None:
            labels = {}
        label_keys = list(labels.keys())
        label_values = [labels[k] for k in label_keys]
        counter = Counter(info[0], info[1], label_keys)
        if len(label_values):
            counter = counter.labels(*label_values)
        return counter
    
    def __init__(self, address, metrics=METRICS, labels=None):
        self.temp = None
        self.eco2 = None
        self.tvoc = None
        self.eco2_gauge = CCS811Exporter.gauge(metrics['eco2'], labels)
        self.temp_gauge = CCS811Exporter.gauge(metrics['temp'], labels)
        self.tvoc_gauge = CCS811Exporter.gauge(metrics['tvoc'], labels)
        self.ioread_counter = CCS811Exporter.counter(metrics['io_reads'], labels)
        self.ioerror_counter = CCS811Exporter.counter(metrics['io_errors'], labels)
        self.ccs = Adafruit_CCS811(address=address)
    
    def wait(self):
        self.ioread_counter.inc()
        try:
            while not self.ccs.available():
                sleep(WAIT_DELAY)
                pass
            return True
        except IOError:
            logger.error("IOError raised when determining CCS811 availability")
            self.ioerror_counter.inc()
        return False

    def set_temp_offset(self, offset):
        temp = self.ccs.calculateTemperature()
        self.ccs.tempOffset = temp + offset

    def calibrate(self, temp, humidity):
        pass

    def measure(self):
        if not self.wait():
            return
        
        self.ioread_counter.inc()
        try:
            self.temp = self.ccs.calculateTemperature()
            result = self.ccs.readData()
        except IOError:
            logger.error("IOError raised while reading CCS811 data")
            self.ioerror_counter.inc()
            return
        
        if result != 0:
            logger.error("CCS811 returned {} when reading data".format(result))
            return
        
        self.eco2 = self.ccs.geteCO2()
        self.tvoc = self.ccs.getTVOC()
        logger.info("   ".join([
            "temp: {:.1f} C".format(self.temp),
            "eco2: {:}ppm".format(self.eco2),
            "tvoc: {:}ppb".format(self.tvoc)
        ]))

    def export(self):
        self.temp_gauge.set(self.temp)
        self.eco2_gauge.set(self.eco2)
        self.tvoc_gauge.set(self.tvoc)
