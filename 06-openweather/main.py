#!/usr/bin/env python3

"""
Open Weather to InfluxDB logger https://openweathermap.org/
"""

from influxdb import InfluxDBClient
import requests
from datetime import datetime
import sched 
import time 
import os

# instance is created 
scheduler = sched.scheduler(time.time, 
                            time.sleep) 

INFLUXDB_ADDRESS = 'influxdb'
INFLUXDB_USER = 'root'
INFLUXDB_PASSWORD = 'root'
INFLUXDB_DATABASE = 'home_db'

POLLING_INTERVAL_SEC = 60 * 5

OPENWEATHER_ZIP =  os.getenv('OPENWEATHER_ZIP')
OPENWEATHER_API_KEY =  os.getenv('OPENWEATHER_API_KEY') 
OPENWEATHER_UNITS =  os.getenv('OPENWEATHER_UNITS') 
OPENWEATHER_API_PATH = f'https://api.openweathermap.org/data/2.5/weather?zip={OPENWEATHER_ZIP}&units={OPENWEATHER_UNITS}&appid={OPENWEATHER_API_KEY}'

MQTT_ADDRESS = 'mosquitto'
MQTT_USER = 'mqttuser'
MQTT_PASSWORD = 'mqttpassword'
MQTT_TOPIC = 'home/+/+' 
MQTT_REGEX = 'home/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'MQTTInfluxDBBridge'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)


def _send_sensor_data_to_influxdb(weather):
    json_body = [
        {
            'measurement': 'weather',
            'tags': {
                'location': 'outside'
            },
            'fields': {
                "temp": float(weather['main']['temp']),
                "feels_like": float(weather['main']['feels_like']),
                "pressure": float(weather['main']['pressure']),
                "humidity": float(weather['main']['humidity']),
                "wind": float(weather['wind']['speed']),
            },
            "time": datetime.utcfromtimestamp(weather['dt']).isoformat() + 'Z',
        }
    ]
    print(json_body)
    influxdb_client.write_points(json_body)


def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

last_weather_time = 0

def get_weather():
    global last_weather_time
    r = requests.get(OPENWEATHER_API_PATH)
    if(r.status_code == requests.codes.ok):
        if(r.json()['dt'] != last_weather_time):
            last_weather_time = r.json()['dt']
            _send_sensor_data_to_influxdb(r.json())


def repeat():
    scheduler.enter(POLLING_INTERVAL_SEC, 1, repeat)
    get_weather()

def main():
    _init_influxdb_database()
    repeat()
    scheduler.run()
    
if __name__ == '__main__':
    print('OpenWeather to InfluxDB bridge')
    main()
