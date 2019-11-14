''' NOTES 
ACCEL_RANGE_2G = 0x00
ACCEL_RANGE_4G = 0x08
ACCEL_RANGE_8G = 0x10
ACCEL_RANGE_16G = 0x1
ACCEL_SCALE_MODIFIER_2G = 16384.0
ACCEL_SCALE_MODIFIER_4G = 8192.0
ACCEL_SCALE_MODIFIER_8G = 4096.0
ACCEL_SCALE_MODIFIER_16G = 2048.0
ACCEL_XOUT0 = 0x3B
ACCEL_YOUT0 = 0x3D
ACCEL_ZOUT0 = 0x3F
'''    
#===============================================================================

#import os
#import datetime
#import gzip as gz
#import pandas as pd

import smbus
import time
import pigpio
import timeit
import numpy as np
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
def servo_leitura(ndt, t, A, df):
    filename = datetime.datetime.now().strftime('%Y-%m-%d__%H-%M-%S.csv.gz')
    print('Acquiring: ' + filename)
    
    data = np.zeros((ndt))
    t    = np.zeros(ndt)
    t0   = time.time()
    
    for i in range (ndt):
        t[i]      = time.time() - t0
        a =read_data(MPU, 0x3d)/8192
        data[i] = a
        if abs(a)>df:
            s = (((middle+A)-(middle-A))*a+4*((middle+A)+(middle-A)))/8
            cs= (((middle+A)-(middle-A))*a-4*((middle+A)+(middle-A)))/-8
            pi.set_servo_pulsewidth(4, s)
    print('Writing valid file...')

    DFrame = pd.DataFrame(data    =   data.T,
                          columns = ['az'],
                          index   =   t  )

    with gz.open(dirname+filename,'wt') as file:
        DFrame.to_csv(file)
              
    print('... done!')

##############SEGUNDA TENTATIVA##############
def servo2(t_total, t_max, A, lim_inf, z, fn):
#Decremento Logarítmico    
    n=435
    w=2*np.pi*fn
    x = np.linspace(0,t_max,int(n*t_max))
    dec = np.e**-(z*w*x)

#Leitura do Sensor
    t0=time.time()
    dif=0
    
    while dif<t_total:
        
        #A_aux=A    
        a = read_data(MPU, 0x3d)/8192
        if abs(a)>lim_inf:
            t1=time.time()
            for i in range (int(n*t_max)):
                A_aux = A*dec[i]
                #print ("Amplitude:",A_aux)
                
                a = read_data(MPU, 0x3d)/8192
                s = (((middle+A_aux)-(middle-A_aux))*a+4*((middle+A_aux)+(middle-A_aux)))/8
                pi.set_servo_pulsewidth(4, s)
                print (a)
                #dif=time.time()-t0
                #print (A_aux)
                #print (dec[i])
            t2=time.time()
            print (t2-t1)


##############TERCEIRA TENTATIVA############## 
def servo3(t_total, t_max, A, lim_inf, z, fn):
#Decremento Logarítmico    
    n=435
    w=2*np.pi*fn
    x = np.linspace(0,t_max,int(n*t_max))
    dec = np.exp(-(z*w*x))

#Leitura do Sensor
    t0=time.time()
    dif=0
    
    while dif<t_total:
        a = read_data(MPU, 0x3d)/8192
        if abs(a)>lim_inf:
            for i in range (int(n*t_max)):
                
                a = read_data(MPU, 0x3d)/8192
                if a<-lim_inf:
                    A_aux = A*dec[i]
                    s = (middle-A_aux)
                    pi.set_servo_pulsewidth(4, s)
                    print (A_aux)
                elif a>lim_inf:
                    A_aux = A*dec[i]
                    s = (middle+A_aux)
                    pi.set_servo_pulsewidth(4, s)
                    print (A_aux)
                else:
                    pi.set_servo_pulsewidth(4, middle)
        dif=time.time()-t0






##############QUARTA TENTATIVA############## 
def servo4(t_total, t_max, A, lim_inf, z, fn):
#Decremento Logarítmico    
    n=435
    w=2*np.pi*fn
    x = np.linspace(0,t_max,int(n*t_max))
    dec = np.exp(-(z*w*x))

#Leitura do Sensor
    t0=time.time()
    dif=0
    
    while dif<t_total:
        a = read_data(MPU, 0x3d)/8192
        if abs(a)>lim_inf:
                        
            for i in range (int(n*t_max)):
            
                a1=read_data(MPU, 0x3d)/8192
                a2=read_data(MPU, 0x3d)/8192
            
            
                a = read_data(MPU, 0x3d)/8192
                if a1<a2:
                    A_aux = A*dec[i]
                    s = (middle-A_aux)
                    pi.set_servo_pulsewidth(4, s)
                    print (A_aux)
                elif a1>a2:
                    A_aux = A*dec[i]
                    s = (middle+A_aux)
                    pi.set_servo_pulsewidth(4, s)
                    print (A_aux)
                else:
                    pi.set_servo_pulsewidth(4, middle)
        dif=time.time()-t0




#############PRIMEIRA TENTATIVA##############
def servo1(ndt, t, A, df):

    for i in range (ndt):
        a =read_data(MPU, 0x3d)/8192
        if abs(a)>df:
            s = (((middle+A)-(middle-A))*a+4*((middle+A)+(middle-A)))/8
            cs= (((middle+A)-(middle-A))*a-4*((middle+A)+(middle-A)))/-8
            pi.set_servo_pulsewidth(4, s)
        else:
            pi.set_servo_pulsewidth(4, middle)



#===============================================================================
#===============================================================================
#===============================================================================

# Create I2C bus
bus = smbus.SMBus(1)
MPU = 0x68

# Now wake up the 6050 up as it starts in sleep mode
bus.write_byte_data(MPU, 0x6b, 0)
# Changing the scale
bus.write_byte_data(MPU, 0x1C, 0x08)

pi = pigpio.pi() # Connect to local Pi.

# set gpio modes
pi.set_mode(4, pigpio.OUTPUT)

# Set servo limits
left=600
right=2300
middle=(left+right)/2

# Initial position - Middle
pi.set_servo_pulsewidth(4, middle)
time.sleep(2)

#===============================================================================
ndt =25000   # Number of cycles
t = 0.0       # Delay
A = 900       # Range
df =.5      # Down filter
#F=2000
#dirname = '/home/pi/Desktop/FinalProject/'
#servo_leitura (ndt, t, A, df)
servo1(ndt,t,A,df)

t_total=50
t_max=2
A=800
lim_inf=.2
z=0.12
fn = 10
#servo1(t_total, t_max, A, lim_inf, z, fn)

#===============================================================================
pi.set_servo_pulsewidth(4, 0) # stop servo pulses
pi.set_PWM_dutycycle(4, 0) # stop PWM
pi.stop() # terminate connection and release resources