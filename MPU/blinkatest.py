import board
import busio

print("Hello! ")

i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok")


