
from flask import Flask
import os
import sys
from dotenv import load_dotenv

# Load env
load_dotenv()
sys.path.append(os.getcwd())

from routes.api_routes import api_bp
from routes.view_routes import view_bp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'images')
app.config['GENERATED_FOLDER'] = os.path.join(os.getcwd(), 'generated_images')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

# Register Blueprints
app.register_blueprint(view_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    print("🚀 LoRA Studio Starting on http://localhost:5002")
    app.run(host='0.0.0.0', port=5002, debug=False, threaded=True)
