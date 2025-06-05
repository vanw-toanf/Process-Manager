FROM python:3.12-slim

WORKDIR /workspace

COPY . .

RUN apt-get update && apt-get install -y\
    libgl1 \
    libxkbcommon0 \
    libegl1-mesa \
    fontconfig \
    libglib2.0-0 \
    libdbus-1-3 \
    libxcb-cursor0 \
    libxcb-xinerama0 \
    libxcb-shape0 \
    libxcb-randr0 \
    libxcb-xfixes0 \
    libx11-xcb1 \
    libxcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-render0 \
    libxcb-shm0 \
    libxcb-xfixes0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    make

ENV QT_QPA_PLATFORM_PLUGIN_PATH=/usr/local/lib/python3.12/site-packages/PyQt6/Qt6/plugins

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r src/requirements.txt

RUN chmod +x build.sh
CMD ["make", "build"]