from googleplaces import GooglePlaces, types, lang
import sys
import urllib.request
from PyQt5 import QtNetwork, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from geolocation.main import GoogleMaps

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.last_clicked = ""
        self.button_list = []
        self.current_places = []
        self.image_label = QLabel(self)
        self.address_label = QLabel(self)
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 100
        self.top = 100
        self.width = 1200
        self.height = 600
        self.initUI()
        self.address = ""

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #initialize image label
        self.image_label.setStyleSheet('border: 10px solid white')
        self.image_label.move(900,200)
        self.image_label.resize(200, 200)
        self.image_label.show()

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

    def on_click(self):
        for place in self.current_places.places:
            if (place.name == self.sender().text()):
                place.get_details()
                if (place.photos):
                    place.photos[0].get(200,200)
                    url = place.photos[0].url
                    resource = urllib.request.urlopen(url).read()
                    pixmap = QPixmap()
                    pixmap.loadFromData(resource)
                    self.image_label.setPixmap(pixmap)



    def geolocation(self):
        self.button_list = []
        #self.current_places = ""
        google_maps = GoogleMaps(api_key='AIzaSyDlJqxwlOWWAPwf54ivrpAZw4R1Yb5j6Yk')

        location = google_maps.search(location=self.newaddress.text()) # sends search to Google Maps.
        my_location = location.first() # returns only first location.
        # BUSINESS FINDER

        API_KEY = 'AIzaSyBPGAbevdKkeXaZT0ZsR0qbO30Bpqqm0Mc'

        google_places = GooglePlaces(API_KEY)

        query_result = google_places.nearby_search(
            location=self.newaddress.text(),
            radius=700, types=[types.TYPE_RESTAURANT])
        self.current_places = query_result

        if query_result.has_attributions:
            print(query_result.html_attributions)

        self.buttonHeightCounter = 0
        for place in query_result.places:
            place.get_details()
            self.button_list.append(QPushButton(place.name, self))
            self.button_list[-1].setStyleSheet("background-color: grey")
            self.button_list[-1].move(650, self.buttonHeightCounter)
            self.button_list[-1].resize(225,23)
            self.button_list[-1].clicked.connect(self.on_click)
            self.button_list[-1].show()
            self.buttonHeightCounter += 24

            #print(place)
            print(place.formatted_address + "\n")

            # END BUSINESS FINDER
        mapUrl = 'http://maps.googleapis.com/maps/api/staticmap'
        mapUrl = mapUrl + '?size=800x400'
        mapUrl = mapUrl + '&center=' + str(my_location.lat) + ',' + str(my_location.lng)
        mapUrl = mapUrl + '&zoom=' + str(15)
        #&markers=color:blue%7Clabel:S%7C40.702147,-74.015794

        mapUrl = mapUrl + '&markers=color:blue'
        mapUrl = mapUrl + '%' + str(7) + 'Clabel:S%' + str(7) + 'C'
        mapUrl = mapUrl + str(my_location.lat) + ',' + str(my_location.lng)

        # mapUrl = mapUrl + '&markers=color:blue'
        # mapUrl = mapUrl + '%' + str(7) + 'Clabel:S%' + str(7) + 'C'
        # mapUrl = mapUrl + str(my_location.lat + 0.0003000) + ',' + str(my_location.lng + 0.0003000)

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

