from balenalib/raspberrypi3-debian-python:3.7.4


WORKDIR /app
COPY app.py .
COPY requirements.txt .

RUN pip  install -r requirements.txt
ENTRYPOINT ["python","app.py"]
