import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import matplotlib.lines as mlines
import numpy as np

# Set up the figure and axes
fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.axis('off')

# Background color
fig.patch.set_facecolor('black')
ax.set_facecolor('#1B1930')

# Eye center positions
left_eye_center = [700, 650]
right_eye_center = [1220, 650]

# Draw eyes function with blinking and eyelashes at 12 o'clock

def draw_eyes(offset_x=0, offset_y=0, blink=1.0):
    eye_elements = []
    for (cx, cy) in [(left_eye_center[0] + offset_x, left_eye_center[1] + offset_y),
                     (right_eye_center[0] + offset_x, right_eye_center[1] + offset_y)]:
        # Elliptical eye components
        eye_outer = patches.Ellipse((cx, cy), 280, 280 * blink, color='#E2F1FF')
        eye_blue = patches.Ellipse((cx, cy), 200, 200 * blink, color='#60A4F9')
        eye_black = patches.Ellipse((cx, cy), 140, 140 * blink, color='black')
        sparkle_dot = patches.Ellipse((cx + 55, cy + 55 * blink), 50, 50 * blink, color='#E2F1FF')

        for patch in [eye_outer, eye_blue, eye_black, sparkle_dot]:
            ax.add_patch(patch)
            eye_elements.append(patch)

        # Add vertical eyelashes at 12 o'clock position (90 degrees)
        lash_radius = 140 * blink  # slightly outside the pupil
        angle = np.radians(90)
        for i in range(-4, 5):  # 9 lashes
            spread = i * 5 * np.pi / 180  # slight angular offset in radians
            x_start = cx + np.cos(angle + spread) * lash_radius
            y_start = cy + np.sin(angle + spread) * lash_radius
            x_end = x_start + np.cos(angle + spread) * 12
            y_end = y_start + np.sin(angle + spread) * 12 * blink
            lash = mlines.Line2D([x_start, x_end], [y_start, y_end], color='white', linewidth=2)
            ax.add_line(lash)
            eye_elements.append(lash)

    return eye_elements

# Initial eye drawing
eye_patches = draw_eyes()

# Draw mouth variations
mouth_patches = []

def draw_mouth(emotion):
    global mouth_patches
    for patch in mouth_patches:
        patch.remove()
    mouth_patches = []

    if emotion == 'happy':
        lip_outer = patches.Wedge((960, 380), 130, 180, 360, facecolor='#A98DF0')
        mouth_inner = patches.Wedge((960, 370), 100, 180, 360, facecolor='#3B0A18')
        tongue = patches.Ellipse((960, 350), 80, 40, facecolor='#F18DB0')
        teeth = patches.Rectangle((860, 370), 200, 20, facecolor='white')
        mouth_patches = [lip_outer, mouth_inner, tongue, teeth]
    elif emotion == 'sad':
        lip_outer = patches.Wedge((960, 300), 130, 0, 180, facecolor='#A98DF0')
        mouth_inner = patches.Wedge((960, 310), 100, 0, 180, facecolor='#3B0A18')
        mouth_patches = [lip_outer, mouth_inner]
    elif emotion == 'surprised':
        mouth = patches.Ellipse((960, 380), 120, 160, facecolor='#3B0A18')
        mouth_patches = [mouth]
    elif emotion == 'sleeping':
        mouth = patches.Ellipse((960, 360), 100, 20, facecolor='#A98DF0')
        mouth_patches = [mouth]
    elif emotion == 'joy':
        arc = patches.Arc((960, 380), 240, 140, angle=0, theta1=0, theta2=180, linewidth=8, color='#F18DB0')
        mouth_patches = [arc]
    elif emotion == 'emotional':
        arc = patches.Arc((960, 360), 200, 120, angle=0, theta1=0, theta2=180, linewidth=8, color='white')
        mouth_patches = [arc]

    for patch in mouth_patches:
        ax.add_patch(patch)

# Initial mouth draw
draw_mouth('happy')

# Sparkling stars
left_star = ax.plot([], [], marker=(4, 1, 0), markersize=40, color='#D8FFC7')[0]
right_star = ax.plot([], [], marker=(4, 1, 0), markersize=20, color='#D8FFC7')[0]

# Emotion and corresponding eye movement
emotion_cycle = [
    ('happy', (0, 0)),
    ('sad', (0, -20)),
    ('joy', (0, 10)),
    ('sleeping', (0, -30)),
    ('surprised', (0, 0)),
    ('emotional', (-10, 10))
]

frames_per_emotion = 300  # 5 seconds at 60 FPS
blink_period = 120  # frames

def blink_factor(frame):
    cycle_frame = frame % blink_period
    if cycle_frame < 10:
        return 1 - (cycle_frame / 10)  # Closing
    elif 10 <= cycle_frame < 20:
        return (cycle_frame - 10) / 10  # Opening
    return 1.0  # Fully open

def update(frame):
    global eye_patches
    emotion_idx = frame // frames_per_emotion % len(emotion_cycle)
    emotion, eye_offset = emotion_cycle[emotion_idx]
    draw_mouth(emotion)

    for patch in eye_patches:
        patch.remove()
    blink = blink_factor(frame)
    eye_patches = draw_eyes(*eye_offset, blink=blink)

    alpha = 0.5 + 0.5 * np.sin(frame * 0.1)
    left_star.set_data(540, 920)
    left_star.set_alpha(alpha)
    right_star.set_data(1390, 930)
    right_star.set_alpha(1 - alpha)

    return eye_patches + mouth_patches + [left_star, right_star]

# Create high-FPS animation
ani = FuncAnimation(fig, update, frames=np.arange(0, frames_per_emotion * len(emotion_cycle)), interval=16, blit=True)

plt.show()
