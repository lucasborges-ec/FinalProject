#===============================================================================

import os
import smbus
import time
import datetime
import gzip as gz
import numpy as np
import pandas as pd
import RPi.GPIO as gpio

#===============================================================================
#===============================================================================
#addr = 0x68 


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
    
    data = np.zeros((6,ndt), dtype='int'  )
    t    = np.zeros(ndt)
    t0   = time.time()

    for i in range(ndt):

        t[i]      = time.time() - t0
        #Acelerômetro
        data[0,i] = read_data(MPU, 0x3b)
        data[1,i] = read_data(MPU, 0x3d)
        data[2,i] = read_data(MPU, 0x3f)
        #Giroscópio
        data[3,i] = read_data(MPU, 0x43)
        data[4,i] = read_data(MPU, 0x45)
        data[5,i] = read_data(MPU, 0x47)
    
   # print('... done! ({0}s, {1}Hz)'.format(int(Td), int(fs)))

    print('Writing valid file...')

    DFrame = pd.DataFrame(data    =   data.T,
                          columns = ['ax','ay','az','gx','gy','gz'],
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

ndt     = 10
dirname = '/home/pi/Desktop/FinalProject/'
t, data = acquire(ndt)

#===============================================================================

