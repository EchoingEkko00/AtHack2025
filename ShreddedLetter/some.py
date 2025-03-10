import cv2
import numpy as np
import os

def load_shreds(folder):
    """Load shredded image pieces from a folder."""
    images = {}
    name = 'shred_'
    for i in range(200):
        file_path = os.path.join(folder, f"{name}{i}.bmp")
        image = cv2.imread(file_path)
        if image is not None:
            # Ensure all images have 3 channels (convert grayscale to 3D)
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            images[i] = image
        else:
            print(f"Failed to load {file_path}")  # Debugging output
    return images

def compare_edges_pixelwise(img1, img2):
    """Compare the right edge of img1 with the left edge of img2 using pixel-by-pixel difference."""
    edge1 = img1[:, -1, :]  # Rightmost column
    edge2 = img2[:, 0, :]   # Leftmost column
    
    diff = np.sum(np.abs(edge1.astype(int) - edge2.astype(int)))  # Sum of absolute differences
    total_pixels = edge1.size  # Total number of pixels in the column
    
    # Calculate similarity percentage
    similarity_percentage = 1 - (diff / total_pixels)  # Higher percentage means better match
    return similarity_percentage

def find_best_order(sorted_shreds, unsorted_shreds):
    """Find the correct order of unsorted shreds based on sorted shreds."""
    ordered_shreds = [None] * 200  # We know there are 200 sorted shreds
    used_indices = set()
    
    for sorted_idx in range(200):  # Loop through all sorted shreds
        sorted_shred = sorted_shreds[sorted_idx]
        
        for unsorted_idx, unsorted_shred in unsorted_shreds.items():
            if unsorted_idx in used_indices:
                continue
            
            # Compare the unsorted shred to the sorted one
            similarity_percentage = compare_edges_pixelwise(sorted_shred, unsorted_shred)
            
            if similarity_percentage >= 0.9:  # Match is found if similarity is at least 90%
                ordered_shreds[sorted_idx] = unsorted_shred  # Place the matched unsorted shred in its sorted position
                used_indices.add(unsorted_idx)  # Mark this unsorted shred as used
                break
    
    return ordered_shreds

def reconstruct_image(ordered_shreds):
    """Reconstruct the image by stacking shreds horizontally."""
    # Filter out any None values (if there was an issue in matching)
    ordered_shreds = [shred for shred in ordered_shreds if shred is not None]
    return np.hstack(ordered_shreds)

def main():
    folder_sorted = 'zainWithoutFlag/sorted'  # Folder with sorted shreds
    folder_noSort = 'rogerWithFlag/noSorted'  # Folder with unsorted shreds
    
    sorted_shreds = load_shreds(folder_sorted)
    unsorted_shreds = load_shreds(folder_noSort)
    
    print(f"Loaded {len(sorted_shreds)} sorted shreds.")
    print(f"Loaded {len(unsorted_shreds)} unsorted shreds.")
    
    #ordered_shreds = find_best_order(sorted_shreds, unsorted_shreds)
    
    print("Reconstruction in progress...")
    reconstructed = reconstruct_image(sorted_shreds)
    cv2.imwrite('reconstructed_image.jpg', reconstructed)
    print("Reconstruction complete! Image saved as 'reconstructed_image.jpg'")
    
if __name__ == "__main__":
    main()
