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

def draw_proud_eyes():
    eye_centers = [(700, 670), (1220, 670)]
    for i, (cx, cy) in enumerate(eye_centers):
        parts[f'eye_outer_{i}'] = patches.Circle((cx, cy), 130, color='#E2F1FF')
        parts[f'eye_blue_{i}'] = patches.Circle((cx, cy + 15), 90, color='#60A4F9')
        parts[f'eye_black_{i}'] = patches.Circle((cx, cy + 15), 60, color='black')
        parts[f'sparkle_{i}'] = patches.Circle((cx + 35, cy + 50), 20, color='white')
        ax.add_patch(parts[f'eye_outer_{i}'])
        ax.add_patch(parts[f'eye_blue_{i}'])
        ax.add_patch(parts[f'eye_black_{i}'])
        ax.add_patch(parts[f'sparkle_{i}'])

def draw_proud_mouth():
    parts['mouth_outer'] = patches.Wedge((960, 360), 130, 180, 360, facecolor='#F7A9A8')
    parts['mouth_inner'] = patches.Wedge((960, 360), 100, 180, 360, facecolor='#3B0A18')
    parts['teeth'] = patches.Rectangle((880, 360), 160, 20, facecolor='white')
    ax.add_patch(parts['mouth_outer'])
    ax.add_patch(parts['mouth_inner'])
    ax.add_patch(parts['teeth'])

def draw_proud_eyebrows():
    brow_coords = [
        [(600, 830), (740, 820), (740, 810), (600, 820)],
        [(1160, 820), (1300, 830), (1300, 840), (1160, 830)]
    ]
    for i, coord in enumerate(brow_coords):
        parts[f'brow_{i}'] = patches.Polygon(coord, closed=True, facecolor='#A84D7B')
        ax.add_patch(parts[f'brow_{i}'])

def update(frame):
    pulse = 1 + 0.02 * np.sin(frame * 0.2)
    parts['teeth'].set_width(160 * pulse)
    parts['teeth'].set_x(880 - (160 * pulse - 160) / 2)
    return list(parts.values())

draw_proud_eyes()
draw_proud_mouth()
draw_proud_eyebrows()

ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()