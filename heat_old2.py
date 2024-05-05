import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

# Full Morse code dictionary
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..'
}

def pulse_heat(sequence, heat_dot=5, heat_dash=10, duration_dot=1, duration_dash=3, gap_dot=1, gap_between_elements=1, gap_between_letters=3):
    heat_pulses = []
    for char in sequence.upper():
        if char in morse_code:  # Check if the character is in the Morse code dictionary
            for i, symbol in enumerate(morse_code[char]):
                if symbol == '.':
                    heat_pulses.extend([heat_dot] * duration_dot)  # Medium heat for dots
                elif symbol == '-':
                    heat_pulses.extend([heat_dash] * duration_dash)  # Higher heat for dashes
                # Add gap between elements of the same letter
                if i < len(morse_code[char]) - 1:
                    heat_pulses.extend([0] * gap_between_elements)
            # Add gap between letters
            heat_pulses.extend([0] * gap_between_letters)
    return heat_pulses

def diffuse_heat(grid, source_position, max_diffusion=0.1):
    x, y = source_position
    max_x, max_y = grid.shape
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < max_x and 0 <= ny < max_y:
                grid[nx, ny] += grid[x, y] * max_diffusion
    return grid

def cool_down(grid, cooling_rate=0.5):
    return grid * cooling_rate

# Grid size and simulation parameters
grid_size = (10, 10)
source_position = (5, 5)
steps = 40  # Adjusted for a longer message

# Message to encode
message = "SOS"

# Generate heat pulses from the message
heat_sequence = pulse_heat(message)

# Simulation of heat dispersal
heat_grid = np.zeros(grid_size)
history = []

for step in range(steps):
    if step < len(heat_sequence):
        heat_grid[source_position] = heat_sequence[step]  # Apply heat based on sequence
    heat_grid = diffuse_heat(heat_grid, source_position)
    heat_grid = cool_down(heat_grid)  # Cool down after each step
    history.append(heat_grid.copy())

# Save frames to disk
output_folder = 'frames'
os.makedirs(output_folder, exist_ok=True)
filenames = []

for i, grid in enumerate(history):
    plt.figure(figsize=(6, 5))
    plt.imshow(grid, cmap='hot', interpolation='nearest', vmin=0, vmax=10)
    plt.title(f'Time Step: {i}')
    plt.colorbar()
    plt.axis('off')
    filename = f'{output_folder}/frame_{i:04d}.png'
    plt.savefig(filename)
    plt.close()
    filenames.append(filename)

# Create a video from images
video_name = 'morse_heat_simulation.avi'
frame = cv2.imread(filenames[0])
height, width, layers = frame.shape
video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 10, (width, height))  # Adjusted FPS for longer sequence

for image in filenames:
    video.write(cv2.imread(image))

cv2.destroyAllWindows()
video.release()

print("Video done")

