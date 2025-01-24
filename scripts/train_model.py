import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from scripts.vqa_model import build_vqa_model
from scripts.data_processing import load_vqa_data, preprocess_questions, preprocess_answers, compute_class_weights, normalize_image_features, split_data

# Load data
data_path = '/home/jacqdut/reorganized_project/data/vqa_data.json'
image_features, questions, answers = load_vqa_data(data_path)

# Normalize image features
image_features = normalize_image_features(image_features)

# Preprocess questions and answers
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(questions)
question_sequences = preprocess_questions(questions, tokenizer)
encoded_answers, answer_classes = preprocess_answers(answers)
num_classes = len(answer_classes)

# Compute class weights
class_weights = compute_class_weights(encoded_answers)

# Split data
X_train_img, X_val_img, X_train_q, X_val_q, y_train, y_val = split_data(image_features, question_sequences, encoded_answers)

# Build and compile model
model = build_vqa_model(image_features.shape[1:], tokenizer.num_words, question_sequences.shape[1], num_classes)

# Define callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.0001)
model_checkpoint = ModelCheckpoint('/home/jacqdut/reorganized_project/vqa_model_best.keras', save_best_only=True, monitor='val_loss')

# Train the model
model.fit(
    [X_train_img, X_train_q], y_train, 
    epochs=100, batch_size=64, validation_data=([X_val_img, X_val_q], y_val),
    class_weight=class_weights,
    callbacks=[early_stopping, reduce_lr, model_checkpoint]
)

# Save the final model
model.save('/home/jacqdut/reorganized_project/vqa_model_final.keras')
