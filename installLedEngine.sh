#!/bin/bash

architecture=$(uname -m)
dir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")

echo "Installing LED-Engine."
echo "Detected architecture: $architecture."

arm7="armv7l"
arm6="armv6l"
cd $dir
echo "installing nodejs for "$architecture""
sudo wget https://nodejs.org/dist/v12.9.1/node-v12.9.1-linux-"$architecture".tar.xz
sudo tar -xvf node-v12.9.1-linux-"$architecture".tar.xz
sudo cp -R node-v12.9.1-linux-"$architecture"/* /usr/local/
sudo rm -R node-v12.9.1-linux-"$architecture".tar.xz
sudo rm -R node-v12.9.1-linux-"$architecture"
testnode=$(node -v)
echo "installed node: $testnode"
sudo npm install --unsafe-perm
sudo npm install socket.io
sudo npm install formidable

echo "Installing python dependencies."

sudo apt install python3-pip
sudo pip3 install board
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
sudo pip3 install pillow
sudo pip3 install RPi.GPIO
sudo apt-get install libopenjp2-7
sudo apt install libtiff5

echo "Successfully installed LED-Engine!"
echo "Type './Led-Engine/LedEngine/startLedEngine.sh' to start LED-Engine."
echo "Enjoy using LED-Engine!"


