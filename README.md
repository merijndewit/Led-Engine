![](https://drive.google.com/uc?export=download&id=1ya2MA8AdjBEed9ltCEVmvmjO0VqLAw5p)

# Welcome to the GitHub page of LED-Engine!
LED-Engine is a software program that lets you control your led's from an external device like a laptop or a smartphone (no apps required on external devices :D ). LED-Engine has support for ws2812b (more to be added in the future) LED-strips and LED-panels. LED-Engine has an easy to use interface with a lot of useful features (again more to be added in the future!). 

What can you exactly do in LED-Engine:

|                |LED-panel                      |LED-strip                         |
|----------------|-------------------------------|------------------------|
|Static Color|✔ |   ✔       
|Rainbow mode|✔ |      ✔     
|Conway's Game of Life|✔ |**X**
|Langton's Ant|✔ |**X**
|Brian's Brain|✔ |**X**
|WireWorld|✔ |**X**
|Drawing canvas|✔ |**X**
|Display images (from image url or upload)|✔ |**X**
|Display gif (from gif url)|✔ |**X**
 
 ### Extra info about some of the different modes:

### WireWorld 
With WireWorld you first have to draw your "circuit" on the website. When you click play it will play wireworld with your circuit on the LED-Panel!

### Drawing canvas
With Drawing canvas you have a canvas with the same amount of pixels as your LED-Panel has. You can draw pixel by pixel on the canvas, you select the color with a color picker or by pressing on one of the preset color buttons. Every time you draw a pixel the LED-Panel directly shows the pixel you drew on the canvas.

### Display images
You can display an image on the LED-Engine. You can simply get the url of the image and the program will take care of it. You can also upload an image from an external device. Most image formats are supported and any resolution so the resolution of the image does not have to match the resolution of the led panel because the program will automatically downscale it! The image will also be displayed on the Drawing canvas so you will be able to edit it.

### Display gif
Display gif is the same as Display images but then it plays a gif on the LED-Panel. 


I hope you will try out LED-Engine. All the info to install/use this program is written into this readme file!


## Installing LED-Engine from scratch

This is a step by step guide to get LED-Engine running from a clean install of raspbian os.
Raspberry Pi OS Lite (bullseye) is reccomended for LED-Engine. The desktop version will also work without any problem but will be a bit slower.

https://www.raspberrypi.com/software/operating-systems/

Once you've installed Raspberry Pi OS on your pi follow all the steps below:

### Nodejs
Let's begin with installing nodejs. LED-Engine uses perfectly with nodejs v12.9.1 so thats what i recommend. Newer versions of nodejs might have some trouble with older pi's.
First we need to know what arm platform the pi is using by entering the command:

	uname -m

look for the file that has your arm platform in the file name and with the file extention: .tar.xz and copy the download link:
https://nodejs.org/dist/v12.9.1/

unofficial builds for older pi's on arm6 :
https://unofficial-builds.nodejs.org/download/release/v12.9.1/

Now we enter this command to download the file:

>note: change "download-URL" to the correct download link

	sudo wget download-URL

To unpack the file we've just downloaded:
>note: change "filename.tar.xz" to the downloaded file

	sudo tar -xvf filename.tar.xz

Now we want to go into the folder of the files we've just extracted.
>note: change "filename.tar.xz" to the folder containing the extracted files

	cd extracted-folder-name

Now we want to copy all the files to /usr/local/

	sudo cp -R * /usr/local/

Now node should be installed!
To test if nodejs is working we type:

	node -v

Now we need to install the socket<span>.io</span> package:

	sudo npm install socket.io


### Python Dependencies
Now we want to install all the python dependencies. First we want to install pip:

	sudo apt-get install python3-pip

Now we can install python dependencies. Enter the following commands:

	sudo pip3 install board

	sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel

	sudo pip3 install pillow

After we've installed all the python dependencies we can install git and clone the GitHub repository:

	sudo apt install git

	sudo git clone https://github.com/merijndewit/Led-Engine.git
Now we are ready to run LED-Engine! Follow the steps at "How to run LED-Engine" to run the program!


## How to run LED-Engine
In order to run LED-Engine we need to run 2 programs: **webserver.js** & <span>**Controller**</span>**.py**.
**webserver** is the frontend and **Controller** is the backend. Both programs need to be running at the same time for everythong to work.

First we want to go into the project folder most likely called: **Led-Engine**.
Then we want to go into the folder **LedEngine**
	
	cd LedEngine
		
When we are in the folder **LedEngine** we want to run **webserver.js**:

	node webserver.js

Then we want to run <span>**Controller**</span>**.py** in another terminal:
 
	sudo python3 Controller.py
	
>Note:If you get the import error "ImportError: libopenjp2.so.7: cannot open shared object file: No such file or directory" run this command: sudo apt-get install libopenjp2-7

Now the program should be running, and you should be able to open the website on an external device like a laptop or mobile phone!




