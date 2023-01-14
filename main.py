#!/usr/bin/env python

import press
import random
import itertools
from tkinter import *
import RPi.GPIO as GPIO

root = Tk()


class Timer:
    def __init__(self, master):
        self.master = master
        # Set up screen and labels
        root.geometry("320x240")
        self.display1 = Label(master, font=("Arial", 25))
        self.display1.place(relx=.5, rely=.5, anchor=S)
        self.display2 = Label(master, font=("Arial", 25))
        self.display2.place(relx=.5, rely=.5, anchor=N)
        self.display1['text'] = 'Game On!'
        # Set up main button press
        reg_event = press.Button(GPIO.IN, GPIO.PUD_DOWN, GPIO.FALLING, self.start)
        reg_event.setup()
        reg_event.event()
        # Press count variable
        self.time_limit = 5
        self.press_count = 0
        # Pick fisrt player and set up cycle
        people = ['Gordon', 'Claire', 'Emma', 'Steve']
        player_count = len(people)
        player_num = random.randint(0, player_count - 1)
        player_cycle = []
        for i in range(player_count):
            player_cycle.append(people[player_num % player_count])
            player_num += 1
        self.next_players = itertools.cycle(player_cycle)

    def start(self, channel):
        # Show randomised First player on first press
        if self.press_count == 0:
            self.player = next(self.next_players)
            self.display1['text'] = self.player + ", You Go First!"
            self.press_count += 1
        elif self.press_count == 1:
            # Start the countdown for first player
            self.timer_text = DoubleVar()
            self.timer_text.set(self.time_limit + 1)
            self.display1['text'] = self.player
            self.display2['textvariable'] = self.timer_text
            self.increment_timer()
            self.press_count += 1
        # Restart the countdown and get the next player
        else:
            self.player = next(self.next_players)
            self.timer_text = DoubleVar()
            self.timer_text.set(self.time_limit)
            self.display1['text'] = self.player
            self.display2['textvariable'] = self.timer_text
            self.press_count += 1

    def increment_timer(self):
        ctr = int(self.timer_text.get())
        # countdown -1 second every second until we hit zero
        if ctr > 0:
            self.timer_text.set(ctr - 1)
            self.master.update()
            self.master.after(1000, self.increment_timer)
        # on zero give shit to the loser
        else:
            self.display1['text'] = self.player + ', You Fucked It!'
            root.update()
            # wait for the button to be pressed again
            wait_event = press.Button(GPIO.IN, GPIO.PUD_DOWN, GPIO.FALLING, self.start)
            wait_event.wait()
            # sends us back to the middle condition on start nut progresses us to the next player
            self.player = next(self.next_players)
            self.press_count = 1


app = Timer(root)
root.mainloop()
