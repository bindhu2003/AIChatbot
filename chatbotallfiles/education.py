from utils import get_user_input_voice
def get_school():
    return "School provides primary education, focusing on basic subjects such as reading, writing, math, and science."

def get_intermediate():
    return "Intermediate education, often referred to as high school, prepares students for higher education and future careers with more specialized subjects."

def get_undergraduation():
    return "Undergraduate education typically involves earning a bachelor's degree in a chosen field of study at a college or university."

def inquire_about_topic(chatbot, input_mode):
    if input_mode == 'text':
        print("We provide information on various education levels. You can ask about:\n- School\n- Intermediate\n- Undergraduation")
        choice = input("Enter the education level you want information about: ").strip().lower()
    elif input_mode == 'voice':
        print("We provide information on various education levels. You can ask about:\n- School\n- Intermediate\n- Undergraduation")
        print("Please speak the education level you want information about:")
        choice = get_user_input_voice(chatbot.recognizer, chatbot.microphone).strip().lower()
    
    if choice == 'school':
        return get_school()
    elif choice == 'intermediate':
        return get_intermediate()
    elif choice == 'undergraduation':
        return get_undergraduation()
    else:
        return "Invalid choice. Please enter a valid education level (School, Intermediate, Undergraduation)."