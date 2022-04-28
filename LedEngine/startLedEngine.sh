function cleanup {
  echo "Stopping processes"
  sudo pkill -f Controller.py
  sudo pkill -f webserver.js

}

trap cleanup EXIT

dir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")

cd $dir

sudo python3 Controller.py & 
node webserver.js


