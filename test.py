import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# Morse Code Mapping
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..'
}

def morse_to_heat(message, dot_duration=1):
    """Converts a Morse code message into a list of heat intensities."""
    heat_sequence = []
    for char in message:
        code = morse_code.get(char.upper(), '')
        for symbol in code:
            if symbol == '.':
                heat_sequence.extend([1] * dot_duration)  # dot
            elif symbol == '-':
                heat_sequence.extend([1] * (3 * dot_duration))  # dash
            heat_sequence.append(0)  # inter-element gap
        heat_sequence.extend([0] * (3 * dot_duration))  # inter-letter gap
    return np.array(heat_sequence[:-3 * dot_duration])  # remove last inter-letter gap

# Simulation parameters
message = "AI"
grid_size = (100, 100)  # size of the 2D grid
source_position = (50, 50)  # center of the grid
dot_duration = 5

# Generate heat pulses
heat_pulses = morse_to_heat(message, dot_duration)
total_time = len(heat_pulses)

# Initialize grid
grid = np.zeros(grid_size)
temporal_heat_maps = []

# Simulate heat diffusion
for pulse in heat_pulses:
    grid[source_position] += pulse  # add heat pulse
    grid = gaussian_filter(grid, sigma=1)  # simulate diffusion
    temporal_heat_maps.append(grid.copy())

# Visualize the heat diffusion
fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(20, 5))
time_steps = np.linspace(0, total_time, 4, dtype=int)
for ax, t in zip(axes, time_steps):
    ax.imshow(temporal_heat_maps[t], cmap='hot', origin='lower')
    ax.set_title(f"Time = {t}")
    ax.axis('off')
plt.show()

