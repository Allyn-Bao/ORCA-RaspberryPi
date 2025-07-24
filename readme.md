# ORCA: Open-Water Routing Course Assistant

This is a 4th-year design project by Allyn Bao, Braden Schulz, Nadia Bhola, and Vidhi Patel, under department of Computer Engineering in University of Waterloo.
The project is consulted by Prof. Gennaro Notomista

## Introduction
ORCA aims to guide swimmers along a designated route and help them to analyze their performance. It will provide additional safety measures such as real-time monitoring and emergency signaling to shore. ORCA aims to fill a critical gap in open-water swim training, the lack of real-time guidance and support for individual swimmers. This solution has remained largely unexplored likely due to the relatively niche size of the open-water swimming community, complexity of developing such an autonomous system and previously high cost of components such as sensors and communication technology.





## ORCA Project Notes

### for Python scripts: 
use virtual env: source ~/robot-env/bin/activate

### WIFI modes

#### AP Mode - Wireless ssh connection without internet access
By default, the Raspberry Pi boots into AccessPoint mode. After 30sec to 1 minutes of boot up, a WIFI access point named "RPi-Hotspot" should showup. This connection occupies port wlan0 and therefore it cannot be activated at the same time as Cilent Hotspot mode. To switch from Client Hotspot mode back to AP mode, reboot the Pi.

On your own computer terminal:
```
ssh pi@192.168.4.1
```

#### Ethernet - Wired ssh connection always on
Connect the Pi through an ethernet cable to laptop. This connection occupies eth0 on the Pi therefore it will always be on along side with either AP mode or Client mode. Run the following command from laptop terminal:
```
ssh pi@169.254.64.2
```

#### Client mode:
In raspberry Pi, configure the pi to connect to a WIFI or phone hotspot, and run the following command in Raspberry Pi:
```
~/wifi_modes/switch_to_client.sh 
```
