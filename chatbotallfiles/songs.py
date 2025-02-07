
from utils import get_user_input_voice
def suggest_songs(chatbot, input_mode):
    if input_mode == "text":
        mood = input("Sure! I'd love to suggest some songs. Could you tell me your current mood? ")
    elif input_mode == "voice":
        print("Sure! I'd love to suggest some songs. Could you tell me your current mood? ")
        mood = get_user_input_voice(chatbot.recognizer, chatbot.microphone)
        if not mood:
            return "Sorry, I couldn't understand the audio."        
    if mood.lower() == 'happy':
        return "Great choice! Here are some happy songs: \"Darshana\" by Anurag Kulkarni\n\"Vachinde\" by Suddala Ashok Teja\n\"ButtaBomma\" by Ramajogayya Sastry\n\"Choti Choti Baatein\" by  Devi Sri Prasad\n\"O Pilla Subhanallah\" by Ananta Sriram"
    elif mood.lower() == 'sad':
        return "I'm sorry to hear that. Here are some comforting songs: \"Nammaka Thappani\" by Devi Sri Prasad\n\"Oosupodu\" by Chaithanya Pingali\n\"Kallalo Unnadedo\" by Vanamali\n\"Koti Koti\" by Ananta Sriram\n\"Nee Tholisariga\" by Sirivennela Seetharama Sastry"
    else:
        return "I'm not sure about that mood. Here are some random songs: \"Inkem Inkem Inkem Kaavaale\" by  Ananta Sriram\n\"Emai Pothane\" by a Anantha Sriram\n\"Emo Emo\" by Sreejo\n\"Ninnu Kori\" by  Ramajogayya Sastry\n\"Prema Desam\" by Sirivennela Seetharama Sastry"