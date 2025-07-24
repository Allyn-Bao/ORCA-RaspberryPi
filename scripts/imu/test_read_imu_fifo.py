"""
WIP -- won't work yet!
Basic test for reading useful data from FIFO on IMU breakout via I2C
    (Should be done using interrupt pin to indicate data ready, wherein
     all data will be read from FIFO in one burst.)
"""

import smbus2
import numpy as np
import time

# Register constants (for cleanliness)
# (from the datasheet, pg 36 on: https://invensense.tdk.com/wp-content/uploads/2024/03/DS-000189-ICM-20948-v1.6.pdf)
WHOAMI_ADDR = 0x00              # WHOAMI (0xEA, can be read as sanity check)

FIFO_EN_2_ADDR = 0x67           # FIFO_EN_2 write required to store ACCEL and GYRO data in FIFO
FIFO_COUNT_ADDR = 0x71          # FIFO_COUNTL indicates number of valid bytes in FIFO
FIFO_R_W_ADDR = 0x72            # FIFO_R_W gives access to FIFO (so read it from here!)
DATA_RDY_STATUS_ADDR = 0x74     # DATA_RDY_STATUS bit 0 indicates whether data was copied from FIFO
FIFO_CFG_ADDR = 0x76

# PWR_MGMT writes required to wake device and enable ACCEL/GYRO
PWR_MGMT_1 = 0x06
PWR_MGMT_2 = 0x07

# Data registers for accel and gyro
ACCEL_XOUT_H_ADDR = 0x2D
ACCEL_XOUT_L_ADDR = 0x2E
ACCEL_YOUT_H_ADDR = 0x2F
ACCEL_YOUT_L_ADDR = 0x30
ACCEL_ZOUT_H_ADDR = 0x31
ACCEL_ZOUT_L_ADDR = 0x32
GYRO_XOUT_H_ADDR = 0x33
GYRO_XOUT_L_ADDR = 0x34
GYRO_YOUT_H_ADDR = 0x35
GYRO_YOUT_L_ADDR = 0x36
GYRO_ZOUT_H_ADDR = 0x37
GYRO_ZOUT_L_ADDR = 0x38

# Config registers for accel and gyro (in user bank 2)
GYRO_CONFIG_1_ADDR = 0x01
ACCEL_CONFIG_ADDR = 0x14

# Slave device address is 0x69 (since ICM20948 AD0 is left floating)
DEV_ADDR = 0x69

# Bits 5:4 can be written to select user bank
REG_BANK_SEL_ADDR = 0x7F

