from car import Car
from controller import Controller


def map_from_to(x, a, b, c, d):
    return (x - a) / (b - a) * (d - c) + c


class CarController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.car = Car()
        self.min_value = -32767
        self.max_value = 32767
        self.throttle = -1
        self.limiter = False
        self.regulator = False

    # R1 for limiter
    def on_R1_press(self):
        self.limiter = not self.limiter
        self.regulator = False

    # L1 for regulator
    def on_L1_press(self):
        self.regulator = not self.regulator
        self.limiter = False

    # R2 for throttle
    def on_R2_press(self, value):
        self.throttle = map_from_to(value, self.min_value, self.max_value, 0, 1 if not self.limiter else self.throttle)
        print("value: {} throttle: {}".format(value, self.throttle))
        self.car.throttle(self.throttle)
        if self.regulator:
            self.on_R2_press(value)

    def on_R2_release(self):
        self.car.stop()

    # L2 for reverse
    def on_L2_press(self, value):
        self.car.reverse(map_from_to(value, self.min_value, self.max_value, 0, 1))

    def on_L2_release(self):
        self.car.stop()

    # R3 for steering
    def on_R3_x_at_rest(self):
        self.car.steer(0)

    def on_R3_left(self, value):
        self.car.steer(map_from_to(value, 0, self.min_value, 0, self.car.steering_servo.min_angle))

    def on_R3_right(self, value):
        self.car.steer(map_from_to(value, 0, self.max_value, 0, self.car.steering_servo.max_angle))
