import datetime
import json
import time

import pyModeS as pms

from constants import constants


class Plane:
    def __init__(self, icao):
        self.icao = icao
        self.callsign = None
        self.category = None
        self.odd = None
        self.even = None
        self.speed = None
        self.heading = None
        self.altitude = None
        self.last = datetime.datetime.now()

    def update_callsign(self, callsign):
        self.callsign = callsign
        self.__update()

    def update_category(self, cat):
        self.category = cat
        self.__update()

    def update_speed(self, speed):
        self.speed = speed
        self.__update()

    def update_heading(self, heading):
        self.heading = heading
        self.__update()

    def update_altitude(self, altitude):
        self.altitude = altitude
        self.__update()

    def update_position(self, message):
        if pms.adsb.oe_flag(message):  # isodd
            self.odd = {"msg": message, "t": int(time.time())}
        else:
            self.even = {"msg": message, "t": int(time.time())}
        self.__update()

        if constants['logging']:
            pos = self.__calc_position()
            if pos:
                f = open("./coords.csv", 'a')
                f.write(f"{round(self.last.timestamp())},{self.icao},{pos[0]},{pos[1]},{pms.adsb.altitude(message)}\n")
                f.close()

    def __calc_position(self):
        if self.odd and self.even:
            try:
                return pms.adsb.position(
                    self.even["msg"], self.odd["msg"],
                    self.even["t"], self.odd["t"],
                    constants['observer'][0], constants['observer'][1]
                )
            except RuntimeError:
                return None
        return None

    def __update(self):
        self.last = datetime.datetime.now()

    def json(self):
        res = {
            "icao": self.icao,
            "callsign": self.callsign,
            "category": self.category,
            "position": self.__calc_position(),
            "speed": self.speed,
            "heading": self.heading,
            "altitude": self.altitude,
            "time": round(self.last.timestamp())
        }
        return json.dumps(res)

    def __str__(self):
        return f"[{self.last.strftime('%H:%M:%S')}] {self.callsign} ({self.category})\n" \
               f"ICAO: {self.icao}\n" \
               f"odd: {self.odd}, even: {self.even}\n" \
               f"speed: {self.speed}km/h, heading: {self.heading}°, altitude: {self.altitude}m"
