import spacy
import speech_recognition as sr
from health import inquire_about_health
from education import inquire_about_topic
from weather import inquire_about_weather
from general import process_general_queries
from tourism import inquire_about_tourism
from songs import suggest_songs
from utils import get_user_input_text, get_user_input_voice, exit_chat
from config import WEATHER_API_KEY, SONG_API_KEY

# Load spaCy model for natural language processing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class SimpleChatbot:
    def __init__(self):
        self.context = {}
        self.nlp = nlp
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.weather_api_key = WEATHER_API_KEY
        self.song_api_key = SONG_API_KEY
        self.load_medical_data()

    def load_medical_data(self):
        from health import load_and_preprocess_medical_data
        self.medical_data, self.label_encoders, self.rf_classifier = load_and_preprocess_medical_data()

    def get_user_input(self):
        choice = input("Choose input mode (text/voice): ").lower()
        if choice == "text":
            return get_user_input_text()
        elif choice == "voice":
            return get_user_input_voice(self.recognizer, self.microphone)
        else:
            print("Invalid choice. Using text input by default.")
            return get_user_input_text()

    def process_input(self, user_input, input_mode):
        user_input = user_input.lower()
        doc = self.nlp(user_input)
        
        response, exit_chat = process_general_queries(user_input)
        if response:
            return response, exit_chat

        if any(topic_keyword in user_input for topic_keyword in ['health', 'medical', 'wellness']):
            return inquire_about_health(self, input_mode), False

        elif any(topic_keyword in user_input for topic_keyword in ['education', 'study', 'learn']):
            return inquire_about_topic(self, input_mode), False

        elif any(topic_keyword in user_input for topic_keyword in ['weather', 'forecast']):
            return inquire_about_weather(self, input_mode)
        
        elif any(topic_keyword in user_input for topic_keyword in ['tourism', 'travel', 'place']):
            return inquire_about_tourism(self, input_mode), False
        
        elif any(topic_keyword in user_input for topic_keyword in ['music','songs','song','entertainment']):
            return suggest_songs(self, input_mode), False

        return "I'm sorry, I didn't understand that. Can you please rephrase?", False

    def run_chat(self):
        print("Chatbot: Hello! (Type 'exit' to end the conversation.)")

        input_mode = input("Choose input mode (text/voice): ").lower()
        while True:
            if input_mode not in ["text", "voice"]:
                print("Invalid choice. Using text input by default.")
                input_mode = "text"

            if input_mode == "text":
                user_input = get_user_input_text()
            elif input_mode == "voice":
                user_input = get_user_input_voice(self.recognizer, self.microphone)

            response, exit_chat = self.process_input(user_input, input_mode)

            if response is not None:
                print("Chatbot:", response)

            if exit_chat:
                break
