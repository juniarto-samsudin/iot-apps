import paho.mqtt.client as mqtt
import simplejson as json
import time
import random
import os

#THINGSBOARD_HOST = "vaultsonchain.com"
#ACCESS_TOKEN="gGK3JTtol0gkcWdAbjjg"
THINGSBOARD_HOST = os.getenv('THINGSBOARD_HOST')
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
TEMPERATURE = 20
#msg={"name": 4444.0}

while loop_flag:
    temperature = TEMPERATURE + (random.random() *15)
    msg = {"temperature": temperature}
    client.publish('v1/devices/me/telemetry', json.dumps(msg, use_decimal=True), 1, retain=True)
    time.sleep(10)

'''
while loop_flag == 1:
    print("waiting for publish callback to occur : ", counter)
    time.sleep(.001)
    counter+=1
'''
