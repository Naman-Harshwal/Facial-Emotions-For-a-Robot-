import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import time
from matplotlib.widgets import Button
from matplotlib.path import Path
import matplotlib.patheffects as path_effects
import matplotlib

# Force matplotlib to use TkAgg backend to avoid Wayland issues
matplotlib.use('TkAgg')

# Set up the figure with dark background
fig = plt.figure(figsize=(10, 8), facecolor='#0c0c0c')
fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1)
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
ax = plt.subplot(gs[0])
ax_controls = plt.subplot(gs[1])

# Configure axes
ax.set_facecolor('#0c0c0c')
ax.axis('off')
ax.set_xlim(-6, 6)
ax.set_ylim(-5, 5)
ax.set_aspect('equal')

ax_controls.set_facecolor('#0c0c0c')
ax_controls.set_xlim(0, 10)
ax_controls.set_ylim(0, 10)
ax_controls.axis('off')

# Global variables
patches_objs = []
eyes_offset = 2.2
reflection_offset = 0.45
current_emotion = "happy"  # Initialize with default emotion
current_eye_state = "neutral"
blink_factor = 1.0
look_x, look_y = 0.0, 0.0
sparkle = False
last_blink_time = time.time()
blink_duration = 0.1
blink_state = "open"
ear_tilt = 0
whisker_wiggle = 0
pupil_size = 0.8
eye_highlight = True
emotion_duration = 0
frame_count = 0

# Emotion colors
emotion_colors = {
    "happy": "#FFD700",       # Gold/yellow
    "sad": "#4169E1",         # Royal blue
    "angry": "#FF4500",       # Orange red
    "surprised": "#FF69B4",   # Hot pink
    "sleepy": "#9370DB",      # Medium purple
    "neutral": "#20B2AA",     # Light sea green
    "playful": "#7CFC00"      # Lawn green
}

# Draw a star shape for sparkles
def draw_star(x, y, size, color):
    return patches.RegularPolygon((x, y), numVertices=5, radius=size, 
                                 orientation=np.pi/5, color=color)

# Draw an eye with parameters
def draw_eye(cx, cy, blink_factor, look_x, look_y, sparkle, emotion):
    components = []
    
    # Eye white - changes color with emotion
    eye_white = patches.Circle((cx, cy), 1.5, color=emotion_colors[emotion], alpha=0.4)
    
    # Eye iris - changes color with emotion
    iris_color = emotion_colors[emotion]
    if emotion == "angry":
        iris_color = "#FF0000"  # Red for angry
    
    eye_iris = patches.Circle((cx + look_x, cy + look_y), 1.0 * blink_factor, 
                             color=iris_color, alpha=0.8)
    
    # Pupil - size changes with emotion
    global pupil_size
    pupil_color = '#121212'
    if emotion == "surprised":
        pupil_size = min(0.6, pupil_size + 0.01)
    elif emotion == "sleepy":
        pupil_size = max(0.4, pupil_size - 0.01)
    else:
        pupil_size = 0.5
    
    eye_pupil = patches.Circle((cx + look_x, cy + look_y), pupil_size * blink_factor, 
                              color=pupil_color)
    
    # Eye highlight
    if eye_highlight:
        eye_glint = patches.Circle((cx + reflection_offset + look_x*0.3, 
                                  cy + reflection_offset + look_y*0.3), 
                                  0.3 * blink_factor, color='white')
        components.append(eye_glint)
    
    # Eyelid - changes with emotion and blink
    lid_color = "#F0E68C"  # Khaki
    if emotion == "sleepy":
        lid_color = "#8B4513"  # Saddle brown
    
    eyelid = patches.Arc((cx, cy), 3.0, 3.0, angle=0, 
                        theta1=180, theta2=360, linewidth=8, 
                        color=lid_color, alpha=1 - blink_factor)
    
    components += [eye_white, eye_iris, eye_pupil, eyelid]
    
    # Sparkle effect
    if sparkle:
        components.append(draw_star(cx + 0.9, cy + 1.1, 0.25, '#b9ffbf'))
        components.append(draw_star(cx - 0.9, cy - 1.1, 0.2, '#b9ffbf'))
    
    return components

