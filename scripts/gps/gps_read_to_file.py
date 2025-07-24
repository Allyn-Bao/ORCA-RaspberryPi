import serial
import pynmea2
import time

# Open serial port (adjust 'COM3' or '/dev/ttyUSB0' and baudrate to your device)
ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)

try:
    f = open("gps_data_parsed.txt", "w")

    while True:
        line = ser.readline().decode('ascii', errors='replace').strip()
        if line.startswith('$GNRMC') or line.startswith('$GNGLL') or line.startswith('$GNGGA'):
            try:
                msg = pynmea2.parse(line)

                if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                    cur_time = time.time()
                    lat = msg.latitude
                    lon = msg.longitude
                    #print(f"Latitude: {lat}, Longitude: {lon}, time: {cur_time}\n")
                    f.write(f"Latitude: {lat}, Longitude: {lon}, time: {cur_time}\n")

            except pynmea2.ParseError:
                continue

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    ser.close()
    f.close()
