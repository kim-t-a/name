import sys
import requests
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
class weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel('Enter city name',self)
        self.city=QLineEdit(self)
        self.get_weather=QPushButton('Get Weather',self)
        self.temperature_label=QLabel(self)
        self.emoji = QLabel( self)
        self.description = QLabel( self)
        self.initUI()
    def initUI(self):
        self.setWindowTitle('WEATHERAPP')
        self.setGeometry(300, 300, 850, 550)
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.get_weather)
        vbox.addWidget(self.city)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji)
        vbox.addWidget(self.description)
        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName('city_label')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji.setObjectName('emoji')
        self.description.setObjectName('description')
        self.city.setObjectName('city')
        self.get_weather.setObjectName('get_weather')

        self.setStyleSheet(""" QLabel#city_label{font-size: 40px; font-family:Arial;font-weight:bold;}QPushButton{font-size:50px;font-family:Arial;font-weight:bold;} QLineEdit{font-size:40px;font-family:Arial;font-weight:bold;}QLabel#temperature_label{font-size:75px;f}QLabel#emoji{font-size:90px;font-weight:bold;font-family: Segoe UI emoji;}QLabel#description{font-size:50px;font-weight:bold;} } """)
        self.get_weather.clicked.connect(self.get_weathers)
    def get_weathers(self):
        api_key = '028ea307f3545a88a2a7a8c9b345846c'
        city=self.city.text()
        url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response=requests.get(url)
        try:
            response.raise_for_status()
            data=response.json()
            if data['cod']==200:
                self.display_weather(data)
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error('Bad Request\n please check your input')
                case 401:
                    self.display_error('Unauthorised\ninvlaid API key')
                case 403:
                    self.display_error('Forbidden\nAccess Denied')
                case 404:
                    self.display_error('Not found\nCity not found')
                case 500:
                    self.display_error('Internal server Error\nTry again later')
                case 502:
                    self.display_error('Bad Gateway\nInvalid response from the server')
                case 503:
                    self.display_error('Service Unavailable\nServer is Down')
                case 504:
                    self.display_error('Gateway Timeout\nServer timed out')
                case _:
                    self.display_error('HTTP ERROR OCCURRED')

        except requests.exceptions.RequestException:
            self.display_error('Connection Error\nCheck yout internet connection ')
        except requests.exceptions.Timeout:
            self.display_error('Timeout Error\nRequest timed out ')

        except requests.exceptions.TooManyRedirects:
            self.display_error('Too many Redirects\nCheck the URL')
        except requests.exceptions.RequestException as req_error:
            self.display_error(f'Request Error\n{req_error}')
        #print(data)


    def display_error(self,message):
        self.temperature_label.setText(message)
        self.emoji.clear()
    def display_weather(self,data):
        self.temperature_label.setStyleSheet('font-size:80px;')
        temperature=data['main']['temp']-273.15
        weather_id=data['weather'][0]['id']
        self.temperature_label.setText(f'{temperature:.0f}°c')
        weather_description = data['weather'][0]['description']
        self.emoji.setText(self.weather_emoji(weather_id))
        self.description.setText(weather_description)
    @staticmethod
    def weather_emoji(weather_id):
        if 200<=weather_id<=232:
             return '⛈️'
        elif 300<=weather_id<=321:
             return '☁️'
        elif 500<=weather_id<=531:
            return '🌧️'
        elif 600<=weather_id<=622:
            return '🌨️'
        elif 701<=weather_id<=741:
            return '🌫️'
        elif weather_id==762:
            return '🌋'
        elif weather_id==771:
            return '💨 '
        elif weather_id==800:
            return '☀️'
        elif weather_id==781:
            return '🌪️'
        elif 801<=weather_id<=804:
            return '☁️'
        else:
            return ''


def main():
    app = QApplication(sys.argv)
    main = weatherapp()
    main.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()