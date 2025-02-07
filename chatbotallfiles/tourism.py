import matplotlib.pyplot as plt
from utils import get_user_input_voice
tourist_places = {
    "golconda": {
        "image": "chatbotallfileszip/chatbotallfiles/tourist images/tourist images/golconda.jpeg",
        "info": "Golconda Fort is a historic fortress and citadel located in Hyderabad, known for its rich history and architectural grandeur."
    },
    "birla mandir": {
        "image": "chatbotallfileszip/chatbotallfiles/tourist images/tourist images/birla mandir.jpeg",
        "info": "Birla Mandir is a Hindu temple built on a 280-foot-high hillock called Naubath Pahad, dedicated to Lord Venkateswara."
    },
    "hussain sagar": {
        "image": "chatbotallfileszip/chatbotallfiles/tourist images/tourist images/Hussain sagar.jpeg",
        "info": "Hussain Sagar is a heart-shaped lake in Hyderabad built by Ibrahim Quli Qutb Shah in 1563. It is famous for the large monolithic statue of Gautama Buddha."
    },
    "lumbini park": {
        "image": "chatbotallfileszip/chatbotallfiles/tourist images/tourist images/Lumbini park.jpeg",
        "info": "Lumbini Park is an urban park located alongside Hussain Sagar Lake, known for its beautiful landscape and musical fountain show."
    },
    "nehru zoological park": {
        "image": "chatbotallfileszip/chatbotallfiles/tourist images/tourist images/Nehru Zoological park.jpeg",
        "info": "Nehru Zoological Park is one of the most visited destinations in Hyderabad, home to a wide variety of animals, birds, and reptiles."
    },
    "ntr gardens": {
        "image": "chatbotallfileszip/chatbotallfiles/tourist images/tourist images/NTR gardens.jpeg",
        "info": "NTR Gardens is a small public park located close to Hussain Sagar Lake, known for its lush green landscape and recreational activities."
    },
    "salarjung museum": {
        "image": "chatbotallfileszip/chatbotallfiles/tourist images/tourist images/salarjung museum.jpeg",
        "info": "Salarjung Museum is an art museum located at Dar-ul-Shifa, famous for its collection of sculptures, paintings, carvings, textiles, and manuscripts."
    },
    "shilparamam": {
        "image": "chatbotallfileszip/chatbotallfiles/tourist images/tourist images/Shilparamam.jpeg",
        "info": "Shilparamam is an arts and crafts village located in Hyderabad, showcasing traditional crafts and cultural festivals."
    },
    "ramoji film city": {
        "image": "chatbotallfileszip/chatbotallfiles/tourist images/tourist images/ramoji film city.jpeg",
        "info": "Ramoji Film City is the world’s largest film studio complex, offering a multitude of entertainment options and film sets."
    },
    "charminar": {
        "image": "D:\CHATBOTADVANCE\chatbotallfileszip\chatbotallfiles\tourist images\tourist images\charminar.jpeg",
        "info": "Charminar is a historic monument and mosque located in Hyderabad, known for its signature architectural style and bustling local markets."
    }
}

def inquire_about_tourism(chatbot, input_mode):
    if input_mode == 'text':
        place = input("Enter the name of the tourist place in Hyderabad: ")
    elif input_mode == 'voice':
        print("Please speak the name of the tourist place:")
        place = get_user_input_voice(chatbot.recognizer, chatbot.microphone)

    # Check if the place is in the dictionary
    place_info = tourist_places.get(place.lower())

    if place_info:
        print(f"Here is an image of {place}:")
        img = plt.imread(place_info["image"])
        plt.imshow(img)
        plt.axis('off')  # Hide axes
        plt.show()
        
        # Display information after closing the image
        print(f"Information about {place}: {place_info['info']}")
    else:
        return "Sorry, I couldn't find an image for that place.", False
