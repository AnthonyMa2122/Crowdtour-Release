from tkinter import Tk, Canvas, Label, Frame, IntVar, Radiobutton, Button, Entry
from PIL import ImageTk
from PyQt5.QtWidgets import *

from goompy import GooMPy
from geolocation.main import GoogleMaps

### integrated with database ###
import pymysql
import pyaudio
import wave
import sys
import os
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QSoundEffect
### integrated with database ###


WIDTH = 800
HEIGHT = 420

LATITUDE  =  37.7280313   #52.4994
LONGITUDE =  -122.477088  #13.3544
ZOOM = 15
MAPTYPE = 'roadmap'

####### database parts top #######
# Open database connection
connection = pymysql.connect(host='localhost',user='root',password='',db='crowdtour')

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
####### database parts bottom #######

class UI(Tk):

    def __init__(self):

        Tk.__init__(self)

        self.geometry('%dx%d+500+500' % (800,600))
        self.title('SimpleApp')
        self.audioCount = 0

        app = QApplication(sys.argv)

        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)

        self.canvas.pack()

        self.bind("<Key>", self.check_quit)
        self.bind('<B1-Motion>', self.drag)
        self.bind('<Button-1>', self.click)

        self.label = Label(self.canvas)

        self.radiogroup = Frame(self.canvas)
        self.radiovar = IntVar()
        self.maptypes = ['roadmap', 'terrain', 'satellite', 'hybrid']
        self.add_radio_button('Road Map',  0)
        self.add_radio_button('Terrain',   1)
        self.add_radio_button('Satellite', 2)
        self.add_radio_button('Hybrid',    3)
        #move entry
        #frame=Frame(self,width=100,heigh=500,bd=11)

        #input
        self.entry = Entry(self, bd=3)
        self.button = Button(self, text="Location", command=self.on_button)
        #self.button.pack(side = "top")
        self.button.place(relx=.28, rely=.90, anchor="c")
        #self.entry.pack(side = "left")
        self.entry.place(relx=.10, rely=.80)
        #self.entry.focus()

        #buttons
        self.recordButton = Button(self,text="Record", command=self.record)
        #self.recordButton.pack(side = "top")
        self.recordButton.place(relx=.48, rely=.75, anchor="c")

        self.uploadButton = Button(self,text="Upload", command=self.upload)
        #self.uploadButton.pack(side = "top")
        self.uploadButton.place(relx=.48, rely=.80, anchor="c")

        self.playButton = Button(self,text="Play/Stop", command=self.play)
        #self.playButton.pack(side = "top")
        self.playButton.place(relx=.48, rely=.85, anchor="c")

        self.deleteButton = Button(self,text="Delete", command=self.delete)
        #self.deleteButton.pack(side = "top")
        self.deleteButton.place(relx=.48, rely=.90, anchor="c")

        ### adding part here ###

        self.sound = QSoundEffect()
        # This is where you set default sound source
        if not os.path.exists('sounds'):
            os.makedirs('sounds')

        defaultBytes = b'27\xe5\xb2\x81\xe5'
        waveTest = wave.open(os.path.join('sounds', 'DefaultSound.wav'), 'w')
        waveTest.setparams((2, 2, 44100, 440320, 'NONE', 'not compressed'))
        waveTest.writeframes(defaultBytes)

        self.sound.setSource(QUrl.fromLocalFile(os.path.join('sounds', 'DefaultSound.wav')))
        self.sound.setLoopCount(QSoundEffect.Infinite)
        self.isPlaying = False


        ### adding part here ###

        self.zoom_in_button  = self.add_zoom_button('+', +1)
        self.zoom_out_button = self.add_zoom_button('-', -1)

        self.zoomlevel = ZOOM

        maptype_index = 0
        self.radiovar.set(maptype_index)
        MARKER = "markers=size:tiny|label:B|color:red|" + str(LATITUDE) + "," + str(LONGITUDE)
        self.goompy = GooMPy(WIDTH, HEIGHT, LATITUDE, LONGITUDE, ZOOM, MAPTYPE, MARKER)

        self.restart()

    def add_zoom_button(self, text, sign):

        button = Button(self.canvas, text=text, width=1, command=lambda:self.zoom(sign))
        return button

    def reload(self):

        self.coords = None
        self.redraw()

        self['cursor']  = ''


    def restart(self):

        # A little trick to get a watch cursor along with loading
        self['cursor']  = 'watch'
        self.after(1, self.reload)

    def add_radio_button(self, text, index):

        maptype = self.maptypes[index]
        Radiobutton(self.radiogroup, text=maptype, variable=self.radiovar, value=index,
                command=lambda:self.usemap(maptype)).grid(row=0, column=index)

            #if maptype == 'Search':


    def click(self, event):

        self.coords = event.x, event.y

    def drag(self, event):

        self.goompy.move(self.coords[0]-event.x, self.coords[1]-event.y)
        self.image = self.goompy.getImage()
        self.redraw()
        self.coords = event.x, event.y

    def redraw(self):

        self.image = self.goompy.getImage()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.label['image'] = self.image_tk

        self.label.place(x=0, y=0, width=WIDTH, height=HEIGHT)

        self.radiogroup.place(x=0,y=0)

        x = int(self.canvas['width']) - 50
        y = int(self.canvas['height']) - 80

        self.zoom_in_button.place(x= x, y=y)
        self.zoom_out_button.place(x= x, y=y+30)

    def usemap(self, maptype):

        self.goompy.useMaptype(maptype)
        self.restart()

    def zoom(self, sign):

        newlevel = self.zoomlevel + sign
        if newlevel > 0 and newlevel < 22:
            self.zoomlevel = newlevel
            self.goompy.useZoom(newlevel)
            self.restart()

    def check_quit(self, event):

        if ord(event.char) == 27: # ESC
            exit(0)

    #input
    def on_button(self):

        google_maps = GoogleMaps(api_key='AIzaSyDlJqxwlOWWAPwf54ivrpAZw4R1Yb5j6Yk')

        location = google_maps.search(location=self.entry.get()) # sends search to Google Maps.

        my_location = location.first() # returns only first location.

        #MARKER = '&markers=color:blue' + '%' + str(7) + 'Clabel:S%' + str(7) + 'C' + str(my_location.lat) + ',' + str(my_location.lng)

        MARKER = "&markers=size:big|label:S|color:red|" + str(my_location.lat) + "," + str(my_location.lng)

        self.zoomlevel = ZOOM

        maptype_index = 0
        self.radiovar.set(maptype_index)

        self.goompy = GooMPy(WIDTH, HEIGHT, my_location.lat, my_location.lng, ZOOM, MAPTYPE, MARKER)

        self.restart()

        print(str(my_location.lat))
        print(str(my_location.lng))

    def record(self):
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

        print("recording...")

        #label = Label(self, text= "recording start for 10 seconds")
        #this creates a new label to the GUI
        #label.place(relx=.70, rely=.75)

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("...done recording")

        label = Label(self, text= "recording is 10 seconds...done recording")
        #this creates a new label to the GUI
        label.place(relx=.60, rely=.80)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(os.path.join('sounds',self.WAVE_OUTPUT_FILENAME), 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        #label = Label(self, text= "recording start for 10 seconds")
        #this creates a new label to the GUI
        #label.place(relx=.70, rely=.75)
        #print("recorded")

    def upload(self):
        #Convert .Wav into Binary
        self.w = wave.open(os.path.join('sounds', 'output0.wav'))

        #Parameters of the source file (keep this)
        #print(self.w.getparams())

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

        #print("uploaded")

    def play(self):
        self.isPlaying = not self.isPlaying
        if self.isPlaying:
            self.sound.play()
            print('Play')
        else:
            self.sound.stop()
            print('Stop')
        #print("play/stop")

    def delete(self):
        print("File Deleted from local device")
        try:
            os.remove('sounds/' + self.WAVE_OUTPUT_FILENAME)
            if self.audioCount < 0:
                self.audioCount-=1
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        #print("deleted")


UI().mainloop()
