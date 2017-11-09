import sys
import urllib.request
from PyQt5 import QtNetwork, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from geolocation.main import GoogleMaps
import gmplot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        self.label = QLabel(self)
        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)

        address = "6171 Mission st, San Francisco"

        google_maps = GoogleMaps(api_key='AIzaSyDlJqxwlOWWAPwf54ivrpAZw4R1Yb5j6Yk')

        location = google_maps.search(location=address) # sends search to Google Maps.

        my_location = location.first() # returns only first location.

        # get zoom level
        #z = sys.argv[1]
        mapUrl = 'http://maps.googleapis.com/maps/api/staticmap'
        mapUrl = mapUrl + '?size=400x400'
        #mapUrl = mapUrl + '&center=37.721,-122.4765'
        mapUrl = mapUrl + '&center=' + str(my_location.lat) + ',' + str(my_location.lng)
        #mapUrl = mapUrl + '&center=1600+Holloway+Ave,San+Francisco,CA'
        mapUrl = mapUrl + '&zoom=' + str(15)
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(mapUrl))

        #self.gmap = gmplot.GoogleMapPlotter(my_location.lat, my_location.lng)

        #self.gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
        #self.gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
        #self.gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
        #self.gmap.heatmap(heat_lats, heat_lngs)

        #self.gmap.draw("mymap.html")

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
