import unittest
from app import app
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import io

class FruitClassifierTest(unittest.TestCase):
    def setUp(self):
        """Setup before tests"""
        self.app = app.test_client()
        self.app.testing = True
        ##self.test_image_dir = 'dataset/test/Apple'
        
    def test_home_page(self):
        """Homepage test"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_predict_without_file(self):
        """Prediction test without file"""
        response = self.app.post('/predict')
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.json)
        
    def test_predict_with_invalid_file(self):
        """Prediction test with invalid file"""
        data = {'file': (io.BytesIO(b"invalid data"), 'test.jpg')}
        response = self.app.post('/predict', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.json)
    # def test_images(self):
    #     """Test all images"""
    #     for filename in os.listdir(self.test_image_dir):
    #         if filename.endswith(('.png', '.jpg', '.jpeg')):  # Supported file extensions
    #             test_image_path = os.path.join(self.test_image_dir, filename)
    #             with open(test_image_path, 'rb') as img:
    #                 data = {'file': (img, filename)}
    #                 response = self.app.post('/predict', data=data)
    #
    #             self.assertEqual(response.status_code, 200)
    #             self.assertIn('class', response.json)
    #             self.assertIn('confidence', response.json)
    #             self.assertIn('image_path', response.json)

        
    def test_predict_with_valid_image(self):
        """Prediction test with valid image"""
        # Load test image
        test_image_path = 'dataset/test/Apple/Apple (1976).jpeg'
        if not os.path.exists(test_image_path):
            self.skipTest("Test image not found")
            
        with open(test_image_path, 'rb') as img:
            data = {'file': (img, 'Apple(1976)')}
            response = self.app.post('/predict', data=data)
            
        self.assertEqual(response.status_code, 200)
        self.assertIn('class', response.json)
        self.assertIn('confidence', response.json)
        self.assertIn('image_path', response.json)

    def test_model_loading(self):
        """Model loading test"""
        model_path = 'model/fruit_model.h5'
        self.assertTrue(os.path.exists(model_path))
        try:
            model = tf.keras.models.load_model(model_path)
            self.assertIsNotNone(model)
        except Exception as e:
            self.fail(f"Model could not be loaded: {str(e)}")

if __name__ == '__main__':
    unittest.main()