import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
import json

fig, ax = plt.subplots(figsize=(20, 16))  # Large figure size for high resolution
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')
ax.axis('off')
ax.set_xlim(-800, 800)  # Very large axis limits
ax.set_ylim(-800, 800)
ax.set_aspect('equal')

# Create sliders for different parameters
slider_ax_eye_dist = plt.axes([0.1, 0.02, 0.8, 0.03], facecolor='#222222')
slider_ax_mouth_dist = plt.axes([0.1, 0.06, 0.8, 0.03], facecolor='#222222')
slider_ax_eye_size = plt.axes([0.1, 0.10, 0.8, 0.03], facecolor='#222222')
slider_ax_mouth_size = plt.axes([0.1, 0.14, 0.8, 0.03], facecolor='#222222')
slider_ax_eye_vert = plt.axes([0.1, 0.18, 0.8, 0.03], facecolor='#222222')

# Create a button to save parameters
button_ax = plt.axes([0.1, 0.22, 0.1, 0.04])
save_button = Button(button_ax, 'Save Parameters', color='#222222', hovercolor='#444444')

# Initialize parameters directly in the script
saved_params = {
    'eye_distance': 800.0,
    'mouth_distance': 616.23,
    'eye_size': 316.3546875,
    'mouth_size': 315.60562500000003,
    'eye_vert': 320.18479033404424
}

eye_distance_slider = Slider(slider_ax_eye_dist, 'Eye Distance', 1.0, 800.0, valinit=saved_params['eye_distance'])
mouth_distance_slider = Slider(slider_ax_mouth_dist, 'Mouth Distance', 1.0, 800.0, valinit=saved_params['mouth_distance'])
eye_size_slider = Slider(slider_ax_eye_size, 'Eye Size', 0.5, 400.0, valinit=saved_params['eye_size'])
mouth_size_slider = Slider(slider_ax_mouth_size, 'Mouth Size', 0.5, 400.0, valinit=saved_params['mouth_size'])
eye_vert_slider = Slider(slider_ax_eye_vert, 'Eye Vertical Position', -400.0, 400.0, valinit=saved_params['eye_vert'])

patches_objs = []

def draw_eye(cx, cy, size, blink, blink_progress):
    eye_elements = []
    # White sclera
    eye_elements.append(patches.Circle((cx, cy), size * 1.2, color='#e6f9ff'))
    # Iris
    eye_elements.append(patches.Circle((cx, cy), size * 1.0, color='#5ab0ff'))
    # Pupil
    eye_elements.append(patches.Circle((cx, cy), size * 0.6, color='#121212'))
    # Highlight
    eye_elements.append(patches.Circle((cx + size * 0.3, cy + size * 0.3), size * 0.2, color='white'))
    
    if blink:
        eye_elements.append(patches.Rectangle((cx - size * 1.2, cy + size * 1.2 - blink_progress), 
                                             size * 2.4, blink_progress * 2, color='black'))
    
    return eye_elements

def draw_realistic_smile(frame, size):
    mouth_elements = []
    # White mouth semi-circle
    mouth_elements.append(patches.Wedge((0, -mouth_distance + eye_vert), size * 1.3, 180, 360, 
                                      facecolor='white', edgecolor='white'))
    # Tongue animation (pulsing)
    tongue_size = size * 1.0 + 0.1 * np.sin(frame * 0.1)
    mouth_elements.append(patches.Wedge((0, -mouth_distance + eye_vert), tongue_size, 180, 360, 
                                      facecolor='#d1a6f9', edgecolor='#d1a6f9'))
    return mouth_elements

def animate_smile(frame):
    global patches_objs, eye_distance, mouth_distance, eye_size, mouth_size, eye_vert
    for p in patches_objs:
        p.remove()
    patches_objs.clear()

    # Update parameters from sliders
    eye_distance = eye_distance_slider.val
    mouth_distance = mouth_distance_slider.val
    eye_size = eye_size_slider.val
    mouth_size = mouth_size_slider.val
    eye_vert = eye_vert_slider.val

    blink_phase = frame % 60
    blink = False
    blink_progress = 0
    if blink_phase < 10:
        blink = True
        blink_progress = (10 - blink_phase) * 0.3 * eye_size
    elif blink_phase > 50:
        blink = True
        blink_progress = (blink_phase - 50) * 0.3 * eye_size

    left_eye = draw_eye(-eye_distance/2, 0.5 + eye_vert, eye_size, blink, blink_progress)
    right_eye = draw_eye(eye_distance/2, 0.5 + eye_vert, eye_size, blink, blink_progress)
    mouth = draw_realistic_smile(frame, mouth_size)

    for item in left_eye + right_eye + mouth:
        ax.add_patch(item)
        patches_objs.append(item)
    
    return patches_objs

def save_parameters(event):
    params = {
        'eye_distance': eye_distance_slider.val,
        'mouth_distance': mouth_distance_slider.val,
        'eye_size': eye_size_slider.val,
        'mouth_size': mouth_size_slider.val,
        'eye_vert': eye_vert_slider.val
    }
    with open('parameters.json', 'w') as f:
        json.dump(params, f)
    print("Parameters saved to parameters.json")

save_button.on_clicked(save_parameters)

ani = animation.FuncAnimation(fig, animate_smile, frames=1000, interval=16, blit=True)

plt.tight_layout()
plt.subplots_adjust(bottom=0.25)
plt.show()