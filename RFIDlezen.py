import RPi.GPIO as GPIO
import sys
sys.path.insert(0, '/home/pi/MFRC522-python')
import MFRC522
import signal
import time
import mysql.connector as mc

print("applicatie word geladen...")
from DbClass import DbClass
time.sleep(10)
print("applicatie geladen!")

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)

continue_reading = True
MIFAREReader = MFRC522.MFRC522()

while continue_reading:
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:

        part1 ='{:02x}'.format(uid[0])
        part2 ='{:02x}'.format(uid[1])
        part3 ='{:02x}'.format(uid[2])
        part4 ='{:02x}'.format(uid[3])

        RFIDrecoNumb = str(part1)+str(part2)+str(part3)+str(part4)
        print("Card read UID: "+ RFIDrecoNumb)

        connection = mc.connect(host="localhost", user="baukeremote", passwd="remote", db="dbUnLockIT")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM system_has_rfid as s, rfid as r WHERE s.rfid_IDRFID=r.IDRFID AND r.RFIDNo = '"+ RFIDrecoNumb +"' AND s.system_IDSystem = 1")
        result = cursor.fetchall()

        if not result:
            print('Access Denied')
        if result:
            print('Access Granted')
            stateRFID = GPIO.input(32)
            if stateRFID == 0 :
              GPIO.output(32, GPIO.HIGH)
            if stateRFID == 1 :
              GPIO.output(32, GPIO.LOW)

        time.sleep(.5)