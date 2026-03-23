import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import requests
import sys

class WeatherApplication(QWidget):
    def __init__(self):
        super().__init__()

        #Main Elements
        self.select_city_button = QPushButton("Show Weather", self)
        self.select_city_button.setObjectName("CityButton")

        self.city_search = QLineEdit(self)
        self.city_search.setObjectName("CitySearch")

        self.city_label = QLabel("Enter City Name:", self)
        self.city_label.setObjectName("CityLabel")

        self.temperature_label = QLabel(self)
        self.temperature_label.setObjectName("TempatureLabel")

        self.weather_description = QLabel(self)
        self.weather_description.setObjectName("WeatherDescription")

        self.emoji_label = QLabel(self)
        self.emoji_label.setObjectName("EmojiLabel")

        self.UI_SETUP()

    def UI_SETUP(self):
        #Window Setup
        self.setWindowTitle("Weather API (Python + PyQt5)")
        self.setFixedSize(600, 400)

        #Layout
        vBox = QVBoxLayout()
        vBox.addWidget(self.city_label)
        vBox.addWidget(self.city_search)
        vBox.addWidget(self.select_city_button)
        vBox.addWidget(self.temperature_label)
        vBox.addWidget(self.emoji_label)
        vBox.addWidget(self.weather_description)

        self.setLayout(vBox)

        #Element Designs
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_search.setAlignment(Qt.AlignCenter)
        self.city_search.setPlaceholderText("Enter City")
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.weather_description.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""    
                    QWidget {
                            background-color: hsl(161, 13%, 44%);
                            }
                           
                    QLabel#CityLabel{
                           font-size: 25px;
                           font-family: calibri;
                           font-style: italic;
                           color: white;
                                    }
                           
                    QLabel#TempatureLabel{
                           font-size: 25px;
                           font-family: calibri;
                           color: white;
                                         }
                           
                    QLabel#EmojiLabel{
                           font-size: 50px;
                           font-family: Segoe UI Emoji;
                           padding: 10 10px;
                           color: white;
                                     }
                           
                    QLabel#WeatherDescription{
                            font-size: 25px;
                            font-family: calibri;
                            color: white;
                                             }
                           
                    QLineEdit#CitySearch{
                           padding: 10px 15px;
                           font-size: 25px;
                           font-family: calibri;
                           border-radius: 15px;
                           border: 1px solid;
                           font-style: italic;
                           color: white;
                             }
                           
                           
                    QPushButton#CityButton{
                           padding: 10px 15px;
                           font-family: calibri;
                           font-size: 20px;
                           font-weight: bold;
                           color: white;
                           background: hsl(161, 13%, 37%);
                           border-radius: 10px;
                                          }      

                    QPushButton#CityButton:Hover{
                           background: hsl(161, 13%, 30%);
                                          }            
                                            

""")
        self.temperature_label.setText("Loading...")

        #Click button to recieve weather
        self.select_city_button.clicked.connect(self.receive_weather)

        #Press enter to get information
        self.city_search.returnPressed.connect(self.receive_weather)
        
    def receive_weather(self):
        print(f"Trying to get weather for {self.city_search.text()}...")

        API_KEY = os.getenv("WEATHER_API_KEY")

        if not API_KEY:
            self.show_error("API Key not found.")
            return
        

        city = self.city_search.text()

        if not city:
            self.show_error("Please enter a city.")
            return

        URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

        try:
            response = requests.get(URL, timeout=5)
            response.raise_for_status()
            weather_data = response.json()

            if weather_data["cod"] == 200:
                self.display_weather(weather_data)

        except requests.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.show_error("Bad Request \n Please check your input.")
                case 401:
                    self.show_error("Unauthorized \n Invalid API Key.")
                case 402:
                    self.show_error("Access is denied.")
                case 403:
                    self.show_error("Access forbidden.")
                case 404:
                    self.show_error("City not found.")
                case 500:
                    self.show_error("Bad gateway.")
                case 503:
                    self.show_error("Server unavailable.")
                case 504:
                    self.show_error("No response from server.")
                case _:
                    self.show_error(f"Request Error: {http_error}")

        except requests.exceptions.ConnectionError:
            self.show_error("Connection error.")

        except requests.exceptions.Timeout:
            self.show_error("The request timed out.")

        except requests.exceptions.TooManyRedirects:
            self.show_error("Too many redirects.")

        except requests.RequestException as req_error:
            self.show_error(f"Request error: {req_error}")

    def show_error(self, error_msg):
        self.temperature_label.setText(error_msg)
        self.emoji_label.clear()
        self.weather_description.clear()
        

    def display_weather(self, weather_data):
        kelvinTemp = weather_data["main"]["temp"]
        tempature = kelvinTemp - 273.15
        description = weather_data['weather'][0]['description']
        description = description.capitalize()
        weather_id = weather_data['weather'][0]["id"]
        emoji = self.get_emoji(weather_id)
        
        self.temperature_label.setText(f"{tempature:.0f}°C")
        self.weather_description.setText(f"{description}")
        self.emoji_label.setText(emoji)

    @staticmethod
    def get_emoji(weather_id):
        if 200 <= weather_id <= 232: #Thunderstorm
            return "⛈️"
        elif 300 <= weather_id <= 321: #Light Rain
            return "🌦️"
        elif 500 <= weather_id <= 531: #Rain
            return "🌧️"
        elif 600 <= weather_id <= 622: #Snowing
            return "🌨️"
        elif 701 <= weather_id <= 741: #Fog
            return "🌫️"
        elif weather_id == 762: #Valcano Ash
            return "🌋"
        elif weather_id == 771: #Heavy Wind
            return "💨"
        elif weather_id == 781: #Tornado
            return "🌪️"
        elif weather_id == 800: #Sunny
            return "☀️"
        elif  801 <= weather_id <= 804: #Cloudy
            return "☁️"
        else:
            return ""


def application_setup():
    application = QApplication(sys.argv)
    weather_app = WeatherApplication()
    weather_app.show()

    #Execute Function.
    sys.exit(application.exec_())

#Run if main file.
if __name__ == "__main__":
    application_setup()
