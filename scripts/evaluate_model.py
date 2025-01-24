import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from scripts.data_processing import load_vqa_data, preprocess_questions, preprocess_answers

# Load data
data_path = '/home/jacqdut/reorganized_project/data/vqa_data.json'  # Update this path
image_features, questions, answers = load_vqa_data(data_path)

# Preprocess questions and answers
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(questions)
question_sequences = preprocess_questions(questions, tokenizer)
num_classes = 1000  # Define the number of classes for your problem
answer_labels = preprocess_answers(answers, num_classes)

# Load the model
model = load_model('/home/jacqdut/reorganized_project/vqa_model_final.keras')

# Evaluate the model
loss, accuracy = model.evaluate([image_features, question_sequences], answer_labels)
print(f"Evaluation loss: {loss}, accuracy: {accuracy}")
