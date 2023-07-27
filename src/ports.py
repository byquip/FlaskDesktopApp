import serial
import sys
import glob
import time

start_time = 0


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result[::-1]


def connect(port):
    global start_time
    start_time = time.time()
    ser = serial.Serial(port, 9600, timeout=1)
    ser.flush()
    return ser


def disconnect(ser):
    ser.close()
    return "disconnected"


def read(ser):
    if ser is None:
        return "No device connected"
    if ser.in_waiting > 20:
        # line = (ser.read_until().decode('utf-8').rstrip().split()[0])
        line = ser.read(ser.in_waiting).decode('utf-8').split("\r\n")[-2].split()[0]
        try:
            float(line)
        except:
            return "No device connected"
        finally:
            print(line)
            return {"x": (time.time()-start_time), "y": (float(line))}
