import time
import pigpio

# ESC_GPIO = 18  # BCM pin 18 = physical pin 12
MOTOR_L = 12
MOTOR_R = 13
MIN_PULSE = 1000
MID_PULSE = 1500
MAX_PULSE = 2000



pi = pigpio.pi()
if not pi.connected:
    print("Could not connect to pigpio daemon. Did you run 'sudo pigpiod'?")
    exit()

try:
    print("Starting ESC at mid throttle...")
    pi.set_servo_pulsewidth(MOTOR_L, MIN_PULSE)
    pi.set_servo_pulsewidth(MOTOR_R, MIN_PULSE)
    time.sleep(8)

    print("Ramping up...")
    for pulse in range(1000, 1101, 5):
        print(f"Pulse: {pulse}")
        pi.set_servo_pulsewidth(MOTOR_L, pulse)
        #pi.set_servo_pulsewidth(MOTOR_R, pulse)

        time.sleep(0.2)
    print("At max speed")
    time.sleep(10)

    print("Ramping down...")
    for pulse in range(1100, 1099, -5):
        print(f"Pulse: {pulse}")
        pi.set_servo_pulsewidth(MOTOR_L, pulse)
        #pi.set_servo_pulsewidth(MOTOR_R, pulse)
        time.sleep(0.2)



finally:
    print("Stopping ESC signal...")
    pi.set_servo_pulsewidth(MOTOR_L, 0)
    pi.set_servo_pulsewidth(MOTOR_R, 0)
    pi.stop()