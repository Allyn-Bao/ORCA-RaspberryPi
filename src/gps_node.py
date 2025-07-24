import sys
import serial
import pynmea2

from rclpy import init, spin, spin_once
from rclpy.node import Node

from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import NavSatStatus


class gps_node(Node):

    def __init__(self, qos):

        super().__init__("gps_node")
        # set up publisher for NavSat messages
        self.publisher = self.create_publisher(NavSatFix, '/gps/fix', 10)

        # Open the serial port to interface with the GPS
        self.ser = serial.Serial('COM5', 38400, timeout=1)

        # Create timer to read from the GPS TODO fine tune frequency (secs)
        self.timer = self.create_timer(0.1, self.read_and_publish)

    def read_and_publish(self):
        try:
            line = self.ser.readline().decode('ascii', errors='replace').strip()
            if line.startswith('$GNRMC') or line.startswith('$GNGLL') or line.startswith('$GNGGA'):
                try:
                    msg = pynmea2.parse(line)
                    if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                        lat = msg.latitude
                        lon = msg.longitude

                        # Prepare NavSatFix message
                        navsat_msg = NavSatFix()
                        navsat_msg.header.stamp = self.get_clock().now().to_msg()
                        navsat_msg.header.frame_id = 'gps'

                        navsat_msg.status.status = NavSatStatus.STATUS_FIX
                        navsat_msg.status.service = NavSatStatus.SERVICE_GPS

                        navsat_msg.latitude = lat
                        navsat_msg.longitude = lon
                        #navsat_msg.altitude = getattr(msg, 'altitude', 0.0)  # if available


                        self.publisher.publish(navsat_msg)

                        self.get_logger().info(f"Published GPS fix: lat={lat:.6f}, lon={lon:.6f}")
                except pynmea2.ParseError:
                    pass
        except serial.SerialException as e:
            self.get_logger().error(f"Serial error: {e}")

    def destroy_node(self):
        self.ser.close()
        super().destroy_node()



def main():
    init()
    navsat_qos = QoSProfile(reliability=2, durability=2, history=1, depth=10)
    GPS = gps_node(navsat_qos)

    try:
        spin(GPS)
    except KeyboardInterrupt:
        pass
    finally:
        gps_node.destroy_node()



if __name__=="__main__":
    main()