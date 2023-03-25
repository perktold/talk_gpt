import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import os
import sounddevice as sd
from scipy.io.wavfile import write
import wavio


def extract_features(file):
    audio, sample_rate = librosa.load(file, res_type='kaiser_fast')
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_processed = np.mean(mfccs.T, axis=0)
    return mfccs_processed

def predict_speaker(file, model):
    features = extract_features(file)
    prediction = model.predict_proba([features])
    return prediction[0] 

def record_audio(filename, duration=7, sample_rate=16000):
    print("Listening...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  
    print("Done Listening.\n")
    wavio.write(filename, recording, sample_rate,sampwidth=2)  

def prepare_model(users):
    felix_files = []
    path = r'audio/felix/'
    for file in os.listdir(path):
        f = path + file
        felix_files.append(f)
    felix_features = [extract_features(file) for file in felix_files]

    daniel_files = []
    path = r'audio/daniel/'
    for file in os.listdir(path):
        f = path + file
        daniel_files.append(f)
    daniel_features = [extract_features(file) for file in daniel_files]

    marcel_files = []
    path = r'audio/marcel/'
    for file in os.listdir(path):
        f = path + file
        marcel_files.append(f)
    marcel_features = [extract_features(file) for file in marcel_files]


    X = np.array(felix_features + daniel_features + marcel_features)
    y = np.array([0] * len(felix_features) + [1] * len(daniel_features) + [2] * len(marcel_features))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GaussianNB()
    model.fit(X_train, y_train)
    return model

def recog_user(model, sample_file, users):
    predicted_probabilities = predict_speaker(sample_file, model)
    max_probability_index = np.argmax(predicted_probabilities)
    max_probability = predicted_probabilities[max_probability_index]

    threshold = 0.78

    if max_probability < threshold:
        print("User not recognized")
        return User("Unknown User")
    elif max_probability_index == 0:
        print("User recognized as Felix")
        return users[0]
    elif max_probability_index == 1:
        print("User recognized as Daniel")
        return users[1]
    elif max_probability_index == 2:
        print("User recognized as Marcel")
        return users[2]
    else:
        return User("Unknown User")
