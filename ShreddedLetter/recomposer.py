import cv2
import numpy as np
import os
from itertools import permutations

def load_shreds(folder):
    """Load shredded image pieces from a folder."""
    images = []
    orderList = [199, 50, 197, 196, 195, 194, 193, 192, 191, 190, 189, 188, 187, 186, 185, 184, 183, 182, 181, 180, 179, 178, 177, 176, 175, 174, 173, 172, 171, 170, 169, 168, 167, 166, 165, 164, 163, 162, 161, 160, 159, 158, 157, 156, 155, 154, 153, 152, 151, 150, 149, 148, 147, 146, 145, 144, 143, 142, 141, 140, 139, 138, 137, 136, 135, 134, 133, 132, 131, 130, 129, 128, 127, 126, 125, 124, 123, 122, 121, 120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 198, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    for i in orderList:
        file_path = os.path.join(folder, f"shred_{i}.bmp")
        image = cv2.imread(file_path)
        if image is not None:
            # Ensure all images have 3 channels (convert grayscale to 3D)
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            images.append(image)
        else:
            print(f"Failed to load {file_path}")
    return images

def compute_edge_similarity(img1, img2, side='right'):
    """Compute similarity between the edges of two images."""
    if side == 'right':
        edge1 = img1[:, -1, :]
        edge2 = img2[:, 0, :]
    else:
        edge1 = img1[:, 0, :]
        edge2 = img2[:, -1, :]
    
    return np.sum((edge1 - edge2) ** 2)  # Sum of squared differences

def reconstruct_image(shreds):
    """Reconstruct the shredded image based on the current order."""
    return np.hstack([shred for shred in shreds])

def swap_shreds(shreds, idx1, idx2):
    """Swap two image pieces by index."""
    shreds[idx1], shreds[idx2] = shreds[idx2], shreds[idx1]
    return shreds

def main():
    folder = 'rogerWithFlag/noSorted'  # Folder containing shredded image pieces
    
    # Load the shredded pieces
    shreds = load_shreds(folder)
    
    # Display the initial reconstruction
    reconstructed = reconstruct_image(shreds)
    cv2.imshow('Reconstructed Image', reconstructed)
    cv2.waitKey(1)  # Wait briefly for initial display
    
    while True:
        # Prompt user for input to swap shreds
        print("\nCurrent shreds order:")
        print("Enter the indices of the two shreds you want to swap (0-based index) or 'exit' to quit:")
        
        user_input = input("Enter two indices to swap (e.g., 1 3): ")
        
        if user_input.lower() == 'exit':
            break
        
        try:
            idx1, idx2 = map(int, user_input.split())
            
            if idx1 < 0 or idx2 < 0 or idx1 >= len(shreds) or idx2 >= len(shreds):
                print("Invalid indices. Please enter valid indices within the range.")
                continue
            
            # Swap the selected shreds
            shreds = swap_shreds(shreds, idx1, idx2)
            
            # Reconstruct the image and show the result
            reconstructed = reconstruct_image(shreds)
            cv2.imshow('Reconstructed Image', reconstructed)
            cv2.waitKey(1)  # Refresh the image immediately after the swap
        
        except ValueError:
            print("Invalid input. Please enter two integers separated by a space.")

    cv2.destroyAllWindows()
    print("Exiting the program.")

if __name__ == "__main__":
    main()
