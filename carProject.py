#!/usr/bin/env python

from subprocess import call
from gpiozero import AngularServo, Servo
from controller import Controller

frontRight = Servo(16)
frontLeft = Servo(19)
backRight = Servo(20)
backLeft = Servo(26)
steering = AngularServo(21, min_angle=-45, max_angle=45)


def map_from_to(x, a, b, c, d):
    return (x - a) / (b - a) * (d - c) + c


def on_connect():
    frontRight.min()
    frontLeft.min()
    backRight.min()
    backLeft.min()
    steering.angle = 0


def on_disconnect():
    # call("sudo shutdown -P 0", shell=True)
    pass


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    # R2 range forward acceleration
    def on_R2_press(self, value):
        forward = map_from_to(value, -32767, 32767, 0, 1)
        frontRight.value = forward
        frontLeft.value = forward

    def on_R2_release(self):
        frontRight.min()
        frontLeft.min()

    # L2 range backward acceleration
    def on_L2_press(self, value):
        backward = map_from_to(value, -32767, 32767, 0, 1)
        backRight.value = backward
        backLeft.value = backward

    def on_L2_release(self):
        backRight.min()
        backLeft.min()

    # R3 for steering left / right
    def on_R3_x_at_rest(self):
        steering.angle = 0

    def on_R3_left(self, value):
        steering.angle = map_from_to(value, 0, -32767, 0, steering.min_angle)

    def on_R3_right(self, value):
        steering.angle = map_from_to(value, 0, 32767, 0, steering.max_angle)


controller = MyController(interface="/dev/input/js0")
controller.listen(on_connect=on_connect, on_disconnect=on_disconnect)
