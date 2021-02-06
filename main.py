import sys
import requests
import pythoncom, pyHook

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

        def OnKeyboardEvent(event):
            print('MessageName:', event.MessageName)
            print('Message:', event.Message)
            print('Time:', event.Time)
            print('Window:', event.Window)
            print('WindowName:', event.WindowName)
            print('Ascii:', event.Ascii, chr(event.Ascii))
            print('Key:', event.Key)
            print('KeyID:', event.KeyID)
            print('ScanCode:', event.ScanCode)
            print('Extended:', event.Extended)
            print('Injected:', event.Injected)
            print('Alt', event.Alt)
            print('Transition', event.Transition)
            print('---')

            return True

        hm = pyHook.HookManager()
        # watch for all mouse events
        hm.KeyDown = OnKeyboardEvent
        # set the hook
        hm.HookKeyboard()
        # wait forever
        pythoncom.PumpMessages()

    def find(self):
        self.requests_api()
        map_photo = QPixmap(self.map_pic)
        map_photo = map_photo.scaled(1051, 751)
        self.map_lable.setPixmap(map_photo)

    def chande_value(self):
        pass

    def requests_api(self):
        lat = self.edit_latitude.text()
        lon = self.edit_longitude.text()
        scale = self.edit_scale.value()
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