from subprocess import call
from car_controller import CarController


# Konami code
konami_code = ["up_arrow_button", "up_arrow_button", "down_arrow_button", "down_arrow_button", "left_arrow_button",
               "right_arrow_button", "left_arrow_button", "right_arrow_button", "share_button", "options_button"]


def konami_callback():
    print("Konami code detected!")


def special_inputs():
    return [[konami_code, konami_callback, 0]]


def on_disconnect():
    # call("sudo reboot", shell=True)
    pass


controller = CarController(interface="/dev/input/js0")
controller.listen(on_disconnect=on_disconnect, special_inputs=special_inputs())
