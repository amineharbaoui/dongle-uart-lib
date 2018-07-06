import re
import sys
import uuid
import serial


def startscan(serial_port):
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
        ser.write(b'scan=01\r\n')  # send the UART command (Start scan : scan=01 , Stop scan : scan=00)

        # Ctrl - C causes KeyboardInterrupt to be raised, so we catch it outside the loop and ignore it
        try:
            # infinite loop to keep read bytes from the serial port
            while 1:
                """ 
                    1. read line of bytes
                    2. remove the (\r\n) from the end of each line
                    3. encode bytes to utf-8
                    4. split each part in and array 
                        
                """
                readline_array = ser.readline().rstrip().decode('utf-8').split(",")

                if len(readline_array) == 6:  # check if the returned line does not missing a part
                    if int(readline_array[4]) == 30:  # check if Data length equals to the length of IBeacon packet (30)

                        scanner_mac = readline_array[0].translate({ord(i): None for i in '@scan:'})
                        advertiser_mac = readline_array[1]
                        rssi = readline_array[2]
                        adv_type = readline_array[3]
                        adv_data_length = readline_array[4]
                        adv_data = readline_array[5]

                        payload = re.findall("^(.{10})(.{4})(.{4})(.{32})(.{4})(.{4})(.{2})", adv_data)[0]


                        flag_info = payload[0]
                        company_id = payload[1]
                        adv_indicator = payload[2]
                        proximity_uuid = str(uuid.UUID(payload[3]))
                        major = int(payload[4], 16)
                        minor = int(payload[5], 16)
                        signal_power = int(payload[6], 16)

                        print("**************************************************************************************")
                        print(
                            " scanner_mac: " + scanner_mac + "\n advertiser_mac: " + advertiser_mac + "\n rssi: " + rssi + "\n adv_type: " + adv_type + "\n adv_data_length: " + adv_data_length)
                        print(
                            " company_id: " + company_id + "\n adv_indicator: " + adv_indicator + "\n proximity_uuid: " + proximity_uuid + "\n major: {}".format(
                                major) + "\n minor: {}".format(minor) + "\n signal_power: {}".format(signal_power))



        except KeyboardInterrupt:
            pass
    except serial.serialutil.SerialException:
        print("No dongle connected to " + serial_port)


if len(sys.argv) != 2:
    print("Enter the serial port to use please")
    sys.exit()
else:
    startscan(sys.argv[1])
