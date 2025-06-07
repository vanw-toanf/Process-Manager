FROM python:3.12-slim

WORKDIR /workspace

COPY src/requirements.txt ./src/

RUN apt-get update && apt-get install -y make

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r src/requirements.txt

COPY . .

RUN chmod +x build.sh
CMD ["make", "build"]