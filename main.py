from subprocess import call
from car_controller import CarController

controller = CarController(interface="/dev/input/js0")
controller.listen(on_disconnect=(call("sudo reboot", shell=True)))
