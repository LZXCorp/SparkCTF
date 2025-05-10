import os
from scipy.io import wavfile
import numpy as np

def lsb_decode(audio_samples, text_length):
    flat_samples = audio_samples.flatten()
    bits = []

    for i in range(text_length * 8):
        bits.append(str(flat_samples[i] & 1))

    chars = [chr(int(''.join(bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def amplitude_decode(encoded_samples, text_length, segment_length=1, fixed_amplitude=100, sample_rate=44100):
    """Decodes text from audio encoded with fixed amplitude modulation."""
    bits = []
    full_segment_length = segment_length * sample_rate

    threshold_amplitude = fixed_amplitude * 2

    for idx in range(text_length * 8):
        start = idx * full_segment_length
        end = start + full_segment_length
        if end >= len(encoded_samples):
            break
        segment = encoded_samples[start:end]
        
        average_amplitude = np.mean(np.abs(segment))
        
        is_one = average_amplitude <= threshold_amplitude
        bits.append('1' if is_one else '0')

    chars = [chr(int(''.join(bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def decode_flag(input_wav, flag_length):
    # Load audio
    sample_rate, samples = wavfile.read(input_wav)
    if samples.ndim > 1:
        samples = np.mean(samples, axis=1).astype(np.int16)  # Convert to mono if stereo

    # Decode first half of flag using LSB
    lsb_text = lsb_decode(samples, flag_length)

    # Decode second half of flag using Amplitude Modulation
    amplitude_text = amplitude_decode(samples, flag_length, segment_length=1, sample_rate=sample_rate)

    # Combine both halves of the flag
    full_flag = lsb_text + amplitude_text
    full_flag = ''.join(filter(lambda x: x != '\x00', full_flag))
    return full_flag

current_dir = os.path.dirname(__file__)
audio_file = os.path.join(current_dir, "../dist/en_track5.wav")

decoded_flag = decode_flag(audio_file, 20)
print(decoded_flag)