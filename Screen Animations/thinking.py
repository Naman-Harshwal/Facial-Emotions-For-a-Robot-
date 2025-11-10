import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import matplotlib.lines as mlines
import numpy as np

fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.axis('off')
fig.patch.set_facecolor('#1B1930')
ax.set_facecolor('#1B1930')

parts = {}

# Thoughtful eyes: looking up

def draw_thinking_eyes():
    eye_centers = [(700, 650), (1220, 650)]
    for i, (cx, cy) in enumerate(eye_centers):
        parts[f'eye_outer_{i}'] = patches.Circle((cx, cy), 140, color='#E2F1FF')
        parts[f'eye_blue_{i}'] = patches.Circle((cx, cy + 30), 90, color='#60A4F9')
        parts[f'eye_black_{i}'] = patches.Circle((cx, cy + 30), 60, color='black')
        parts[f'sparkle_{i}'] = patches.Circle((cx + 40, cy + 70), 20, color='white')
        ax.add_patch(parts[f'eye_outer_{i}'])
        ax.add_patch(parts[f'eye_blue_{i}'])
        ax.add_patch(parts[f'eye_black_{i}'])
        ax.add_patch(parts[f'sparkle_{i}'])

# Thinking mouth: tilted straight line

def draw_thinking_mouth():
    parts['mouth'] = mlines.Line2D([920, 1000], [360, 370], color='#E2F1FF', lw=4)
    ax.add_line(parts['mouth'])

# Eyebrows positioned directly above the eyes

def draw_eyebrows():
    coords = [
        [(610, 830), (730, 820), (730, 810), (610, 820)],  # Left eyebrow above left eye
        [(1190, 820), (1310, 830), (1310, 840), (1190, 830)]  # Right eyebrow above right eye
    ]
    for i in range(2):
        parts[f'brow_{i}'] = patches.Polygon(coords[i], closed=True, facecolor='#A84D7B')
        ax.add_patch(parts[f'brow_{i}'])

# Subtle blinking animation effect

def update(frame):
    alpha = 0.9 + 0.1 * np.sin(frame * 0.2)
    for i in range(2):
        parts[f'eye_blue_{i}'].set_alpha(alpha)
        parts[f'eye_black_{i}'].set_alpha(alpha)
    return list(parts.values())

# Draw components
draw_thinking_eyes()
draw_thinking_mouth()
draw_eyebrows()

ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()
