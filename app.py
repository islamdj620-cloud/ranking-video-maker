import os
import uuid
from flask import Flask, request, jsonify, send_file
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, concatenate_videoclips
from gtts import gTTS

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
        if not data or 'items' not in data:
            return jsonify({"error": "No items provided"}), 400
        
        items = data.get('items', [])
        video_filename = f"{uuid.uuid4()}.mp4"
        audio_filename = f"{uuid.uuid4()}.mp3"
        
        # 1. إنشاء الصوت باستخدام gTTS
        full_text = " . ".join(items)
        tts = gTTS(text=full_text, lang='en')
        tts.save(audio_filename)

        # 2. إنشاء مقاطع الفيديو
        clips = []
        # إنشاء خلفية سوداء
        background = ColorClip(size=VIDEO_SIZE, color=(0, 0, 0)).set_duration(3 * len(items))
        
        for i, item in enumerate(items):
            # إنشاء نص لكل عنصر في القائمة
            txt_clip = TextClip(f"Rank {i + 1}: {item}", fontsize=70, color='white', size=VIDEO_SIZE)
            txt_clip = txt_clip.set_start(i * 3).set_duration(3).set_position('center')
            clips.append(txt_clip)

        # 3. دمج الفيديو النهائي
        final_video = CompositeVideoClip([background] + clips)
        final_video = final_video.set_audio(audio_filename)
        
        # كتابة ملف الفيديو
        output_path = os.path.join("/tmp", video_filename) # استخدام المجلد المؤقت في Render
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=FPS)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        # هذا هو الجزء الذي كان ينقصك في الصورة الأخيرة
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
