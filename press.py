#!/usr/bin/env python

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


class Button:
    def __init__(self, inout, updown, fallrise, call):
        self.inout = inout
        self.updown = updown
        self.fallrise = fallrise
        self.call = call

    def setup(self):
        GPIO.setup(10, self.inout, pull_up_down=self.updown)
        GPIO.setup(12, self.inout, pull_up_down=self.updown)

    def event(self):
        GPIO.add_event_detect(10, self.fallrise, callback=self.call, bouncetime=1000)

    def wait(self):
        GPIO.wait_for_edge(12, self.fallrise, bouncetime=1000)
