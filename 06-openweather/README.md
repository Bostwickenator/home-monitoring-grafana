# MQTT to InfluxDB Bridge

## Build

```sh
$ docker build -t bostwickenator/openweather .
```


## Run

```sh
$ docker run -d --name openweather bostwickenator/openweather
```


## Dev

```sh
$ docker run -it --rm -v `pwd`:/app --name python python:3.7-alpine sh
```
