from flask import request, jsonify
from object_detect_track import video_tracking
from config import app, socketio
import os, json, cv2

customClsList = []

def generate_frames(clsList, path_x=''):
    for result, cls_dict in video_tracking(clsList, path_x):
        ref, buffer = cv2.imencode('.jpg', result)

        frame_bytes = buffer.tobytes()
        cls_json = json.dumps(cls_dict)

        yield (frame_bytes, cls_json)

# POST method to accept custom clsList
@app.route('/receive_list', methods=['POST'])
def receive_list():    
    recv_clsList = request.json.get('selectedClasses', [])
    global customClsList
    customClsList = recv_clsList

    return jsonify({'message': 'clsList sent successfully'}), 201

# POST method to accept video file and save it locally
@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'}), 201
    else:
        return jsonify({'error': 'Invalid file type'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_frames')
def handle_request_frames(path_x):
    for frame_bytes, cls_json in generate_frames(customClsList, path_x):
        socketio.emit('update_frame', {'frame': frame_bytes, 'cls': cls_json})


if __name__ == "__main__":
    socketio.run(app, debug=True)