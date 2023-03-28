import numpy as np
import librosa
import matplotlib.pyplot as plt

def analyze(path):
    # Load audio data
    y, sr = librosa.load(path)
    
    # Plot waveform
    plt.figure(figsize=(14, 5))
    librosa.display.waveshow(y, sr=sr)
    plt.title('Audio waveform')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.show()
    
    # Compute spectrogram
    spec = librosa.stft(y)
    spec_db = librosa.amplitude_to_db(abs(spec))
    
    # Plot spectrogram
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(spec_db, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar()
    plt.title('Spectrogram')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency (Hz)')
    plt.show()
    
    # Compute and plot mel spectrogram
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    mel_spec_db = librosa.amplitude_to_db(mel_spec, ref=np.max)
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar()
    plt.title('Mel spectrogram')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Mel frequency')
    plt.show()
    
    # Compute and plot chromagram
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma')
    plt.colorbar()
    plt.title('Chromagram')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Pitch class')
    plt.show()
    
    # Compute and plot MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(mfccs, sr=sr, x_axis='time')
    plt.colorbar()
    plt.title('MFCCs')
    plt.xlabel('Time (seconds)')
    plt.ylabel('MFCC coefficient')
    plt.show()
