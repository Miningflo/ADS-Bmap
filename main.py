import datetime
import http
import json
import shlex
import threading
from http.server import HTTPServer
from subprocess import Popen, PIPE, STDOUT
import pyModeS as pms

import constants
from planelist import PlaneList
from server import MyHandler


def lookup(type, value):
    if value < 0:
        return "Recursion error"
    try:
        return table[type][str(value)]
    except KeyError:
        value -= 1
        return lookup(type, value)


def decode(l):
    line = l.decode("utf-8").strip()
    if line.startswith("*"):
        msg = line[1:-1]
        if pms.crc(msg) == 0:
            icao = pms.icao(msg).upper()
            df = pms.df(msg)
            if df == 17:
                tc = pms.adsb.typecode(msg)
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] |{icao}| " + lookup("message", tc) + f" ({tc})")
                if tc <= 4:
                    cat = pms.adsb.category(msg)
                    c = "No category information"
                    if cat != 0:
                        c = lookup("category", int(str(tc) + str(cat)))
                    planelist.category(icao, c)
                    call = pms.adsb.callsign(msg).replace("_", " ").strip()
                    planelist.callsign(icao, call)
                elif tc == 19:
                    (speed, heading, vrate, *other) = pms.adsb.velocity(msg)
                    speed *= 1.852
                    vrate *= 0.3048
                    planelist.speed(icao, round(speed, 2))
                    planelist.heading(icao, heading)
                elif tc <= 22:
                    alt = pms.adsb.altitude(msg)
                    alt *= 0.3048
                    planelist.altitude(icao, round(alt, 2))
                    planelist.position(icao, msg)
                # print(planelist)
    else:
        print(line)


def run_command(command):
    process = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    for line in process.stdout:
        try:
            decode(line)
        except UnicodeDecodeError:
            print(line)


f = open("lookup.json")
table = json.load(f)
f.close()
planelist = PlaneList()

handler = MyHandler(planelist)
server = http.server.HTTPServer(constants.server_address, handler)
print(f"Starting server on http://{constants.server_address[0]}:{constants.server_address[1]}")
thread = threading.Thread(target=server.serve_forever)
thread.setDaemon(True)
thread.start()

print("It is normal the copyright notice is buffered, RAW output is unbuffered")
print("Currently Handling DF17 messages 1-22 (identification, position and velocity)")
run_command(f"{constants.dump1090} --raw --fix")
