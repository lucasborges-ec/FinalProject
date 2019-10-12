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
def servo(ndt, t, A, df):
    for i in range (ndt):
        a = read_data(MPU, 0x3F)/8192
        if a>df:
            s = (((middle+A)-(middle-A))*a+4*((middle+A)+(middle-A)))/8
            cs= (((middle+A)-(middle-A))*a-4*((middle+A)+(middle-A)))/-8
            pi.set_servo_pulsewidth(4, cs)
            time.sleep(t)
            
def harmonic (nc, f):
    Tm= 1/f
    n = int(Tm/0.001)
    t = np.linspace(0,Tm,n)
    a = np.sin(2*np.pi*f*t)
#    start=np.zeros(n)
#    end=np.zeros(n)
    for i in range (nc):
        for i in range (n):
            a = 4*np.sin(2*np.pi*f*t[i])
            s = (((middle+A)-(middle-A))*a+4*((middle+A)+(middle-A)))/8
            pi.set_servo_pulsewidth(4, s)

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
left=500
right=2400
middle=(left+right)/2

# Initial position - Middle
pi.set_servo_pulsewidth(4, middle)
time.sleep(1.5)

#===============================================================================
ndt = 0000   # Number of cycles
t = 0.0       # Delay
A = 500       # Range
df = 0.3      # Down filter

servo (ndt, t, A, df)

#===============================================================================
nc = 0
f = 5
harmonic (nc, f)


#===============================================================================

pi.set_servo_pulsewidth(4, 0) # stop servo pulses
pi.set_PWM_dutycycle(4, 0) # stop PWM
pi.stop() # terminate connection and release resources