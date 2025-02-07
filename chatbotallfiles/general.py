from utils import exit_chat

def process_general_queries(user_input):
    greetings = ['hello', 'hai', 'hey', 'howdy']
    fami = ['family', 'parents', 'father', 'mother']
    siblings = ['brother', 'sister', 'siblings']
    live = ['live', 'home', 'stay', 'house', 'address', 'location']
    farewells = ['bye', 'goodbye', 'see you later', 'cya' ,'exit' ,'quit']

    if any(word in user_input for word in greetings):
        return "Hello! What topic would you like information on? Options include education, weather, health, songs,tourism  etc.", False

    elif any(word in user_input for word in farewells):
        return exit_chat()

    elif any(word in user_input for word in fami):
        return "I don't have a family in the way humans do. I'm here to assist and provide information. Is there anything else you'd like to know?", False

    elif any(word in user_input for word in live):
        return "I reside in the cloud, enjoying the virtual breeze and soaking up the digital sunshine. It's a bit crowded up here with all the data, but the neighbors are friendly.", False

    elif any(word in user_input for word in siblings):
        return "I'm a chatbot here to assist you. I don't have siblings in the traditional sense. I'm not a living being, so I don't have family relationships.", False

    return None, False

