import os
from flask import Flask, request, jsonify, send_file
from moviepy.editor import TextClip, ColorClip, concatenate_videoclips, CompositeVideoClip
from gtts import gTTS
import uuid

app = Flask(__name__)

# إعدادات الفيديو
VIDEO_SIZE = (720, 1280)
FPS = 24

@app.route('/')
def home():
    return "<h1>Ranking Video Generator is Online!</h1>"

@app.route('/generate', methods=['POST'])
def generate_video():
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        if not items:
            return jsonify({"error": "No items provided"}), 400

        video_filename = f"{uuid.uuid4()}.mp4"
        audio_filename = f"{uuid.uuid4()}.mp3"
        
        # 1. إنشاء الصوت
        full_text = " . ".join(items)
        tts = gTTS(text=full_text, lang='en')
        tts.save(audio_filename)

        # 2. إنشاء مقاطع الفيديو لكل عنصر
        clips = []
        background = ColorClip(size=VIDEO_SIZE, color=(0, 0, 0)).set_duration(3 * len(items))
