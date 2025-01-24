import json
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.utils import class_weight

def load_vqa_data(data_path):
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    image_features = []
    questions = []
    answers = []

    for item in data:
        if len(item['image_features']) != 2048:
            raise ValueError(f"Invalid shape for image_features: {len(item['image_features'])}, expected 2048")
        image_features.append(item['image_features'])
        questions.append(item['question'])
        answers.append(item['answer'])

    return np.array(image_features), questions, answers

def preprocess_questions(questions, tokenizer, max_len=20):
    sequences = tokenizer.texts_to_sequences(questions)
    padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')
    return padded_sequences

def preprocess_answers(answers):
    encoder = LabelEncoder()
    encoded_answers = encoder.fit_transform(answers)
    return encoded_answers, encoder.classes_

def compute_class_weights(labels):
    class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(labels), y=labels)
    return dict(enumerate(class_weights))

def normalize_image_features(image_features):
    scaler = StandardScaler()
    return scaler.fit_transform(image_features)

def split_data(image_features, question_sequences, encoded_answers):
    return train_test_split(image_features, question_sequences, encoded_answers, test_size=0.2, random_state=42)
