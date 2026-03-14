from acquisition.dataset_loader import EEGDataset
from emotion_model.emotion_predictor import EmotionModel
from temporal_analysis.emotion_tracker import EmotionHistory
from temporal_analysis.drift_metrics import drift_score
from fatigue_index.mfbi_calculator import compute_mfbi
from recommendations.exercise_engine import recommend

import numpy as np
import time


# Load dataset
dataset = EEGDataset("../dataset/emotions.xlsx")

# Load trained model
emotion_model = EmotionModel()

# Emotion history tracker
history = EmotionHistory()


while True:

    # Get next row from dataset
    sample = dataset.get_sample()

    # Convert to numpy
    sample = np.array(sample)

    # Features = all columns except last (label)
    features = sample[:-1]

    # Predict emotion
    emotion = emotion_model.predict(features)

    # Track emotion timeline
    history.add(emotion)

    # Calculate emotion drift
    drift = drift_score(history.timeline)

    # Simple fatigue estimation
    fatigue, score = compute_mfbi(
        np.mean(features),
        np.std(features),
        np.max(features),
        drift
    )

    # Exercise recommendation
    exercise = recommend(fatigue)

    print("\n----------------------------")
    print("Predicted Emotion:", emotion)
    print("Fatigue Level:", fatigue)
    print("Recommended Exercise:", exercise)

    time.sleep(1)