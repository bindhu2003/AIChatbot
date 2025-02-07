import requests
from config import WEATHER_API_KEY

from utils import get_user_input_voice

def get_weather_info(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f"The current temperature in {city} is {temp}°C with {description}."
    else:
        return "Sorry, I couldn't retrieve the weather information right now."

def inquire_about_weather(chatbot, input_mode):
    print("Which city's weather would you like to know about?")
    if input_mode == 'text':
        city = input("You (Text): ")
    elif input_mode == 'voice':
        city =get_user_input_voice(chatbot.recognizer, chatbot.microphone)
        if not city:
            return "Sorry, I couldn't understand the audio.", False

    weather_info = get_weather_info(city)
    return weather_info, False
