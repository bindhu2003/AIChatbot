import speech_recognition as sr

def get_user_input_text():
    user_input = input("You (Text): ")
    return user_input.lower()

def get_user_input_voice(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Speak something:")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            print("You (Voice):", user_input)
            return user_input.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
            return ""

def exit_chat():
    feedback = input("Was this information helpful? (yes/no): ").lower()
    if feedback == 'yes':
        return "Thank you! I'm glad I could help. Goodbye!", True
    elif feedback == 'no':
        return "I'm sorry to hear that. If you have any suggestions for improvement, feel free to share. Goodbye!", True
    else:
        return "Invalid feedback. Goodbye!", True
