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

tears = []
tear_paths = []
mouth_parts = {}

TEAR_INTERVAL = 10  # pixels (~1cm for 100dpi)


def draw_eyes():
    eye_centers = [(700, 700), (1220, 700)]
    for cx, cy in eye_centers:
        ax.add_patch(patches.Circle((cx, cy), 140, color='#E2F1FF'))
        ax.add_patch(patches.Circle((cx, cy), 100, color='#60A4F9'))
        ax.add_patch(patches.Circle((cx, cy), 70, color='black'))
        ax.add_patch(patches.Circle((cx + 55, cy + 55), 25, color='white'))
        ax.add_patch(patches.Arc((cx, cy + 160), 160, 50, theta1=0, theta2=180, color='white', lw=5))  # eyebrow

        direction = -1 if cx < 960 else 1
        start_x, start_y = cx, cy - 90
        for row in range(3):
            divergence = (row - 1) * 0.5  # -0.5, 0, 0.5 for diverging effect
            for n in range(0, int(1920 / TEAR_INTERVAL)):
                tear = patches.Ellipse((start_x, start_y), 10, 25, facecolor='#A4D6F4', alpha=0.9)
                tears.append(tear)
                offset = n * TEAR_INTERVAL
                tear_paths.append((start_x, start_y, offset, row, direction, divergence))
                ax.add_patch(tear)


def draw_mouth():
    mouth_parts['lip'] = patches.Wedge((960, 330), 190, 0, 180, facecolor='#A98DF0')
    mouth_parts['inner'] = patches.Wedge((960, 340), 160, 0, 180, facecolor='#3B0A18')
    mouth_parts['tongue'] = patches.Ellipse((960, 360), 100, 30, facecolor='#F18DB0')
    mouth_parts['teeth'] = patches.Rectangle((800, 340), 320, 20, facecolor='white')
    mouth_parts['corner_l'] = patches.Circle((800, 340), 10, facecolor='#3B0A18')
    mouth_parts['corner_r'] = patches.Circle((1120, 340), 10, facecolor='#3B0A18')
    for part in mouth_parts.values():
        ax.add_patch(part)


left_star = ax.plot([], [], marker=(4, 1, 0), markersize=40, color='#B3D6FF')[0]
right_star = ax.plot([], [], marker=(4, 1, 0), markersize=20, color='#B3D6FF')[0]


def update(frame):
    alpha = 0.6 + 0.4 * np.sin(frame * 0.1)
    left_star.set_data(540, 920)
    left_star.set_alpha(alpha)
    right_star.set_data(1390, 930)
    right_star.set_alpha(1 - alpha)

    for i, (tear, (x0, y0, offset, row, direction, divergence)) in enumerate(zip(tears, tear_paths)):
        time_shift = (frame * 2 + offset + row * 30) % 2000
        x = x0 + direction * time_shift
        arc_height = 100 + row * 40
        arc_width = 700
        angle = np.pi * (time_shift / arc_width)
        y = y0 - arc_height * np.sin(angle) + divergence * time_shift * 0.2  # diverge vertically
        tear.center = (x, y)

    pulse = 1 + 0.03 * np.sin(frame * 0.3)
    mouth_parts['lip'].set_radius(190 * pulse)
    mouth_parts['inner'].set_radius(160 * pulse)
    mouth_parts['tongue'].width = 100 * pulse
    mouth_parts['tongue'].height = 30 * pulse
    mouth_parts['teeth'].set_bounds(800, 340, 320 * pulse, 20)
    mouth_parts['corner_l'].center = (800 - 10 * pulse, 340)
    mouth_parts['corner_r'].center = (1120 + 10 * pulse, 340)

    return [left_star, right_star] + tears + list(mouth_parts.values())


draw_eyes()
draw_mouth()
ani = FuncAnimation(fig, update, frames=300, interval=16, blit=True)
plt.show()
