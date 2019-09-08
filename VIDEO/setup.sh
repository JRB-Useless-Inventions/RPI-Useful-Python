sudo apt-get update
sudo apt-get install build-essential python3-dev python3-smbus python3-pip python3-imaging python3-numpy git

cd ~
git clone https://github.com/adafruit/Adafruit_Python_ILI9341.git
cd Adafruit_Python_ILI9341
sudo python3 setup.py install