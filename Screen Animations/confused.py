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

def draw_confused_eyes():
    centers = [(700, 660), (1220, 660)]
    for i, (cx, cy) in enumerate(centers):
        parts[f'eye_outer_{i}'] = patches.Circle((cx, cy), 140, color='#E2F1FF')
        parts[f'eye_blue_{i}'] = patches.Circle((cx, cy), 90, color='#60A4F9')
        parts[f'eye_black_{i}'] = patches.Circle((cx, cy), 60, color='black')
        parts[f'sparkle_{i}'] = patches.Circle((cx + 35, cy + 35), 20, color='white')
        ax.add_patch(parts[f'eye_outer_{i}'])
        ax.add_patch(parts[f'eye_blue_{i}'])
        ax.add_patch(parts[f'eye_black_{i}'])
        ax.add_patch(parts[f'sparkle_{i}'])

def draw_confused_mouth():
    parts['mouth'] = patches.Arc((960, 340), 160, 100, theta1=20, theta2=160, color='#E2F1FF', lw=4)
    ax.add_patch(parts['mouth'])

def draw_confused_eyebrows():
    coords = [
        [(620, 800), (740, 790), (740, 780), (620, 790)],
        [(1210, 770), (1330, 780), (1330, 770), (1210, 760)]
    ]
    for i in range(2):
        parts[f'brow_{i}'] = patches.Polygon(coords[i], closed=True, facecolor='#A84D7B')
        ax.add_patch(parts[f'brow_{i}'])

def update(frame):
    jitter = 3 * np.sin(frame * 0.6)
    for i in range(2):
        cx = 700 if i == 0 else 1220
        cy = 660
        parts[f'eye_black_{i}'].center = (cx + jitter, cy - jitter)
    return list(parts.values())

draw_confused_eyes()
draw_confused_mouth()
draw_confused_eyebrows()

ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()
