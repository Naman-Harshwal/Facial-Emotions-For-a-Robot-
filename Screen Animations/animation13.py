import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider
import matplotlib.animation as animation

fig, ax = plt.subplots(figsize=(19.2, 10.8))  # Full HD
plt.subplots_adjust(bottom=0.25)
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.set_aspect('equal')
ax.axis('off')

# Cat face base
face = patches.Circle((960, 540), 400, facecolor='#ffcc99', edgecolor='black', linewidth=2)
ax.add_patch(face)

# Initial parameters
eye_radius = 60
eye_distance = 200
mouth_width = 200
mouth_height = 50

# Add eyes (left and right)
left_eye = patches.Circle((960 - eye_distance, 640), eye_radius, facecolor='white', edgecolor='black')
right_eye = patches.Circle((960 + eye_distance, 640), eye_radius, facecolor='white', edgecolor='black')
left_pupil = patches.Circle((960 - eye_distance, 640), eye_radius * 0.4, facecolor='black')
right_pupil = patches.Circle((960 + eye_distance, 640), eye_radius * 0.4, facecolor='black')
eye_shine_left = patches.Circle((960 - eye_distance - 15, 650), eye_radius * 0.15, color='white')
eye_shine_right = patches.Circle((960 + eye_distance - 15, 650), eye_radius * 0.15, color='white')

for part in [left_eye, right_eye, left_pupil, right_pupil, eye_shine_left, eye_shine_right]:
    ax.add_patch(part)

# Add smiling mouth using Bezier-like arc
mouth = patches.Arc((960, 450), mouth_width, mouth_height, theta1=180, theta2=0, lw=4)
ax.add_patch(mouth)

# Sliders
ax_eye = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_mouth = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_spacing = plt.axes([0.25, 0.05, 0.65, 0.03])

eye_slider = Slider(ax_eye, 'Eye Size', 20, 150, valinit=eye_radius)
mouth_slider = Slider(ax_mouth, 'Mouth Size', 50, 500, valinit=mouth_width)
spacing_slider = Slider(ax_spacing, 'Feature Spacing', 100, 500, valinit=eye_distance)

# Blinking logic
blink_state = [1]
def blink(frame):
    blink_phase = (frame % 60) / 60
    if blink_phase < 0.1 or 0.5 < blink_phase < 0.6:
        scale = 0.1  # Almost closed
    else:
        scale = 1.0
    blink_state[0] = scale

    for eye, pupil in [(left_eye, left_pupil), (right_eye, right_pupil)]:
        eye.height = eye_radius * 2 * scale
        pupil.height = eye_radius * 0.8 * scale
        pupil.center = (pupil.center[0], eye.center[1])

# Update features
def update(val):
    global eye_radius, mouth_width, eye_distance

    eye_radius = eye_slider.val
    mouth_width = mouth_slider.val
    eye_distance = spacing_slider.val

    # Update eyes
    left_eye.center = (960 - eye_distance, 640)
    right_eye.center = (960 + eye_distance, 640)
    left_eye.width = left_eye.height = eye_radius * 2
    right_eye.width = right_eye.height = eye_radius * 2

    left_pupil.center = (960 - eye_distance, 640)
    right_pupil.center = (960 + eye_distance, 640)
    left_pupil.width = left_pupil.height = eye_radius * 0.8
    right_pupil.width = right_pupil.height = eye_radius * 0.8

    eye_shine_left.center = (960 - eye_distance - 15, 650)
    eye_shine_right.center = (960 + eye_distance - 15, 650)

    # Update mouth
    mouth.center = (960, 450)
    mouth.width = mouth_width
    mouth.height = mouth_height

eye_slider.on_changed(update)
mouth_slider.on_changed(update)
spacing_slider.on_changed(update)

ani = animation.FuncAnimation(fig, blink, interval=50)

plt.show()
