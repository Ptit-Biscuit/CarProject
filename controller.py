import os
import struct
import time
from actions import Actions
from event import Event

# Konami code
konami_code = ["up_arrow_button", "up_arrow_button", "down_arrow_button", "down_arrow_button", "left_arrow_button",
               "right_arrow_button", "left_arrow_button", "right_arrow_button", "share_button", "options_button"]


def check_for(sub, full, start_index):
    return [start for start in range(start_index, len(full) - len(sub) + 1) if sub == full[start:start + len(sub)]]


class Controller(Actions):

    def __init__(self, interface, event_definition=None, event_format=None):
        """
        Initiate controller instance that is capable of listening to all events on specified input interface
        :param interface: STRING aka /dev/input/js0 or any other PS4 Dualshock controller interface.
                          You can see all available interfaces with a command "ls -la /dev/input/"
        """
        Actions.__init__(self)
        self.stop = False
        self.is_connected = False
        self.interface = interface
        self.debug = False  # If you want to see raw event stream, set this to True.
        self.black_listed_buttons = []  # set a list of blocked buttons if you don't want to process their events
        self.event_definition = event_definition if event_definition else Event
        self.event_format = event_format if event_format else "LhBB"
        self.event_size = struct.calcsize(self.event_format)
        self.event_history = []
        self.konami_index = 0

    def listen(self, timeout=30, on_connect=None, on_disconnect=None, on_konami=None):
        """
        Start listening for events on a given self.interface
        :param timeout: INT, seconds. How long you want to wait for the self.interface.
                        This allows you to start listening and connect your controller after the fact.
                        If self.interface does not become available in N seconds, the script will exit with exit code 1.
        :param on_connect: function object, allows to register a call back when connection is established
        :param on_disconnect: function object, allows to register a call back when connection is lost
        :param on_konami: function object, allows to register a call back when konami command is played
        :return: None
        """

        def on_disconnect_callback():
            self.is_connected = False
            if on_disconnect is not None:
                on_disconnect()

        def on_connect_callback():
            self.is_connected = True
            if on_connect is not None:
                on_connect()

        def on_konami_callback():
            if on_konami is not None:
                on_konami()
            else:
                print("konami command detected!")

        def wait_for_interface():
            print("Waiting for interface: {} to become available . . .".format(self.interface))
            for i in range(timeout):
                if os.path.exists(self.interface):
                    print("Successfully bound to: {}.".format(self.interface))
                    on_connect_callback()
                    return
                time.sleep(1)
            print("Timeout({} sec). Interface not available.".format(timeout))
            exit(1)

        def read_events():
            try:
                return _file.read(self.event_size)
            except IOError:
                print("Interface lost. Device disconnected?")
                on_disconnect_callback()
                exit(1)

        wait_for_interface()
        try:
            _file = open(self.interface, "rb")
            event = read_events()
            while not self.stop and event:
                (*tv_sec, value, button_type, button_id) = struct.unpack(self.event_format, event)
                if self.debug:
                    print("button_id: {} button_type: {} value: {}".format(button_id, button_type, value))
                self.__handle_event(button_id=button_id, button_type=button_type, value=value)
                check = check_for(konami_code, self.event_history, self.konami_index)
                if len(check) != 0:
                    self.konami_index = check[0] + 1
                    on_konami_callback()
                event = read_events()
        except KeyboardInterrupt:
            print("\nExiting (Ctrl + C)")
            on_disconnect_callback()
            exit(1)

    def __handle_event(self, button_id, button_type, value):
        event = self.event_definition(button_id=button_id, button_type=button_type, value=value)

        if event.R3_event():
            self.event_history.append("right_joystick")
            if event.R3_y_at_rest():
                self.on_R3_y_at_rest()
            elif event.R3_x_at_rest():
                self.on_R3_x_at_rest()
            elif event.R3_right():
                self.on_R3_right(value)
            elif event.R3_left():
                self.on_R3_left(value)
            elif event.R3_up():
                self.on_R3_up(value)
            elif event.R3_down():
                self.on_R3_down(value)
        elif event.L3_event():
            self.event_history.append("left_joystick")
            if event.L3_y_at_rest():
                self.on_L3_y_at_rest()
            elif event.L3_x_at_rest():
                self.on_L3_x_at_rest()
            elif event.L3_up():
                self.on_L3_up(value)
            elif event.L3_down():
                self.on_L3_down(value)
            elif event.L3_left():
                self.on_L3_left(value)
            elif event.L3_right():
                self.on_L3_right(value)
        elif event.circle_pressed():
            self.event_history.append("circle_button")
            self.on_circle_press()
        elif event.circle_released():
            self.on_circle_release()
        elif event.x_pressed():
            self.event_history.append("x_button")
            self.on_x_press()
        elif event.x_released():
            self.on_x_release()
        elif event.triangle_pressed():
            self.event_history.append("triangle_button")
            self.on_triangle_press()
        elif event.triangle_released():
            self.on_triangle_release()
        elif event.square_pressed():
            self.event_history.append("square_button")
            self.on_square_press()
        elif event.square_released():
            self.on_square_release()
        elif event.L1_pressed():
            self.event_history.append("left_button_1")
            self.on_L1_press()
        elif event.L1_released():
            self.on_L1_release()
        elif event.L2_pressed():
            self.event_history.append("left_button_2")
            self.on_L2_press(value)
        elif event.L2_released():
            self.on_L2_release()
        elif event.R1_pressed():
            self.event_history.append("right_button_1")
            self.on_R1_press()
        elif event.R1_released():
            self.on_R1_release()
        elif event.R2_pressed():
            self.event_history.append("right_button_2")
            self.on_R2_press(value)
        elif event.R2_released():
            self.on_R2_release()
        elif event.options_pressed():
            self.event_history.append("options_button")
            self.on_options_press()
        elif event.options_released():
            self.on_options_release()
        elif event.left_right_arrow_released():
            self.on_left_right_arrow_release()
        elif event.up_down_arrow_released():
            self.on_up_down_arrow_release()
        elif event.left_arrow_pressed():
            self.event_history.append("left_arrow_button")
            self.on_left_arrow_press()
        elif event.right_arrow_pressed():
            self.event_history.append("right_arrow_button")
            self.on_right_arrow_press()
        elif event.up_arrow_pressed():
            self.event_history.append("up_arrow_button")
            self.on_up_arrow_press()
        elif event.down_arrow_pressed():
            self.event_history.append("down_arrow_button")
            self.on_down_arrow_press()
        elif event.playstation_button_pressed():
            self.event_history.append("ps_button")
            self.on_playstation_button_press()
        elif event.playstation_button_released():
            self.on_playstation_button_release()
        elif event.share_pressed():
            self.event_history.append("share_button")
            self.on_share_press()
        elif event.share_released():
            self.on_share_release()
        elif event.R3_pressed():
            self.event_history.append("right_joystick_button")
            self.on_R3_press()
        elif event.R3_released():
            self.on_R3_release()
        elif event.L3_pressed():
            self.event_history.append("left_joystick_button")
            self.on_L3_press()
        elif event.L3_released():
            self.on_L3_release()