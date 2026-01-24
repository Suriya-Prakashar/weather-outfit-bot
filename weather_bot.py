import os
import sys
import requests
from dotenv import load_dotenv 
from pathlib import Path 

# --- 1. SETUP & CONFIGURATION ---
# Force Python to find the .env file in the current folder
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Try to get the key
API_KEY = os.getenv("WEATHER_API_KEY")

# Safety Check
if not API_KEY:
    print("❌ Failed: API Key variable is None. Check your .env file.")
    sys.exit(1)

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# --- 2. FUNCTIONS ---

def get_weather_data(city_name):
    """
    Sends a request to the weather API and returns the JSON data.
    """
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def generate_smart_suggestion(temp, feels_like, weather_desc, humidity, wind_speed, is_daytime):
    """
    Analyzes multiple data points to return smart advice.
    """
    suggestion = ""
    condition = weather_desc.lower()

    # --- A. TEMPERATURE LOGIC (Tropical Context) ---
    if temp < 20:
        suggestion += "❄️ It's chilly. Bring a light jacket or sweater.\n"
    elif 20 <= temp < 30:
        suggestion += "👕 It's pleasant weather. Normal cotton clothes are perfect.\n"
    else:
        suggestion += "☀️ It's hot! Wear breathable clothes and stay hydrated.\n"

    # --- B. FEELS LIKE (Heat Index) LOGIC ---
    # If the difference between actual temp and 'feels like' is significant
    if (feels_like - temp) > 3:
         suggestion += f"🥵 CAUTION: It feels much hotter ({feels_like}°C) due to humidity!\n"

    # --- C. CONDITION LOGIC ---
    if "thunderstorm" in condition:
        suggestion += "⚡ THUNDERSTORM WARNING! Stay indoors and unplug electronics.\n"
    elif "rain" in condition or "drizzle" in condition:
        suggestion += "☔ It's raining. Take an umbrella and wear water-resistant shoes.\n"
    elif "mist" in condition or "haze" in condition or "fog" in condition:
        suggestion += "🌫️ Visibility is low (Mist/Haze). Drive carefully.\n"
    elif "overcast" in condition:
        suggestion += "☁️ Total cloud cover. The lighting is flat/gloomy.\n"
    
    # --- D. SUN & DAYLIGHT LOGIC ---
    if "clear" in condition and is_daytime:
        suggestion += "😎 It's bright and sunny. Don't forget sunglasses!\n"
    elif "clear" in condition and not is_daytime:
        suggestion += "✨ It's a clear night. Good for stargazing.\n"

    # --- E. WIND & HUMIDITY LOGIC ---
    if wind_speed > 6: # approx 20 km/h
        suggestion += "💨 It's breezy/windy. Watch your hair and secure loose items.\n"
    
    if humidity > 80:
        suggestion += f"💧 High Humidity ({humidity}%). Expect frizzy hair and sweat that won't dry.\n"

    return suggestion

# --- 3. MAIN EXECUTION ---
if __name__ == "__main__":
    # Get user input
    city = input("Enter city name: ")
    print(f"\nFetching weather for {city}...\n")
    
    data = get_weather_data(city)
    
    if data:
        # 1. Parse Data Points
        current_temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"] # Speed in meters/sec
        
        # 2. Calculate Day vs Night
        sunrise = data["sys"]["sunrise"]
        sunset = data["sys"]["sunset"]
        now = data["dt"]
        is_daytime = sunrise < now < sunset

        # 3. Display the Report
        print(f"--- WEATHER REPORT FOR {city.upper()} ---")
        print(f"Temperature: {current_temp}°C (Feels like {feels_like}°C)")
        print(f"Condition:   {description.capitalize()}")
        print(f"Humidity:    {humidity}%")
        print(f"Wind Speed:  {wind_speed} m/s")
        print("-" * 30)
        
        # 4. Generate & Print Advice
        advice = generate_smart_suggestion(
            current_temp, 
            feels_like, 
            description, 
            humidity, 
            wind_speed, 
            is_daytime
        )
        print("💡 SMART OUTFIT ADVICE:")
        print(advice)