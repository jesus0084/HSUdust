sleep 10
sh /home/pi/mjpg.sh &
sleep 5
cd /home/pi/Downloads/JSDK/SDK_JAVA
make run &
sleep 5
sudo python3 /home/pi/Desktop/DustDetector/base.py