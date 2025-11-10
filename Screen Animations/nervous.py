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

def draw_nervous_eyes():
    eye_centers = [(700, 660), (1220, 660)]
    for i, (cx, cy) in enumerate(eye_centers):
        parts[f'eye_outer_{i}'] = patches.Circle((cx, cy), 130, color='#E2F1FF')
        parts[f'eye_blue_{i}'] = patches.Circle((cx, cy - 10), 90, color='#60A4F9')
        parts[f'eye_black_{i}'] = patches.Circle((cx, cy - 10), 60, color='black')
        parts[f'sparkle_{i}'] = patches.Circle((cx + 30, cy + 20), 20, color='white')
        ax.add_patch(parts[f'eye_outer_{i}'])
        ax.add_patch(parts[f'eye_blue_{i}'])
        ax.add_patch(parts[f'eye_black_{i}'])
        ax.add_patch(parts[f'sparkle_{i}'])

def draw_nervous_mouth():
    parts['mouth'] = patches.Arc((960, 350), 180, 90, theta1=20, theta2=160, color='#E2F1FF', lw=4)
    ax.add_patch(parts['mouth'])

def draw_nervous_eyebrows():
    brow_coords = [
        [(610, 780), (740, 760), (740, 750), (610, 770)],
        [(1180, 760), (1310, 780), (1310, 770), (1180, 750)]
    ]
    for i, coord in enumerate(brow_coords):
        parts[f'brow_{i}'] = patches.Polygon(coord, closed=True, facecolor='#A84D7B')
        ax.add_patch(parts[f'brow_{i}'])

def update(frame):
    jitter = 3 * np.sin(frame * 0.8)
    for i in range(2):
        parts[f'eye_blue_{i}'].center = (parts[f'eye_blue_{i}'].center[0] + jitter * 0.1, parts[f'eye_blue_{i}'].center[1])
        parts[f'eye_black_{i}'].center = (parts[f'eye_black_{i}'].center[0] + jitter * 0.1, parts[f'eye_black_{i}'].center[1])
    return list(parts.values())

draw_nervous_eyes()
draw_nervous_mouth()
draw_nervous_eyebrows()

ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()