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

sleepy_parts = {}

# Draw sleepy eyes (closed with drooping eyelids)
def draw_sleepy_eyes():
    eye_centers = [(700, 640), (1220, 640)]
    for i, (cx, cy) in enumerate(eye_centers):
        sleepy_parts[f'eye_lid_{i}'] = patches.Arc((cx, cy), 180, 80, theta1=0, theta2=180, color='#E2F1FF', lw=3)
        sleepy_parts[f'eye_line_{i}'] = mlines.Line2D([cx - 90, cx + 90], [cy, cy], color='#E2F1FF', lw=2)
        ax.add_patch(sleepy_parts[f'eye_lid_{i}'])
        ax.add_line(sleepy_parts[f'eye_line_{i}'])

# Draw gentle mouth (slightly open, sleepy)
def draw_sleepy_mouth():
    sleepy_parts['mouth'] = patches.Ellipse((960, 360), 60, 25, facecolor='#8855AA')
    ax.add_patch(sleepy_parts['mouth'])

# Eyebrows drooping

def draw_eyebrows():
    brow_coords = [
        [(650, 750), (730, 740), (740, 745), (660, 755)],  # Left brow
        [(1190, 740), (1270, 750), (1280, 755), (1200, 745)]  # Right brow
    ]
    for i in range(2):
        sleepy_parts[f'brow_{i}'] = patches.Polygon(brow_coords[i], closed=True, facecolor='#8855AA')
        ax.add_patch(sleepy_parts[f'brow_{i}'])

# Sleepy breathing/motion effect

def update(frame):
    scale = 1 + 0.02 * np.sin(frame * 0.1)
    sleepy_parts['mouth'].width = 60 * scale
    sleepy_parts['mouth'].height = 25 * scale
    return list(sleepy_parts.values())

# Draw all parts
draw_sleepy_eyes()
draw_sleepy_mouth()
draw_eyebrows()

ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()
