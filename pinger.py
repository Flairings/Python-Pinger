import socket
import sys
import os
import json
import time
from colorama import Fore, init
from icmplib import ping, multiping, traceroute, resolve, Host, Hop, PID, NameLookupError
import signal
init()

# clears the screen for windows and linux
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class GracefulInterruptHandler(object):

    def __init__(self, sig=signal.SIGINT):
        self.sig = sig

    def __enter__(self):

        self.interrupted = False
        self.released = False

        self.original_handler = signal.getsignal(self.sig)

        def handler(signum, frame):
            self.release()
            self.interrupted = True

        signal.signal(self.sig, handler)

        return self

    def __exit__(self, type, value, tb):
        self.release()

    def release(self):

        if self.released:
            return False

        signal.signal(self.sig, self.original_handler)

        self.released = True

        return True


with open("config.json", "r") as settings:
    config = json.load(settings)
    color = config.get("color")
    online_color = config.get("online-color")
    offline_color = config.get("offline-color")
    online = config.get("online")
    offline = config.get("offline")

if color == "RED":
    color = Fore.RED
elif color == "LIGHT_RED":
    color = Fore.LIGHTRED_EX
elif color == "BLUE":
    color = Fore.BLUE
elif color == "LIGHT_BLUE":
    color = Fore.LIGHTBLUE_EX
elif color == "MAGENTA":
    color = Fore.MAGENTA
elif color == "LIGHT_MAGENTA":
    color = Fore.LIGHTMAGENTA_EX
elif color == "YELLOW":
    color = Fore.YELLOW
elif color == "LIGHT_YELLOW":
    color = Fore.LIGHTYELLOW_EX
elif color == "GREEN":
    color = Fore.GREEN
elif color == "LIGHT_GREEN":
    color = Fore.LIGHTGREEN_EX
elif color == "CYAN":
    color = Fore.CYAN
elif color == "LIGHT_CYAN":
    color = Fore.LIGHTCYAN_EX
elif color == "BLACK":
    color = Fore.BLACK
else:
    color = Fore.LIGHTWHITE_EX
    print("color is invalid.")

if online_color == "RED":
    online_color = Fore.RED
elif online_color == "LIGHT_RED":
    online_color = Fore.LIGHTRED_EX
elif online_color == "BLUE":
    online_color = Fore.BLUE
elif online_color == "LIGHT_BLUE":
    online_color = Fore.LIGHTBLUE_EX
elif online_color == "MAGENTA":
    online_color = Fore.MAGENTA
elif online_color == "LIGHT_MAGENTA":
    online_color = Fore.LIGHTMAGENTA_EX
elif online_color == "YELLOW":
    online_color = Fore.YELLOW
elif online_color == "LIGHT_YELLOW":
    online_color = Fore.LIGHTYELLOW_EX
elif online_color == "GREEN":
    online_color = Fore.GREEN
elif online_color == "LIGHT_GREEN":
    online_color = Fore.LIGHTGREEN_EX
elif online_color == "CYAN":
    online_color = Fore.CYAN
elif online_color == "LIGHT_CYAN":
    online_color = Fore.LIGHTCYAN_EX
elif online_color == "BLACK":
    online_color = Fore.BLACK
else:
    online_color = Fore.LIGHTWHITE_EX
    print("online_color is invalid.")

if offline_color == "RED":
    offline_color = Fore.RED
elif offline_color == "LIGHT_RED":
    offline_color = Fore.LIGHTRED_EX
elif offline_color == "BLUE":
    offline_color = Fore.BLUE
elif offline_color == "LIGHT_BLUE":
    offline_color = Fore.LIGHTBLUE_EX
elif offline_color == "MAGENTA":
    offline_color = Fore.MAGENTA
elif offline_color == "LIGHT_MAGENTA":
    offline_color = Fore.LIGHTMAGENTA_EX
elif offline_color == "YELLOW":
    offline_color = Fore.YELLOW
elif offline_color == "LIGHT_YELLOW":
    offline_color = Fore.LIGHTYELLOW_EX
elif offline_color == "GREEN":
    offline_color = Fore.GREEN
elif offline_color == "LIGHT_GREEN":
    offline_color = Fore.LIGHTGREEN_EX
elif offline_color == "CYAN":
    offline_color = Fore.CYAN
elif offline_color == "LIGHT_CYAN":
    offline_color = Fore.LIGHTCYAN_EX
elif offline_color == "BLACK":
    offline_color = Fore.BLACK
else:
    offline_color = Fore.LIGHTWHITE_EX
    print("offline_color is invalid.")

def start():
    clear()
    print("")
    print(f"  {color}Press CTRL + C to return at any time.")
    print("")
    address = input(f"{color}IP: ")

    with GracefulInterruptHandler() as h:
        while 1:
            try:
                host = ping(address, count=1, interval=0.1)
                if host.is_alive:
                    print(f"{online_color}{online}"
                          .replace("{host.address}", host.address)
                          .replace("{host.min_rtt}", (str(host.min_rtt)))
                          .replace("{host.avg_rtt}", (str(host.min_rtt)))
                          .replace("{host.max_rtt}", (str(host.max_rtt))))
                else:
                    print(f"{offline_color}{offline}"
                          .replace("{host.address}", host.address)
                          .replace("{host.min_rtt}", (str(host.min_rtt)))
                          .replace("{host.avg_rtt}", (str(host.min_rtt)))
                          .replace("{host.max_rtt}", (str(host.max_rtt))))
            except NameLookupError as e:
                print("Could not find address.")
                time.sleep(2)
                start()
            if h.interrupted:
                print("Returning")
                time.sleep(2)
                start()
                break

start()
