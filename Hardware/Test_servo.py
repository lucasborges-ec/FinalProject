import time
import pigpio
import os
import smbus
import time
import datetime
import gzip as gz
import numpy as np
import pandas as pd
import RPi.GPIO as gpio


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


def read_data(MPU, addr):
    high = bus.read_byte_data(MPU, addr  )
    low  = bus.read_byte_data(MPU, addr+1)

    val  = (high << 8) + low

    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

#===============================================================================

def acquire(ndt):
    
    filename = datetime.datetime.now().strftime('%Y-%m-%d__%H-%M-%S.csv.gz')
    print('Acquiring: ' + filename)
    
    data = np.zeros((ndt), dtype='int'  )
    t    = np.zeros(ndt)
    t0   = time.time()

    for i in range(ndt):

        t[i]      = time.time() - t0
        #Acelerômetro
        data[i] = read_data(MPU, 0x3b)
#        data[1,i] = read_data(MPU, 0x3d)
 #       data[i] = read_data(MPU, 0x3f)
        #Giroscópio
#        data[3,i] = read_data(MPU, 0x43)
#        data[4,i] = read_data(MPU, 0x45)
#        data[5,i] = read_data(MPU, 0x47)
    
   # print('... done! ({0}s, {1}Hz)'.format(int(Td), int(fs)))

n = 15     #Number of cycles
t = .1     #Sleep time
A = 800
d = 0
for i in range (n):
    pi.set_servo_pulsewidth(4, middle-A+d*i)
    time.sleep(t)
    pi.set_servo_pulsewidth(4, middle+A-d*i)
    time.sleep(2*t)
    pi.set_servo_pulsewidth(4, middle)
    time.sleep(t)





    print('Writing valid file...')

    DFrame = pd.DataFrame(data    =   data.T,
                          columns = ['az'],
                          index   =   t  )

    with gz.open(dirname+filename,'wt') as file:
        DFrame.to_csv(file)
              
    print('... done!')
    return t, data

#===============================================================================
#===============================================================================
#===============================================================================

# Create I2C bus
bus = smbus.SMBus(1)
MPU = 0x68

# Now wake up the 6050 up as it starts in sleep mode
bus.write_byte_data(MPU, 0x6b, 0)

#===============================================================================

ndt     = 7000
dirname = '/home/pi/Desktop/FinalProject/'
t, data = acquire(ndt)

#===============================================================================


### Harmonic Excitation

pi.set_servo_pulsewidth(4, 0) # stop servo pulses

pi.set_PWM_dutycycle(4, 0) # stop PWM

pi.stop() # term