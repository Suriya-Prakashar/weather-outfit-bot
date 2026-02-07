## Smart Weather & Outfit Assistant
A Python-based CLI tool that fetches real-time weather data and uses context-aware logic to suggest the perfect outfit. Unlike standard weather apps, this tool analyzes humidity, wind speed, and "feels like" temperatures to provide safety and comfort advice specifically tuned for tropical climates.

## Features
Real-Time Data: Fetches live weather metrics (Temp, Humidity, Wind, Conditions) via the OpenWeatherMap API.
Smart "Real Feel" Analysis: Detects when high humidity makes the temperature feel hotter than the thermometer reads.
Tropical Context Logic: Adjusted temperature thresholds (e.g., 26°C is "Pleasant," not "Hot") to suit warmer regions like India.

## Safety Alerts:
Wind: Warns bikers/commuters if wind speeds are dangerous.
Visibility: Detects Mist/Haze conditions for safer driving.
Thunderstorms: Provides immediate safety warnings.
Day/Night Awareness: intelligently distinguishes between "Sunny" (needs sunglasses) and "Clear Night" (good for stargazing) based on sunset times.
Secure: Uses environment variables to protect API keys.

## Tech Stack
Language: Python 3.x
API: OpenWeatherMap
Libraries: requests, python-dotenv, pathlib
Security: .gitignore & Environment Variables

## Installation & Setup
Clone the repository
# Bash
git clone https://github.com/YOUR_USERNAME/weather-outfit-bot.git
cd weather-outfit-bot
Install dependencies

# Bash
pip install requests python-dotenv
Configure API Key
Sign up at OpenWeatherMap to get a free API key.
Rename the example config file:

# Bash
mv .env.example .env
Open .env and paste your key:
Ini, TOML
WEATHER_API_KEY=your_actual_api_key_here
Run the App

# Bash
python weather_bot.py

## The Logic Behind the Code
I moved beyond simple if-else statements to create a more helpful assistant:
Humidity Impact: If (FeelsLike - ActualTemp) > 3°C → Trigger "Sticky/Muggy" warning.
Wind Safety: If WindSpeed > 6 m/s → Trigger "Secure loose items" warning.
Regional Tuning:
< 20°C: Cool/Chilly
20°C - 30°C: Pleasant (Cotton clothes)
> 30°C: Hot

# Time Awareness:
Uses sunrise < current_time < sunset to determine if sunglasses are actually needed.

## Project Structure
├── weather_bot.py    # Main script with logic engine

├── .env.example      # Template for API key (safe to share)

├── .gitignore        # Hides sensitive files from Git

└── README.md         # Project documentation

##Future Improvements
[ ] Add a GUI using Tkinter or Streamlit.

[ ] Support for 5-day forecasts.

[ ] SMS alerts using Twilio for severe weather.
