import os
import sys
import requests
from dotenv import load_dotenv 
from pathlib import Path # Add this import

# 1. Force Python to find the .env file in the current folder
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# 2. Try to get the key
API_KEY = os.getenv("WEATHER_API_KEY")

# Debugging: Print "Found" or "Not Found" (Safe, doesn't print the key)
if API_KEY:
    print("✅ Success: API Key loaded!")
else:
    print("❌ Failed: API Key variable is None.")
    sys.exit(1)

# --- REST OF YOUR CODE BELOW ---
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
CITY = "chennai"  # You can change this or make it user input

def get_weather_data(city_name):
    """
    Sends a request to the weather API and returns the JSON data.
    """
    # Construct the full URL with query parameters
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"  # Use 'imperial' for Fahrenheit
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        
        # Check if the request was successful (Status Code 200)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def generate_outfit_suggestion(temp, weather_desc):
    """
    Analyzes temperature and description to return advice.
    """
    suggestion = ""
    
   # Temperature Logic (Adjusted for Tropical Climates)
    if temp < 20:
        # In Chennai, anything below 20 actually feels quite cool
        suggestion += "❄️ It's a bit chilly. Bring a light jacket or sweater.\n"
        
    elif 20 <= temp < 30:
        # 20 to 30 is standard "nice" weather here
        suggestion += "👕 It's pleasant weather. Normal cotton clothes are perfect.\n"
        
    else:
        # Now, only 30+ is considered "Hot"
        suggestion += "☀️ It's hot! Wear breathable clothes and stay hydrated.\n"

   # Condition Logic
    condition = weather_desc.lower()
    
    if "rain" in condition or "drizzle" in condition:
        suggestion += "☔ Take an umbrella, it's wet out there."
    elif "mist" in condition or "haze" in condition or "fog" in condition:
        suggestion += "🌫️ Visibility might be low due to mist/haze. Drive carefully!"
    elif "clear" in condition and temp > 25:
        suggestion += "😎 Don't forget your sunglasses!"
        
    return suggestion

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print(f"Fetching weather for {CITY}...\n")
    
    data = get_weather_data(CITY)
    
    if data:
        # 1. Parse the specific data points we need
        current_temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        # 2. Display the Data
        print(f"--- WEATHER REPORT FOR {CITY.upper()} ---")
        print(f"Temperature: {current_temp}°C (Feels like {feels_like}°C)")
        print(f"Condition:   {description.capitalize()}")
        print(f"Humidity:    {humidity}%")
        print("-" * 30)
        
        # 3. The 'Value Add' (Outfit Suggestion)
        advice = generate_outfit_suggestion(current_temp, description)
        print("💡 OUTFIT ADVICE:")
        print(advice)