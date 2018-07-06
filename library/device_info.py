import sys
import serial


def getinfo(serial_port):
    """
        Scan beacon and read info
        :param serial_port: the serial port which the dongle connected
    """
    try:
        """
            Check if dongle connected to serial port 
        """
        ser = serial.Serial()  # initialize the serial
        ser.baudrate = 115200  # set the baud rate to 115200 because the Firmware of the dongle use this value
        ser.port = sys.argv[1]  # set the port to use
        ser.timeout = 10

        ser.open()  # Open port
        ser.write(b'info\r\n')  # send the UART command (info)

        # Ctrl - C causes KeyboardInterrupt to be raised, so we catch it outside the loop and ignore it
        try:
            # infinite loop to keep read bytes from the serial port
            while 1:
                readline_array = ser.readline().rstrip().decode('utf-8')
                print(readline_array)
        except KeyboardInterrupt:
            ser.close()  # Close port
            pass
    except serial.serialutil.SerialException:
        print("No dongle connected to " + serial_port)


if len(sys.argv) != 2:
    print("Enter the serial port to use please")
    sys.exit()
else:
    getinfo(sys.argv[1])
