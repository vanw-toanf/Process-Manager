# Process-Manager
This project simulates the task manager like in windows on ubuntu.

To run this app you must be in terminal window!

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
sudo docker build -t <image_name> .
sudo docker run -it --rm <image_name>
```