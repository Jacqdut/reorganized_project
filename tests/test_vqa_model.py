import os
import sys
import unittest
import numpy as np
import tensorflow as tf
from tensorflow import keras

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print("Python Path:", sys.path)  # Print the Python path for debugging

from scripts.vqa_model import build_vqa_model, save_model_weights, load_model_weights


class TestVQAModel(unittest.TestCase):
    def test_model_structure(self):
        model = build_vqa_model()
        expected_layer_count = (
            7  # Update this to match the actual number of layers in the model
        )
        self.assertEqual(len(model.layers), expected_layer_count)

    def test_model_output_shape(self):
        model = build_vqa_model()
        num_classes = 1000  # Number of classes in the output layer
        # Create example inputs with the correct shape
        example_image_input = np.random.random(
            (1, 2048)
        )  # Example image feature vector
        example_question_input = np.random.randint(
            10000, size=(1, 10)
        )  # Example question tensor
        output = model.predict([example_image_input, example_question_input])
        expected_output_shape = (1, num_classes)  # Adjust based on your model
        self.assertEqual(output.shape, expected_output_shape)

    def test_model_training(self):
        model = build_vqa_model()
        num_classes = 1000  # Define the number of classes here
        # Example training data
        example_image_input = np.random.random(
            (10, 2048)
        )  # Batch of 10 image feature vectors
        example_question_input = np.random.randint(
            10000, size=(10, 10)
        )  # Batch of 10 question tensors
        example_labels = np.eye(num_classes)[
            np.random.choice(num_classes, 10)
        ]  # One-hot encoded labels

        model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )

        # Increase the number of epochs to give the model more time to learn
        history = model.fit(
            [example_image_input, example_question_input],
            example_labels,
            epochs=5,
            verbose=1,
        )

        # Check if training accuracy is greater than 0
        self.assertGreater(history.history["accuracy"][-1], 0)

    def test_model_evaluation(self):
        model = build_vqa_model()
        num_classes = 1000  # Define the number of classes here
        # Example evaluation data
        example_image_input = np.random.random(
            (10, 2048)
        )  # Batch of 10 image feature vectors
        example_question_input = np.random.randint(
            10000, size=(10, 10)
        )  # Batch of 10 question tensors
        example_labels = np.eye(num_classes)[
            np.random.choice(num_classes, 10)
        ]  # One-hot encoded labels

        model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )

        # Train the model before evaluation
        model.fit(
            [example_image_input, example_question_input],
            example_labels,
            epochs=5,
            verbose=1,
        )

        # Perform evaluation
        loss, accuracy = model.evaluate(
            [example_image_input, example_question_input], example_labels
        )
        print(f"Evaluation loss: {loss}, accuracy: {accuracy}")
        self.assertGreater(
            accuracy, 0
        )  # Check if evaluation accuracy is greater than 0

    def test_model_prediction(self):
        model = build_vqa_model()
        num_classes = 1000  # Define the number of classes here
        # Example prediction data
        example_image_input = np.random.random((1, 2048))  # Single image feature vector
        example_question_input = np.random.randint(
            10000, size=(1, 10)
        )  # Single question tensor

        model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )

        # Perform prediction
        predictions = model.predict([example_image_input, example_question_input])
        self.assertEqual(
            predictions.shape, (1, num_classes)
        )  # Check if prediction shape is correct

    def test_model_save_and_load(self):
        model = build_vqa_model()
        num_classes = 1000  # Define the number of classes here
        # Example training data
        example_image_input = np.random.random(
            (10, 2048)
        )  # Batch of 10 image feature vectors
        example_question_input = np.random.randint(
            10000, size=(10, 10)
        )  # Batch of 10 question tensors
        example_labels = np.eye(num_classes)[
            np.random.choice(num_classes, 10)
        ]  # One-hot encoded labels

        model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )

        # Train the model before saving
        model.fit(
            [example_image_input, example_question_input],
            example_labels,
            epochs=5,
            verbose=1,
        )

        # Use a simplified absolute path for saving the model
        save_path = os.path.join(
            "/home/jacqdut/reorganized_project/", "vqa_model.keras"
        )

        # Ensure the directory exists
        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory)
        else:
            print(f"Directory already exists: {directory}")

        # Verify the directory exists
        print(f"Directory exists: {os.path.exists(directory)}")

        # Check if the directory is writable
        if os.access(directory, os.W_OK):
            print(f"Directory is writable: {directory}")
        else:
            print(f"Directory is not writable: {directory}")

        # Try writing a test file to the directory
        test_file_path = os.path.join(directory, "test_file.txt")
        try:
            with open(test_file_path, "w") as f:
                f.write("Test file content")
            print(f"Successfully wrote test file: {test_file_path}")
            os.remove(test_file_path)
        except Exception as e:
            print(f"Failed to write test file: {e}")

        # Print the save path for debugging
        print(f"Model save path: {save_path}")

        # Save the model
        model.save(save_path)  # Use the recommended .keras format

        # Load the model
        loaded_model = keras.models.load_model(save_path)

        # Perform evaluation on the loaded model
        loss, accuracy = loaded_model.evaluate(
            [example_image_input, example_question_input], example_labels
        )
        print(f"Loaded model evaluation loss: {loss}, accuracy: {accuracy}")
        self.assertGreater(
            accuracy, 0
        )  # Check if evaluation accuracy is greater than 0

    def test_model_save_and_load_weights(self):
        model = build_vqa_model()
        num_classes = 1000
        example_image_input = np.random.random((10, 2048))
        example_question_input = np.random.randint(10000, size=(10, 10))
        example_labels = np.eye(num_classes)[np.random.choice(num_classes, 10)]

        model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )
        model.fit(
            [example_image_input, example_question_input],
            example_labels,
            epochs=5,
            verbose=1,
        )

        weights_path = os.path.join(
            "/home/jacqdut/reorganized_project/", "vqa_model_weights.weights.h5"
        )

        # Save the model weights
        save_model_weights(model, weights_path)

        # Create a new model instance and load the weights
        new_model = build_vqa_model()
        new_model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )
        load_model_weights(new_model, weights_path)

        # Evaluate the loaded model
        loss, accuracy = new_model.evaluate(
            [example_image_input, example_question_input], example_labels
        )
        print(f"Loaded model weights evaluation loss: {loss}, accuracy: {accuracy}")
        self.assertGreater(accuracy, 0)


if __name__ == "__main__":
    unittest.main()
