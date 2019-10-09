import RPi.GPIO as GPIO
import time
GPIO.cleanup()
#Pins identification
GPIO.setmode(GPIO.BOARD)

#Pins that are going to control de module
ControlPin=[7,11,13,15]

#Number of cycles
n=1
n2=1

#Wainting time
t=.001
for pin in ControlPin:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)
#Counterclockwise
    
## Single Phase Stepping
seq_single1=[[1,0,0,0],
             [0,1,0,0],
             [0,0,1,0],
             [0,0,0,1]]
## Dual Phase Stepping
seq_dual1 = [[1,0,0,1],
             [1,1,0,0],
             [0,1,1,0],
             [0,0,1,1]]


seq_half1 = [[1,0,0,0],
             [1,1,0,0],
             [0,1,0,0],
             [0,1,1,0],
             [0,0,1,0],
             [0,0,1,1],
             [0,0,0,1],
             [1,0,0,1]]

#Clockwise
## Single Phase Stepping
seq_single2=[[0,0,0,1],
             [0,0,1,0],
             [0,1,0,0],
             [1,0,0,0]]
## Dual Phase Stepping
seq_dual2 = [[0,0,1,1],
             [0,1,1,0],
             [1,1,0,0],
             [1,0,0,1]]
## Half Stepping
seq_half2 = [[1,0,0,1],
             [0,0,0,1],
             [0,0,1,1],
             [0,0,1,0],
             [0,1,1,0],
             [0,1,0,0],
             [1,1,0,0],
             [1,0,0,0]]
for i in range (10):
##Spin range (512 for one turn)    
    for i in range(n*20):
        ##Number of lines in array
        for halfstep in range(8):
            ##Number of pins
            for pin in range (4):
                GPIO.output(ControlPin[pin], seq_half1[halfstep][pin])
            ##Time Delay
            time.sleep(t)
            
    for i in range(n2*20):
        for halfstep in range(8):
            for pin in range (4):
                GPIO.output(ControlPin[pin], seq_half2[halfstep][pin])
            time.sleep(t) 
GPIO.cleanup()

