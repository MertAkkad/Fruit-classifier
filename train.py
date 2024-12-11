import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import matplotlib.pyplot as plt

# Constants
DATASET_PATH = "dataset/train"
IMAGE_SIZE = 224
BATCH_SIZE = 40
EPOCHS = 10
NUM_CLASSES = 9

class FruitClassifier:
    def __init__(self):
        self.model = None
        self.class_names = ['apple fruit', 'banana fruit', 'cherry fruit', 'chickoo fruit', 'grapes fruit', 'kiwi fruit', 'mango fruit', 'orange fruit', 'strawberry fruit'] 

    def create_model(self):
        """Creates a CNN model using transfer learning"""
        # Use MobileNetV2 as the base model
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
            include_top=False,
            weights='imagenet'
        )
        base_model.trainable = False  # Freeze the base model

        # Build the model
        self.model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(NUM_CLASSES, activation='softmax')
        ])

        # Compile the model
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

    def prepare_dataset(self):
        """Prepares the dataset and applies data augmentation"""
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

        # Training data
        train_generator = train_datagen.flow_from_directory(
            DATASET_PATH,
            target_size=(IMAGE_SIZE, IMAGE_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='training'
        )

        # Validation data
        validation_generator = train_datagen.flow_from_directory(
            DATASET_PATH,
            target_size=(IMAGE_SIZE, IMAGE_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='validation'
        )

        return train_generator, validation_generator

    def train(self):
        """Trains and saves the model"""
        # Prepare the dataset
        train_generator, validation_generator = self.prepare_dataset()

        # Create the model
        self.create_model()

        # Training
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

        # Save the model
        os.makedirs('model', exist_ok=True)
        self.model.save('model/fruit_model2.h5')
        
        return history

    def plot_training_history(self, history):
        """Plots the training metrics"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Accuracy graph
        ax1.plot(history.history['accuracy'], label='Training')
        ax1.plot(history.history['val_accuracy'], label='Validation')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        
        # Loss graph
        ax2.plot(history.history['loss'], label='Training')
        ax2.plot(history.history['val_loss'], label='Validation')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        plt.close()

def main():
    # Dataset check
    if not os.path.exists(DATASET_PATH):
        print(f"Error: {DATASET_PATH} directory not found!")
        return

    # Model training
    classifier = FruitClassifier()
    history = classifier.train()
    classifier.plot_training_history(history)
    print("Model successfully trained and saved!")

if __name__ == "__main__":
    main()