# Draw the mouth with emotion-based expressions
def draw_mouth(emotion):
    components = []
    mouth_color = emotion_colors[emotion]
    linewidth = 6
    
    if emotion == "happy":
        # Smile with tongue
        components.append(patches.Arc((0, -2.5), 3.0, 2.0, angle=0, 
                                     theta1=0, theta2=180, linewidth=linewidth, 
                                     color=mouth_color))
        components.append(patches.Wedge((0, -3.0), 1.0, 0, 180, 
                                       facecolor='#FF69B4', alpha=0.7))
    elif emotion == "sad":
        # Sad frown
        components.append(patches.Arc((0, -3.0), 3.0, 2.0, angle=0, 
                                     theta1=180, theta2=360, linewidth=linewidth, 
                                     color=mouth_color))
        # Tear drops
        components.append(patches.Ellipse((-1.5, -3.5), 0.3, 0.6, 
                                        angle=30, color='#87CEEB', alpha=0.7))
        components.append(patches.Ellipse((1.5, -3.5), 0.3, 0.6, 
                                        angle=-30, color='#87CEEB', alpha=0.7))
    elif emotion == "angry":
        # Angry mouth
        verts = [
            (-1.5, -2.5), (-0.5, -3.5), (0.5, -3.5), (1.5, -2.5),
            (1.0, -3.0), (0.0, -3.7), (-1.0, -3.0), (-1.5, -2.5)
        ]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, 
                Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        path = Path(verts, codes)
        components.append(patches.PathPatch(path, facecolor='none', 
                                          edgecolor=mouth_color, lw=linewidth))
        # Angry teeth
        for i in range(-1, 2):
            components.append(patches.Rectangle((i*0.7-0.2, -3.5), 0.4, 0.4, 
                                              angle=0, color='white', alpha=0.9))
    elif emotion == "surprised":
        # Surprised "O" mouth
        components.append(patches.Circle((0, -3.0), 1.2, 
                                       facecolor='none', edgecolor=mouth_color, 
                                       linewidth=linewidth))
    elif emotion == "sleepy":
        # Sleepy mouth (zzz)
        components.append(patches.Arc((0, -3.0), 2.0, 1.0, angle=0, 
                                     theta1=180, theta2=360, linewidth=linewidth-2, 
                                     color=mouth_color))
        # ZZZ bubbles
        components.append(patches.Circle((1.5, -2.0), 0.3, color='#87CEEB', alpha=0.6))
        components.append(patches.Circle((2.0, -1.5), 0.4, color='#87CEEB', alpha=0.4))
        components.append(patches.Circle((2.5, -1.0), 0.5, color='#87CEEB', alpha=0.2))
    elif emotion == "neutral":
        # Straight line mouth
        components.append(patches.FancyArrowPatch((-1.5, -3.0), (1.5, -3.0), 
                                         mutation_scale=10, color=mouth_color, 
                                         arrowstyle='-', linewidth=linewidth))
    elif emotion == "playful":
        # Playful winky mouth
        verts = [
            (-1.5, -3.0), (0, -2.0), (1.5, -3.0)
        ]
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        path = Path(verts, codes)
        components.append(patches.PathPatch(path, facecolor='none', 
                                          edgecolor=mouth_color, lw=linewidth))
    
    return components

# Draw cat ears with emotion-based tilt
def draw_ears(emotion, tilt):
    components = []
    ear_color = "#F0E68C"  # Khaki
    inner_ear_color = "#FFB6C1"  # Light pink
    
    # Left ear
    left_ear_points = [(-3.5, 1.5), (-2.0, 3.0 + tilt), (-0.5, 1.5)]
    left_ear = patches.Polygon(left_ear_points, closed=True, color=ear_color)
    left_inner_ear = patches.Polygon([
        (-3.0, 1.7), (-2.0, 2.7 + tilt*0.8), (-1.0, 1.7)
    ], closed=True, color=inner_ear_color)
    
    # Right ear
    right_ear_points = [(3.5, 1.5), (2.0, 3.0 - tilt), (0.5, 1.5)]
    right_ear = patches.Polygon(right_ear_points, closed=True, color=ear_color)
    right_inner_ear = patches.Polygon([
        (3.0, 1.7), (2.0, 2.7 - tilt*0.8), (1.0, 1.7)
    ], closed=True, color=inner_ear_color)
    
    # Emotion-based ear adjustments
    if emotion == "angry":
        # Angry flattened ears
        left_ear_points[1] = (-2.0, 2.0)
        right_ear_points[1] = (2.0, 2.0)
        ear_color = "#8B4513"  # Darker for angry
    elif emotion == "surprised":
        # Surprised upright ears
        left_ear_points[1] = (-2.0, 3.5)
        right_ear_points[1] = (2.0, 3.5)
    
    components += [left_ear, left_inner_ear, right_ear, right_inner_ear]
    return components

