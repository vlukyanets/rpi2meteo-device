#!/usr/bin/python2.7
# 2016 (C) Valentin Lukyanets


import sys

import tornado
import tornado.options
import tornado.httpserver
import tornado.ioloop
import tornado.web

from datetime import datetime
import httplib

import web_application
import sensors
import json

from apscheduler.schedulers.blocking import BlockingScheduler

import libs.Adafruit_BME280


DEVICE_ID_FILENAME = 'rpi2meteo.deviceid'
AWS_HOST_FILENAME = "awshost"


def initialize_sensors_manager(sensors_manager):
    bme280 = libs.Adafruit_BME280.BME280()

    sensor_temperature = sensors.Sensor("Temperature", bme280.read_temperature)
    sensor_pressure = sensors.Sensor("Pressure", bme280.read_pressure)
    sensor_humidity = sensors.Sensor("Humidity", bme280.read_humidity)
    sensor_gps = sensors.Sensor("Coordinates", sensors.get_coordinates)

    sensors_manager.add(sensor_temperature, "C")
    sensors_manager.add(sensor_pressure, "Pa")
    sensors_manager.add(sensor_humidity, "%")
    sensors_manager.add(sensor_gps)
    sensors_manager.add_dependency(bme280)


def start_web_server(sensors_manager):
    tornado.options.define("port", 80, help="Run on the given port", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(
        web_application.Application(sensors_manager)
    )
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


def get_device_id():
    with open(DEVICE_ID_FILENAME, "r") as f:
        return f.read()


def get_aws_host():
    with open(AWS_HOST_FILENAME, "r") as f:
        return f.read()


def schedule_send_data(aws_host, device_id, sensors_manager):
    scheduler = BlockingScheduler()

    @scheduler.scheduled_job('interval', seconds=10)
    def send_data():
        body = {"device_id": device_id, "sensors": [], "method": "data.put"}
        for sensor, unit in sensors_manager.sensors:
            body["sensors"].append((sensor.name, sensor.reading_function(), unit))

        connection = httplib.HTTPConnection(aws_host)
        headers = {"Content-Type": "application/json", "Accept": "text/plain"}
        connection.request("POST", "/api", json.dumps(body), headers)
        response = connection.getresponse()
        with open("/tmp/rpi2meteo-log", "a+") as f:
            log_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + str(response.status) + " " + str(response.reason) + "\n"
            f.write(log_str)
        print response.status, response.reason
        connection.close()

    scheduler.start()


def main():
    aws_host = get_aws_host()
    device_id = get_device_id()
    sensors_manager = sensors.SensorsManager()
    initialize_sensors_manager(sensors_manager)
    schedule_send_data(aws_host, device_id, sensors_manager)
    start_web_server(sensors_manager)


if __name__ == "__main__":
    main()
    sys.exit()
