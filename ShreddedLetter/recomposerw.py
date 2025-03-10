import cv2
import numpy as np
import os

# Paths to shredded images
ordered_folder = "zainWithoutFlag/sorted"  # Folder with ordered shreds (0-199)
shuffled_folder = "rogerWithFlag/noSorted"   # Folder with shuffled shreds (0-199, but unordered)

# Load ordered shreds (unflagged)
ordered_shreds = []
for i in range(200):
    path = os.path.join(ordered_folder, f"shred_{i}.bmp")
    shred = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if shred is None:
        raise FileNotFoundError(f"Missing ordered shred {i}")
    ordered_shreds.append(shred)

# Load shuffled shreds (flagged)
shuffled_shreds = {}
for filename in os.listdir(shuffled_folder):
    if filename.endswith(".bmp"):
        idx = int(filename.split("_")[1].split(".")[0])  # Extract index
        path = os.path.join(shuffled_folder, filename)
        shred = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if shred is None:
            raise FileNotFoundError(f"Missing shuffled shred {idx}")
        shuffled_shreds[idx] = shred

# Convert shuffled dictionary to list (unordered)
shuffled_indices = list(shuffled_shreds.keys())
shuffled_shreds_list = [shuffled_shreds[idx] for idx in shuffled_indices]

# Ensure all images have the same dimensions
shred_height, shred_width = ordered_shreds[0].shape
for i in range(200):
    ordered_shreds[i] = cv2.resize(ordered_shreds[i], (shred_width, shred_height))
for i in range(len(shuffled_shreds_list)):
    shuffled_shreds_list[i] = cv2.resize(shuffled_shreds_list[i], (shred_width, shred_height))

# Compute Sobel edges
def compute_edges(image):
    return cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)  # Horizontal edges

# Extract left and right edges
def extract_edges(shred):
    left_edge = shred[:, 0]   # Leftmost column
    right_edge = shred[:, -1] # Rightmost column
    return left_edge, right_edge

# Match shuffled shreds to ordered ones
def match_shreds(ordered, shuffled):
    matches = {}  # Map shuffled index -> correct position

    for shuffled_idx, shuffled_shred in enumerate(shuffled):
        best_match = -1
        best_score = float("inf")

        shuffled_left, shuffled_right = extract_edges(shuffled_shred)

        for ordered_idx, ordered_shred in enumerate(ordered):
            ordered_left, ordered_right = extract_edges(ordered_shred)

            # Compare right edge of previous with left edge of current
            right_diff = np.sum((shuffled_right - ordered_left) ** 2)

            if right_diff < best_score:
                best_score = right_diff
                best_match = ordered_idx

        matches[shuffled_idx] = best_match  # Store matched position

    return matches

# Find correct order
matched_indices = match_shreds(ordered_shreds, shuffled_shreds_list)

# Reorder the flagged shreds based on matched positions
reconstructed_order = [None] * 200
for shuffled_idx, correct_pos in matched_indices.items():
    reconstructed_order[correct_pos] = shuffled_shreds_list[shuffled_idx]

# Fill missing spots with black images (failsafe)
for i in range(200):
    if reconstructed_order[i] is None:
        reconstructed_order[i] = np.zeros((shred_height, shred_width), dtype=np.uint8)

# Concatenate shreds to form the full image
reconstructed_image = np.hstack(reconstructed_order)

# Save or display the reconstructed image
cv2.imwrite("reconstructed_flagged_image.bmp", reconstructed_image)
cv2.imshow("Reconstructed Image", reconstructed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
