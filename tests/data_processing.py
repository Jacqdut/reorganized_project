import json
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences


def load_vqa_data(data_path):
    with open(data_path, "r") as f:
        data = json.load(f)

    image_features = []
    questions = []
    answers = []

    for item in data:
        if len(item["image_features"]) != 2048:
            raise ValueError(
                f"Invalid shape for image_features: {len(item['image_features'])}, expected 2048"
            )
        image_features.append(item["image_features"])
        questions.append(item["question"])
        answers.append(item["answer"])

    return np.array(image_features), questions, answers


def preprocess_questions(questions, tokenizer, max_len=20):
    sequences = tokenizer.texts_to_sequences(questions)
    padded_sequences = pad_sequences(sequences, maxlen=max_len, padding="post")
    return padded_sequences


def preprocess_answers(answers, num_classes):
    labels = np.zeros((len(answers), num_classes))
    for idx, answer in enumerate(answers):
        labels[idx, answer] = 1  # Assuming answers are already encoded as integers
    return labels
