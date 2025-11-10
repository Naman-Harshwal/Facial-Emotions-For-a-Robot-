import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import numpy as np

# Initial parameters
eye_radius = 140
pupil_radius = 70
iris_radius = 100
mouth_radius = 130
star_size = 40
inter_eye_distance = 520

# Setup the figure and axes
fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
plt.subplots_adjust(left=0.25, bottom=0.4)
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.axis('off')
fig.patch.set_facecolor('#1B1930')
ax.set_facecolor('#1B1930')

# Placeholder patches
eye_patches = []
mouth_patches = []
star_patches = []

# Draw eyes function
def draw_eyes():
    for patch in eye_patches:
        patch.remove()
    eye_patches.clear()
    
    left_eye_center = (960 - inter_eye_distance // 2, 650)
    right_eye_center = (960 + inter_eye_distance // 2, 650)

    for cx, cy in [left_eye_center, right_eye_center]:
        outer = patches.Circle((cx, cy), eye_radius, color='#E2F1FF')
        iris = patches.Circle((cx, cy), iris_radius, color='#60A4F9')
        pupil = patches.Circle((cx, cy), pupil_radius, color='black')
        sparkle = patches.Circle((cx + 55, cy + 55), eye_radius * 0.18, color='#E2F1FF')

        for part in [outer, iris, pupil, sparkle]:
            ax.add_patch(part)
            eye_patches.append(part)

# Draw realistic mouth
def draw_mouth():
    for patch in mouth_patches:
        patch.remove()
    mouth_patches.clear()

    # Lips
    lips = patches.Wedge((960, 380), mouth_radius, 180, 360, facecolor='#A98DF0')
    mouth_inner = patches.Wedge((960, 370), mouth_radius * 0.77, 180, 360, facecolor='#3B0A18')
    tongue = patches.Ellipse((960, 350), mouth_radius * 0.62, 40, facecolor='#F18DB0')

    # Curved teeth using a Wedge slightly smaller than inner mouth
    teeth = patches.Wedge((960, 370), mouth_radius * 0.77, 180, 360, facecolor='white')

    for part in [lips, teeth, mouth_inner, tongue]:
        ax.add_patch(part)
        mouth_patches.append(part)

# Draw stars
def draw_stars():
    for patch in star_patches:
        patch.remove()
    star_patches.clear()

    left = ax.plot([], [], marker=(4, 1, 0), markersize=star_size, color='#D8FFC7')[0]
    right = ax.plot([], [], marker=(4, 1, 0), markersize=star_size * 0.5, color='#D8FFC7')[0]

    star_patches.extend([left, right])
    return left, right

# Initial draw
left_star, right_star = draw_stars()
draw_eyes()
draw_mouth()

# Blinking control
blink_state = True
def blink(frame):
    global blink_state
    if frame % 30 == 0:
        blink_state = not blink_state
    for i, patch in enumerate(eye_patches):
        if i % 4 == 2:  # pupil
            patch.set_visible(blink_state)
        if i % 4 == 3:  # sparkle
            patch.set_visible(blink_state)

# Animation update
def update(frame):
    alpha = 0.5 + 0.5 * np.sin(frame * 0.6)
    left_star.set_data(540, 920)
    left_star.set_alpha(alpha)
    right_star.set_data(1390, 930)
    right_star.set_alpha(1 - alpha)
    blink(frame)
    return [left_star, right_star] + eye_patches

ani = FuncAnimation(fig, update, frames=np.arange(0, 300), interval=16, blit=True)

# Slider axes
ax_eye = plt.axes([0.25, 0.3, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_mouth = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_star = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_eye_dist = plt.axes([0.25, 0.15, 0.65, 0.03])

# Sliders
s_eye = Slider(ax_eye, 'Eye Size', 50, 200, valinit=eye_radius)
s_mouth = Slider(ax_mouth, 'Mouth Size', 50, 200, valinit=mouth_radius)
s_star = Slider(ax_star, 'Star Size', 10, 100, valinit=star_size)
s_eye_dist = Slider(ax_eye_dist, 'Eye Distance', 300, 800, valinit=inter_eye_distance)

# Slider update function
def update_all(val):
    global eye_radius, iris_radius, pupil_radius, mouth_radius, star_size, inter_eye_distance
    eye_radius = s_eye.val
    iris_radius = s_eye.val * 0.71
    pupil_radius = s_eye.val * 0.5
    mouth_radius = s_mouth.val
    star_size = s_star.val
    inter_eye_distance = int(s_eye_dist.val)

    draw_eyes()
    draw_mouth()
    draw_stars()

    fig.canvas.draw_idle()

s_eye.on_changed(update_all)
s_mouth.on_changed(update_all)
s_star.on_changed(update_all)
s_eye_dist.on_changed(update_all)

plt.show()
