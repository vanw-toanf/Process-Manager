# Process-Manager
This project simulates the task manager like in windows on ubuntu.

```bash
git clone https://github.com/vanw-toanf/Process-Manager
cd Process-Manger
chmod +x build.sh
make build
```

If you have Docker, 
```bash
git clone https://github.com/vanw-toanf/Process-Manager
cd Process-Manger
xhost +local:root
sudo docker build -t <image_name> .
sudo docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -e QT_QPA_PLATFORM_PLUGIN_PATH=$(find /usr -type d -name platforms | sed 's:/platforms$::') \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  <image_name>