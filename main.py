from subprocess import call
from car_controller import CarController


def on_disconnect():
    call("sudo reboot", shell=True)


controller = CarController(interface="/dev/input/js0")
controller.listen(on_disconnect=on_disconnect)
