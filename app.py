from flask import Flask, render_template, request, redirect, url_for, Response
import os
import cv2

app = Flask(__name__)

video_path = None  # Global variable to store the video path

# Mocked object detection results (replace with actual YOLO logic)
def detect_objects(frame):
    # Implement object detection logic using YOLO
    # Mocked results: Assume you have the counts for each class
    counts = {'can': 10, 'HDPE': 5, 'PET_Bottle': 8, 'Tetrapak': 3, 'Plastic_wrapper': 6}

    # Display counts on the frame
    for i, (label, count) in enumerate(counts.items()):
        cv2.putText(frame, f"{label}: {count}", (10, 450 + 30 * i), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return frame

# Video stream generator
def generate():
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Resize the frame for better visualization
        frame = cv2.resize(frame, (800, 600))

        # Perform object detection
        processed_frame = detect_objects(frame)

        _, jpeg = cv2.imencode('.jpg', processed_frame)
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html', video_path=video_path)

# Route for video streaming
@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for uploading video
@app.route('/upload', methods=['POST'])
def upload():
    global video_path

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        video_path = os.path.join('static', 'uploads', file.filename)
        file.save(video_path)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
