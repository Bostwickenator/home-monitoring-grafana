FROM python:3.7-alpine

LABEL maintainer="Bostwickenator" \
      description="Open Weather to InfluxDB logger https://openweathermap.org/"

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "-u", "main.py"]
