import RPi.GPIO as GPIO
import time
import timeit
import numpy as np

GPIO.cleanup()
#Pins identification
GPIO.setmode(GPIO.BOARD)

#Pins that are going to control de module
ControlPin=[7,11,13,15]

#Initial Parameters

A = 10 ## Amplitude [steps]
#f = 10  ## Excitation Frequency [Hz]


#Number of cycles
n=100

#Wainting time
t=.001
for pin in ControlPin:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)

#Counterclockwise
seq_half1 = [[1,0,0,0],
             [1,1,0,0],
             [0,1,0,0],
             [0,1,1,0],
             [0,0,1,0],
             [0,0,1,1],
             [0,0,0,1],
             [1,0,0,1]]
#Clockwise
seq_half2 = [[0,0,0,1],
             [0,0,1,1],
             [0,0,1,0],
             [0,1,1,0],
             [0,1,0,0],
             [1,1,0,0],
             [1,0,0,0],
             [1,0,0,1]]

start=np.zeros(n)
end=np.zeros(n)

for j in range (n):
    start[j]=timeit.default_timer()    
    
    for i in range(A): ##Spin range (512 for one turn)
        for halfstep in range(8): ##Number of lines in array
            for pin in range (4): ##Number of pins
                GPIO.output(ControlPin[pin], seq_half1[halfstep][pin])
            time.sleep(t) ##Time Delay

    for i in range(2*A): ##Spin range (512 for one turn)
        for halfstep in range(8): ##Number of lines in array
            for pin in range (4): ##Number of pins
                GPIO.output(ControlPin[pin], seq_half2[halfstep][pin])
            time.sleep(t) ##Time Delay
            
    for i in range(A): ##Spin range (512 for one turn)
        for halfstep in range(8): ##Number of lines in array
            for pin in range (4): ##Number of pins
                GPIO.output(ControlPin[pin], seq_half1[halfstep][pin])
            time.sleep(t) ##Time Delay
    end[j]=timeit.default_timer()

GPIO.cleanup()

total_time=end-start
mean=np.mean(total_time)
f=1/(mean)

print ("The number of cycles is: {0:4.2f}".format(n))
print ("The time for 1 cycle is: {0:4.8f}s".format(mean))
print ("The frequency is: {0:4.2f}Hz".format(f))
print ("The lag time per step is:", mean/(A*4*8))
