import numpy as np
from scipy.io.wavfile import read
import os

def decode_audio(audio_file, sample_rate, duration_per_char):
    # Read the audio file
    _, signal = read(audio_file)
    signal = signal / (2**15 - 1)  # Normalize the signal

    # Parameters
    samples_per_char = sample_rate * duration_per_char

    # Extract frequencies and decode
    decoded_text = ""
    for i in range(0, len(signal), samples_per_char):
        segment = signal[i:i + samples_per_char]
        fft_result = np.fft.fft(segment)
        freqs = np.fft.fftfreq(len(fft_result), 1 / sample_rate)

        # Find the peak frequency
        peak_freq = abs(freqs[np.argmax(np.abs(fft_result))])
        decoded_char = chr(int(round(peak_freq)))

        decoded_text += decoded_char
    return decoded_text

# Get the relative path to the audio file
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
audio_file = os.path.join(parent_dir, "dist", "neon_en_comb.wav")
sample_rate = 44100
duration_per_char = 1  # Duration of each character in seconds

# Perform decoding
decoded_message = decode_audio(audio_file, sample_rate, duration_per_char)
print("Decoded message:", decoded_message)
