import numpy as np
from typing import List, Tuple, Union
import os
from PIL import Image
from typing import List
# We need numpy for efficient array handling
import numpy as np
# We use scikit-learn for KMeans clustering
from sklearn.cluster import KMeans
import airline_logos


# Define the array dimensions and bits per element
ARRAY_SIZE = 20
BITS_PER_ELEMENT = 2
NUM_CLUSTERS = 4 # Represents the 4 colors (0, 1, 2, 3)

# --- Core Compression Logic (retained) ---
def compress_20x20_array(array_2d: List[List[int]]) -> bytes:
    """
    Converts a 20x20 array (with values 0-3) into a compact byte string.
    Packs 4 elements (8 bits) into a single byte for maximum efficiency.
    """
    # if len(array_2d) != ARRAY_SIZE or any(len(row) != ARRAY_SIZE for row in array_2d):
    #     raise ValueError(f"Input array must be {ARRAY_SIZE}x{ARRAY_SIZE}.")

    byte_list = []
    element_buffer = []

    # Flatten the array and iterate through all 400 elements
    for row in array_2d:
        for value in row:
            # The quantization using K-Means ensures this is true
            if not (0 <= value <= 3):
                raise ValueError(f"Value {value} is out of the allowed range (0-3).")
            
            element_buffer.append(value)
            
            # Pack 4 elements into a byte
            if len(element_buffer) == 4:
                # E3, E2, E1, E0 (MSB to LSB)
                E3, E2, E1, E0 = element_buffer
                
                # Use bitwise OR to combine shifted values
                packed_byte = (E3 << 6) | (E2 << 4) | (E1 << 2) | E0
                byte_list.append(packed_byte)
                
                element_buffer = []

    return bytes(byte_list)


import numpy as np
from scipy.ndimage import zoom

def resize_image(image_array: np.ndarray) -> np.ndarray:
    """
    Resizes a 20x20 image array to a 16x16 array using nearest-neighbor interpolation.

    This method is appropriate for image data with discrete values (like 0-3 colors)
    as it selects the nearest existing value rather than calculating a new, potentially
    non-integer, interpolated value.

    Args:
        image_array: A NumPy array of shape (20, 20) representing the image.

    Returns:
        A NumPy array of shape (16, 16).
    """
    # The target dimension is 16, and the source dimension is 20.
    # The zoom factor is 16 / 20 = 0.8
    zoom_factor = 18 / 20

    # The zoom function handles the resizing:
    # 'order=0' specifies nearest-neighbor interpolation, which is essential
    # for preserving the discrete nature of your color values (0, 1, 2, 3).
    resized_array = zoom(
        input=image_array,
        zoom=zoom_factor,
        order=0,
        mode='nearest' # Use nearest value for padding if needed, though not strictly required for downscaling
    )

    # Ensure the output still contains integer values (0, 1, 2, 3)
    # The interpolation sometimes converts to float, so we cast it back to int.
    return resized_array.astype(np.int32)

def image_to_byte_string(filepath: str) -> bytes:
    """
    Loads a 20x20 color image, quantizes its pixel data to 4 optimal RGB colors
    using K-Means, and compresses the resulting 0-3 index values into a 100-byte string.
    """
    try:
        # 1. Load the image and ensure it's in RGB format for color quantization
        img = Image.open(filepath).convert('RGB')
    except FileNotFoundError:
        print(f"Error: Image file not found at {filepath}")
        return b''

    # 2. Ensure correct dimensions
    if img.size != (ARRAY_SIZE, ARRAY_SIZE):
        # Resize if needed
        print(f"Warning: Image size is {img.size}. Resizing to {ARRAY_SIZE}x{ARRAY_SIZE}.")
        img = img.resize((ARRAY_SIZE, ARRAY_SIZE))

    # 3. Get pixel data and quantize to 0-3 using K-Means
    # Reshape to (N, 3) where N=400, and 3 represents the R, G, B channels.
    pixel_data_3channel = np.array(list(img.getdata()), dtype=float).reshape(-1, 3)
    print(pixel_data_3channel)

    # Perform K-Means clustering to find 4 optimal RGB color centroids
    print(f"Running K-Means with {NUM_CLUSTERS} clusters on 400 RGB pixels...")
    # Setting n_init='auto' handles modern sklearn requirement
    kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42)
    kmeans.fit(pixel_data_3channel)

    # The labels (0, 1, 2, 3) directly correspond to the cluster index assigned to each pixel.
    quantized_labels_1d = kmeans.labels_
    
    # Print the optimized centroid values for verification (now RGB)
    # Convert centroids to integers and format as (R, G, B) tuples
    centroids_rgb = [tuple(map(int, c)) for c in kmeans.cluster_centers_]
    print(f"Optimal RGB Centroids found (4 Colors):")
    hex_colors = []
    for i, (r, g, b) in enumerate(centroids_rgb):
        # Convert RGB tuple to Hex string
        hex_color = f'0x{r:02x}{g:02x}{b:02x}'
        hex_colors.append(hex_color)
    print(hex_colors)

    # Reshape the 1D labels array back into a 20x20 list of lists
    array_2d_quantized: List[List[int]] = quantized_labels_1d.reshape(ARRAY_SIZE, ARRAY_SIZE).tolist()

    # 4. Compress the 2D array of 0-3 values
    compressed_bytes = compress_20x20_array(array_2d_quantized)

    return compressed_bytes


def get_element_from_bytes(byte_string: bytes, i: int, j: int) -> int:
    linear_index = i * ARRAY_SIZE + j
    byte_index = linear_index // 4
    element_position_in_byte = linear_index % 4
    shift = (3 - element_position_in_byte) * BITS_PER_ELEMENT
    packed_byte = byte_string[byte_index]
    shifted_value = packed_byte >> shift
    original_value = shifted_value & 0b11

    return original_value

# --- Example Usage and Verification ---
if __name__ == '__main__':
    byte_str = airline_logos.SOUTHWEST
    # arr = np.zeros((20, 20))
    # for i in range(20):
    #     for j in range(20):
    #         arr[i, j] = get_element_from_bytes(byte_str, i, j)
    
    # smaller_arr = resize_image(arr)
    # smaller_str = compress_20x20_array(smaller_arr)
    # print(smaller_str)

    byte_str = image_to_byte_string('/Users/etalius/Downloads/spirit.png')
    arr = np.zeros((20, 20))
    for i in range(20):
        for j in range(20):
            arr[i, j] = get_element_from_bytes(byte_str, i, j)
    
    smaller_arr = resize_image(arr)
    smaller_str = compress_20x20_array(smaller_arr)
    print(smaller_str)