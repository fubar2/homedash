"""Detect weather sensors and save data from
appropriate devices connected to a Xiaomi Aqara Gateway.
Relies on the Home Assistant Aqara gateway interface
https://github.com/Danielhiversen/PyXiaomiGateway"""

import os
import sys
import time
import signal
import logging
from collections import defaultdict
logging.basicConfig(filename='xiaoweather.log',level=logging.INFO)

from xiaomi_gateway import XiaomiGateway

WSENSORID='weather.v1'
global RUNNING
RUNNING = True
SAMPINT = 300 # sleep seconds between read loops


# todo make config
ip_address = "192.168.1.122"
port = 9898
sid = "7811dc6c9975"
key = 'czeeoimwtjkdsdix'
discovery_retries = 10
interface = 'any'

class xweathersensor():
    """class for xiaomi weather sensors - temp/hum/baro
    instantiate when detected
    methods to get latest data and write to a file
    example from detection:
    INFO:root:{'model': 'weather.v1', 'proto':
    '1.0.9', 'sid': '158d0002273666', 'short_id': 52719, 'data':
    {'voltage': 2905, 'temperature': '1815', 'humidity': '5888',
    'pressure': '102190'}, 'raw_data': {'cmd': 'read_ack', 'model':
    'weather.v1', 'sid': '158d0002273666', 'short_id': 52719, 'data':
    '{"voltage":2905,"temperature":"1815","humidity":"5888","pressure":"102190"}'}}

    """

    def __init__(self,drec,updateint):
        self.HEADER = 'time\ttemp\thumidity\tpressure\n'
        self.sid = drec['sid']
        self.updateint = updateint
        self.tdinit = time.strftime('%H%M%S_%d%m%Y')
        self.outfname = '%s_%s_%d.xls' % (WSENSORID.split('.')[0],self.sid,self.updateint)
        logging.debug('## using outfname = %s' % self.outfname)
        fdat = drec['data']
        v,t,h,p = fdat['voltage'],fdat['temperature'],fdat['humidity'],fdat['pressure']
        if os.path.isfile(self.outfname):
            self.fout = open(self.outfname,'a')
        else:
            self.fout = open(self.outfname,'w')
            self.fout.write(self.HEADER)
            self.fout.flush()
        self.started = time.time()

    def writedat(self,jdat,dat):
        """ add this as the callback in the gateway instance for this SID
        """
        v = jdat['voltage']/1000.0
        t = int(jdat['temperature'])/100.0
        h = int(jdat['humidity'])/100.0
        p = int(jdat['pressure'])/100.0
        dt = time.strftime('%Y%m%d_%H%M%S')
        s = '%s\t%.1f\t%.1f\t%.1f\n' % (dt,t,h,p)
        # sid in filename, voltage not useful
        self.fout.write(s)
        self.fout.flush()

 
def sigint_handler(signum, frame):
    RUNNING = False
    for sid in sensors.keys():
        sensors[sid].fout.close()
    sys.exit()
 
        
if __name__=="__main__":
    global sensors
    sensors = {}
    xG = XiaomiGateway(ip_address, port, sid, key, discovery_retries, interface, proto=None)
    for dt in xG.devices.keys():
        logging.info('dt %s\n' % dt)
        for d in xG.devices[dt]:
            logging.info('%s\n' % d)
            if d['model'] == WSENSORID:
                sid = d['sid']
                xw = xweathersensor(drec=d,updateint = SAMPINT)
                sensors[sid] = xw
                xG.callbacks[sid].append(xw.writedat)
                # so a call to x.get_from_hub calling push_data will write out data
                logging.info('## Added weather sensor %s sid %s' % (d['model'],sid))
            else:
                logging.info('!! Not adding non-weather sensor %s sid %s' % (d['model'],sid))
    while RUNNING == True:
        for sid in sensors.keys():
            sidok = xG.get_from_hub(sid)
            if not sidok:
                logging.warning('### device SID %s not responding' % sid)
        time.sleep(SAMPINT)


