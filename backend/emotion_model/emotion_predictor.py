import pickle
import os

class EmotionModel:

    def __init__(self):

        # find the directory of this file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # construct full path to model
        model_path = os.path.join(current_dir, "emotion_model.pkl")

        # load model
        self.model = pickle.load(open(model_path, "rb"))

    def predict(self, features):

        return self.model.predict([features])[0]