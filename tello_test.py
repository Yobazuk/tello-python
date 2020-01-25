from tello import *
from keyboard_controller import *
import time


def main():
    server = Server()
    drone = Tello()
    controller = KeyboardController(drone)

    '''print(drone.takeoff())
    print(drone.get_battery())
    time.sleep(3)
    print(drone.flip('l'))
    time.sleep(0.4)
    print(drone.flip('r'))
    time.sleep(1)
    print(drone.land())'''


if __name__ == '__main__':
    main()