# Draw cat face outline
def draw_face(emotion):
    face_color = "#F0E68C"  # Khaki
    if emotion == "angry":
        face_color = "#CD853F"  # Peru (darker)
    elif emotion == "sleepy":
        face_color = "#D2B48C"  # Tan
    
    return [patches.Circle((0, 0), 3.5, color=face_color)]

# Draw whiskers with wiggle effect
def draw_whiskers(emotion, wiggle):
    components = []
    whisker_color = "#D3D3D3"  # Light gray
    
    # Left whiskers
    for i in range(3):
        y_offset = i * 0.5 - 0.5
        wiggle_offset = wiggle * (1 if i == 1 else 0.5)  # Middle whisker wiggles more
        whisker = patches.FancyArrowPatch(
            (-1.5, -1.0 + y_offset), 
            (-4.5 - wiggle_offset, -1.0 + y_offset + wiggle_offset*0.3),
            mutation_scale=8, color=whisker_color, arrowstyle='-', 
            linewidth=1.5 + i*0.3
        )
        components.append(whisker)
    
    # Right whiskers
    for i in range(3):
        y_offset = i * 0.5 - 0.5
        wiggle_offset = wiggle * (1 if i == 1 else 0.5)  # Middle whisker wiggles more
        whisker = patches.FancyArrowPatch(
            (1.5, -1.0 + y_offset), 
            (4.5 + wiggle_offset, -1.0 + y_offset + wiggle_offset*0.3),
            mutation_scale=8, color=whisker_color, arrowstyle='-', 
            linewidth=1.5 + i*0.3
        )
        components.append(whisker)
    
    return components

# Draw eyebrows with emotion-based expressions
def draw_eyebrows(emotion):
    components = []
    brow_color = "#8B4513"  # Saddle brown
    
    # Left eyebrow
    if emotion == "angry":
        # Angry V-shaped eyebrows
        left_brow = patches.FancyArrowPatch(
            (-2.8, 1.0), (-1.0, 0.5), mutation_scale=15, 
            color=brow_color, arrowstyle='-', linewidth=4
        )
        right_brow = patches.FancyArrowPatch(
            (2.8, 1.0), (1.0, 0.5), mutation_scale=15, 
            color=brow_color, arrowstyle='-', linewidth=4
        )
    elif emotion == "sad":
        # Sad upward eyebrows
        left_brow = patches.FancyArrowPatch(
            (-3.0, 0.8), (-1.5, 1.2), mutation_scale=15, 
            color=brow_color, arrowstyle='-', linewidth=3
        )
        right_brow = patches.FancyArrowPatch(
            (3.0, 0.8), (1.5, 1.2), mutation_scale=15, 
            color=brow_color, arrowstyle='-', linewidth=3
        )
    elif emotion == "surprised":
        # Surprised curved eyebrows
        left_brow = patches.Arc((-2.0, 1.5), 1.5, 0.8, angle=0, 
                               theta1=0, theta2=180, linewidth=3, color=brow_color)
        right_brow = patches.Arc((2.0, 1.5), 1.5, 0.8, angle=0, 
                                theta1=0, theta2=180, linewidth=3, color=brow_color)
    else:
        # Neutral eyebrows
        left_brow = patches.FancyArrowPatch(
            (-3.0, 1.0), (-1.5, 1.0), mutation_scale=15, 
            color=brow_color, arrowstyle='-', linewidth=3
        )
        right_brow = patches.FancyArrowPatch(
            (3.0, 1.0), (1.5, 1.0), mutation_scale=15, 
            color=brow_color, arrowstyle='-', linewidth=3
        )
    
    components += [left_brow, right_brow]
    return components

# Add side sparkles to background
def draw_background_sparkles(emotion):
    sparkles = []
    num_sparkles = 15 if emotion == "playful" else 8
    
    for _ in range(num_sparkles):
        x = np.random.uniform(-5.5, 5.5)
        y = np.random.uniform(-4.5, 4.5)
        size = np.random.uniform(0.1, 0.3)
        alpha = np.random.uniform(0.3, 0.8)
        color = emotion_colors[emotion]
        
        # Create sparkle with glow effect
        sparkle = patches.RegularPolygon((x, y), numVertices=5, 
                                       radius=size*1.5, orientation=np.pi/5, 
                                       color=color, alpha=alpha*0.3)
        sparkles.append(sparkle)
        
        sparkle = patches.RegularPolygon((x, y), numVertices=5, 
                                       radius=size, orientation=np.pi/5, 
                                       color='white', alpha=alpha)
        sparkles.append(sparkle)
    
    return sparkles

