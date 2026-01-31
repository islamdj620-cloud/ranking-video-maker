from flask import Flask, request, jsonify
from moviepy.editor import *
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json
    title = data['title']
    items = data['items']

    # Create a unique filename
    video_filename = f"video_{uuid.uuid4()}.mp4"
    audio_filename = f"audio_{uuid.uuid4()}.mp3"

    # Generate voiceover
    text = f"{title}. Top {len(items)} items. " + ', '.join(items)
    tts = gTTS(text=text, lang='en')
    tts.save(audio_filename)

    # Load background video or image
    background = VideoFileClip("background.mp4").resize(height=720)  # Ensure it fits a vertical format
    audio_clip = AudioFileClip(audio_filename)

    # Create video clips for each rank item
    clips = []
    for i, item in enumerate(items):
        txt_clip = TextClip(f"Rank {i + 1}: {item}", fontsize=70, color='white', bg_color='black', size=background.size)
        txt_clip = txt_clip.set_position('center').set_duration(3)  # Display each item for 3 seconds
        clips.append(txt_clip)

    # Concatenate clips
    video = concatenate_videoclips(clips)
    final_video = CompositeVideoClip([background, video.set_position("center")])
    final_video = final_video.set_audio(audio_clip)

    # Write the output video file
    final_video.write_videofile(video_filename, codec='libx264', audio_codec='aac')

    # Clean up the audio file
    os.remove(audio_filename)

    return jsonify({"video_url": video_filename})

if __name__ == '__main__':
    app.run(debug=True)
