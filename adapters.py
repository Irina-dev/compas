import smbus		# import SMBus module of I2C
import math
from config import config

class CompassAdapter:

    def __init__(self):
        # some MPU6050 Registers and their Address
        self.__register_A = 0  # Address of Configuration register A
        self.__register_B = 0x01  # Address of configuration register B
        self.__register_mode = 0x02  # Address of mode register

        self.__x_axis_H = 0x03  # Address of X-axis MSB data register
        self.__z_axis_H = 0x05  # Address of Z-axis MSB data register
        self.__y_axis_H = 0x07  # Address of Y-axis MSB data register
        self.__pi = 3.14159265359  # define pi value

        self.__bus = smbus.SMBus(1)
        self.__declination = config.DECLINATION
        self.__device_address = config.DEVICE_ADDRESS

    def magnetometer_init(self):
        # write to Configuration Register A
        self.__bus.write_byte_data( self.__device_address, self.__register_A, 0x70)

        # Write to Configuration Register B for gain
        self.__bus.write_byte_data( self.__device_address, self.__register_B, 0xa0)

        # Write to mode Register for selecting mode
        self.__bus.write_byte_data( self.__device_address, self.__register_mode, 0)

    def read_raw_data(self, addr):
        # Read raw 16-bit value
        high = self.__bus.read_byte_data( self.__device_address, addr)
        low = self.__bus.read_byte_data( self.__device_address, addr + 1)

        # concatenate higher and lower value
        value = ((high << 8) | low)

        # to get signed value from module
        if (value > 32768):
            value = value - 65536
        return value

    def get_heading_angle(self):
        self.magnetometer_init()
        print(" Reading Heading Angle")

        while True:

            # Read Accelerometer raw value
            x = self.read_raw_data(self.__x_axis_H)
            z = self.read_raw_data(self.__z_axis_H)
            y = self.read_raw_data(self.__y_axis_H)

            heading = math.atan2(y, x) + self.__declination

            # Due to declination check for >360 degree
            if (heading > 2 * self.__pi):
                heading = heading - 2 * self.__pi

            # check for sign
            if (heading < 0):
                heading = heading + 2 * self.__pi

            # convert into angle
            return int(heading * 180 / self.__pi) # heading_angle