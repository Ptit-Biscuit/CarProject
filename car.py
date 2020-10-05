from gpiozero import AngularServo, Servo


class Car:

    def __init__(self):
        self.front_right_wheel = Servo(16)
        self.front_left_wheel = Servo(19)
        self.back_right_wheel = Servo(20)
        self.back_left_wheel = Servo(26)
        self.steering_servo = AngularServo(21, min_angle=-45, max_angle=45)

    def forward(self, value):
        self.front_right_wheel.value = value
        self.front_left_wheel.value = value

    def backward(self, value):
        self.back_right_wheel = value
        self.back_left_wheel = value

    def steer(self, value):
        self.steering_servo.angle = value

    def stop(self):
        self.front_right_wheel.min()
        self.front_left_wheel.min()
        self.back_right_wheel.min()
        self.back_left_wheel.min()
