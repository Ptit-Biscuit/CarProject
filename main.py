from subprocess import call
from car_controller import CarController

# Konami code
konami_code = ["up", "up", "down", "down", "left", "right", "left", "right", "share", "options"]


def konami_callback():
    print("Konami code detected!")


def special_inputs():
    return [{"inputs": konami_code, "callback": konami_callback}]


def on_disconnect():
    # call("sudo reboot", shell=True)
    pass


controller = CarController(interface="/dev/input/js0")
controller.listen(on_disconnect=on_disconnect, special_inputs=special_inputs())
