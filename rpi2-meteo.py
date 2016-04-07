#!/usr/bin/python2.7
# 2016 (C) Valentin Lukyanets


import sys

import tornado
import tornado.options
import tornado.httpserver
import tornado.ioloop
import tornado.web

import web_application
import sensors

import libs.Adafruit_BME280


def initialize_sensors_manager(sensors_manager):
    bme280 = libs.Adafruit_BME280.BME280()

    sensor_temperature = sensors.Sensor("Temperature", bme280.read_temperature)
    sensor_pressure = sensors.Sensor("Pressure", bme280.read_pressure)
    sensor_humidity = sensors.Sensor("Humidity", bme280.read_humidity)
    sensor_gps = sensors.Sensor("Coordinates", lambda: [50.00, 36.22])  # Fake coordinates

    sensors_manager.add(sensor_temperature, "C")
    sensors_manager.add(sensor_pressure, "Pa")
    sensors_manager.add(sensor_humidity, "%")
    sensors_manager.add(sensor_gps)
    sensors_manager.add_dependency(bme280)


def start_web_server(sensors_manager):
    tornado.options.define("port", 8888, help="Run on the given port", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(
        web_application.Application(sensors_manager)
    )
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
    return 0


def main():
    sensors_manager = sensors.SensorsManager()
    initialize_sensors_manager(sensors_manager)

    return start_web_server(sensors_manager)


if __name__ == "__main__":
    sys.exit(main())
