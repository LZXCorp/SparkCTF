import numpy as np
import matplotlib.pyplot as plt
import os

# Load the binary string from the uploaded file
file_path = os.path.join(os.path.dirname(__file__), "totally_not_qr_code.txt")
with open(file_path, "r") as file:
    binary_string = file.read().strip()

# Convert binary string into a 2D matrix
size = int(len(binary_string) ** 0.5)  # Assuming a square QR code
qr_matrix = np.array([int(bit) for bit in binary_string]).reshape((size, size))

# Create an image from the matrix
plt.imshow(qr_matrix, cmap='binary', interpolation='nearest')
plt.axis('off')

# Save the QR code image
qr_image_path = os.path.join(os.path.dirname(__file__), "totally_not_qr_code.png")
plt.savefig(qr_image_path, bbox_inches='tight', pad_inches=0)