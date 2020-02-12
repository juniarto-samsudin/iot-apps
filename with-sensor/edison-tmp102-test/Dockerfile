from balenalib/intel-edison-ubuntu-python:3.7.4
RUN apt-get install -y i2c-tools
RUN install_packages libmraa2 libmraa-dev libmraa-java python-mraa python3-mraa node-mraa mraa-tools
#RUN apt-get install python-sofware-properties
#RUN add-apt-repository ppa:mraa/mraa
#RUN apt-get update
#RUN apt-get install libmraa2 libmraa-dev libmraa-java python-mraa python3-mraa node-mraa mraa-tools
WORKDIR /app
COPY app.py .
COPY tmp102.py .
COPY requirements.txt .
RUN pip3  install -r requirements.txt
ENTRYPOINT ["python","app.py"]
