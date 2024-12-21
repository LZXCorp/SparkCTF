import numpy as np
from scipy.io.wavfile import read
import os

# HINT: The core task involves decoding frequencies into readable characters.

def decode_audio(audio_file, sample_rate, duration_per_char):
    """TODO: Complete this function to decode the hidden message from the audio signal."""
    # Step 1: Read the audio file (Hint: Use the read function)
    _, signal = read(audio_file)

    # Step 2: Normalize the signal (Hint: Map the range to -1 to 1)
    # TODO: Normalize correctly if needed
    ???

    samples_per_char = sample_rate * duration_per_char

    decoded_text = ""  # Initialize an empty string for the decoded message

    # Step 3: Loop through the signal in chunks
    for i in range(0, len(signal), samples_per_char):
        segment = signal[i:i + samples_per_char]
        fft_result = np.fft.fft(segment)

        # Step 4: Extract the dominant frequency (Hint: Use np.argmax on the FFT result)
        freqs = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
        peak_freq = abs(???)

        # Step 5: Convert the frequency to a character (Hint: Use chr() with rounding)
        decoded_char = ???

        decoded_text += decoded_char  # Append the character to the decoded message

    return decoded_text  # Return the full decoded message

# Get the relative path to the audio file
current_dir = os.path.dirname(__file__)
audio_file = os.path.join(current_dir, "neon_en.wav")
sample_rate = 44100
duration_per_char = ???

# Perform decoding and print the result
decoded_message = decode_audio(audio_file, sample_rate, duration_per_char)
print("Decoded message:", decoded_message)