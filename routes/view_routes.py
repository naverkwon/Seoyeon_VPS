
from flask import Blueprint, render_template, send_from_directory, current_app
import os
from lora_system.lora_manager import CHARACTER_PROFILES
from lora_system.data.constants import HAIR_STYLES, LOCATIONS, POSES, TOPS, BOTTOMS, OUTERWEAR, FULL_BODY

view_bp = Blueprint('view', __name__)

@view_bp.route('/')
def home():
    # Pass dynamic lists to template for Builder Mode
    return render_template('lora_studio.html', 
                           characters=CHARACTER_PROFILES,
                           hair_styles=HAIR_STYLES,
                           locations=LOCATIONS,
                           poses=POSES,
                           tops=TOPS,
                           bottoms=BOTTOMS,
                           outerwear=OUTERWEAR
                           )

@view_bp.route('/generated_images/<filename>')
def serve_generated_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'generated_images'), filename)

@view_bp.route('/static/images/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'static', 'images'), filename)
