
![](https://drive.google.com/uc?export=download&id=1ya2MA8AdjBEed9ltCEVmvmjO0VqLAw5p)

# Welcome to the GitHub page of LED-Engine!
Always wanted pixel art or a playing gif on your wall, then this program is for you!


LED-Engine is a software program that lets you control your led's with a Raspberry Pi from an external device like a laptop or a smartphone (no apps required on external devices :D ). LED-Engine has support for ws2812b (more to be added in the future) LED-strips and LED-panels. LED-Engine has an easy to use interface with a lot of useful features (again more to be added in the future!). 

![](https://drive.google.com/uc?export=download&id=1CFfCzoUidTyI6hnm8ohEUrq-_4fWohcS)

- The left image shows the different modes you can play on an led panel.
- The top right image shows the drawing canvas
- The bottom right image shows me using the Load Image (displaying an image on to the led panel)

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
 
## Extra info about some of the different modes:

### WireWorld 
With WireWorld you first have to draw your "circuit" on the website. When you click play it will play wireworld with your circuit on the LED-Panel!

### Drawing canvas
With Drawing canvas you have a canvas with the same amount of pixels as your LED-Panel has. You can draw pixel by pixel on the canvas, you select the color with a color picker or by pressing on one of the preset color buttons. Every time you draw a pixel the LED-Panel directly shows the pixel you drew on the canvas.

### Display images
You can display an image on the LED-Engine. You can simply get the url of the image and the program will take care of it. You can also upload an image from an external device. Most image formats are supported and any resolution so the resolution of the image does not have to match the resolution of the led panel because the program will automatically downscale it! The image will also be displayed on the Drawing canvas so you will be able to edit it.

### Display gif
Display gif is the same as Display images but then it plays a gif on the LED-Panel. 


I hope you will try out LED-Engine. All the info to install/use this program is written into this readme file!

### Supported Raspberry Pi's
All raspberry pi's are supported from the pi 4 to the pi zero w. The pi zero w is reccomended for this project because you dont need more processing power running LED-Engine.

# Installing LED-Engine
We have multiple ways for installing LED-Engine.

- **Installing LED-Engine with bash script**
- **Installing LED-Engine with an image**
- **Installing LED-Engine from scratch**
### Installing LED-Engine with bash script
This way is reccomended if you already have an raspberry pi os on your pi. 

### Installing LED-Engine with an image
This way is reccomended if you dont have an os on your pi.

### Installing LED-Engine from scratch
this way is reccomended if you had trouble with **Installing LED-Engine with bash script**. 



## Installing LED-Engine with bash script
This will guide you installing LED-Engine on a raspberry pi that already has an os installed. To make installing easy for you we have a bash script that you can download to you pi and run. The bash script will detect what pi you are using and will install all the dependencies needed. 

First we need to download the bash script:

	sudo wget https://github.com/merijndewit/Led-Engine/releases/download/v0.1.1/installLedEngine.sh

Then we can execute the script:

	sh installLedEngine.sh

After you see this in the terminal the install was succesfull:

	Successfully installed LED-Engine!
	Type 'sh /Led-Engine/LedEngine/startLedEngine.sh' to start LED-Engine.
	Enjoy using LED-Engine!

Then simply enter:

	sh /Led-Engine/LedEngine/startLedEngine.sh

>Note:If you get the import error "ImportError: libopenjp2.so.7: cannot open shared object file: No such file or directory" run this command: sudo apt-get install libopenjp2-7

>Note: If you get the import error "ImportError: libtiff5: cannot open shared object file: No such file or directory" run this command: sudo apt install libtiff5

And the program is running!
#### Enjoy LED-Engine!


## Installing LED-Engine with an image
This will guide you installing LED-Engine on a raspberry pi. If you are using another platform or if you dont want to install a custom image on your sd card then please follow the instructions at **"Installing LED-Engine from scratch"**. 

First we need to create a bootable sd card from a custom image. Go to [releases](https://github.com/merijndewit/Led-Engine/releases) and download LedEngine_Images_vX.X.X .zip. inside that zip file we can find 2 different images. 

LedEngine_Image_ARM6_vX.X.X  is for:
- Pi zero W
- Pi 1

LedEngine_Image_ARM7_vX.X.X is for:
- Pi 2
- Pi 3
- Pi 4

Extract the correct image file into a folder and install a program that can create a bootable usb drive/sd card like [Rufus](https://rufus.ie/en/). Create a bootable sd card with the extracted image.

If you want to install the os headless (highly recommended) you can add [These files](https://github.com/merijndewit/Led-Engine/files/8015636/add_containing_files_to_sd_boot_folder.zip) to the boot folder of the sd card so the pi will connect to the internet and we can access it with a SSH like [putty](https://www.putty.org/). When you added the files to the boot folder edit Inside the wpa_config file: "put-your-ssid-here" to your network name and  
"put-your-wifi-password-here" to your network password.
>Note: only 2G networks work on the pi zero and pi 1

Now we are all set!
Just put the sd card into the raspberry pi and let the pi boot. Now you should be able to access it with an SSH.

The password and username are default.
- username: pi
- password: raspberry

To start the program just go into the LED-Engine directory:

	cd /Led-Engine/LedEngine/

Then we just need to run the shell script. The shell script runs the python and webserver program at the same time:

	sh startLedEngine.sh

Now the program is running!

>Note:If you get the import error "ImportError: libopenjp2.so.7: cannot open shared object file: No such file or directory" run this command: sudo apt-get install libopenjp2-7

>Note: If you get the import error "ImportError: libtiff5: cannot open shared object file: No such file or directory" run this command: sudo apt install libtiff5

You can access LED-Engine on any browser by typing the pi's address and default port (8080) for LED-Engine Example: 192.168.x.x:8080

#### Enjoy LED-Engine!



# Installing LED-Engine from scratch

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


### Running LED-Engine
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

# Wiring for the LED-Panel or led strip

The wiring is quite easy.
LED-Engine uses GPIO 21 as default. Feel free to change this in "LedstripController<span>.py</span>"

On the image below we can see how to wire an Led-strip or Led-panel to the raspberry pi. 
![](https://drive.google.com/uc?export=download&id=1UtZRdzRrpeSM5KbMVe16H3CQBcbshNfd)
If your led-panel or led strip is small you could try to hook it up directly to the raspberry pi (exactly like on the picture). If you have a bigger led panel (bigger than 8x8) or led strip that has more than 64 led's then i would reccomend using an external power supply.


