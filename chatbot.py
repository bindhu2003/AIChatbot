import spacy
import speech_recognition as sr
import requests
import matplotlib.pyplot as plt
from PIL import Image
import requests

# Load spaCy model for natural language processing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Download the spaCy model if not found
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Define a SimpleChatbot class
class SimpleChatbot:
    def __init__(self):
        self.context = {}  # Context to store information during the conversation(working on this thing)
        self.nlp = nlp  # Use the loaded spaCy model
        self.recognizer = sr.Recognizer()
        self.weather_api_key = '3fad28b1f6617e940610f44e42304a7e'
        self.song_api_key = 'SONG_API_KEY'  # working on it

    # Method to get user input in text format
    def get_user_input_text(self):
        user_input = input("You (Text): ")
        return user_input.lower()

    # Method to get user input using voice recognition
    def get_user_input_voice(self):
        with sr.Microphone() as source:
            print("Speak something:")
            audio = self.recognizer.listen(source)
            try:
                user_input = self.recognizer.recognize_google(audio)
                print("You (Voice):", user_input)
                return user_input.lower()
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand the audio.")
                return ""
            except sr.RequestError as e:
                print(f"Error with the speech recognition service: {e}")
                return ""

    # Method to get weather information from OpenWeatherMap API
    def get_weather_info(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"The current temperature in {city} is {temp}°C with {description}."
        else:
            return "Sorry, I couldn't retrieve the weather information right now."

    # Method to get song suggestions from Last.fm API
    def get_song_suggestions(self, mood):
        url = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={mood}&api_key={self.song_api_key}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            tracks = data['tracks']['track']
            suggestions = [track['name'] for track in tracks[:5]]  # Get top 5 songs
            return f"Here are some {mood} songs:\n" + "\n".join(suggestions)
        else:
            return "Sorry, I couldn't retrieve song suggestions right now."

    # Method to prompt the user to choose between text and voice input modes
    def get_user_input(self):
        choice = input("Choose input mode (text/voice): ").lower()
        if choice == "text":
            return self.get_user_input_text()
        elif choice == "voice":
            return self.get_user_input_voice()
        else:
            print("Invalid choice. Using text input by default.")
            return self.get_user_input_text()

    # Method to process user input and generate a response
    def process_input(self, user_input, input_mode):
        user_input = user_input.lower()
        doc = self.nlp(user_input)

        # Define keywords for different conversation topics
        greetings = ['hello', 'hai', 'hey', 'howdy']
        fami= ['family','parents','father','mother']
        siblings=['brother','sister','siblings']
        live=['live','home','stay','house','address','location']
        song_keywords = ['song', 'music', 'suggest songs']
        farewells = ['bye', 'goodbye', 'see you later', 'cya']
        
        # Check if user input matches specific topics
        if any(word in user_input for word in greetings):
            return "Hello! What topic would you like information on? Options include education, weather, health, songs etc.", False

        elif any(word in user_input for word in farewells):
            return self.exit_chat(), True
        
        elif any(word in user_input for word in fami):
            return "I don't have a family in the way humans do. I'm here to assist and provide information. Is there anything else you'd like to know?", False
        
        elif any(word in user_input for word in live):
            return "I reside in the cloud, enjoying the virtual breeze and soaking up the digital sunshine. It's a bit crowded up here with all the data, but the neighbors are friendly.", False

        elif any(word in user_input for word in siblings):
            return " I'm a chatbot there to assist you. I don't have siblings in the traditional sense.I'm not a living being, so I don't have family relationships.", False

        elif any(word in user_input for word in song_keywords):
            return self.suggest_songs(input_mode), False
        
        elif user_input == 'exit':
            return self.exit_chat(), True
        
        elif any(topic_keyword in user_input for topic_keyword in ['education', 'study', 'learn']):
            return self.inquire_about_topic('education'), False

        elif any(topic_keyword in user_input for topic_keyword in ['weather', 'forecast']):
            return self.inquire_about_weather(input_mode), False

        elif any(topic_keyword in user_input for topic_keyword in ['health', 'medical', 'wellness']):
            return self.inquire_about_topic('health'), False

        elif 'not well' in user_input:
            return "I'm not a doctor, but here are some general tips: " \
                   "Stay hydrated, get enough rest, and consult with a healthcare professional for personalized advice.", False

        elif 'name' in user_input:
            return "I'm a chatbot. You can call me ChatBot!", False

        elif 'favorite color' in user_input:
            return "I like all colors, but I don't have a favorite. What about you?", False

        elif 'headache' in user_input or any(ent.text.lower() == 'headache' for ent in doc.ents):
            return self.get_headache_remedy(), False

        elif 'sore throat' in user_input or any(ent.text.lower() == 'sore throat' for ent in doc.ents):
            return self.get_sore_throat_remedy(), False

        elif 'cough' in user_input or any(ent.text.lower() == 'cough' for ent in doc.ents):
            return self.get_cough_remedy(), False

        elif 'fever' in user_input or any(ent.text.lower() == 'fever' for ent in doc.ents):
            return self.get_fever_remedy(), False

        elif 'stomach ache' in user_input or any(ent.text.lower() == 'stomach ache' for ent in doc.ents):
            return self.get_stomach_ache_remedy(), False

        elif 'nausea' in user_input or any(ent.text.lower() == 'nausea' for ent in doc.ents):
            return self.get_nausea_remedy(), False

        elif 'school' in user_input or any(ent.text.lower() == 'school' for ent in doc.ents):
            return self.get_school(), False

        elif 'intermediate' in user_input or any(ent.text.lower() == 'intermediate' for ent in doc.ents):
            return self.get_intermediate(), False

        elif 'undergraduation' in user_input or any(ent.text.lower() == 'undergraduation' for ent in doc.ents):
            return self.get_undergraduation(), False
        
        else:
            return "I'm sorry, I didn't understand that. Can you please rephrase?", False

    def inquire_about_topic(self, topic):
        print(f"What specific information would you like about {topic}? Please provide more details or ask a specific question.")
        if topic == 'health':
            print("*headache\n*sore throat\n*cough\n*fever\n*stomach ache\n*nausea")
        elif topic == 'education':
            print("We provide information on various education levels. Choose one:\n1. School\n2. Intermediate\n3. Undergraduation")

    def inquire_about_weather(self, input_mode):
        print("Which city's weather would you like to know about?")
        if input_mode == 'text':
            city = input("You (Text): ")
        elif input_mode == 'voice':
            city = self.get_user_input_voice()
            if not city:
                return "Sorry, I couldn't understand the audio."

        weather_info = self.get_weather_info(city)
        return weather_info

    def exit_chat(self):
        feedback = input("Was this information helpful? (yes/no): ").lower()
        if feedback == 'yes':
            return "Thank you! I'm glad I could help. Goodbye!"
        elif feedback == 'no':
            return "I'm sorry to hear that. If you have any suggestions for improvement, feel free to share. Goodbye!"
        else:
            return "Invalid feedback. Goodbye!"
        
    def suggest_songs(self, input_mode):
        if input_mode == "text":
            mood = input("Sure! I'd love to suggest some songs. Could you tell me your current mood? ")
        elif input_mode == "voice":
            print("Sure! I'd love to suggest some songs. Could you tell me your current mood? ")
            mood = self.get_user_input_voice()
            if not mood:
                return "Sorry, I couldn't understand the audio."

        song_suggestions = self.get_song_suggestions(mood.lower())
        return song_suggestions

    # Health remedies functions (simplified for brevity)
    def get_headache_remedy(self):
        return "For a headache, consider resting in a quiet, dark room, staying hydrated, and taking over-the-counter pain relief if necessary."

    def get_sore_throat_remedy(self):
        return "For a sore throat, try gargling with warm salt water, staying hydrated, and using throat lozenges."

    def get_cough_remedy(self):
        return "For a cough, stay hydrated, use a humidifier, and consider honey or cough medicine."

    def get_fever_remedy(self):
        return "For a fever, stay hydrated, rest, and take over-the-counter fever reducers if needed."

    def get_stomach_ache_remedy(self):
        return "For a stomach ache, try drinking clear fluids, avoiding solid food for a few hours, and eating bland foods when you feel ready."

    def get_nausea_remedy(self):
        return "For nausea, try eating small, frequent meals, avoiding strong smells, and drinking ginger tea."

    def get_school(self):
        return "School provides primary education, focusing on basic subjects such as reading, writing, math, and science."

    def get_intermediate(self):
        return "Intermediate education, often referred to as high school, prepares students for higher education and future careers with more specialized subjects."

    def get_undergraduation(self):
        return "Undergraduate education typically involves earning a bachelor's degree in a chosen field of study at a college or university."

# Main loop for the chatbot
chatbot = SimpleChatbot()
print("Chatbot: Hello! (Type 'exit' to end the conversation.)")

# Ask for input mode only once at the beginning
input_mode = input("Choose input mode (text/voice): ").lower()

while True:
    if input_mode not in ["text", "voice"]:
        print("Invalid choice. Using text input by default.")
        input_mode = "text"

    # Get user input
    if input_mode == "text":
        user_input = chatbot.get_user_input_text()
    elif input_mode == "voice":
        user_input = chatbot.get_user_input_voice()

    # Process user input
    response, exit_chat = chatbot.process_input(user_input, input_mode)

    # Print chatbot's response
    if response is not None:
        print("Chatbot:", response)

    # Check if the chat is ending
    if exit_chat:
        break
