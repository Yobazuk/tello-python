from pynput.keyboard import Key, Listener, KeyCode


class KeyboardController:

    DEFAULT_MOVE_DIST = 90
    DEFAULT_DEGREE_TURN = 90

    def __init__(self, drone):
        self.drone = drone

        self.move_functions = {KeyCode.from_char('a'): 'move_left', KeyCode.from_char('d'): 'move_right',
                               KeyCode.from_char('w'): 'move_forward', KeyCode.from_char('s'): 'move_backward',
                               Key.left: 'rotate_ccw', Key.right: 'rotate_cw', Key.up: 'move_up', Key.down: 'move_down'}
        self.functions = {Key.tab: 'takeoff', Key.backspace: 'land', Key.esc: 'emergency_stop', 
                          KeyCode.from_char('b'): 'print_battery', KeyCode.from_char('t'): 'throw_and_go'}

        self.flips = {KeyCode.from_char('z'): 'l', KeyCode.from_char('x'): 'r', KeyCode.from_char('c'): 'b'}

        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.daemon = True
        self.listener.start()
        self.listener.join()

    def on_press(self, key):
        print(f'key {key} pressed')
        if self.drone is not None:
            if key in self.functions.keys():
                print(self.functions[key])
                getattr(self.drone, self.functions[key])()
            elif key in self.move_functions.keys():
                print(self.move_functions[key])
                getattr(self.drone, self.move_functions[key])(self.DEFAULT_MOVE_DIST)
            elif key in self.flips.keys():
                print('flip ' + self.flips[key])
                getattr(self.drone, 'flip')(self.flips[key])
            else:
                print('Unrecognized Key!')

    @ staticmethod
    def on_release(key):
        print(f'key {key} released')
