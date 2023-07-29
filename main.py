from flask import Flask, request, send_file
import os
import uuid
from werkzeug.utils import secure_filename
from add_subtitles_to_video import add_subtitles_to_video

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    # Get the uploaded file from the request
    video_file = request.files['video_file']
    # Save the file to a temporary directory
    filename = secure_filename(video_file.filename)
    tmp_file = os.path.join('/tmp', str(uuid.uuid4()), filename)
    os.makedirs(os.path.dirname(tmp_file), exist_ok=True)
    video_file.save(tmp_file)
    # Call the Python script to add subtitles to the video
    output_file = os.path.join('/tmp', str(uuid.uuid4()), 'output.mp4')
    add_subtitles_to_video(tmp_file, output_file)
    # Return the output file for download
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
