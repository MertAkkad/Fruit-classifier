import unittest
from app import app
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import io

class FruitClassifierTest(unittest.TestCase):
    def setUp(self):
        """Test öncesi hazırlıklar"""
        self.app = app.test_client()
        self.app.testing = True
        ##self.test_image_dir = 'dataset/test/Apple'
        
    def test_home_page(self):
        """Ana sayfa testi"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_predict_without_file(self):
        """Dosya olmadan tahmin testi"""
        response = self.app.post('/predict')
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.json)
        
    def test_predict_with_invalid_file(self):
        """Geçersiz dosya ile tahmin testi"""
        data = {'file': (io.BytesIO(b"invalid data"), 'test.jpg')}
        response = self.app.post('/predict', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.json)
    # def test_images(self):
    #     """Tüm görüntüleri test et"""
    #     for filename in os.listdir(self.test_image_dir):
    #         if filename.endswith(('.png', '.jpg', '.jpeg')):  # Desteklenen dosya uzantıları
    #             test_image_path = os.path.join(self.test_image_dir, filename)
    #             with open(test_image_path, 'rb') as img:
    #                 data = {'file': (img, filename)}
    #                 response = self.app.post('/predict', data=data)

    #             self.assertEqual(response.status_code, 200)
    #             self.assertIn('class', response.json)
    #             self.assertIn('confidence', response.json)
    #             self.assertIn('image_path', response.json)
        
    def test_predict_with_valid_image(self):
                """Geçerli görüntü ile tahmin testi"""
                # Test görüntüsünü yükle
                test_image_path = 'dataset/test/Apple/Apple (1976).jpeg'
                if not os.path.exists(test_image_path):
                    self.skipTest("Test görüntüsü bulunamadı")
                    
                with open(test_image_path, 'rb') as img:
                    data = {'file': (img, 'Apple(1976)')}
                    response = self.app.post('/predict', data=data)
                    
                self.assertEqual(response.status_code, 200)
                self.assertIn('class', response.json)
                self.assertIn('confidence', response.json)
                self.assertIn('image_path', response.json)

        
    def test_model_loading(self):
        """Model yükleme testi"""
        model_path = 'model/fruit_model.h5'
        self.assertTrue(os.path.exists(model_path))
        try:
            model = tf.keras.models.load_model(model_path)
            self.assertIsNotNone(model)
        except Exception as e:
            self.fail(f"Model yüklenemedi: {str(e)}")

if __name__ == '__main__':
    unittest.main()
