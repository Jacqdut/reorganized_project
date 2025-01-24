import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Embedding, LSTM, Concatenate, Dropout
from tensorflow.keras.regularizers import l2


def build_vqa_model(image_input_shape, vocab_size, question_max_len, num_classes):
    # Image feature input
    image_input = Input(shape=image_input_shape, name="image_input")
    image_dense = Dense(64, activation="relu", kernel_regularizer=l2(0.01))(image_input)
    image_dense = Dropout(0.5)(image_dense)

    # Question input
    question_input = Input(shape=(question_max_len,), name="question_input")
    question_embedding = Embedding(input_dim=vocab_size, output_dim=64)(question_input)
    question_lstm = LSTM(64, kernel_regularizer=l2(0.01))(question_embedding)
    question_lstm = Dropout(0.5)(question_lstm)

    # Concatenate image and question features
    combined = Concatenate()([image_dense, question_lstm])
    combined_dense = Dense(64, activation="relu", kernel_regularizer=l2(0.01))(combined)
    combined_dense = Dropout(0.5)(combined_dense)
    output = Dense(num_classes, activation="softmax")(combined_dense)

    model = Model(inputs=[image_input, question_input], outputs=output)
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    return model
