import argparse
from ccs811_exporter import CCS811Exporter
import json
import logging
import prometheus_client
from time import sleep

DEFAULT_I2C_ADDRESS = 0x5B
DEFAULT_PORT = 9501
DEFAULT_SAMPLE_INTERVAL = 2

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action='store_true')
parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT, help="exporter port")
parser.add_argument("-a", "--address", type=lambda x: int(x, 0), default=DEFAULT_I2C_ADDRESS, help="CCS811 I2C address")
parser.add_argument("-l", "--labels", type=json.loads, help="JSON object of Prometheus labels to apply")
parser.add_argument("-i", "--interval", type=int, default=DEFAULT_SAMPLE_INTERVAL, help="measurement sample interval")


def main(args=None):
    if args is None:
        args = parser.parse_args()

    f = logging.Formatter('%(asctime)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(f)
    logger = logging.getLogger('ccs811_exporter')
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    logger.addHandler(ch)
    
    exporter = CCS811Exporter(address=args.address, labels=args.labels)

    logger.info("waiting for CCS811")
    exporter.wait()
    exporter.set_temp_offset(-25.0)
    
    logger.info("starting exporter on port {}".format(args.port))
    prometheus_client.start_http_server(args.port)

    logger.info("starting sampling with {}s interval".format(args.interval))
    while True:
        exporter.measure()
        exporter.export()
        sleep(args.interval)


if __name__ == "__main__":
    main()
