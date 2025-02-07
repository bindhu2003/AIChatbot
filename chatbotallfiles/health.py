import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from utils import get_user_input_voice

def load_and_preprocess_medical_data():
    # Load medical data
    medical_data = pd.read_csv('medical data.csv')
    
    # Fill missing values with mode
    for column in ['Gender', 'Symptoms', 'Causes', 'Disease', 'Medicine']:
        medical_data[column].fillna(medical_data[column].mode()[0], inplace=True)
    
    # Drop unnecessary columns
    medical_data = medical_data.drop(['Name', 'DateOfBirth'], axis=1)
    
    # Encode categorical columns
    label_encoders = {}
    for column in medical_data.columns:
        label_encoders[column] = LabelEncoder()
        medical_data[column] = label_encoders[column].fit_transform(medical_data[column])
        
    # Split data into features (X) and target (y)
    X = medical_data[['Symptoms', 'Causes', 'Disease']]
    y = medical_data['Medicine']
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train Random Forest classifier
    rf_classifier = RandomForestClassifier(random_state=42)
    rf_classifier.fit(X_train, y_train)
    
    # Evaluate model accuracy
    y_pred_rf = rf_classifier.predict(X_test)
    accuracy_rf = accuracy_score(y_test, y_pred_rf)
    print(f"Random Forest Accuracy: {accuracy_rf}")
    
    return medical_data, label_encoders, rf_classifier

def transform_input(label_encoder, value):
    # Transform input value to match the encoded format
    transformed_value = label_encoder.transform([value.capitalize()])[0]
    return transformed_value

def inquire_about_health(chatbot, input_mode):
    print("Please enter the following details:")
    
    if input_mode == 'text':
        symptoms = input("Enter Symptoms: ")
        causes = input("Enter Causes: ")
        disease = input("Enter Disease: ")
    elif input_mode == 'voice':
        print("Please speak your symptoms:")
        symptoms = get_user_input_voice(chatbot.recognizer, chatbot.microphone)
        print("Please speak the causes:")
        causes = get_user_input_voice(chatbot.recognizer, chatbot.microphone)
        print("Please speak the disease:")
        disease = get_user_input_voice(chatbot.recognizer, chatbot.microphone)
        
        if not symptoms or not causes or not disease:
            return "Sorry, I couldn't understand the audio.", False
    
    print(f"Received inputs: Symptoms={symptoms}, Causes={causes}, Disease={disease}")
    
    try:
        # Transform inputs
        transformed_symptoms = transform_input(chatbot.label_encoders['Symptoms'], symptoms)
        transformed_causes = transform_input(chatbot.label_encoders['Causes'], causes)
        transformed_disease = transform_input(chatbot.label_encoders['Disease'], disease)
        
        # Create a DataFrame for prediction
        input_data = {
            'Symptoms': [transformed_symptoms],
            'Causes': [transformed_causes],
            'Disease': [transformed_disease]
        }
        input_df = pd.DataFrame(input_data)
        
        # Predict with the classifier
        predicted_medicine_encoded = chatbot.rf_classifier.predict(input_df)
        
        # Inverse transform to get original medicine name
        predicted_medicine = chatbot.label_encoders['Medicine'].inverse_transform(predicted_medicine_encoded)
        
        return f"Predicted Medicine: {predicted_medicine[0]}"

    except KeyError as e:
        return f"Invalid input: {e}. Please provide different symptoms, causes, or disease.", False

# Example usage
if __name__ == "__main__":
    # Assume `chatbot` has attributes `label_encoders` and `rf_classifier` initialized
    medical_data, label_encoders, rf_classifier = load_and_preprocess_medical_data()
    chatbot = {
        'label_encoders': label_encoders,
        'rf_classifier': rf_classifier,
        'recognizer': None,  # Your recognizer initialization
        'microphone': None   # Your microphone initialization
    }
    response, _ = inquire_about_health(chatbot, 'voice')
    print("Chatbot:", response)
