# Welcome to the GitHub page of LED-Engine!
Always wanted pixel art or a playing gif on your wall, then this program is for you!


LED-Engine is a software program that lets you control your led's with a Raspberry Pi from an external device like a laptop or a smartphone (no apps required on external devices :D ).

![](https://drive.google.com/uc?export=download&id=1CFfCzoUidTyI6hnm8ohEUrq-_4fWohcS)

- The left image shows the different modes you can play on an led panel.
- The top right image shows the drawing canvas
- The bottom right image shows me using the Load Image (displaying an image on to the led panel)

What can you exactly do in LED-Engine:

|                |LED-panel                      |LED-strip                         |
|----------------|-------------------------------|------------------------|
|Static Color|✔ |   ✔       
|Rainbow mode|✔ |      ✔     
|Sine Wave|✔ |      ✔     
|Star Effect|✔ |      ✔     
|Fire Effect|✔ |      ✔     
|Knight Rider|✔ |      ✔     
|Conway's Game of Life|✔ |**X**
|Langton's Ant|✔ |**X**
|Brian's Brain|✔ |**X**
|WireWorld|✔ |**X**
|Drawing canvas|✔ |**X**
|Display images (from image url or upload)|✔ |**X**
|Display gif (from gif url)|✔ |**X**
|Text|✔ |**X**
|Fishtank|✔ |**X**
 
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

# Hardware
### Supported Raspberry Pi's
All raspberry pi's are supported from the pi 4 to the pi zero w. The pi zero w is reccomended for this project because you don't need more processing power running LED-Engine (though the pi 4 will be quicker of course!).

### Supported Led's
We are using the [Adafruit neopixel ](https://learn.adafruit.com/neopixels-on-raspberry-pi) module that support WS2811/WS2812  led's. If you have a different module you would like to use then you can change the file: "LedEngine/led_lib.py" and change the module to whatever you want! This is the only place in the program were neopixels is being used (to make it easyer switching between modules). Led-Engine will support multiple modules in the future! 

# Add your own modes!
### Still in progress
We are currently working on a document that describes step by step how you can add your own mode.
Expect this coming soon!


# Installing LED-Engine
We have two ways of installing LED-Engine.

- **Installing LED-Engine with bash script**
- **Installing LED-Engine from scratch**

### Installing LED-Engine with bash script
This way is reccomended if you already have an raspberry pi os on your pi. 

### Installing LED-Engine from scratch
this way is reccomended if you had trouble with **Installing LED-Engine with bash script**. 



## Installing LED-Engine with bash script
This will guide you installing LED-Engine on a raspberry pi that already has an os installed. To make installing easy for you we have a bash script that you can download to you pi and run. The bash script will detect what pi you are using and will install all the dependencies needed. 

First we need to download the bash script:

	git clone https://github.com/merijndewit/Led-Engine.git

Then we can execute the script:

	./Led-Engine/installLedEngine.sh

After you see this in the terminal the install was succesfull:

	Successfully installed LED-Engine!
	Type './Led-Engine/LedEngine/startLedEngine.sh' to start LED-Engine.
	Enjoy using LED-Engine!

Then simply enter:

	./Led-Engine/LedEngine/startLedEngine.sh

And the program should be running!
#### Enjoy LED-Engine!

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

Now we want to go cback to the root folder and install the socket<span>.io</span> package:

	cd /

	sudo npm install socket.io
	sudo npm install formidable


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
	
	cd /Led-Engine/LedEngine/
		
When we are in the folder **LedEngine** we want to run **webserver.js**:

	node webserver.js

Then we want to run <span>**Controller**</span>**.py** in another terminal:
 
	sudo python3 Controller.py
	
>Note:If you get the import error "ImportError: libopenjp2.so.7: cannot open shared object file: No such file or directory" run this command: sudo apt-get install libopenjp2-7

>Note: If you get the import error "ImportError: libtiff5: cannot open shared object file: No such file or directory" run this command: sudo apt install libtiff5

Now the program should be running, and you should be able to open the website on an external device like a laptop or mobile phone!

You can access LED-Engine on any browser by typing the pi's address and default port for LED-Engine Example: 192.168.x.x:8080

#### Enjoy LED-Engine!


