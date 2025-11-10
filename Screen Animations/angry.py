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

angry_parts = {}

# Draw angry eyes with slanted eyebrows
def draw_angry_eyes():
    eye_centers = [(700, 700), (1220, 700)]
    for i, (cx, cy) in enumerate(eye_centers):
        direction = -1 if i == 0 else 1
        angry_parts[f'eye_white_{i}'] = patches.Circle((cx, cy), 130, color='#E2F1FF')
        angry_parts[f'eye_iris_{i}'] = patches.Circle((cx, cy), 80, color='#60A4F9')
        angry_parts[f'eye_pupil_{i}'] = patches.Circle((cx, cy), 50, color='black')
        angry_parts[f'sparkle_{i}'] = patches.Circle((cx + 30, cy + 30), 15, color='white')
        angry_parts[f'eyebrow_{i}'] = patches.Polygon(
            [[cx - 90, cy + 180], [cx + 90, cy + 160], [cx + 80, cy + 180], [cx - 100, cy + 200]],
            closed=True, color='red')

        for part in ['eye_white_', 'eye_iris_', 'eye_pupil_', 'sparkle_', 'eyebrow_']:
            ax.add_patch(angry_parts[f'{part}{i}'])

# Draw angry mouth (frown shape)
def draw_angry_mouth():
    angry_parts['mouth'] = patches.Arc((960, 300), 250, 100, theta1=0, theta2=180, color='red', lw=8)
    ax.add_patch(angry_parts['mouth'])

# Draw animation stars (for dynamic tension)
def draw_stars():
    angry_parts['left_star'] = ax.plot([], [], marker=(4, 1, 0), markersize=30, color='red')[0]
    angry_parts['right_star'] = ax.plot([], [], marker=(4, 1, 0), markersize=30, color='red')[0]

# Update animation
def update(frame):
    alpha = 0.5 + 0.5 * np.sin(frame * 0.6)
    angry_parts['left_star'].set_data(540, 920)
    angry_parts['left_star'].set_alpha(alpha)
    angry_parts['right_star'].set_data(1390, 930)
    angry_parts['right_star'].set_alpha(1 - alpha)

    dx = 8 * np.sin(frame * 0.5)
    for i, cx in enumerate([700, 1220]):
        angry_parts[f'eye_pupil_{i}'].center = (cx + dx, 700)
        angry_parts[f'eye_iris_{i}'].center = (cx + dx * 0.6, 700)
        angry_parts[f'sparkle_{i}'].center = (cx + 30 + dx * 0.3, 730)

    return list(angry_parts.values())


draw_angry_eyes()
draw_angry_mouth()
draw_stars()
ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()
