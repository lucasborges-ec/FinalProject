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
def servo(ndt, t):
    for i in range (ndt):
        a = read_data(MPU, 0x3F)/8192
        if a>.6:
            s = ((right-left)*a+4*(right+left))/8
            cs= ((right-left)*a-4*(right+left))/-8
            pi.set_servo_pulsewidth(4, cs)
            time.sleep(t)
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
left=1100
right=1800
middle=(left+right)/2

# Initial position - Middle
pi.set_servo_pulsewidth(4, middle)
time.sleep(1.5)



#===============================================================================
t = 0.0
ndt     = 20000
#t, data = acquire(ndt)
servo (ndt, t)
#===============================================================================

pi.set_servo_pulsewidth(4, 0) # stop servo pulses

pi.set_PWM_dutycycle(4, 0) # stop PWM

pi.stop() # terminate connection and release resources