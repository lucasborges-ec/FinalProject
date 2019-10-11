#===============================================================================

import os
import smbus
import time
import datetime
import gzip as gz
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import RPi.GPIO as gpio

#===============================================================================
#===============================================================================


def read_data(MPU, addr):
    high = bus.read_byte_data(MPU, addr  )
    low  = bus.read_byte_data(MPU, addr+1)

    val  = (high << 8) + low

    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

#===============================================================================

def plot(ndt):
    data = np.zeros((ndt), dtype='int'  )
    t    = np.zeros(ndt)
    t0   = time.time()

    for i in range(ndt):

        t[i]      = time.time() - t0
        #Acelerômetro
        data[i] = read_data(MPU, 0x3f)
        
        plt.figure(1, figsize=(8, 4), clear=True)
        plt.plot(t, data)

        #plt.xlim( 0, 10);
        plt.xlabel('time (s)') 
        #plt.ylim(-2,  2);
        plt.ylabel('a(t)') 

        plt.grid(True) 
        
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

ndt     = 50
t, data = plot(ndt)

#===============================================================================