# Draw emotion indicator
def draw_emotion_indicator(emotion):
    ax_controls.clear()
    ax_controls.set_xlim(0, 10)
    ax_controls.set_ylim(0, 10)
    ax_controls.axis('off')
    
    # Draw emotion name
    emotion_text = ax_controls.text(5, 7, emotion.capitalize(), 
                                  fontsize=20, color=emotion_colors[emotion],
                                  ha='center', va='center')
    emotion_text.set_path_effects([path_effects.withStroke(linewidth=3, 
                                                         foreground='black')])
    
    # Draw emotion color bar
    color_bar = patches.Rectangle((2, 4), 6, 1.5, color=emotion_colors[emotion], alpha=0.7)
    ax_controls.add_patch(color_bar)
    
    # Draw frame counter
    frame_text = ax_controls.text(5, 2, f"Frame: {frame_count}", 
                                fontsize=14, color='white', 
                                ha='center', va='center')
    
    # Draw controls info
    ctrl_text = ax_controls.text(5, 0.5, 
                                "Controls: 1-Happy  2-Sad  3-Angry  4-Surprised  5-Sleepy  6-Neutral  7-Playful  S-Sparkle  B-Blink",
                                fontsize=10, color='#AAAAAA', ha='center', va='center')
    
    return [color_bar, emotion_text, frame_text, ctrl_text]

# Animation function
def animate(frame):
    global patches_objs, blink_factor, blink_state, last_blink_time, sparkle
    global look_x, look_y, current_eye_state, ear_tilt, whisker_wiggle
    global pupil_size, eye_highlight, emotion_duration, frame_count, current_emotion
    
    frame_count = frame
    
    # Clear previous frame
    for p in patches_objs:
        p.remove()
    patches_objs.clear()
    
    # Automatic blinking
    current_time = time.time()
    if current_time - last_blink_time > 3:  # Blink every 3 seconds
        blink_state = "closing"
        last_blink_time = current_time
    
    # Handle blinking states
    if blink_state == "closing":
        blink_factor = max(0.1, blink_factor - 0.15)
        if blink_factor <= 0.1:
            blink_state = "opening"
    elif blink_state == "opening":
        blink_factor = min(1.0, blink_factor + 0.15)
        if blink_factor >= 1.0:
            blink_state = "open"
    
    # Automatic emotion changes
    emotion_duration += 1
    if emotion_duration > 200:  # Change emotion every 200 frames
        emotions = list(emotion_colors.keys())
        current_emotion = np.random.choice(emotions)
        emotion_duration = 0
    
    # Automatic eye movement
    if frame % 60 == 0:
        eye_states = ["left", "right", "up", "down", "neutral"]
        current_eye_state = np.random.choice(eye_states)
    
    # Update eye position based on state
    if current_eye_state == "left":
        look_x = max(-0.8, look_x - 0.05)
        look_y *= 0.9  # Dampen vertical movement
    elif current_eye_state == "right":
        look_x = min(0.8, look_x + 0.05)
        look_y *= 0.9  # Dampen vertical movement
    elif current_eye_state == "up":
        look_y = min(0.8, look_y + 0.05)
        look_x *= 0.9  # Dampen horizontal movement
    elif current_eye_state == "down":
        look_y = max(-0.8, look_y - 0.05)
        look_x *= 0.9  # Dampen horizontal movement
    else:  # neutral
        look_x *= 0.9
        look_y *= 0.9
    
    # Sparkle effect (random or triggered)
    if sparkle:
        sparkle = (frame % 30) < 15  # Sparkle for 15 frames
    else:
        sparkle = (frame % 300) < 5  # Occasional random sparkle
    
    # Ear tilt animation (subtle movement)
    ear_tilt = 0.5 * np.sin(frame * 0.05)
    
    # Whisker wiggle animation
    whisker_wiggle = 0.5 * np.sin(frame * 0.1)
    
    # Eye highlight effect
    eye_highlight = (frame % 100) < 95  # Occasionally remove highlight
    
    # Draw face components
    face = draw_face(current_emotion)
    ears = draw_ears(current_emotion, ear_tilt)
    eyebrows = draw_eyebrows(current_emotion)
    
    # Eyes
    left_eye_center = (-eyes_offset, 0)
    right_eye_center = (eyes_offset, 0)
    eyes = draw_eye(*left_eye_center, blink_factor, look_x, look_y, sparkle, current_emotion) + \
           draw_eye(*right_eye_center, blink_factor, look_x, look_y, sparkle, current_emotion)
    
    # Mouth
    mouth = draw_mouth(current_emotion)
    
    # Whiskers
    whiskers = draw_whiskers(current_emotion, whisker_wiggle)
    
    # Background sparkles
    background = draw_background_sparkles(current_emotion)
    
    # Emotion indicator
    indicator = draw_emotion_indicator(current_emotion)
    
    # Combine and draw
    for element in face + ears + eyebrows + eyes + mouth + whiskers + background + indicator:
        if isinstance(element, list):
            for el in element:
                if ax == el.axes or ax_controls == el.axes:
                    patches_objs.append(el)
        else:
            if ax == element.axes or ax_controls == element.axes:
                patches_objs.append(element)
    
    return patches_objs

