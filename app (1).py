from flask import Flask, request, jsonify, send_file
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    concatenate_audioclips,
    CompositeVideoClip,
    ColorClip,
    ImageClip,
    concatenate_videoclips,
)
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import tempfile
import os
import uuid
import textwrap
import shutil

app = Flask(__name__)

# Target vertical size (9:16)
VIDEO_SIZE = (720, 1280)
FPS = 24


def render_text_image(text, size, font_path=None, fontsize=70):
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font_path, fontsize) if font_path else ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    draw.text((size[0]//2, size[1]//2), text, font=font, fill="white", anchor="mm")
    return image
