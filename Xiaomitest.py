"""Test Library to handle connection with Xiaomi Gateway
Uses https://github.com/Danielhiversen/PyXiaomiGateway"""
import logging
logging.basicConfig(filename='xiao.log',level=logging.DEBUG)

from xiaomi_gateway import XiaomiGateway

if __name__=="__main__":
    ip_address = "192.168.1.122"
    port = 9898
    sid = "7811dc6c9975"
    key = 'czeeoimwtjkdsdix'
    discovery_retries = 10
    interface = 'any'
    logging.debug('##start gateway')
    x = XiaomiGateway(ip_address, port, sid, key, discovery_retries, interface, proto=None)
    for dt in x.devices.keys():
        logging.info('dt %s\n' % dt)
        for d in x.devices[dt]:
            logging.info('%s\n' % d)

"""INFO:root:dt sensor
INFO:root:{'model': 'sensor_motion.aq2',
'proto': '1.0.9', 'sid': '158d0001e47d9d', 'short_id': 13768, 'data':
{'voltage': 3015}, 'raw_data': {'cmd': 'read_ack', 'model':
'sensor_motion.aq2', 'sid': '158d0001e47d9d', 'short_id': 13768,
'data': '{"voltage":3015}'}}
INFO:root:{'model': 'weather.v1', 'proto':
'1.0.9', 'sid': '158d0002273666', 'short_id': 52719, 'data':
{'voltage': 2905, 'temperature': '1815', 'humidity': '5888',
'pressure': '102190'}, 'raw_data': {'cmd': 'read_ack', 'model':
'weather.v1', 'sid': '158d0002273666', 'short_id': 52719, 'data':
'{"voltage":2905,"temperature":"1815","humidity":"5888","pressure":"102190"}'}}
INFO:root:{'model': 'weather.v1', 'proto': '1.0.9', 'sid':
'158d000223a48a', 'short_id': 16125, 'data': {'voltage': 2905,
'temperature': '1866', 'humidity': '6225', 'pressure': '102190'},
'raw_data': {'cmd': 'read_ack', 'model': 'weather.v1', 'sid':
'158d000223a48a', 'short_id': 16125, 'data':
'{"voltage":2905,"temperature":"1866","humidity":"6225","pressure":"102190"}'}}
INFO:root:{'model': 'gateway', 'proto': '1.0.9', 'sid': '7811dc6c9975',
'short_id': 0, 'data': {'rgb': 0, 'illumination': 279, 'proto_version':
'1.0.9'}, 'raw_data': {'cmd': 'read_ack', 'model': 'gateway', 'sid':
'7811dc6c9975', 'short_id': 0, 'data':
'{"rgb":0,"illumination":279,"proto_version":"1.0.9"}'}}
INFO:root:dt binary_sensor
INFO:root:{'model': 'sensor_motion.aq2', 'proto':
'1.0.9', 'sid': '158d0001e47d9d', 'short_id': 13768, 'data':
{'voltage': 3015}, 'raw_data': {'cmd': 'read_ack', 'model':
'sensor_motion.aq2', 'sid': '158d0001e47d9d', 'short_id': 13768,
'data': '{"voltage":3015}'}}
INFO:root:dt light
INFO:root:{'model':
'gateway', 'proto': '1.0.9', 'sid': '7811dc6c9975', 'short_id': 0,
'data': {'rgb': 0, 'illumination': 279, 'proto_version': '1.0.9'},
'raw_data': {'cmd': 'read_ack', 'model': 'gateway', 'sid':
'7811dc6c9975', 'short_id': 0, 'data':
'{"rgb":0,"illumination":279,"proto_version":"1.0.9"}'}}


"""
