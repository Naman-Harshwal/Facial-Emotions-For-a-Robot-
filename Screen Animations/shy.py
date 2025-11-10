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

shy_parts = {}

# Draw shy baby girl eyes looking down and blinking gently

def draw_shy_eyes():
    eye_centers = [(700, 640), (1220, 640)]
    for i, (cx, cy) in enumerate(eye_centers):
        shy_parts[f'eye_white_{i}'] = patches.Ellipse((cx, cy), 220, 130, facecolor='#E2F1FF')
        shy_parts[f'eye_iris_{i}'] = patches.Circle((cx, cy - 30), 55, facecolor='#60A4F9')
        shy_parts[f'eye_pupil_{i}'] = patches.Circle((cx, cy - 30), 30, facecolor='black')
        shy_parts[f'sparkle_{i}'] = patches.Circle((cx + 15, cy - 15), 8, facecolor='white')

        # Eyelashes pointing slightly downward
        shy_parts[f'eyelid_{i}'] = patches.Arc((cx, cy + 50), 180, 50, theta1=0, theta2=180, color='#AA77FF', lw=4)

        for part in ['eye_white_', 'eye_iris_', 'eye_pupil_', 'sparkle_', 'eyelid_']:
            ax.add_patch(shy_parts[f'{part}{i}'])

# Blushing cheeks

def draw_blush():
    shy_parts['blush_left'] = patches.Ellipse((640, 520), 100, 50, facecolor='#FFB6C1', alpha=0.6)
    shy_parts['blush_right'] = patches.Ellipse((1280, 520), 100, 50, facecolor='#FFB6C1', alpha=0.6)
    ax.add_patch(shy_parts['blush_left'])
    ax.add_patch(shy_parts['blush_right'])

# Shy closed smile

def draw_shy_mouth():
    shy_parts['mouth'] = patches.Arc((960, 370), 100, 50, theta1=0, theta2=180, color='white', lw=3)
    ax.add_patch(shy_parts['mouth'])

# Eyebrows soft and tilted up in middle

def draw_eyebrows():
    positions = [(700, 740), (1220, 740)]
    for i, (cx, cy) in enumerate(positions):
        direction = -1 if i == 0 else 1
        shy_parts[f'brow_{i}'] = patches.Polygon(
            [
                [cx - 60 * direction, cy + 20],
                [cx + 60 * direction, cy],
                [cx + 50 * direction, cy + 20],
                [cx - 50 * direction, cy + 40]
            ],
            closed=True, facecolor='#8855AA'
        )
        ax.add_patch(shy_parts[f'brow_{i}'])

# Update animation: blinking and head tilt

def update(frame):
    blink = 1 - 0.4 * abs(np.sin(frame * 0.3))
    tilt = 4 * np.sin(frame * 0.05)

    for i in [0, 1]:
        shy_parts[f'eye_white_{i}'].height = 130 * blink
        shy_parts[f'eye_iris_{i}'].center = (shy_parts[f'eye_iris_{i}'].center[0], 610 * blink + 30)
        shy_parts[f'eye_pupil_{i}'].center = (shy_parts[f'eye_pupil_{i}'].center[0], 610 * blink + 30)
        shy_parts[f'eyelid_{i}'].theta2 = 180 * blink

        shy_parts[f'brow_{i}'].set_xy(
            np.array(shy_parts[f'brow_{i}'].get_xy()) + np.array([[0, tilt * (-1 if i == 0 else 1),] * 4])
        )

    return list(shy_parts.values())

# Draw all parts
draw_shy_eyes()
draw_blush()
draw_shy_mouth()
draw_eyebrows()

ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()
