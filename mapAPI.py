import sys
import urllib.request
from PyQt5 import QtNetwork, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from geolocation.main import GoogleMaps

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 600
        self.initUI()
        self.address = ""

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        self.label = QLabel(self)
        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)

        #textbox
        self.newaddress = QLineEdit(self)
        self.newaddress.move(20,440)
        self.newaddress.resize(200,40)

        #location button
        self.button = QPushButton('location', self)
        self.button.setStyleSheet("background-color: grey")
        self.button.move(20,500)

        self.button.clicked.connect(self.geolocation)

        self.address = "6171 Mission st, San Francisco"

        google_maps = GoogleMaps(api_key='AIzaSyDlJqxwlOWWAPwf54ivrpAZw4R1Yb5j6Yk')

        location = google_maps.search(location=self.address) # sends search to Google Maps.

        my_location = location.first() # returns only first location.

        # get zoom level
        #z = sys.argv[1]
        mapUrl = 'http://maps.googleapis.com/maps/api/staticmap'
        mapUrl = mapUrl + '?size=800x400'
        #mapUrl = mapUrl + '&center=37.721,-122.4765'
        mapUrl = mapUrl + '&center=' + str(my_location.lat) + ',' + str(my_location.lng)
        #mapUrl = mapUrl + '&center=1600+Holloway+Ave,San+Francisco,CA'
        mapUrl = mapUrl + '&zoom=' + str(15)
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(mapUrl))


        self.nam.get(req)

        self.pixmap = QPixmap()
        self.show()

    def handleResponse(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:
            url_data = reply.readAll()
            self.pixmap.loadFromData(url_data)
            self.label.setPixmap(self.pixmap)
            self.label.resize(self.pixmap.width(), self.pixmap.height())
            self.label.show()

    def geolocation(self):

        google_maps = GoogleMaps(api_key='AIzaSyDlJqxwlOWWAPwf54ivrpAZw4R1Yb5j6Yk')

        location = google_maps.search(location=self.newaddress.text()) # sends search to Google Maps.

        my_location = location.first() # returns only first location.

        mapUrl = 'http://maps.googleapis.com/maps/api/staticmap'
        mapUrl = mapUrl + '?size=800x400'
        mapUrl = mapUrl + '&center=' + str(my_location.lat) + ',' + str(my_location.lng)
        mapUrl = mapUrl + '&zoom=' + str(15)
        #&markers=color:blue%7Clabel:S%7C40.702147,-74.015794
        mapUrl = mapUrl + '&markers=color:blue'
        mapUrl = mapUrl + '%' + str(7) + 'Clabel:S%' + str(7) + 'C'
        mapUrl = mapUrl + str(my_location.lat) + ',' + str(my_location.lng)
        mapUrl = mapUrl + '&sensor=true'
        #mapUrl = mapUrl + '&markers=color:blue|label:S|' + str(my_location.lat) + ',' + str(my_location.lng)
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(mapUrl))

        self.nam.get(req)

        self.pixmap = QPixmap()
        self.show()

        print('lat is ' + str(my_location.lat))
        print('lng is ' + str(my_location.lng))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
