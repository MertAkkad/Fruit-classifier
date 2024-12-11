from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Model and classes
MODEL_PATH = 'model/fruit_model2.h5'
CLASSES = ['apple', 'banana', 'cherry', 'chickoo', 'grape', 'kiwi', 'mango', 'orange', 'strawberry']

class FruitClassifierApp:
    def __init__(self):
        self.model = tf.keras.models.load_model(MODEL_PATH)

    def preprocess_image(self, image_path):
        """Prepares the image for the model"""
        img = Image.open(image_path)
        img = img.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        img_array = img_array / 255.0
        return img_array

    def predict(self, image_path):
        """Performs image classification"""
        img_array = self.preprocess_image(image_path)
        predictions = self.model.predict(img_array)
        predicted_class = CLASSES[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))
        return predicted_class, confidence

# Create an instance of the application
classifier = FruitClassifierApp()

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction API"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    try:
        # Save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Make a prediction
        predicted_class, confidence = classifier.predict(filepath)
        
        return jsonify({
            'class': predicted_class,
            'confidence': confidence,
            'image_path': filepath
        })
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