try:
    f = open("imu_data.txt", "w")

    # Init I2C struct (smbus2) assuming default I2C channel
    bus = smbus2.SMBus(bus="/dev/i2c-1")

    # Sanity check -- should read as 0xEA
    whoami_result = bus.read_byte_data(DEV_ADDR, WHOAMI_ADDR)
    print(f"Read from WHOAMI register {WHOAMI_ADDR:#04x}: {whoami_result}")

    # Enable FIFO write of ACCEL and GYRO data
    result = bus.read_i2c_block_data(DEV_ADDR, WHOAMI_ADDR, 1)

    # Wake chip from sleep mode (so we can poll the accel gyro data)
    # (bits 7:6 of PWR_MGMT_2 are reserved, so bitwise OR -- don't touch them)
    bus.write_byte_data(DEV_ADDR, PWR_MGMT_1, 0x01)

    cur_pwr_mgmt_2 = bus.read_byte_data(DEV_ADDR, PWR_MGMT_2)
    bus.write_byte_data(DEV_ADDR, PWR_MGMT_2, cur_pwr_mgmt_2 | 0b00000000)

    # Configure accel and gyro FSR (must be known to convert raw values into usable data)
    # (we'll go with accel FSR = +-2 g, gyro FSR = +-250 dps)
    cur_reg_bank_sel = bus.read_byte_data(DEV_ADDR, REG_BANK_SEL_ADDR)
    bus.write_byte_data(DEV_ADDR, REG_BANK_SEL_ADDR, cur_reg_bank_sel | 0b00100000)

    cur_accel_config = bus.read_byte_data(DEV_ADDR, ACCEL_CONFIG_ADDR)
    bus.write_byte_data(DEV_ADDR, ACCEL_CONFIG_ADDR, cur_accel_config & 0b11111001)
    cur_gyro_config = bus.read_byte_data(DEV_ADDR, GYRO_CONFIG_1_ADDR)
    bus.write_byte_data(DEV_ADDR, GYRO_CONFIG_1_ADDR, cur_gyro_config & 0b11111001)
    accel_fsr = 2.0
    gyro_fsr = 250.0

    cur_reg_bank_sel = bus.read_byte_data(DEV_ADDR, REG_BANK_SEL_ADDR)
    bus.write_byte_data(DEV_ADDR, REG_BANK_SEL_ADDR, cur_reg_bank_sel & 0b11001111)

    while (1):
        raw_accel_arr = np.zeros(3, dtype=np.int16)
        raw_gyro_arr = np.zeros(3, dtype=np.int16)
        processed_accel_arr = np.zeros(3, dtype=np.float64)
        processed_gyro_arr = np.zeros(3, dtype=np.float64)
        
        # Read raw accel via i2c
        raw_accel_arr[0] |= bus.read_byte_data(DEV_ADDR, ACCEL_XOUT_H_ADDR) << 8
        raw_accel_arr[0] |= bus.read_byte_data(DEV_ADDR, ACCEL_XOUT_L_ADDR)
        raw_accel_arr[1] |= bus.read_byte_data(DEV_ADDR, ACCEL_YOUT_H_ADDR) << 8
        raw_accel_arr[1] |= bus.read_byte_data(DEV_ADDR, ACCEL_YOUT_L_ADDR)
        raw_accel_arr[2] |= bus.read_byte_data(DEV_ADDR, ACCEL_ZOUT_H_ADDR) << 8
        raw_accel_arr[2] |= bus.read_byte_data(DEV_ADDR, ACCEL_ZOUT_L_ADDR)

        # Read raw gyro via i2c
        raw_gyro_arr[0] |= bus.read_byte_data(DEV_ADDR, GYRO_XOUT_H_ADDR) << 8
        raw_gyro_arr[0] |= bus.read_byte_data(DEV_ADDR, GYRO_XOUT_L_ADDR)
        raw_gyro_arr[1] |= bus.read_byte_data(DEV_ADDR, GYRO_YOUT_H_ADDR) << 8
        raw_gyro_arr[1] |= bus.read_byte_data(DEV_ADDR, GYRO_YOUT_L_ADDR)
        raw_gyro_arr[2] |= bus.read_byte_data(DEV_ADDR, GYRO_ZOUT_H_ADDR) << 8
        raw_gyro_arr[2] |= bus.read_byte_data(DEV_ADDR, GYRO_ZOUT_L_ADDR)

        cur_time = time.time()

        # Process raw accel into m/s^2
        for i in range(raw_accel_arr.size):
            processed_accel_arr[i] = (raw_accel_arr[i] / (2**15 / accel_fsr)) * 9.80665

        # Process raw gyro into angular rate
        for i in range(raw_gyro_arr.size):
            processed_gyro_arr[i] = raw_gyro_arr[i] / (2**15 / gyro_fsr)
            
        time.sleep(0.04)
        #print(f"Accel (m/s^2, xyz): {processed_accel_arr}, Gyro (dps, xyz): {processed_gyro_arr}, time: {cur_time}")
        f.write(f"Accel: {processed_accel_arr}, Gyro: {processed_gyro_arr}, time: {cur_time}\n")

except KeyboardInterrupt:
    print ("Stopped by user.")

finally:
    f.close()