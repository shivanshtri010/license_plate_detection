from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

DETECTION_URL = 'https://inf-1b8785d9-8b32-4db1-a6f4-581f9de7cde8-no4xvrhsfq-uc.a.run.app/detect'  # Replace with your model's URL

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_objects():
    image_file = request.files['image']
    if image_file:
        image_path = 'uploaded_image.jpg'
        image_file.save(image_path)

        data = request.form.to_dict()
        response = requests.post(DETECTION_URL, data=data, files={'image': open(image_path, 'rb')})

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to detect license plates'})

if __name__ == '__main__':
    app.run()
