import tensorflow as tf
from models.vqa_model import build_vqa_model

def train_model():
    model = build_vqa_model()
    # Add your training logic here
    model.fit(...)

if __name__ == "__main__":
    train_model()
