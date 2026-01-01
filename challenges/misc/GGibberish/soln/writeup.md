# Gibberish Audio challenge writeup

## Context of challenge:
The python source code generates an audio file which has the flag encoded within it (randomized ROT as well)

## Solution Steps:

To determine the flag, the audio can be loaded into python and read using the wave module. This will return raw bytes that can be parsed using ggwave.decode(). This will return the flag that has been encoded using ROT(randomized between 1 and 12). 

Sample python code to generate ROT flag:

```python
import ggwave
import wave
import numpy as np

# Initialize GGWave
instance = ggwave.init()

# Function to load the waveform from the .wav file
def load_wav_file(filename):
    with wave.open(filename, 'rb') as wav_file:
        # Get basic info from the wav file
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        
        # Read the raw waveform bytes from the .wav file
        raw_data = wav_file.readframes(num_frames)
        
        # Convert the raw byte data to numpy array
        if sample_width == 4:  # 32-bit float
            return raw_data, framerate
        else:
            raise ValueError("Unsupported sample width: Only 32-bit float supported")


# Function to decode the waveform using GGWave
def decode_waveform(waveform, framerate):
    # Use the ggwave decoder to decode the waveform into the original message
    decoded_message = ggwave.decode(instance, waveform)
    return decoded_message

# Load the waveform from the saved .wav file
waveform, framerate = load_wav_file("C:\\Users\\user\\Desktop\\secret.wav")

# Decode the waveform to get the original message
decoded_message = decode_waveform(waveform, framerate)

# Print the decoded message
print("Decoded message:", decoded_message)

```

After getting the ROT flag, use a tool such as cyberchef to "brute force" the randomized rotation to reveal the flag. 