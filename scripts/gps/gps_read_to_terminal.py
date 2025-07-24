import serial
import pynmea2

# Open serial port (adjust 'COM3' or '/dev/ttyUSB0' and baudrate to your device)
ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)

try:
    while True:
        line = ser.readline().decode('ascii', errors='replace').strip()
        if line.startswith('$GNRMC') or line.startswith('$GNGLL') or line.startswith('$GNGGA'):
            try:
                msg = pynmea2.parse(line)

                if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                    lat = msg.latitude
                    lon = msg.longitude
                    print(f"Latitude: {lat}, Longitude: {lon}")

            except pynmea2.ParseError:
                continue

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    ser.close()
