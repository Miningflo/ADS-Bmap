import datetime
import json

import requests as requests

from plane import Plane
from constants import constants


def lookup(icao):
    if icao.upper() in map(str.upper, constants["poi"]):
        # send discord webhook message
        url = "https://globe.adsbexchange.com/?icao=" + icao
        requests.post(constants["hook"], data={'content': url})


class PlaneList:
    def __init__(self):
        self.planes = dict()

    def __update(self):
        copy = self.planes.copy()
        for i, (icao, plane) in enumerate(copy.items()):
            if (datetime.datetime.now() - plane.last).total_seconds() > 45:
                del self.planes[icao]

    def __create(self, icao):
        if icao not in self.planes.keys():
            self.planes[icao] = Plane(icao)
            lookup(icao)
            self.__update()

    def callsign(self, icao, callsign):
        self.__create(icao)
        self.planes[icao].update_callsign(callsign)

    def category(self, icao, cat):
        self.__create(icao)
        self.planes[icao].update_category(cat)

    def speed(self, icao, speed):
        self.__create(icao)
        self.planes[icao].update_speed(speed)

    def heading(self, icao, heading):
        self.__create(icao),
        self.planes[icao].update_heading(heading)

    def altitude(self, icao, altitude):
        self.__create(icao)
        self.planes[icao].update_altitude(altitude)

    def position(self, icao, message):
        self.__create(icao)
        self.planes[icao].update_position(message)

    def json(self):
        self.__update()
        return json.dumps([json.loads(plane.json()) for plane in self.planes.values()])

    def __str__(self):
        self.__update()
        res = f"+++++++[{datetime.datetime.now().strftime('%H:%M:%S')}]+++++++\n"
        for i, e in enumerate(self.planes.values()):
            res += f"{i})--------------------\n{e}\n"
        return res + "*****************"


