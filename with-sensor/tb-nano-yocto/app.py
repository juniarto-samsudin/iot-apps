import os, sys

from yoctopuce.yocto_api import *
from yoctopuce.yocto_humidity import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_pressure import *

def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>')
    print(scriptname + ' <logical_name>')
    print(scriptname + ' any  ')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


errmsg = YRefParam()

'''
if len(sys.argv) < 2:
    usage()

target = sys.argv[1]
'''

#target = 'METEOMK1-90AF6'
target = os.getenv('SENSOR_SN')

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'any':
    # retreive any humidity sensor
    sensor = YHumidity.FirstHumidity()
    if sensor is None:
        die('No module connected')
    m = sensor.get_module()
    target = m.get_serialNumber()

else:
    m = YModule.FindModule(target)

if not m.isOnline():
    die('device not connected')









import paho.mqtt.client as mqtt
import simplejson as json
import time
import random
import os

THINGSBOARD_HOST = os.getenv('THINGSBOARD_HOST')
#ACCESS_TOKEN="tTkrnM9PZRlNYM8nPaQW"
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code :" + str(rc))

def on_message(client, userdata, msg):
    print("sent")
'''
def on_publish(client, userdata, result):
    print("publish: ", result)
    global loop_flag
    loop_flag=0
    client.loop_stop()
    client.disconnect()
'''


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.on_publish = on_publish
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 8080, 60)
print("after connect")

client.loop_start()


loop_flag=1
counter = 0
#TEMPERATURE = 20
TEMPERATURE= YTemperature.FindTemperature(target + '.temperature')
#msg={"name": 1234.0}

#while loop_flag:
while m.isOnline():
    #temperature = TEMPERATURE + (random.random() *15)
    temperature = TEMPERATURE.get_currentValue()
    msg = {"temperature": temperature}
    client.publish('v1/devices/me/telemetry', json.dumps(msg, use_decimal=True), 1, retain=True)
    time.sleep(10)

'''
while loop_flag == 1:
    print("waiting for publish callback to occur : ", counter)
    time.sleep(.001)
    counter+=1
'''
