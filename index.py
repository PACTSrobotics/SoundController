import RPi.GPIO as GPIO
import time
import yaml
import socket

# Loads config, pins
cfg = yaml.safe_load(open("./soundController.yml"))
pins = cfg["robots"]["dalek"]

LOCAL_IP = "192.168.8.198"
LOCAL_PORT = 5005
UDP_IP = cfg["server"]["address"] # Dalek's IP
UDP_PORT = cfg["server"]["port"] 

sock = socket.socket(socket.AF_INET, # InternetUDP_IP, UDP_PORT)
                     socket.SOCK_DGRAM) # UDP
sock.bind((LOCAL_IP, LOCAL_PORT))

timeout = False

GPIO.setwarnings(False) #waRNinGS mORe LIKe big DUmb
GPIO.setmode(GPIO.BOARD)

# Makes messages look nice
def formatMessage(soundName):
    return '{"commands":{"playsound":"' + soundName + '"}}'


def onclick(channel):
    global timeout
    if timeout:
        return
    soundName = pins[channel]
    if not soundName:
        return #Not all buttons are used
    message = formatMessage(soundName)
    sock.sendto(str.encode(message), (UDP_IP, UDP_PORT))
    timeout = True
    time.sleep(0.5)  #No more than 1 input per 0.5 sec
    timeout = False

for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=onclick)

message = input("Press enter to quit\n\n")
GPIO.cleanup()