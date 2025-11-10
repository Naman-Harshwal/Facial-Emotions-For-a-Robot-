import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.axis('off')
fig.patch.set_facecolor('#1B1930')
ax.set_facecolor('#1B1930')

parts = {}

def draw_excited_eyes():
    eye_centers = [(700, 680), (1220, 680)]
    for i, (cx, cy) in enumerate(eye_centers):
        parts[f'eye_outer_{i}'] = patches.Circle((cx, cy), 140, color='#E2F1FF')
        parts[f'eye_blue_{i}'] = patches.Circle((cx, cy), 100, color='#60A4F9')
        parts[f'eye_black_{i}'] = patches.Circle((cx, cy), 60, color='black')
        parts[f'sparkle_{i}'] = patches.Circle((cx + 45, cy + 45), 25, color='white')
        ax.add_patch(parts[f'eye_outer_{i}'])
        ax.add_patch(parts[f'eye_blue_{i}'])
        ax.add_patch(parts[f'eye_black_{i}'])
        ax.add_patch(parts[f'sparkle_{i}'])

def draw_excited_mouth():
    parts['mouth_outer'] = patches.Wedge((960, 370), 150, 180, 360, facecolor='#F7A9A8')
    parts['mouth_inner'] = patches.Wedge((960, 370), 120, 180, 360, facecolor='#3B0A18')
    parts['tongue'] = patches.Ellipse((960, 340), 80, 40, facecolor='#F18DB0')
    ax.add_patch(parts['mouth_outer'])
    ax.add_patch(parts['mouth_inner'])
    ax.add_patch(parts['tongue'])

def draw_excited_eyebrows():
    brow_coords = [
        [(600, 850), (740, 860), (740, 870), (600, 860)],
        [(1160, 860), (1300, 850), (1300, 860), (1160, 870)]
    ]
    for i, coord in enumerate(brow_coords):
        parts[f'brow_{i}'] = patches.Polygon(coord, closed=True, facecolor='#A84D7B')
        ax.add_patch(parts[f'brow_{i}'])

def update(frame):
    scale = 1 + 0.02 * np.sin(frame * 0.4)
    parts['tongue'].width = 80 * scale
    parts['tongue'].height = 40 * scale
    return list(parts.values())

draw_excited_eyes()
draw_excited_mouth()
draw_excited_eyebrows()

ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()
