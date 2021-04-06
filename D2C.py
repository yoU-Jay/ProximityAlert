#libraries
import RPi.GPIO as GPIO
import time
from azure.iot.device import IoTHubDeviceClient, Message

#Primary Connection String
CONNECTION_STRING = "HostName=homeiot1111.azure-devices.net;DeviceId=myraspi;SharedAccessKey=OaqU6NKWtasDnm+YnoUco0mfLUkQrHbJexvTh/R5M9E="

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

MSG_TXT = '{{"distance":{distance}}}'

def iothub_client_init():
     client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
     return client

print ("Distance Measurement in progress")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def iothub_client_telemetry_sample_run():

 try:
   client = iothub_client_init()
   print ("IoT Hub device sending periodic messages, press Ctrl+C to exit")
   while True:

         GPIO.output(TRIG, False)
         print ("Waiting for sensor to settle")
         time.sleep(2)

         GPIO.output(TRIG, True)
         time.sleep(0.00001)
         GPIO.output(TRIG,False)

         while GPIO.input(ECHO) == 0:
          pulse_start = time.time()

         while GPIO.input(ECHO) == 1:
          pulse_end = time.time()

         pulse_duration = pulse_end - pulse_start

         distance = pulse_duration * 17150

         distance = round(distance, 2)   ## Distance recorded by the sensor
         msg_txt_formatted = MSG_TXT.format(distance=distance)
         message = Message(msg_txt_formatted)

         if distance < 5.00:
           message.custom_properties["distanceAlert"] = "true"
           print("YES")
         else:
           message.custom_properties["distanceAlert"] = "false"
           print("NO")
        # print ("Sending message: {}".format(message))
         for property in vars(message).items():
            if all(property):
                 print("     {0}".format(property))
         client.send_message(message)
         print ("Message sent")
         time.sleep(3)
         print ("Distance:",distance,"cm")

 except KeyboardInterrupt:
   print("Cleaning up!")
   GPIO.cleanup()

if __name__ == '__main__':
      print ("IoT Hub Quickstart ")
      print ("ctrlcto exit")
      iothub_client_telemetry_sample_run()