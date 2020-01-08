import RPi.GPIO as GPIO
from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
import time

# Pins for Motor Driver Inputs
Motor1A = 24
Motor1B = 23
Motor2A = 25
Motor2B = 20
# Pins for the ultrasonic sensor
GPIO_TRIGGER = 18
GPIO_ECHO = 27
# Pins for RF receiver
RADIOA = 5
RADIOB = 6
RADIOC = 13
RADIOD = 19
# Pin for motion sensor
MOTION_PIN = 4

#obstacle detection flag
global forward_flag
forwardflag = 1

pir = MotionSensor(4)
camera = PiCamera()

def setup():    
    GPIO.setmode(GPIO.BCM) # GPIO Numbering
    GPIO.setwarnings(False)
    GPIO.setup(Motor1A,GPIO.OUT) # All pins as Outputs
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor2A,GPIO.OUT) # All pins as Outputs
    GPIO.setup(Motor2B,GPIO.OUT)
    GPIO.setup(RADIOA,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(RADIOB,GPIO.IN)
    GPIO.setup(RADIOC,GPIO.IN)
    GPIO.setup(RADIOD,GPIO.IN)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(MOTION_PIN, GPIO.IN)
    
   
    # motor control function 
def left(channel):
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    time.sleep(0.4)
    # small sleep value for accuate turn function
    stop()

    # motor control function 
def right(channel):
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    time.sleep(0.4)
    stop()

    # motor control function
def forward(channel):
    global forward_flag
    if forward_flag == 1:
    # flag for obstacle detection
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
    time.sleep(1)
    stop()    

    # motor control function 
def backward(channel):
    global backward_flag
    backward_flag = 1
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    time.sleep(1)
    stop()
    
    # motor control function
def stop():
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    stop_flag=1;
    status=0
#    GPIO.cleanup()
#    setup()
#    GPIO.input(RADIOA,GPIO.LOW)
#    time.sleep(1)

    
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance    
    


def motion_detect(channel):
    stop()
    now = datetime.now()
    filename = "{0:%Y}-{0:%m}-{0:%d}---{0:%X}.h264".format(now)
    pir.wait_for_motion()    
#    camera.start_preview()
#    pir.wait_for_no_motion()
#    camera.stop_preview()
    camera.start_recording(filename)
    time.sleep(15)
    #pir.wait_for_no_motion()  
    camera.stop_recording()
    print("Motion detected!")

def my_callback(channel):
    # Here, alternatively, an application / command etc. can be started.
    print('There was a movement!')


if __name__ == '__main__': # Program start from here
    setup()

try: # RF signal detection and corresponding motor control function call
    GPIO.add_event_detect(RADIOA, GPIO.RISING, callback=forward)

    GPIO.add_event_detect(RADIOB, GPIO.RISING, callback=backward)
 
    GPIO.add_event_detect(RADIOC, GPIO.RISING, callback=right)

    GPIO.add_event_detect(RADIOD, GPIO.RISING, callback=left)

    GPIO.add_event_detect(MOTION_PIN , GPIO.RISING, callback=motion_detect)
          
    while True:   
        dist = distance()
        print ("Measured Distance = %.1f cm" % dist)
        # print the exact obstacle distance for the user information
        if (dist <= 100):
            stop()

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup() 
     # clear pins set



    

