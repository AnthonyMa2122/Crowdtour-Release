#!/usr/bin/python3
#Crowdtour
import pymysql
import wave
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QSoundEffect


# Open database connection
connection = pymysql.connect(host='localhost',user='testhost',password='test',db='crowdtour')

# prepare a cursor object using cursor() method
cursor = connection.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS MARKERS")

# Create table as per requirement
sql = """CREATE TABLE MARKERS (
   id  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(60) NOT NULL,
   address VARCHAR(80) NOT NULL,  
   lat FLOAT (10,6) NOT NULL,
   lng FLOAT (10,6) NOT NULL,
   type VARCHAR(30) NOT NULL,
   annotation VARCHAR(160),
   sound LONGBLOB
   ) ENGINE = MYISAM"""

cursor.execute(sql)

sqlInsert = """
INSERT INTO `MARKERS` (`id`, `name`, `address`, `lat`, `lng`, `type`) VALUES ('1', 'Love.Fish', '580 Darling Street, Rozelle, NSW', '-33.861034', '151.171936', 'restaurant');
INSERT INTO `MARKERS` (`id`, `name`, `address`, `lat`, `lng`, `type`) VALUES ('2', 'Young Henrys', '76 Wilford Street, Newtown, NSW', '-33.898113', '151.174469', 'bar');
INSERT INTO `MARKERS` (`id`, `name`, `address`, `lat`, `lng`, `type`) VALUES ('3', 'Hunter Gatherer', 'Greenwood Plaza, 36 Blue St, North Sydney NSW', '-33.840282', '151.207474', 'bar');
INSERT INTO `MARKERS` (`id`, `name`, `address`, `lat`, `lng`, `type`) VALUES ('4', 'The Potting Shed', '7A, 2 Huntley Street, Alexandria, NSW', '-33.910751', '151.194168', 'bar');
INSERT INTO `MARKERS` (`id`, `name`, `address`, `lat`, `lng`, `type`) VALUES ('5', 'Nomad', '16 Foster Street, Surry Hills, NSW', '-33.879917', '151.210449', 'bar');
INSERT INTO `MARKERS` (`id`, `name`, `address`, `lat`, `lng`, `type`) VALUES ('6', 'Three Blue Ducks', '43 Macpherson Street, Bronte, NSW', '-33.906357', '151.263763', 'restaurant');
INSERT INTO `MARKERS` (`id`, `name`, `address`, `lat`, `lng`, `type`) VALUES ('7', 'Single Origin Roasters', '60-64 Reservoir Street, Surry Hills, NSW', '-33.881123', '151.209656', 'restaurant');
INSERT INTO `MARKERS` (`id`, `name`, `address`, `lat`, `lng`, `type`) VALUES ('8', 'Red Lantern', '60 Riley Street, Darlinghurst, NSW', '-33.874737', '151.215530', 'restaurant');
"""

cursor.execute(sqlInsert)

#Create a cursor and print the results from the row 'name'
cursors = connection.cursor(pymysql.cursors.DictCursor)
cursors.execute("SELECT name FROM MARKERS")
result_set = cursors.fetchall()
for row in result_set:
    print(row["name"])

#disconnect from server
#connection.close()

#Test GUI
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 play QSoundEffect demo'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.setGeometry(100, 100, 250, 250)
        self.show()
        self.sound = QSoundEffect()
        #THIS IS WHERE YOU SET THE SOUND FILE SOURCE
        self.sound.setSource(QUrl.fromLocalFile(os.path.join('sounds', 'Slurps.wav')))
        self.sound.setLoopCount(QSoundEffect.Infinite)
        self.isPlaying = False
        #CONVERT WAV TO BINARY
        self.w = wave.open(os.path.join('sounds', 'Beep.wav'))
        #Parameters of the source file
        print(self.w.getparams())
        #Write the binary as a string...
        self.binary_data = self.w.readframes(self.w.getnframes())
        #print(self.binary_data)
        self.w.close()

        #STORE BINARY INTO SQL
        connectionTest = pymysql.connect(host='localhost', user='testhost', password='test', db='crowdtour')
        cursorTest = connectionTest.cursor()
        cursorTest.execute("INSERT INTO `MARKERS` (`id`, `name`, `address`, `lat`, `lng`, `type`,`sound`) VALUES (%s, %s, %s, %s, %s, %s, %s)" , ('9', 'Test Human', '999 Test Street, Rozelle, NSW', '-33.861034', '151.171936', 'restaurant',self.binary_data))

        #READ FROM SQL
        cursors = connection.cursor(pymysql.cursors.DictCursor)
        cursors.execute("SELECT sound FROM MARKERS")
        result_set = cursors.fetchall()
        x = 0
        listSoundbytes = [None] * 1
        for row in result_set:
            listSoundbytes.insert(0,row["sound"])
            x+=1
        #Convert string to wav file
        stringToByte = bytes(listSoundbytes[0])
        waveSave = wave.open(os.path.join('sounds','testFile.wav'), 'w')
        #Set parameters for writing
        waveSave.setparams((2, 2, 44100, 440965, 'NONE', 'not compressed'))
        waveSave.writeframes(stringToByte)
        #TODO: save wave file
        #TODO: Play wave file
        connectionTest.close()
        self.sound.setSource(QUrl.fromLocalFile(os.path.join('sounds', 'testFile.wav')))
        #The "All clear"
        print("Mucho Bueno, hit Spacebar")

    def keyPressEvent(self, event):
        if (event.key() == 32):
            self.isPlaying = not self.isPlaying
            if self.isPlaying:
                self.sound.play()
                print('Play')
            else:
                self.sound.stop()
                print('Stop')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())