from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to save uploaded files
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mkv'}  # Allowed file extensions for videos