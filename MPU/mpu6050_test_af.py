import time
import board
import adafruit_mpu6050 as a_mpu
import matplotlib.pyplot as plt




i2c = board.I2C()
mpu = a_mpu.MPU6050(i2c)
acc_x = []
acc_y = []
acc_z = []
gyro_x = []
gyro_y = []
gyro_z = []
temp = []

i=0

try:
    print("Starting... ")
    while i<200:
        acc_x.append(mpu.acceleration[0])
        acc_y.append(mpu.acceleration[1])
        acc_z.append(mpu.acceleration[2])
        gyro_x.append(mpu.gyro[0])
        gyro_y.append(mpu.gyro[1])
        gyro_z.append(mpu.gyro[2])
        temp.append(mpu.temperature)
        #print("Acceleration: X:%.2f, Y:%.2f, Z:%.2f m/s^2" % (mpu.acceleration))
        #print("Gyro: X:%.2f, Y:%.2f, Z:%.2f rad/s" % (mpu.gyro))
        #print("Temperature: %.2fC" % (mpu.temperature))
        print(i)
        i += 1
        #time.sleep(1)
except KeyboardInterrupt:
    pass


plt.plot(acc_x, color='red')
plt.plot(acc_y, color = 'blue')
plt.plot(acc_z, color = 'yellow')
plt.title("Acc")
plt.show()

plt.plot(gyro_x, color='red')
plt.plot(gyro_y, color = 'blue')
plt.plot(gyro_z, color = 'yellow')
plt.title("Gyro")
plt.show()

print("Dome")


