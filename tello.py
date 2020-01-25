import socket
from threading import Thread


class Server:
    """
        Receiving Tello's state
    """
    def __init__(self):
        self.local_ip = '0.0.0.0'
        self.local_port = 8890
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.local_ip, self.local_port))
        self._receive_thread = Thread(target=self.receive_thread)
        self._receive_thread.daemon = True
        self._receive_thread.start()
        self.data = None

    def parse(self):
        if self.data:
            params = [(p.split(':')) for p in self.data[:-1:].split(';')]
            return params
        return None

    def receive_thread(self):
        while True:
            try:
                self.data, ip = self.socket.recvfrom(4096)
                self.data = self.data.decode()
            except socket.error as e:
                print(f"Caught exception socket.error : {e}")


class Tello:
    """
        Sending and receiving basic commands and data.
    """
    def __init__(self):
        self._port = 8889
        self._ip = '192.168.10.1'
        self.address = (self._ip, self._port)
        self.response = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self._port))
        self.socket.sendto(b'command', self.address)
        self._receive_thread = Thread(target=self.receive_thread)
        self._receive_thread.daemon = True
        self._receive_thread.start()

    def land(self):
        """
        :return: Response from Tello, 'OK' or 'ERROR'.
        """
        return self.send_command('land')

    def takeoff(self):
        """
        :return: Response from Tello, 'OK' or 'ERROR'.
        """
        return self.send_command('takeoff')

    def throw_and_go(self):
        return self.send_command('throw and go')

    def flip(self, direction):
        """
        :param direction: Direction to flip, 'l', 'r', 'f', 'b'.
        :return: Response from Tello, 'OK' or 'ERROR'.
        """
        return self.send_command(f'flip {direction}')

    def move(self, direction, distance):
        # distance = int(round(float(distance) * 100))
        return self.send_command(f'{direction} {distance}')

    def rotate(self, direction, degree):
        """
        :param direction: Direction to rotate: 'cw' (clockwise), 'ccw' (counter-clockwise).
        :param degree: Degree range 1-3600.
        :return: Response from Tello, 'OK' or 'ERROR'.
        """
        return self.send_command(f'{direction} {degree}')

    def rotate_cw(self, degree):
        return self.rotate('cw', degree)

    def rotate_ccw(self, degree):
        return self.rotate('ccw', degree)

    def move_up(self, distance):
        return self.move('up', distance)

    def move_down(self, distance):
        return self.move('down', distance)

    def move_forward(self, distance):
        return self.move('forward', distance)

    def move_backward(self, distance):
        return self.move('back', distance)

    def move_right(self, distance):
        return self.move('right', distance)

    def move_left(self, distance):
        return self.move('left', distance)

    def go(self, x, y, z, speed):
        """
        Fly to x y z in speed
        :param x: 20-500
        :param y: 20-500
        :param z: 20-500
        :param speed: 10-100
        :return: Response from Tello, 'OK' or 'ERROR'.
        """
        return self.send_command(f'go {x} {y} {z} {speed}')

    def set_speed(self, speed):
        speed = int(round(float(speed)))
        return self.send_command(f'speed {speed}')

    def get_battery(self):
        battery = self.send_command('battery?')
        try:
            battery = int(battery)
        except Exception as e:
            print(e)
        return battery

    def get_speed(self):
        speed = self.send_command('speed?')
        try:
            speed = float(speed)
        except Exception as e:
            print(e)
        return speed

    def get_height(self):
        height = self.send_command('height?')
        try:
            height = float(height)
        except Exception as e:
            print(e)
        return height

    def get_fly_time(self):
        time = self.send_command('time?')
        try:
            time = int(time)
        except Exception as e:
            print(e)
        return time

    def get_temp(self):
        temp = self.send_command('temp?')
        try:
            temp = float(temp)
        except Exception as e:
            print(e)
        return temp

    def get_attitude(self):
        attitude = self.send_command('attitude?')
        try:
            attitude = str(attitude)
        except Exception as e:
            print(e)
        return attitude

    def get_acceleration(self):
        acc = self.send_command('acceleration?')
        try:
            pass
            # acc = str(acc)
        except Exception as e:
            print(e)
        return acc

    def emergency_stop(self):
        """
        :return: Response from Tello, 'OK' or 'ERROR'.
        """
        return self.send_command('emergency')

    def receive_thread(self):
        while True:
            try:
                self.response = self.socket.recv(4096)
            except socket.error as e:
                print(e)

    def send_command(self, command):
        print("-> sent cmd: {}".format(command))
        last = self.response
        self.socket.sendto(command.encode(), self.address)
        while self.response is last:
            pass
        return self.response

    def send(self, command):
        print("-> sent cmd: {}".format(command))
        last = self.response
        self.socket.sendto(command, self.address)
        while self.response is last:
            pass
        return self.response
