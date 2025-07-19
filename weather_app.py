import requests
import json
from datetime import datetime

class WeatherApp:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city_name):
        try:
            # Make API request
            params = {
                'q': city_name,
                'appid': self.api_key,
                'units': 'metric'  # Use 'imperial' for Fahrenheit
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Parse JSON response
            weather_data = response.json()
            
            # Extract and format relevant data
            weather_info = {
                'city': weather_data['name'],
                'country': weather_data['sys']['country'],
                'temperature': weather_data['main']['temp'],
                'feels_like': weather_data['main']['feels_like'],
                'humidity': weather_data['main']['humidity'],
                'wind_speed': weather_data['wind']['speed'],
                'description': weather_data['weather'][0]['description'].title(),
                'sunrise': datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M'),
                'pressure': weather_data['main']['pressure'],
                'visibility': weather_data.get('visibility', 'N/A')
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing weather data: {e}")
            return None
    
    def display_weather(self, weather_info):
        if not weather_info:
            print("No weather data to display.")
            return
        
        print("\n=== Current Weather ===")
        print(f"Location: {weather_info['city']}, {weather_info['country']}")
        print(f"Temperature: {weather_info['temperature']}°C (Feels like {weather_info['feels_like']}°C)")
        print(f"Weather: {weather_info['description']}")
        print(f"Humidity: {weather_info['humidity']}%")
        print(f"Wind Speed: {weather_info['wind_speed']} m/s")
        print(f"Pressure: {weather_info['pressure']} hPa")
        print(f"Visibility: {weather_info['visibility']} meters")
        print(f"Sunrise: {weather_info['sunrise']}")
        print(f"Sunset: {weather_info['sunset']}")
        print("======================\n")

def main():
    # Get API key (in a real app, you might want to store this more securely)
    api_key = "1a45e0667b1074687306201df0cf198f"
    
    # Initialize weather app
    app = WeatherApp(api_key)
    
    while True:
        print("\nWeather App Menu:")
        print("1. Get weather by city name")
        print("2. Exit")
        
        choice = input("Enter your choice (1-2): ").strip()
        
        if choice == '1':
            city_name = input("Enter city name: ").strip()
            weather_data = app.get_weather(city_name)
            app.display_weather(weather_data)
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
