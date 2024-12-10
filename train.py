import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import matplotlib.pyplot as plt

# Sabit değişkenler
DATASET_PATH = "dataset/train"
IMAGE_SIZE = 224
BATCH_SIZE = 40
EPOCHS = 10
NUM_CLASSES = 9  # Meyve sınıfı sayısı

class FruitClassifier:
    def __init__(self):
        self.model = None
        self.class_names = ['apple fruit', 'banana fruit', 'cherry fruit', 'chickoo fruit', 'grapes fruit', 'kiwi fruit', 'mango fruit', 'orange fruit', 'strawberry fruit'] 

    def create_model(self):
        """Transfer learning ile CNN modeli oluşturur"""
        # MobileNetV2'yi temel model olarak kullan
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
            include_top=False,
            weights='imagenet'
        )
        base_model.trainable = False  # Temel modeli dondur

        # Modeli oluştur
        self.model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(NUM_CLASSES, activation='softmax')
        ])

        # Modeli derle
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

    def prepare_dataset(self):
        """Veri setini hazırlar ve veri artırma uygular"""
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            validation_split=0.2
        )

        # Eğitim verisi
        train_generator = train_datagen.flow_from_directory(
            DATASET_PATH,
            target_size=(IMAGE_SIZE, IMAGE_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='training'
        )

        # Doğrulama verisi
        validation_generator = train_datagen.flow_from_directory(
            DATASET_PATH,
            target_size=(IMAGE_SIZE, IMAGE_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='validation'
        )

        return train_generator, validation_generator

    def train(self):
        """Modeli eğitir ve kaydeder"""
        # Veri setini hazırla
        train_generator, validation_generator = self.prepare_dataset()

        # Modeli oluştur
        self.create_model()

        # Eğitim
        history = self.model.fit(
            train_generator,
            epochs=EPOCHS,
            validation_data=validation_generator,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=3,
                    restore_best_weights=True
                )
            ]
        )

        # Modeli kaydet
        os.makedirs('model', exist_ok=True)
        self.model.save('model/fruit_model2.h5')
        
        return history

    def plot_training_history(self, history):
        """Eğitim metriklerinin grafiklerini çizer"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Doğruluk grafiği
        ax1.plot(history.history['accuracy'], label='Eğitim')
        ax1.plot(history.history['val_accuracy'], label='Doğrulama')
        ax1.set_title('Model Doğruluğu')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Doğruluk')
        ax1.legend()
        
        # Kayıp grafiği
        ax2.plot(history.history['loss'], label='Eğitim')
        ax2.plot(history.history['val_loss'], label='Doğrulama')
        ax2.set_title('Model Kaybı')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Kayıp')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        plt.close()

def main():
    # Veri seti kontrolü
    if not os.path.exists(DATASET_PATH):
        print(f"Hata: {DATASET_PATH} klasörü bulunamadı!")
        return

    # Model eğitimi
    classifier = FruitClassifier()
    history = classifier.train()
    classifier.plot_training_history(history)
    print("Model başarıyla eğitildi ve kaydedildi!")

if __name__ == "__main__":
    main()
