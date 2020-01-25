from tello import *
from keyboard_controller import *
import time


def main():
    server = Server()
    drone = Tello()
    # controller = KeyboardController(drone)

    print(drone.takeoff())
    print(drone.get_battery())
    time.sleep(2)
    print(drone.flip('l'))
    time.sleep(0.5)
    print(drone.flip('r'))
    time.sleep(0.2)
    print(drone.land())


if __name__ == '__main__':
    main()
