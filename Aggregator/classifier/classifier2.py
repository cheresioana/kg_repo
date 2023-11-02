import pickle

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud

nltk.download('stopwords')

from classifier.utils import clean_text


class Classifier2:
    def __init__(self, num_words=10000, max_length=100, embedding_dim=128,
                 model_path='classifier/model', tokenizer_path='classifier/tokenizer.pkl',
                 label_encoder_path='classifier/label_encoder.pkl',
                 retrain=0):
        self.tokenizer = Tokenizer(num_words=num_words, oov_token="<OOV>")
        self.label_encoder = LabelEncoder()
        self.max_length = max_length
        self.embedding_dim = embedding_dim
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.label_encoder_path = label_encoder_path
        if retrain == 0 and os.path.exists(self.model_path):
            print("Loading saved model...")
            self.load_model()
            self.load_tokenizer()
            self.load_label_encoder()
        else:
            print("Initializing new model...")
            self.model = self.build_model(num_words, embedding_dim, max_length)

    def build_model(self, num_words, embedding_dim, max_length):
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(num_words, embedding_dim, input_length=max_length),
            #tf.keras.layers.LSTM(32),
            # tf.keras.layers.Dense(32, activation='relu'),
            # tf.keras.layers.Dense(3, activation='softmax')
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(3, activation='softmax')
        ])
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        print(model.summary())
        return model

    def preprocess_data(self, statements, labels):
        encoded_labels = self.label_encoder.fit_transform(labels)
        encoded_labels = tf.keras.utils.to_categorical(encoded_labels)

        self.tokenizer.fit_on_texts(statements)
        sequences = self.tokenizer.texts_to_sequences(statements)
        padded = pad_sequences(sequences, maxlen=self.max_length, padding='post', truncating='post')

        return padded, encoded_labels

    def train(self, statements, labels, epochs=30, batch_size=32, validation_split=0.2):
        padded, encoded_labels = self.preprocess_data(statements, labels)
        history = self.model.fit(padded, encoded_labels, epochs=epochs, batch_size=batch_size,
                                 validation_split=validation_split)
        self.save_label_encoder()
        self.save_tokenizer()
        self.save_model()
        return history

    def evaluate(self, statements, labels):

        sequences = self.tokenizer.texts_to_sequences(statements)
        padded = pad_sequences(sequences, maxlen=self.max_length, padding='post', truncating='post')
        encoded_labels = self.label_encoder.transform(labels)
        encoded_labels = tf.keras.utils.to_categorical(encoded_labels)
        loss, accuracy = self.model.evaluate(padded, encoded_labels)
        print('Test accuracy:', accuracy)
        return accuracy

    def predict(self, statement):
        sequences = self.tokenizer.texts_to_sequences([statement])
        padded = pad_sequences(sequences, maxlen=self.max_length, padding='post', truncating='post')
        prediction = self.model.predict(padded)
        predicted_label_index = tf.argmax(prediction, axis=1).numpy()[0]
        predicted_label = self.label_encoder.inverse_transform([predicted_label_index])[0]
        return predicted_label

    def save_model(self):
        self.model.save(self.model_path)
        print("Model saved!")

    def load_model(self):
        self.model = tf.keras.models.load_model(self.model_path)
        print("Model loaded!")

    def save_tokenizer(self):
        with open(self.tokenizer_path, 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("Tokenizer saved!")

    def load_tokenizer(self):
        with open(self.tokenizer_path, 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        print("Tokenizer loaded!")

    def save_label_encoder(self):
        with open(self.label_encoder_path, 'wb') as handle:
            pickle.dump(self.label_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("Label encoder saved!")

    def load_label_encoder(self):
        with open(self.label_encoder_path, 'rb') as handle:
            self.label_encoder = pickle.load(handle)
        print("Label encoder loaded!")


def retrain_model():
    classifier = Classifier2(retrain=1)
    data = pd.read_csv('local_data.csv')
    data = data[['statement', 'label']]
    data = data.dropna()

    statements = data['statement'].tolist()
    labels = data['label'].tolist()

    sns.countplot(x='label', data=data)
    plt.savefig("static/initial_data.jpg")
    unique_values = data['label'].unique()
    min = {'label': -1, 'vals': -1}
    for label in unique_values:
        count_x = (data['label'] == label).sum()
        if min['vals'] == -1 or (min['vals'] > count_x):
            min['label'] = label
            min['vals'] = count_x

    train_data = {}
    final_ds = pd.DataFrame()
    for label in unique_values:
        train_data[label] = data[data['label'] == label].sample(n=min['vals'], random_state=42)
        final_ds = pd.concat([final_ds, train_data[label]])

    data = final_ds
    data['statement'] = data['statement'].apply(lambda x: clean_text(x))
    statements = data['statement'].tolist()
    # statements = clean_text()
    labels = data['label'].tolist()
    sns.countplot(x='label', data=data)
    plt.savefig("static/selected_training.jpg")

    statements_train, statements_test, labels_train, labels_test = train_test_split(statements, labels,
                                                                                    test_size=int(0.25 * data.shape[0]),
                                                                                    random_state=42)
    history = classifier.train(statements_train, labels_train)
    plt.clf()
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend()
    plt.savefig("static/training_history.jpg")

    return (classifier.evaluate(statements_test, labels_test))


def predict_statement(statement):
    classifier = Classifier2()
    return classifier.predict(statement)


import matplotlib.pyplot as plt

if __name__ == '__main__':
    classifier = Classifier2(model_path='model', tokenizer_path='tokenizer.pkl', label_encoder_path='label_encoder.pkl',
                             retrain=1)
    data = pd.read_csv('data_clean.csv')
    data = data[['statement', 'label']]
    data = data.dropna()
    print(data.shape)
    sns.countplot(x='label', data=data)
    plt.show()

    unique_values = data['label'].unique()
    min = {'label': -1, 'vals': -1}
    for label in unique_values:
        count_x = (data['label'] == label).sum()
        if min['vals'] == -1 or (min['vals'] > count_x):
            min['label'] = label
            min['vals'] = count_x

    print(min)
    train_data = {}
    final_ds = pd.DataFrame()
    for label in unique_values:
        train_data[label] = data[data['label'] == label].sample(n=min['vals'], random_state=42)
        final_ds = pd.concat([final_ds, train_data[label]])
    print(train_data)

    print("training data")
    print(final_ds.shape)
    data = final_ds
    data['statement'] = data['statement'].apply(lambda x: clean_text(x))
    print('CLEAN TEXT')
    print(data['statement'])
    statements = data['statement'].tolist()

    statements_train, statements_test, labels_train, labels_test = train_test_split(statements, labels,
                                                                                    test_size=int(0.15 * data.shape[0]),
                                                                                    random_state=42)
    sns.countplot(data=labels_test)
    plt.title("test")
    plt.show()
    history = classifier.train(statements_train, labels_train)
    history_dict = history.history
    print(history_dict.keys())
    print(classifier.evaluate(statements_test, labels_test))
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend()
    plt.show()

