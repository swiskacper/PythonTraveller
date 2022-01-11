import json


class Weather:
    def __init__(self, city, temp, speed, clouds):
        self.city = city
        self.temp = temp
        self.speed = speed
        self.clouds = clouds

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)