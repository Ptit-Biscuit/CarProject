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

    # R2 range forward acceleration
    def on_R2_press(self, value):
        self.car.forward(map_from_to(value, self.min_value, self.max_value, 0, 1))

    def on_R2_release(self):
        self.car.stop()

    # L2 range backward acceleration
    def on_L2_press(self, value):
        self.car.backward(map_from_to(value, self.min_value, self.max_value, 0, 1))

    def on_L2_release(self):
        self.car.stop()

    # R3 for steering left / right
    def on_R3_x_at_rest(self):
        self.car.steer(0)

    def on_R3_left(self, value):
        self.car.steer(map_from_to(value, 0, self.min_value, 0, self.car.steering_servo.min_angle))

    def on_R3_right(self, value):
        self.car.steer(map_from_to(value, 0, self.max_value, 0, self.car.steering_servo.max_angle))
