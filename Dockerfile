FROM resin/rpi-raspbian:latest

ENTRYPOINT []

RUN apt-get update && apt-get -qy install build-essential python python-pip python-dev gcc make

COPY ./ /app

WORKDIR /app/SPI-Py

RUN python setup.py install

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "toggle.py"]
