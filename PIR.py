from gpiozero import MotionSensor
import mysql.connector as mc
pir = MotionSensor(24)

while True:
    pir.wait_for_motion()
    print("You moved")
    connection = mc.connect(host="localhost", user="baukeremote", passwd="remote", db="dbUnLockIT")
    cursor = connection.cursor()
    q1 = "INSERT INTO motion(Date, Time, system_IDSystem) VALUES(curdate(), CURTIME(), 1)"
    cursor.execute(q1)
    connection.commit()
    pir.wait_for_no_motion()