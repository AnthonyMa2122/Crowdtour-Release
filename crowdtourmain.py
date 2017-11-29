#!/usr/bin/python3
#Crowdtour
import pymysql
import pyaudio
import wave
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
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
        self.audioCount = 0

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 250, 250)

        self.recordButton = QPushButton('Record', self)
        self.recordButton.clicked.connect(self.recordSound)

        self.deleteButton = QPushButton('Delete', self)
        self.deleteButton.clicked.connect(self.deleteSound)
        self.deleteButton.move(0, 50)

        self.playButton = QPushButton('Play/Stop', self)
        self.playButton.clicked.connect(self.playSound)
        self.playButton.move(0,100)

        self.uploadButton = QPushButton('Upload', self)
        self.uploadButton.clicked.connect(self.uploadSound)
        self.uploadButton.move(0, 150)


        self.show()

    def playSound(self):
        self.isPlaying = not self.isPlaying
        if self.isPlaying:
            self.sound.play()
            print('Play')
        else:
            self.sound.stop()
            print('Stop')

    def recordSound(self):
            print("Hello Anthony")
            #audioCount = 0
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            RECORD_SECONDS = 10
            self.WAVE_OUTPUT_FILENAME = "output" + str(self.audioCount) +".wav"
            self.audioCount+=1

            p = pyaudio.PyAudio()

            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            print("* recording")

            frames = []

            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            print("* done recording")

            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open(os.path.join('sounds',self.WAVE_OUTPUT_FILENAME), 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

    def deleteSound(self):
        print("File Delete")
        try:
            os.remove('sounds/' + self.WAVE_OUTPUT_FILENAME)
            if self.audioCount < 0:
                self.audioCount-=1
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    def uploadSound(self):

        self.sound = QSoundEffect()
        #This is where you set default sound source
        self.sound.setSource(QUrl.fromLocalFile(os.path.join('sounds', 'Slurps.wav')))
        self.sound.setLoopCount(QSoundEffect.Infinite)
        self.isPlaying = False
        #Convert .Wav into Binary
        self.w = wave.open(os.path.join('sounds', 'output0.wav'))
        #Parameters of the source file
        print(self.w.getparams())
        #Write the binary as a string...
        self.binary_data = self.w.readframes(self.w.getnframes())
        self.w.close()

        #Store binary into SQL
        cursorTest = connection.cursor()
        #TEST INSERT
        cursorTest.execute("INSERT INTO `MARKERS` (`id`, `name`, `address`, `lat`, `lng`, `type`,`sound`) VALUES (%s, %s, %s, %s, %s, %s, %s)" , ('9', 'Test Human', '999 Test Street, Rozelle, NSW', '-33.861034', '151.171936', 'restaurant',self.binary_data))
#       cursorTest.execute("INSERT INTO `MARKERS` (`name`) VALUES (%s)", ('10'))
#       cursorTest.execute("INSERT INTO `MARKERS` (`address`) VALUES (%s)", ('Insert Name Here'))
#       cursorTest.execute("INSERT INTO `MARKERS` (`lat`) VALUES (%s)", ('0'))
#       cursorTest.execute("INSERT INTO `MARKERS` (`lng`) VALUES (%s)", ('0'))
#       cursorTest.execute("INSERT INTO `MARKERS` (`type`) VALUES (%s)", ('Insert Type Here'))
#       cursorTest.execute("INSERT INTO `MARKERS` (`sound`) VALUES (%s)", ('Insert Sound Here'))

        #Read Binary from SQL
        cursors = connection.cursor(pymysql.cursors.DictCursor)
        cursors.execute("SELECT sound FROM MARKERS")
        result_set = cursors.fetchall()
        x = 0
        listSoundbytes = [None] * 1
        for row in result_set:
            listSoundbytes.insert(0,row["sound"])
            x+=1

        #Convert string to .wav file
        stringToByte = bytes(listSoundbytes[0])
        waveSave = wave.open(os.path.join('sounds','testFile.wav'), 'w')

        #Set parameters for writing
        waveSave.setparams((2, 2, 44100, 440320, 'NONE', 'not compressed'))
        waveSave.writeframes(stringToByte)
        connection.close()

        #Set sound source to soundbyte from SQL
        self.sound.setSource(QUrl.fromLocalFile(os.path.join('sounds', 'testFile.wav')))

        #The "All clear"
        print("Upload Successful")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())