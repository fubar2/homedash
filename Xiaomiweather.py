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
import Xiaomiweatherconfig as settings # neat trick - put config there
logging.basicConfig(filename=settings.LOGFNAME,level=logging.INFO)

from xiaomi_gateway import XiaomiGateway

global RUNNING
RUNNING = True
SAMPINT = settings.SAMPINT # sleep seconds between read loops



class Xweathersensor():
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

    def __init__(self,drec,updateint,xid):
        self.HEADER = 'time\ttemp\thumidity\tpressure\n'
        self.sid = drec['sid']
        self.updateint = updateint
        self.tdinit = time.strftime('%H%M%S_%d%m%Y')
        self.outfname = '%s_%s_%d.xls' % (xid.split('.')[0],self.sid,self.updateint)
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
    xG = XiaomiGateway(settings.IP_ADDRESS, settings.PORT, settings.SID,
       settings.KEY, settings.DISCOVERY_RETRIES, settings.INTERFACE, proto=None)
    for dt in xG.devices.keys():
        logging.info('device types %s found\n' % dt)
        for d in xG.devices[dt]:
            logging.info('%s\n' % d)
            foundSid = d['sid']
            if d['model'] in settings.XSENSORIDS: # YMMV - I only have weather sensors
                xw = Xweathersensor(drec=d,updateint = settings.SAMPINT,xid = d['model'])
                sensors[foundSid] = xw
                xG.callbacks[foundSid].append(xw.writedat)
                # so a call to x.get_from_hub calling push_data will write out data
                logging.info('## Added weather sensor %s sid %s' % (d['model'],foundSid))
            else:
                logging.info('!! Not adding non-weather sensor %s sid %s' % (d['model'],foundSid))
    while RUNNING == True:
        for sid in sensors.keys():
            sidok = xG.get_from_hub(sid)
            if not sidok:
                logging.warning('### device SID %s not responding' % sid)
        time.sleep(settings.SAMPINT)


