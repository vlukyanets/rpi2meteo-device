# 2016 (C) Valentin Lukyanets


class Sensor(object):

    def __init__(self, name, reading_function):
        self.name = name
        self.reading_function = reading_function

    def __normalize(self, reading):
        if isinstance(reading, list):
            return [self.__normalize(nested_reading) for nested_reading in reading]
        elif isinstance(reading, float):
            return round(reading, 2)
        else:
            return reading

    def __call__(self):
        data = self.reading_function()
        return self.__normalize(data)


class SensorsManager(object):

    def __init__(self):
        self.sensors = []
        self.dependencies = []

    def add(self, sensor, unit=""):
        if sensor not in self.sensors:
            self.sensors.append((sensor, unit))

    def add_dependency(self, dependency):
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)


COORDINATES_FILE_NAME = "gps-coordinates"


# Function to read coordinates from file
def read_coordinates():
    with open(COORDINATES_FILE_NAME, "r") as f:
        strnumbers = f.read().split()
        values = map(float, strnumbers)
        return values[0], values[1]


latitude, longitude = read_coordinates()


def get_coordinates():
    return {"lat": latitude, "lng": longitude}
