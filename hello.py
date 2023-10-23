from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DETECTION_URL = 'https://inf-1b8785d9-8b32-4db1-a6f4-581f9de7cde8-no4xvrhsfq-uc.a.run.app/detect'  # Replace with your model's URL

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>License Plate Detection</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f0f0f0;
                display: flex;
                flex-direction: column;
                align-items: center;
                height: 100vh;
            }
            h1 {
                color: #007BFF;
            }
            .form-container {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 0px 10px #999;
                max-width: 400px;
                text-align: center;
            }
            label {
                display: block;
                margin-bottom: 10px;
                font-weight: bold;
                color: #333;
            }
            input[type="file"] {
                display: block;
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
            }
            button {
                background-color: #007BFF;
                color: #fff;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 20px;
            }
            button:hover {
                background-color: #0056b3;
            }
            #detection-results {
                margin-top: 20px;
                white-space: pre;
                color: #333;
            }
            .image-preview {
                width: 100%;
                max-width: 400px;
                display: none;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>License Plate Detection</h1>

        <div class="form-container">
            <label for="image-upload">Select an image for license plate detection:</label>
            <input type="file" id="image-upload" accept="image/*">
            <button type="button" id="detect-button">Detect License Plates</button>
        </div>

        <div class="image-preview">
            <img id="uploaded-image" src="" alt="Uploaded Image">
        </div>

        <div id="detection-results">
            <!-- Results will be displayed here -->
        </div>

        <button type="button" id="reset-button" style="display: none;">Reset</button>

        <script>
            document.getElementById('detect-button').addEventListener('click', function() {
                const fileInput = document.getElementById('image-upload');
                const formData = new FormData();
                formData.append('image', fileInput.files[0]);

                fetch('/detect', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    const resultsContainer = document.getElementById('detection-results');
                    resultsContainer.textContent = '';

                    if (data.length > 0) {
                        const result = data[0];
                        const imagePreview = document.getElementById('uploaded-image');
                        const canvas = document.createElement('canvas');
                        canvas.width = imagePreview.width;
                        canvas.height = imagePreview.height;
                        const context = canvas.getContext('2d');

                        context.drawImage(imagePreview, 0, 0, canvas.width, canvas.height);

                        const x = result.x;
                        const y = result.y;
                        const width = result.width;
                        const height = result.height;

                        context.strokeStyle = '#00ffcc';
                        context.lineWidth = 2;
                        context.strokeRect(x, y, width, height);

                        imagePreview.parentNode.replaceChild(canvas, imagePreview);

                        // Show the reset button
                        const resetButton = document.getElementById('reset-button');
                        resetButton.style.display = 'block';
                    } else {
                        resultsContainer.textContent = 'No license plates found.';
                    }
                })
                .catch(error => {
                    resultsContainer.textContent = 'Error occurred: ' + error.message;
                });
            });

            document.getElementById('reset-button').addEventListener('click', function() {
                location.reload();
            });

            document.getElementById('image-upload').addEventListener('change', function() {
                const imagePreview = document.querySelector('.image-preview');
                const uploadedImage = document.getElementById('uploaded-image');
                const file = this files[0];
                const reader = new FileReader();

                reader.onload = function(e) {
                    uploadedImage.src = e.target.result;
                    imagePreview.style.display = 'block';
                };

                reader.readAsDataURL(file);
            });
        </script>
    </body>
    </html>
    '''

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
