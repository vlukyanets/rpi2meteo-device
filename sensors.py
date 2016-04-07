# 2016 (C) Valentin Lukyanets


class Sensor(object):

    def __init__(self, name, reading_function):
        self.name = name
        self.reading_function = reading_function

    def __call__(self):
        return self.reading_function()


class SensorsManager(object):

    def __init__(self):
        self.sensors = []
        self.dependencies = []

    def add(self, sensor):
        if sensor not in self.sensors:
            self.sensors.append(sensor)

    def add_dependency(self, dependency):
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)
