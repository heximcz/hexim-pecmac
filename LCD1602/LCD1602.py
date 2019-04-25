"""
Hardware:
LCD1602 ITEAD ADD-ON v1.0: https://www.itead.cc/wiki/RPI_LCD1602_ADD-ON_V1.0
&
Raspberry PI 3

Buttons configuration:
UP     - next (light on)
DOWN   - previous (light on)
SELECT - stop/start autorun (light on)
"""

import time
import board
import digitalio
import threading
import adafruit_character_lcd.character_lcd as characterlcd
from NcdIoCurrent import NcdIo


class LCD1602:

    def __init__(self, ncdio):

        # Current Values Board from NCD.io
        if not isinstance(NcdIo, ncdio):
            raise AssertionError
        self.ncdio = ncdio

        # Character LCD Config
        # Modify this if you have a different sized character LCD
        self.lcd_columns = 16
        self.lcd_rows = 2

        # Default back_light state (default False)
        self.blight = False
        # Back light, time in seconds (default 300 = 5min)
        self.btime = 300
        # Back light counter
        self.btime_counter = 0
        # Sleep time (default 100ms) - reduce CPU usage, use anything between 0.1 - 0.001
        self.sleep_time = 0.1
        # While counter
        self.while_counter = 0

        # messages
        self.message = dict()

        # Message counter
        self.message_sum = 3
        # Message actual index
        self.message_idx = 0
        # autoplay (boolean)
        self.autoplay = True

        # Raspberry Pi Pin Config:
        self.lcd_rs = digitalio.DigitalInOut(board.D23)
        self.lcd_en = digitalio.DigitalInOut(board.D24)
        self.lcd_d4 = digitalio.DigitalInOut(board.D17)
        self.lcd_d5 = digitalio.DigitalInOut(board.D18)
        self.lcd_d6 = digitalio.DigitalInOut(board.D27)
        self.lcd_d7 = digitalio.DigitalInOut(board.D22)
        self.lcd_back_light = digitalio.DigitalInOut(board.D25)

        # Init the lcd class
        self.lcd = characterlcd.Character_LCD_Mono(self.lcd_rs, self.lcd_en, self.lcd_d4, self.lcd_d5, self.lcd_d6,
                                                   self.lcd_d7, self.lcd_columns, self.lcd_rows, self.lcd_back_light)

        # Turn back_light off
        self.lcd.back_light = self.blight

        # Select button
        self.button_select = digitalio.DigitalInOut(board.D11)
        self.button_select.direction = digitalio.Direction.INPUT
        self.button_select.pull = digitalio.Pull.UP

        # Up button
        self.button_up = digitalio.DigitalInOut(board.D7)
        self.button_up.direction = digitalio.Direction.INPUT
        self.button_up.pull = digitalio.Pull.UP

        # Down button
        self.button_down = digitalio.DigitalInOut(board.D10)
        self.button_down.direction = digitalio.Direction.INPUT
        self.button_down.pull = digitalio.Pull.UP

        # load actual data from sensors
        self.refresh_messages()

        self.lock = threading.Lock()

    def back_light(self):
        """ BackLight on/off """
        if self.blight:
            self.btime_counter += 1
            if self.btime_counter > self.btime:
                self.btime_counter = 0
                self.lcd.back_light = False
                self.blight = False
            return
        if not self.blight:
            self.btime_counter = 0
            self.lcd.back_light = True
            self.blight = True
        return

    def msg_index(self, idx):
        """ message index manipulate """
        if idx >= self.message_sum:
            self.message_idx = 0
            return
        if idx < 0:
            self.message_idx = (self.message_sum - 1)
            return
        self.message_idx = idx
        return

    def auto_play_change(self, state):
        self.autoplay = state
        return

    def buttons(self):
        while True:
            """ Select button - on/off autoplay """
            if not self.button_select.value:
                with self.lock:
                    if not self.blight:
                        self.back_light()
                    if self.autoplay:
                        self.auto_play_change(False)
                    else:
                        self.auto_play_change(True)
                    time.sleep(.5)

            """ Button UP - mean next """
            if not self.button_up.value:
                self.auto_play_change(False)
                if not self.blight:
                    self.back_light()
                with self.lock:
                    self.lcd.clear()
                    self.msg_index(self.message_idx + 1)
                    self.lcd.message = self.message[self.message_idx]
                    time.sleep(.5)

            """ Button DOWN - mean back """
            if not self.button_down.value:
                self.auto_play_change(False)
                if not self.blight:
                    self.back_light()
                with self.lock:
                    self.lcd.clear()
                    self.msg_index(self.message_idx - 1)
                    self.lcd.message = self.message[self.message_idx]
                    time.sleep(.5)
            time.sleep(self.sleep_time)

    def messages(self):
        while True:
            if self.autoplay:
                while self.message_idx < self.message_sum:
                    if not self.autoplay:
                        break
                    with self.lock:
                        self.msg_index(self.message_idx)
                        self.lcd.clear()
                        self.lcd.message = self.message[self.message_idx]
                        self.message_idx += 1
                    time.sleep(3)
                self.message_idx = 0
            # CPU no 100%
            time.sleep(self.sleep_time)

    def back_light_control(self):
        while True:
            if self.blight:
                """check back_light expiration"""
                self.while_counter += self.sleep_time
                if self.while_counter >= 1:
                    self.while_counter = 0
                    self.back_light()
            time.sleep(self.sleep_time)

    def refresh_messages(self):
        """ load actual data """
        while True:
            data = self.ncdio.read_current()
            for i in range(0, self.ncdio.channels):
                # Convert the data to ampere
                current = self.ncdio.compute_current(i, data)
                # Output data to screen
                self.message[i] = "F{i}: {current}A\n    {watts}W"\
                    .format(i=i+1, current=current, watts=current*self.ncdio.volts)
            time.sleep(2)

    def run(self):
        # Create two threads as follows
        t_msgr = threading.Thread(name='messages', target=self.messages)
        t_button = threading.Thread(name='buttons', target=self.buttons)
        t_back_light = threading.Thread(name='back_light_control', target=self.back_light_control)
        t_messages = threading.Thread(name='reload_messages', target=self.refresh_messages())

        t_messages.start()
        t_msgr.start()
        t_button.start()
        t_back_light.start()