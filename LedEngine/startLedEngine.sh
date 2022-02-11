if [ -d "/Led-Engine/LedEngine/" ]
then
    sudo python3 /Led-Engine/LedEngine/Controller.py &
    node /Led-Engine/LedEngine/webserver.js
elif [ -d "/home/pi/Led-Engine/LedEngine/" ]
then
    sudo python3 /home/pi/Led-Engine/LedEngine/Controller.py &
    node /home/pi/Led-Engine/LedEngine/webserver.js
fi

