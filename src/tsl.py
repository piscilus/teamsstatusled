# -*- coding: utf-8 -*-

"""MS Teams Status LED

This tool accesses the current Microsoft Teams user presence state and maps it
to a color which is then displayed by a RGB-LED.
"""

__author__ = "<piscilus> Julian Krämer"
__copyright__ = "Copyright 2023, Julian Krämer"
__date__ = "2023-07-13"
__license__ = "MIT"
__version__ = "0.1.0-alpha"

import argparse
import contextlib
import os
import re
import sys
from time import sleep

from blinkstick310 import blinkstick
from file_read_backwards import FileReadBackwards

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='tsl',
                        description='Show MS Teams user presence state with LED',
                        epilog='Text at the bottom of help')
    parser.add_argument('-i', '--interval',
                        type=int,
                        default=5,
                        help="Interval in seconds to check state (default: 5)")
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    parser.add_argument('-V' '--version',
                        action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()

    state_colors = {"Offline"       : "#000000",
                    "Available"     : "#225500",
                    "Busy"          : "#552500",
                    "DoNotDisturb"  : "#550000",
                    "Away"          : "#555500",
                    "BeRightBack"   : "#553333",
                    "Presenting"    : "#550000",
                    "OnThePhone"    : "#552500",
                    "InAMeeting"    : "#552500"}

    bstick = blinkstick.find_first()
    if bstick == None:
        print("Error: BlinkStick not found!")
        sys.exit(1)

    bstick.set_led_count(8)
    bstick.set_mode(0)
    current_color = bstick.get_color(0, "hex")

    path = os.path.join(os.getenv('APPDATA'), "Microsoft", "Teams", "logs.txt")
    try:
        while True:
            state = "Offline"
            with FileReadBackwards(path, encoding="utf-8") as frb:
                for line in frb:
                    match = re.search(r'StatusIndicatorStateService: Added\s+(\w+)', line)
                    if match:
                        if match.group(1) != "NewActivity":
                            state = match.group(1)
                            break
            with contextlib.redirect_stdout(None) if not args.verbose else contextlib.nullcontext():
                try:
                    color = state_colors[state]
                except KeyError:
                    color = state_colors["Offline"]
                if current_color != color:
                    for i in range(1, 8, 2):
                        bstick.set_color(channel=0, index=i, hex=color)
                    current_color = color
                    print("Changing LED to: ", color)
            sleep(args.interval)
    except FileNotFoundError:
        print("Error: File not found: %s." % path)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    for i in range(1, 8, 2):
        bstick.set_color(channel=0, index=i, hex=state_colors["Offline"])
    sys.exit(0)
