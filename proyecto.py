from machine import Pin, PWM
import utime
import random

leds=[Pin(6,Pin.OUT),Pin(7,Pin.OUT),Pin(8,Pin.OUT),Pin(9,Pin.OUT)]
botones=[Pin(10, Pin.IN, Pin.PULL_DOWN), Pin(11, Pin.IN, Pin.PULL_DOWN), Pin(12, Pin.IN, Pin.PULL_DOWN), Pin(13, Pin.IN, Pin.PULL_DOWN)]
switches=[Pin(0,Pin.IN),Pin(1,Pin.IN),Pin(2,Pin.IN)]
buzzer=PWM(Pin(3))