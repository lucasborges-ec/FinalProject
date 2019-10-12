## Execute PIGPIO DAEMON
## sudo pigpiod
##

import time
import pigpio

pi = pigpio.pi() # Connect to local Pi.

# set gpio modes

pi.set_mode(4, pigpio.OUTPUT)

# Set servo limits
left=550
right=2325
middle=(left+right)/2

# Initial position - Middle
pi.set_servo_pulsewidth(4, middle)
time.sleep(1)





### Harmonic Excitation
n = 25     #Number of cycles
t = .1     #Sleep time
A = 500
d = 0
for i in range (n):
    pi.set_servo_pulsewidth(4, middle-A+d*i)
    time.sleep(t)
    pi.set_servo_pulsewidth(4, middle+A-d*i)
    time.sleep(2*t)
    pi.set_servo_pulsewidth(4, middle)
    time.sleep(t)

### Working with increments
n = 0
step = 100
A = int((right-middle)/step)
t = .1
for l in range (n):
    for i in range (A):
        a = middle + step*i
        pi.set_servo_pulsewidth(4, a)
        time.sleep(t)    
    for j in range (2*A):
        b = a - step*j
        pi.set_servo_pulsewidth(4, b)
        time.sleep(t)    
    for k in range (A):
        c = b + step*k
        pi.set_servo_pulsewidth(4, c)
        time.sleep(t)    


# start 75% dutycycle PWM on gpio17

#pi.set_PWM_dutycycle(17, 192) # 192/255 = 75%

#start = time.time()

#while (time.time() - start) < 60.0:

#      pi.write(18, 1) # on

#      time.sleep(0.5)

#      pi.write(18, 0) # off

#      time.sleep(0.5)

      # mirror gpio24 from gpio23

#      pi.write(24, pi.read(23))

pi.set_servo_pulsewidth(4, 0) # stop servo pulses

pi.set_PWM_dutycycle(4, 0) # stop PWM

pi.stop() # terminate connection and release resources