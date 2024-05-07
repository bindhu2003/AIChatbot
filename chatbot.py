# Import necessary libraries
import spacy
import speech_recognition as sr
#from IPython.display import display
import matplotlib.pyplot as plt
from PIL import Image

try:
    # Load spaCy model for natural language processing
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Download the spaCy model if not found
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Define a SimpleChatbot class
class SimpleChatbot:
    def __init__(self):
        self.context = {} # Context to store information during the conversation
        self.nlp = nlp  # Use the loaded spaCy model
        self.recognizer = sr.Recognizer()

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
            return "I don't have a family in the way humans do. I'm here to assist and provide information. Is there anything else you'd like to know?",False
        
        elif any(word in user_input for word in live):
            return "I reside in the cloud, enjoying the virtual breeze and soaking up the digital sunshine. It's a bit crowded up here with all the data, but the neighbors are friendly.",False
        elif any(word in user_input for word in siblings):
            return " I'm a chatbot there to assist you. I don't have siblings in the traditional sense.I'm not a living being, so I don't have family relationships.",False
        elif any(word in user_input for word in song_keywords):
            if 'type' in user_input:  # Check for keywords related to music type selection
                return self.select_music_type(user_input), False
            else:
                return self.suggest_songs(), False
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

    def inquire_about_weather(self,input_mode):
        print("What season are you interested in for the weather forecast? (summer/winter/rainy)")
        if input_mode == 'text':
            season = input("You (Text):")
        elif input_mode == 'voice':
            season = self.get_user_input_voice()
            if not season:
                return "Sorry, I couldn't understand the audio."

        season = season.lower()

        if season == 'summer':
            return self.get_summer_weather_response()
        elif season == 'winter':
            return self.get_winter_weather_response()
        elif season == 'rainy':
            return self.get_rainy_weather_response()
        else:
            return "I'm sorry, I didn't recognize that season. Please choose summer, winter, or rainy.\nWhat topic would you like information on? Options include education, weather, health, songs etc."

    def get_summer_weather_response(self):
        return "In summer, you can expect warm temperatures. It's a good time for outdoor activities and enjoying the sunshine.\nWhat topic would you like information on? Options include education, weather, health, songs etc."

    def get_winter_weather_response(self):
        return "During winter, temperatures are colder, and you might experience snow or rain. It's advisable to dress warmly and be cautious of slippery surfaces.\nWhat topic would you like information on? Options include education, weather, health, songs etc."

    def get_rainy_weather_response(self):
        return "In the rainy season, you can expect precipitation. Don't forget to carry an umbrella or raincoat when heading out.\nWhat topic would you like information on? Options include education, weather, health, songs etc."
   
    def select_music_type(self, user_input):
        if 'text' in user_input:
            return self.suggest_songs_text()
        elif 'voice' in user_input:
            return self.suggest_songs_voice()
        else:
            return "I didn't catch that. Please specify whether you want song suggestions through text or voice.", False

    
            
    def exit_chat(self):
        feedback = input("Was this information helpful? (yes/no): ").lower()
        if feedback == 'yes':
            return "Thank you! I'm glad I could help. Goodbye!"
        elif feedback == 'no':
            return "I'm sorry to hear that. If you have any suggestions for improvement, feel free to share. Goodbye!"
        else:
            return "Invalid feedback. Goodbye!"
        
    def suggest_songs(self):
        if input_mode == "text":
            mood = input("Sure! I'd love to suggest some songs. Could you tell me your current mood? ")
        elif input_mode == "voice":
            print("Sure! I'd love to suggest some songs. Could you tell me your current mood? ")
            mood = self.get_user_input_voice()
            if not mood:
                return "Sorry, I couldn't understand the audio."        
        if mood.lower() == 'happy':
            return "Great choice! Here are some happy songs: \"Darshana\" by Anurag Kulkarni\n\"Vachinde\" by Suddala Ashok Teja\n\"ButtaBomma\" by Ramajogayya Sastry\n\"Choti Choti Baatein\" by  Devi Sri Prasad\n\"O Pilla Subhanallah\" by Ananta Sriram"
        elif mood.lower() == 'sad':
            return "I'm sorry to hear that. Here are some comforting songs: \"Nammaka Thappani\" by Devi Sri Prasad\n\"Oosupodu\" by Chaithanya Pingali\n\"Kallalo Unnadedo\" by Vanamali\n\"Koti Koti\" by Ananta Sriram\n\"Nee Tholisariga\" by Sirivennela Seetharama Sastry"
        else:
            return "I'm not sure about that mood. Here are some random songs: \"Inkem Inkem Inkem Kaavaale\" by  Ananta Sriram\n\"Emai Pothane\" by a Anantha Sriram\n\"Emo Emo\" by Sreejo\n\"Ninnu Kori\" by  Ramajogayya Sastry\n\"Prema Desam\" by Sirivennela Seetharama Sastry"
        
    def get_education_response(self):
        return "We offer a variety of educational courses. Whether you're interested in programming, science, or art, we have something for everyone. " \
               "Please visit our website or contact our support team for more details."

    def get_weather_response(self):
        return "I don't have access to real-time weather information right now. " \
               "But it's always good to carry an umbrella, just in case!"

    def get_health_response(self):
        return "For health-related queries, it's important to consult with a healthcare professional. " \
               "If you have specific symptoms, please provide more details for personalized advice."

    def get_school(self):
        return "School education lays the foundation for future learning. Make sure to attend classes regularly and stay curious!\nAfter School education, you can enter into intermediate courses like MPC, BiPC, MEC, CEC, and you may also take other diploma courses too.."

    def get_intermediate(self):
        return "Intermediate education is crucial for specialization. Consider subjects that align with your interests and career goals.\nAfter intermediate education, you can pursue courses like: Engineering/Technology: BTech, BE\nMedical Sciences: MBBS, BDS, BSc Nursing\nCommerce/Business: BCom, BBA, CA, CS\nComputer Science/IT: BCA, BSc IT\nArts/Humanities: BA, BFA, BSW\nPsychology: BSc Psychology\nParamedical: BSc Paramedical"

    def get_undergraduation(self):
        return "Undergraduation is a significant step. Explore various courses and choose a major that aligns with your passion and career aspirations.\nAfter undergraduate studies: Master's Degree: MA, MBA\nDoctoral Programs (Ph.D.)\nLaw (LL.M.)\nMedical Specializations (MD, MS)\nEducation (B.Ed, M.Ed)\nEntrepreneurship Programs"

    def get_headache_remedy(self):
        image_path = 'headache.jpg'  
        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        return "For a headache, you might try resting in a quiet, dark room, staying hydrated, and taking over-the-counter pain relievers. " \
               "However, it's essential to consult with a healthcare professional for persistent headaches."
    
    def get_sore_throat_remedy(self):
        image_path = 'sorethroat.jpg'  
        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        return "For a sore throat, you can try drinking warm tea with honey, gargling with saltwater, and staying hydrated. " \
               "If the sore throat persists, it's recommended to consult with a healthcare professional."

    def get_cough_remedy(self):
        image_path = 'cough.jpg'  
        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        return "For a cough, consider staying hydrated, using a humidifier, and taking over-the-counter cough medicine. " \
               "If the cough persists or is accompanied by other symptoms, consult with a healthcare professional."

    def get_fever_remedy(self):
        image_path = 'fever.jpg'  
        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        return "For a fever, it's important to rest, stay hydrated, and consider taking over-the-counter fever-reducing medications like acetaminophen or ibuprofen or paracetamol or dolo 650 " \
               "If the fever persists or is accompanied by other concerning symptoms, consult with a healthcare professional."

    def get_stomach_ache_remedy(self):
        image_path = 'stomachache.jpg'  
        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        return "For a stomach ache, you can try resting, drinking clear fluids, and avoiding spicy or fatty foods. " \
               "If the stomach ache persists or is severe, it's advisable to consult with a healthcare professional."

    def get_nausea_remedy(self):
        image_path = 'nausea.jpg'  
        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        return "For nausea, consider sipping on clear fluids, eating bland foods, and avoiding strong odors. " \
               "If nausea persists or is accompanied by other symptoms, it's important to consult with a healthcare professional."


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