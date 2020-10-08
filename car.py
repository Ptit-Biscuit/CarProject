import threading
from gpiozero import AngularServo, Servo


class Car:

    def __init__(self, controller_connected):
        self.front_right_wheel = Servo(16)
        self.front_left_wheel = Servo(19)
        self.back_right_wheel = Servo(20)
        self.back_left_wheel = Servo(26)
        self.steering_servo = AngularServo(21, min_angle=-45, max_angle=45)
        self.speed = -1
        self.limiter = -1
        self.regulator = threading.Event()
        self.regulator_thread = threading.Thread(target=self.regulator_run, args=(lambda: controller_connected,))
        self.regulator_thread.start()
        self.regulator_thread.join()

    def regulator_run(self, controller_connected):
        while controller_connected():
            if self.regulator.wait(2):
                self.throttle(self.speed)

    def throttle(self, value):
        self.front_right_wheel.value = value
        self.front_left_wheel.value = value

    def reverse(self, value):
        self.back_right_wheel.value = value
        self.back_left_wheel.value = value

    def steer(self, value):
        self.steering_servo.angle = value

    def stop(self):
        self.front_right_wheel.min()
        self.front_left_wheel.min()
        self.back_right_wheel.min()
        self.back_left_wheel.min()
