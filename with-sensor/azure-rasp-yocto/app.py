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


'''
humSensor = YHumidity.FindHumidity(target + '.humidity')
pressSensor = YPressure.FindPressure(target + '.pressure')
tempSensor = YTemperature.FindTemperature(target + '.temperature')

while m.isOnline():
    print('%2.1f' % tempSensor.get_currentValue() + "°C   " +
          "%4.0f" % pressSensor.get_currentValue() + "mb  " +
          "%4.0f" % humSensor.get_currentValue() + "% (Ctrl-c to stop)  ")
    YAPI.Sleep(1000)
YAPI.FreeAPI()
'''





# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
#CONNECTION_STRING = "HostName=i3-sg.azure-devices.net;DeviceId=raspberry;SharedAccessKey=ZLJdoJHoqOgmoNdXmJireqRGlIfPHl6UVQtURDcqMps="
AZURE_HOST_NAME = os.getenv('AZURE_HOST_NAME')
AZURE_DEVICE_ID = os.getenv('AZURE_DEVICE_ID')
AZURE_ACCESS_KEY = os.getenv('AZURE_ACCESS_KEY')
CONNECTION_STRING = "HostName=" + AZURE_HOST_NAME + ";" + "DeviceId=" + AZURE_DEVICE_ID + ";" + "SharedAccessKey=" + AZURE_ACCESS_KEY

# Define the JSON message to send to IoT Hub.
#TEMPERATURE = 20.0
#HUMIDITY = 60
humSensor = YHumidity.FindHumidity(target + '.humidity')
pressSensor = YPressure.FindPressure(target + '.pressure')
tempSensor = YTemperature.FindTemperature(target + '.temperature')
MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        #while True:
        while m.isOnline():
            # Build the message with simulated telemetry values.
            #temperature = TEMPERATURE + (random.random() * 15)
            #humidity = HUMIDITY + (random.random() * 20)
            temperature = tempSensor.get_currentValue()
            humidity = humSensor.get_currentValue()
            msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity)
            message = Message(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            if temperature > 30:
              message.custom_properties["temperatureAlert"] = "true"
            else:
              message.custom_properties["temperatureAlert"] = "false"
            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(1)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
