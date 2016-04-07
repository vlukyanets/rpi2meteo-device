# 2016 (C) Valentin Lukyanets


import tornado.web
import os.path


class HomeHandler(tornado.web.RequestHandler):

    def initialize(self, sensors_manager):
        self.sensors_manager = sensors_manager

    def get(self):
        sensors_readings = {}
        for sensor, unit in self.sensors_manager.sensors:
            name, data = sensor.name, sensor()
            sensors_readings[name] = (data, unit)

        self.render("home.html", sensors_readings=sensors_readings)


class Application(tornado.web.Application):

    def __init__(self, sensors_manager):
        handlers = [
            (r"^/$", HomeHandler, dict(sensors_manager=sensors_manager))
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            site_title="RPI2-meteostation",
        )

        super(Application, self).__init__(handlers, **settings)
