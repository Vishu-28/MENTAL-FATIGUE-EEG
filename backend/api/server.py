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


# -------------------------------
# Paths
# -------------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

dataset_path = os.path.join(BASE_DIR, "dataset", "emotions.xlsx")

frontend_path = os.path.join(BASE_DIR, "backend", "frontend", "dist")


# -------------------------------
# Flask App
# -------------------------------

app = Flask(__name__, static_folder=frontend_path, static_url_path="/")
CORS(app)


# -------------------------------
# Load Components
# -------------------------------

dataset = EEGDataset(dataset_path)
emotion_model = EmotionModel()
history = EmotionHistory()


# -------------------------------
# API Endpoint
# -------------------------------

@app.route("/api/eeg")
def get_eeg_data():
    try:

        sample = dataset.get_sample()
        sample = np.array(sample)

        # remove label column
        features = sample[:-1].reshape(1, -1)

        # predict emotion
        emotion = emotion_model.predict(features)

        history.add(int(emotion))

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

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------
# React Frontend
# -------------------------------

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return send_from_directory(app.static_folder, "index.html")


# -------------------------------
# Run Server
# -------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)