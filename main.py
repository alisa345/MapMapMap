import sys
import requests

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_map.ui', self)
        self.button_find.clicked.connect(self.find)
        self.edit_longitude.setText('60.58985462732907')
        self.edit_latitude.setText('56.84822763650701')
        self.edit_scale.setText('0.01')

    def find(self):
        self.requests_api()
        map_photo = QPixmap(self.map_pic)
        map_photo = map_photo.scaled(1051, 751)
        self.map_lable.setPixmap(map_photo)

    def requests_api(self):
        lat = self.edit_latitude.text()
        lon = self.edit_longitude.text()
        scale = self.edit_scale.text()
        api_server = "http://static-maps.yandex.ru/1.x/"

        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "ll": ",".join([lon, lat]),
            "spn": ",".join([scale, scale]),
            "l": "map"
        }

        response = requests.get(api_server, params=params)
        self.map_pic = 'map.png'

        with open(self.map_pic, 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())