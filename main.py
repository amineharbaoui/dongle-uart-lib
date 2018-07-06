import re
import sys
import uuid

import serial

if len(sys.argv) != 2:
    print("Enter the serial port to use please")
else:

    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = sys.argv[1]

    ser.open()

    ser.write(b'scan=01\r\n')  # get info command
    try:
        while 1:
            data_array = ser.readline().rstrip().decode('utf-8').split(",")

            if len(data_array) == 6:
                if int(data_array[4]) == 30:
                    scannerMac = data_array[0].translate({ord(i): None for i in '@scan:'})
                    advertiserMac = data_array[1]
                    rssi = data_array[2]
                    advType = data_array[3]
                    advDataLength = data_array[4]
                    advData = data_array[5]

                    cutData = re.findall("^(.{10})(.{4})(.{4})(.{32})(.{4})(.{4})(.{2})", advData)[0]

                    # print(cutData)

                    flagInfo = cutData[0]
                    companyId = cutData[1]
                    advIndicator = cutData[2]
                    proximityUUID = str(uuid.UUID(cutData[3]))
                    major = int(cutData[4], 16)
                    minor = int(cutData[5], 16)
                    signalPower = int(cutData[6], 16)

                    print(
                        "************************************************************************************************")
                    print(
                        " scannerMac: " + scannerMac + "\n advertiserMac: " + advertiserMac + "\n rssi: " + rssi + "\n advType: " + advType + "\n advDataLength: " + advDataLength)
                    print(
                        " companyId: " + companyId + "\n advIndicator: " + advIndicator + "\n proximityUUID: " + proximityUUID + "\n major: {}".format(
                            major) + "\n minor: {}".format(minor) + "\n signalPower: {}".format(signalPower))
    except KeyboardInterrupt:
        pass
