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

surprise_parts = {}

# Draw surprised eyes and raised eyebrows
def draw_surprised_eyes():
    eye_centers = [(700, 700), (1220, 700)]
    for cx, cy in eye_centers:
        surprise_parts[f'eye_white_{cx}'] = patches.Circle((cx, cy), 150, color='#E2F1FF')
        surprise_parts[f'eye_iris_{cx}'] = patches.Circle((cx, cy), 60, color='#60A4F9')
        surprise_parts[f'eye_pupil_{cx}'] = patches.Circle((cx, cy), 40, color='black')
        surprise_parts[f'sparkle_{cx}'] = patches.Circle((cx + 25, cy + 25), 15, color='white')
        surprise_parts[f'eyebrow_{cx}'] = patches.Arc((cx, cy + 180), 180, 50, theta1=0, theta2=180, color='white', lw=5)
        
        for part in ['eye_white_', 'eye_iris_', 'eye_pupil_', 'sparkle_', 'eyebrow_']:
            ax.add_patch(surprise_parts[f'{part}{cx}'])

# Draw open round mouth
def draw_surprised_mouth():
    surprise_parts['mouth'] = patches.Circle((960, 320), 90, color='#FF007F')  # Open surprised mouth
    ax.add_patch(surprise_parts['mouth'])

# Draw animation stars
def draw_stars():
    surprise_parts['left_star'] = ax.plot([], [], marker=(4, 1, 0), markersize=40, color='#B3D6FF')[0]
    surprise_parts['right_star'] = ax.plot([], [], marker=(4, 1, 0), markersize=20, color='#B3D6FF')[0]

# Update animation
def update(frame):
    alpha = 0.5 + 0.5 * np.sin(frame * 0.1)
    surprise_parts['left_star'].set_data(540, 920)
    surprise_parts['left_star'].set_alpha(alpha)
    surprise_parts['right_star'].set_data(1390, 930)
    surprise_parts['right_star'].set_alpha(1 - alpha)

    # Pupil jitter for surprise
    dx = 10 * np.sin(frame * 0.3)
    for cx in [700, 1220]:
        surprise_parts[f'eye_pupil_{cx}'].center = (cx + dx, 700)
        surprise_parts[f'eye_iris_{cx}'].center = (cx + dx * 0.5, 700)
        surprise_parts[f'sparkle_{cx}'].center = (cx + 25 + dx * 0.3, 725)

    # Mouth pulse
    pulse = 1 + 0.05 * np.sin(frame * 0.2)
    surprise_parts['mouth'].radius = 90 * pulse

    return list(surprise_parts.values())


draw_surprised_eyes()
draw_surprised_mouth()
draw_stars()
ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()
