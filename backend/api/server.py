import sys
import os

# allow imports from backend folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np

from acquisition.dataset_loader import EEGDataset
from emotion_model.emotion_predictor import EmotionModel
from temporal_analysis.emotion_tracker import EmotionHistory
from temporal_analysis.drift_metrics import drift_score
from fatigue_index.mfbi_calculator import compute_mfbi
from recommendations.exercise_engine import recommend

# path to frontend build folder (created during Render build)
frontend_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
    "../../frontend/dist")
)

app = Flask(__name__, static_folder=frontend_path, static_url_path="/")
CORS(app)

dataset = EEGDataset("../../dataset/emotions.xlsx")
emotion_model = EmotionModel()
history = EmotionHistory()


@app.route("/api/eeg")
def get_eeg_data():

    sample = dataset.get_sample()
    sample = np.array(sample)

    features = sample[:-1]

    emotion = emotion_model.predict(features)

    history.add(emotion)

    drift = drift_score(history.timeline)

    fatigue, score = compute_mfbi(
        np.mean(features),
        np.std(features),
        np.max(features),
        drift
    )

    exercise = recommend(fatigue)

    return jsonify({
        "emotion": int(emotion),
        "fatigue_level": fatigue,
        "fatigue_score": float(score),
        "drift": int(drift),
        "exercise": exercise
    })


# serve React dashboard
@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")


# Render uses dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)