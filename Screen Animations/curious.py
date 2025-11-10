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

def draw_curious_eyes():
    centers = [(700, 660), (1220, 660)]
    for i, (cx, cy) in enumerate(centers):
        parts[f'eye_outer_{i}'] = patches.Circle((cx, cy), 140, color='#E2F1FF')
        parts[f'eye_blue_{i}'] = patches.Circle((cx + 20, cy + 20), 90, color='#60A4F9')
        parts[f'eye_black_{i}'] = patches.Circle((cx + 20, cy + 20), 60, color='black')
        parts[f'sparkle_{i}'] = patches.Circle((cx + 55, cy + 55), 20, color='white')
        ax.add_patch(parts[f'eye_outer_{i}'])
        ax.add_patch(parts[f'eye_blue_{i}'])
        ax.add_patch(parts[f'eye_black_{i}'])
        ax.add_patch(parts[f'sparkle_{i}'])

def draw_curious_mouth():
    parts['mouth'] = patches.Arc((960, 360), 140, 80, theta1=200, theta2=340, color='#E2F1FF', lw=4)
    ax.add_patch(parts['mouth'])

def draw_curious_eyebrows():
    coords = [
        [(610, 770), (730, 790), (730, 780), (610, 760)],
        [(1210, 760), (1330, 780), (1330, 770), (1210, 750)]
    ]
    for i in range(2):
        parts[f'brow_{i}'] = patches.Polygon(coords[i], closed=True, facecolor='#A84D7B')
        ax.add_patch(parts[f'brow_{i}'])

def update(frame):
    shift = 5 * np.sin(frame * 0.2)
    for i in range(2):
        cx = 700 if i == 0 else 1220
        cy = 660
        parts[f'eye_blue_{i}'].center = (cx + 20 + shift, cy + 20)
        parts[f'eye_black_{i}'].center = (cx + 20 + shift, cy + 20)
    return list(parts.values())

draw_curious_eyes()
draw_curious_mouth()
draw_curious_eyebrows()

ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()