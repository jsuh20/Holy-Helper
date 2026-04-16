from flask import Flask, request, jsonify
from flask_cors import CORS

import cv2, numpy as np, torch
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
sys.path.insert(0, PARENT_DIR)

from Emotion_ML_Model.deep_emotion import Deep_Emotion

app = Flask(__name__)
CORS(app)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_PATH = os.path.join(BASE_DIR, "..", "Emotion_ML_Model", "deep_emotion-100-128-0.005.pt")

model = Deep_Emotion()
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu", weights_only=True))
model.eval()

@app.post("/predict")
def predict():
    file = request.files["image"]
    nparr = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (48, 48))
    tensor = torch.tensor(resized).float().unsqueeze(0).unsqueeze(0) / 255.

    with torch.no_grad():
        output = model(tensor)
        emotion_idx = torch.argmax(output).item()
    
    emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    prompt = "I am feeling " + emotions[emotion_idx] + " right now. Can you give me a random bible verse (like the line and which chaper+verse) related to this? Give me only the bible verse, nothing else, none of you input or thoughts."

    model_genai = genai.GenerativeModel('gemini-2.5-flash')
    response = model_genai.generate_content(prompt)
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    return jsonify({
        "emotion": emotions[emotion_idx],
        "bible_verse": response.text
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)