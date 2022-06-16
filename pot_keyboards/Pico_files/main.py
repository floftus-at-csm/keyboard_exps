# all these imports come from MicroPython. https://docs.micropython.org/en/latest/index.html
from urandom import randint
import uselect
from machine import Pin, SPI, PWM, RTC
import framebuf
import time
import random
from epaper import EPD_7in5
import gc
import math
from sys import stdin, exit
import micropython
import sys

# size of each letter in pixels
CHARACTER_SIZE = 8

# how serial lines are ended
TERMINATOR = "\n"

class Pico:
    """
    Global singleton, so we can use `self`. instead of global.
    Not sure if this will increase ram usage.
    """

    def __init__(self):
        """
        Run any once-off startup tasks.
        Set up the global e-paper display.
        """

        self.epd = EPD_7in5()
        self.epd.Clear()

        self.run_loop = True

        # store incomplete lines from serial here. list of strings (no typing module in micropython)
        self.buffered_input = []
        # when we get a full line store it here, without the terminator.
        # gets overwritten if a new line is read (as early as next tick).
        # blanked each tick.
        self.input_line_this_tick = ""

    def main(self):
        """
        Code entrypoint.
        The function that gets called to start.
        All non-setup code here or in functions under it.
        """
        counter = 0

        latest_input_line = ""
        lines_of_text = []
        # main loop
        while self.run_loop:


            # buffer from the USB to serial port
            self.read_serial_input()


            # show serial input on the screen.
            # only update if we have a new line
            if self.input_line_this_tick:
                latest_input_line = self.input_line_this_tick
                lines_of_text.append(latest_input_line)
            # self.lcd.text(latest_input_line, 5, 14, 0xFFFF)
            # need to do this differently - have a signal that this is the end of the message
            # e.g contents /n
            # contents /n
            # contens /n
            # ending_message /n
            # then break out of the loop and display the image

            ########################### end app per tick code here


            # quit program to avoid locking serial up if specified
            if latest_input_line == "ending_message":
                self.exit()

            # simple loop speed control
            time.sleep_ms(100)

            return lines_of_text



    def read_serial_input(self):
        """
        Buffers serial input.
        Writes it to input_line_this_tick when we have a full line.
        Clears input_line_this_tick otherwise.
        """
        # stdin.read() is blocking which means we hang here if we use it. Instead use select to tell us if there's anything available
        # note: select() is deprecated. Replace with Poll() to follow best practises
        select_result = uselect.select([stdin], [], [], 0)
        while select_result[0]:
            # there's no easy micropython way to get all the bytes.
            # instead get the minimum there could be and keep checking with select and a while loop
            input_character = stdin.read(1)
            # add to the buffer
            self.buffered_input.append(input_character)
            # check if there's any input remaining to buffer
            select_result = uselect.select([stdin], [], [], 0)
        # if a full line has been submitted
        if TERMINATOR in self.buffered_input:
            line_ending_index = self.buffered_input.index(TERMINATOR)
            # make it available
            self.input_line_this_tick = "".join(self.buffered_input[:line_ending_index])
            # remove it from the buffer.
            # If there's remaining data, leave that part. This removes the earliest line so should allow multiple lines buffered in a tick to work.
            # however if there are multiple lines each tick, the buffer will continue to grow.
            if line_ending_index < len(self.buffered_input):
                self.buffered_input = self.buffered_input[line_ending_index + 1 :]
            else:
                self.buffered_input = []
        # otherwise clear the last full line so subsequent ticks can infer the same input is new input (not cached)
        else:
            self.input_line_this_tick = ""



    def exit(self):
        self.run_loop = False

    def on_key_a_pressed(self, p):
        print("key a pressed: ", p)

switch_off = False
# start the code
if __name__ == "__main__":
    pico = Pico()
    val = 60
    loop_num = 0
    while switch_off == False:
        current_text_image = pico.main()
        for _ in range(val):
            current_string = current_text_image[val-loop_num]
            pico.epd.text(current_string, 0, (val-loop_num-1)*8, 0xff)
        pico.epd.display(pico.epd.buffer)
        pico.epd.delay_ms(500)


    
    # display here
    # then go back into the loop
    # when the above exits, clean up
    gc.collect()