# Button click handlers
def set_emotion(emotion):
    global current_emotion, emotion_duration
    current_emotion = emotion
    emotion_duration = 0

def on_happy_click(event):
    set_emotion("happy")

def on_sad_click(event):
    set_emotion("sad")

def on_angry_click(event):
    set_emotion("angry")

def on_surprised_click(event):
    set_emotion("surprised")

def on_sleepy_click(event):
    set_emotion("sleepy")

def on_neutral_click(event):
    set_emotion("neutral")

def on_playful_click(event):
    set_emotion("playful")

def on_sparkle_click(event):
    global sparkle
    sparkle = True

def on_blink_click(event):
    global blink_state, last_blink_time
    blink_state = "closing"
    last_blink_time = time.time()

# Create control buttons
button_props = dict(color='#333333', hovercolor='#555555')
button_y = 7
button_height = 1.5
button_width = 1.2

ax_happy = plt.axes([0.1, 0.05, button_width, button_height])
btn_happy = Button(ax_happy, 'Happy', color='#FFD700')
btn_happy.on_clicked(on_happy_click)

ax_sad = plt.axes([0.3, 0.05, button_width, button_height])
btn_sad = Button(ax_sad, 'Sad', color='#4169E1')
btn_sad.on_clicked(on_sad_click)

ax_angry = plt.axes([0.5, 0.05, button_width, button_height])
btn_angry = Button(ax_angry, 'Angry', color='#FF4500')
btn_angry.on_clicked(on_angry_click)

ax_surprised = plt.axes([0.7, 0.05, button_width, button_height])
btn_surprised = Button(ax_surprised, 'Surprised', color='#FF69B4')
btn_surprised.on_clicked(on_surprised_click)

ax_sleepy = plt.axes([0.1, 0.01, button_width, button_height])
btn_sleepy = Button(ax_sleepy, 'Sleepy', color='#9370DB')
btn_sleepy.on_clicked(on_sleepy_click)

ax_neutral = plt.axes([0.3, 0.01, button_width, button_height])
btn_neutral = Button(ax_neutral, 'Neutral', color='#20B2AA')
btn_neutral.on_clicked(on_neutral_click)

ax_playful = plt.axes([0.5, 0.01, button_width, button_height])
btn_playful = Button(ax_playful, 'Playful', color='#7CFC00')
btn_playful.on_clicked(on_playful_click)

ax_sparkle = plt.axes([0.7, 0.01, button_width, button_height])
btn_sparkle = Button(ax_sparkle, 'Sparkle', color='white')
btn_sparkle.on_clicked(on_sparkle_click)

ax_blink = plt.axes([0.85, 0.03, button_width, button_height*1.5])
btn_blink = Button(ax_blink, 'BLINK', color='#FF6347')
btn_blink.on_clicked(on_blink_click)

# Set button label colors
for btn in [btn_happy, btn_sad, btn_angry, btn_surprised, 
           btn_sleepy, btn_neutral, btn_playful, btn_sparkle, btn_blink]:
    btn.label.set_color('white')
    btn.label.set_fontweight('bold')

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=10000, interval=30, blit=True)

# Add keyboard controls
def on_key(event):
    global current_emotion, sparkle, blink_state, last_blink_time
    
    if event.key == '1':
        set_emotion("happy")
    elif event.key == '2':
        set_emotion("sad")
    elif event.key == '3':
        set_emotion("angry")
    elif event.key == '4':
        set_emotion("surprised")
    elif event.key == '5':
        set_emotion("sleepy")
    elif event.key == '6':
        set_emotion("neutral")
    elif event.key == '7':
        set_emotion("playful")
    elif event.key == 's':
        sparkle = True
    elif event.key == 'b':
        blink_state = "closing"
        last_blink_time = time.time()

fig.canvas.mpl_connect('key_press_event', on_key)

plt.tight_layout()
plt.show()