from typing import TypedDict
import httpx
import os
from dotenv import find_dotenv, load_dotenv

from agents import Agent, function_tool
from openai import api_type

# Load environment variables
load_dotenv(find_dotenv())

class Location(TypedDict):
    city: str

@function_tool  
async def fetch_weather(location: Location) -> str:
    """Fetch the weather for a given location from OpenWeatherMap API.

    Args:
        location: The location to fetch the weather for.
    
    Returns:
        A string describing the current weather conditions.
    """
    api_key = os.getenv("OPENWEATHER_API")

    print(api_key)
    
    if not api_key:
        return "Error: OpenWeatherMap API key not found. Please set OPENWEATHERMAP_API_KEY in your .env file."
    
    city = location.get("city", "")

    print(city)

    if not city:
        return "Error: City name is required."
    
    try:
        # OpenWeatherMap API endpoint
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  # Use metric units (Celsius)
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        
        # Extract relevant weather information
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        # Format the response
        weather_info = (
            f"Weather in {city.title()}: {weather_description.capitalize()}. "
            f"Temperature: {temperature}°C (feels like {feels_like}°C). "
            f"Humidity: {humidity}%. Wind speed: {wind_speed} m/s."
        )
        
        return weather_info
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: City '{city}' not found. Please check the spelling."
        elif e.response.status_code == 401:
            return "Error: Invalid API key. Please check your OPENWEATHERMAP_API_KEY."
        else:
            return f"Error: Unable to fetch weather data. Status code: {e.response.status_code}"
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

weather_agent = Agent(
    name='Weather Agent',
    instructions=(
        "You are a helpful assistant that provides weather information. "
        "When users ask about weather in a specific city, use the fetch_weather tool. "
        "Be friendly and conversational in your responses."
    ),
    tools=[fetch_weather]
)