from balenalib/jetson-nano-debian-python:3.7.4


WORKDIR /app
COPY app.py .
COPY requirements.txt .

RUN pip3  install -r requirements.txt
ENTRYPOINT ["python","app.py"]
