from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import json
import csv
from datetime import datetime

app = Flask(__name__)

# Constants
IMAGE_DIR = os.path.join(os.getcwd(), 'generated_images')
UPLOAD_DIR = os.path.join(os.getcwd(), 'user_uploads')
LOG_FILE = 'conversation_log.csv'
STATUS_FILE = 'status.json'
GALLERY_METADATA_FILE = 'gallery_metadata.json'

@app.route('/')
def index():
    # 1. Load Status
    status = {"activity": "Unknown", "updated": "N/A"}
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                status = json.load(f)
        except:
            pass

    # 2. Load Recent Logs (Last 5)
    recent_logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            reader = list(csv.reader(f))
            if len(reader) > 1:
                recent_logs = reader[-5:][::-1] # Reverse order

    # 3. Recent Images (Last 4)
    images = []
    if os.path.exists(IMAGE_DIR):
        files = sorted(os.listdir(IMAGE_DIR), key=lambda x: os.path.getmtime(os.path.join(IMAGE_DIR, x)), reverse=True)
        images = files[:4]

    return render_template('index.html', status=status, recent_logs=recent_logs, images=images)

@app.route('/gallery')
def gallery():
    images = []
    metadata = {}
    
    if os.path.exists(IMAGE_DIR):
        files = sorted(os.listdir(IMAGE_DIR), key=lambda x: os.path.getmtime(os.path.join(IMAGE_DIR, x)), reverse=True)
        images = files
        
    if os.path.exists(GALLERY_METADATA_FILE):
        try:
            with open(GALLERY_METADATA_FILE, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        except:
            pass
            
    return render_template('gallery.html', images=images, metadata=metadata)

@app.route('/api/delete_image', methods=['POST'])
def delete_image():
    try:
        data = request.json
        filename = data.get('filename')
        
        if not filename:
             return jsonify({"success": False, "error": "No filename provided"}), 400

        # Security: Simple check
        if ".." in filename or "/" in filename:
             return jsonify({"success": False, "error": "Invalid filename"}), 400
             
        # 1. Delete File
        filepath = os.path.join(IMAGE_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            
        # 2. Update Metadata
        if os.path.exists(GALLERY_METADATA_FILE):
            try:
                with open(GALLERY_METADATA_FILE, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                if filename in metadata:
                    del metadata[filename]
                    
                    with open(GALLERY_METADATA_FILE, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Metadata cleanup error: {e}")
                
        return jsonify({"success": True})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/logs')
def logs():
    full_logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            reader = list(csv.reader(f))
            if len(reader) > 1:
                full_logs = reader[1:][::-1] # Skip header, reverse
    return render_template('logs.html', logs=full_logs)

@app.route('/image/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
