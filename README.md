# Weather App (Python + PyQt5)

A modern desktop weather application built with Python and PyQt5 that fetches real-time weather data using the OpenWeatherMap API.

---

## Features

- 🌍 Search weather by city
- Displays temperature in Celsius
- 🌤 Shows weather condition (e.g. Clear, Cloudy, Rain)
- Dynamic weather emojis
- ⚠️ Error handling (invalid city, API issues, connection errors)
- Clean and modern UI

---

## Tech Stack

- Python 3
- PyQt5 (GUI)
- Requests (API calls)
- OpenWeatherMap API

---

## Screenshot

<img width="594" height="427" alt="image" src="https://github.com/user-attachments/assets/4583b777-a5a8-4b50-becc-bc4aff64eff3" />

---

## Installation

1. Clone the repository:
   
```powershell
git clone https://github.com/Michael-Georgi/weather-app-python.git
cd weather-app-python
```

2. Install dependencies:

```powershell
pip install PyQt5
pip install requests
```

## API Setup

This app uses the OpenWeatherMap API.

1. Go to: https://openweathermap.org
2. Create an account and get your API key
3. Set your API key as an environment variable

Windows(Powershell):

```powershell
setx WEATHER_API_KEY "your_api_key_here"
```

Mac/Linux:

```bash
export WEATHER_API_KEY="your_api_key_here"
```

## Future Improvements

- 5-day weather forecast
- Save last searched city
- Convert to web app (JavaScript frontend)
- Add animations / transitions
