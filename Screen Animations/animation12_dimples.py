import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
import json

# Set up the figure and axes
fig, ax = plt.subplots(figsize=(16, 9))  # 1920x1080 aspect ratio
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')
ax.axis('off')
ax.set_xlim(-1920, 1920)  # Full HD width
ax.set_ylim(-1080, 1080)  # Full HD height
ax.set_aspect('equal')

# Create sliders in the top right corner with reduced size
slider_width = 0.2  # Width of each slider
slider_height = 0.03
slider_left = 0.75  # Start position for sliders on the right
slider_vertical_spacing = 0.08

# Sliders for main parameters
slider_ax_face_size = plt.axes([slider_left, 0.95 - 0 * slider_vertical_spacing, slider_width, slider_height], facecolor='#222222')
slider_ax_eye_dist = plt.axes([slider_left, 0.95 - 1 * slider_vertical_spacing, slider_width, slider_height], facecolor='#222222')
slider_ax_mouth_dist = plt.axes([slider_left, 0.95 - 2 * slider_vertical_spacing, slider_width, slider_height], facecolor='#222222')
slider_ax_eye_size = plt.axes([slider_left, 0.95 - 3 * slider_vertical_spacing, slider_width, slider_height], facecolor='#222222')
slider_ax_mouth_size = plt.axes([slider_left, 0.95 - 4 * slider_vertical_spacing, slider_width, slider_height], facecolor='#222222')
slider_ax_eye_vert = plt.axes([slider_left, 0.95 - 5 * slider_vertical_spacing, slider_width, slider_height], facecolor='#222222')

# Sliders for dimple parameters
slider_ax_dimple_h = plt.axes([slider_left, 0.95 - 6 * slider_vertical_spacing, slider_width, slider_height], facecolor='#222222')
slider_ax_dimple_v = plt.axes([slider_left, 0.95 - 7 * slider_vertical_spacing, slider_width, slider_height], facecolor='#222222')
slider_ax_dimple_dist = plt.axes([slider_left, 0.95 - 8 * slider_vertical_spacing, slider_width, slider_height], facecolor='#222222')
slider_ax_left_dimple_rot = plt.axes([slider_left, 0.95 - 9 * slider_vertical_spacing, slider_width, slider_height], facecolor='#222222')
slider_ax_right_dimple_rot = plt.axes([slider_left, 0.95 - 10 * slider_vertical_spacing, slider_width, slider_height], facecolor='#222222')

# Create a button to save parameters
button_ax = plt.axes([slider_left, 0.95 - 11 * slider_vertical_spacing, slider_width, slider_height*2])
save_button = Button(button_ax, 'Save Parameters', color='#222222', hovercolor='#444444')

# Initialize parameters
saved_params = {
    'face_size': 1.0,
    'eye_distance': 800.0,
    'mouth_distance': 616.23,
    'eye_size': 316.3546875,
    'mouth_size': 315.60562500000003,
    'eye_vert': 320.18479033404424,
    'dimple_h': 0.0,
    'dimple_v': 0.0,
    'dimple_dist': 200.0,
    'left_dimple_rot': 0.0,
    'right_dimple_rot': 0.0
}

# Create sliders with initial values from saved parameters
face_size_slider = Slider(slider_ax_face_size, 'Face Size', 0.1, 2.0, valinit=saved_params['face_size'])
eye_distance_slider = Slider(slider_ax_eye_dist, 'Eye Distance', 1.0, 800.0, valinit=saved_params['eye_distance'])
mouth_distance_slider = Slider(slider_ax_mouth_dist, 'Mouth Distance', 1.0, 800.0, valinit=saved_params['mouth_distance'])
eye_size_slider = Slider(slider_ax_eye_size, 'Eye Size', 0.5, 400.0, valinit=saved_params['eye_size'])
mouth_size_slider = Slider(slider_ax_mouth_size, 'Mouth Size', 0.5, 400.0, valinit=saved_params['mouth_size'])
eye_vert_slider = Slider(slider_ax_eye_vert, 'Eye Vertical Position', -400.0, 400.0, valinit=saved_params['eye_vert'])

# Dimple control sliders
dimple_h_slider = Slider(slider_ax_dimple_h, 'Dimple Horizontal', -100.0, 100.0, valinit=saved_params['dimple_h'])
dimple_v_slider = Slider(slider_ax_dimple_v, 'Dimple Vertical', -800.0, 800.0, valinit=saved_params['dimple_v'])
dimple_dist_slider = Slider(slider_ax_dimple_dist, 'Dimple Distance', 0.0, 200.0, valinit=saved_params['dimple_dist'])
left_dimple_rot_slider = Slider(slider_ax_left_dimple_rot, 'Left Dimple Rotation', -1440.0, 1440.0, valinit=saved_params['left_dimple_rot'])
right_dimple_rot_slider = Slider(slider_ax_right_dimple_rot, 'Right Dimple Rotation', -1440.0, 1440.0, valinit=saved_params['right_dimple_rot'])

patches_objs = []

def draw_eye(cx, cy, size, blink, blink_progress, face_scale):
    eye_elements = []
    # White sclera
    eye_elements.append(patches.Circle((cx, cy), size * 1.2 * face_scale, color='#e6f9ff'))
    # Iris
    eye_elements.append(patches.Circle((cx, cy), size * 1.0 * face_scale, color='#5ab0ff'))
    # Pupil
    eye_elements.append(patches.Circle((cx, cy), size * 0.6 * face_scale, color='#121212'))
    # Highlight
    eye_elements.append(patches.Circle((cx + size * 0.3 * face_scale, cy + size * 0.3 * face_scale), size * 0.2 * face_scale, color='white'))
    
    if blink:
        eye_elements.append(patches.Rectangle((cx - size * 1.2 * face_scale, cy + size * 1.2 * face_scale - blink_progress * face_scale), 
                                             size * 2.4 * face_scale, blink_progress * 2 * face_scale, color='black'))
    
    return eye_elements

def draw_realistic_smile(frame, size, face_scale):
    mouth_elements = []
    # White mouth semi-circle
    mouth_elements.append(patches.Wedge((0, -mouth_distance * face_scale + eye_vert * face_scale), 
                                      size * 1.3 * face_scale, 180, 360, 
                                      facecolor='white', edgecolor='white'))
    # Tongue animation (pulsing)
    tongue_size = size * 1.0 * face_scale + 0.1 * np.sin(frame * 0.1) * face_scale
    mouth_elements.append(patches.Wedge((0, -mouth_distance * face_scale + eye_vert * face_scale), 
                                      tongue_size, 180, 360, 
                                      facecolor='#d1a6f9', edgecolor='#d1a6f9'))
    return mouth_elements

def draw_dimples(mouth_distance, mouth_size, face_scale):
    dimple_elements = []
    dimple_radius = mouth_size * 1.3 * 0.3 * face_scale  # Size relative to mouth size
    base_dimple_center_y = -mouth_distance * face_scale + eye_vert * face_scale - mouth_size * 1.3 * 0.2 * face_scale
    
    # Calculate base horizontal positions
    mouth_wedge = patches.Wedge((0, -mouth_distance * face_scale + eye_vert * face_scale), 
                               mouth_size * 1.3 * face_scale, 180, 360)
    base_left_dimple_x = -mouth_wedge.r * 0.8
    base_right_dimple_x = mouth_wedge.r * 0.8
    
    # Apply dimple distance adjustment
    adjusted_left_dimple_x = base_left_dimple_x - dimple_dist / 2 * face_scale
    adjusted_right_dimple_x = base_right_dimple_x + dimple_dist / 2 * face_scale
    
    # Apply horizontal and vertical adjustments
    final_left_dimple_x = adjusted_left_dimple_x + dimple_h * face_scale
    final_right_dimple_x = adjusted_right_dimple_x + dimple_h * face_scale
    final_dimple_center_y = base_dimple_center_y + dimple_v * face_scale
    
    # Calculate rotation angles
    left_rotation_angle = np.radians(left_dimple_rot)
    right_rotation_angle = np.radians(right_dimple_rot)
    
    # Left dimple with individual rotation
    left_theta1 = -135 + left_rotation_angle
    left_theta2 = -45 + left_rotation_angle
    
    dimple_elements.append(patches.Arc(
        (final_left_dimple_x, final_dimple_center_y),
        dimple_radius, dimple_radius,
        theta1=left_theta1, theta2=left_theta2,
        color="#d1ccff", linewidth=5 * face_scale, fill=False
    ))
    
    # Right dimple with individual rotation
    right_theta1 = -135 + right_rotation_angle
    right_theta2 = -45 + right_rotation_angle
    
    dimple_elements.append(patches.Arc(
        (final_right_dimple_x, final_dimple_center_y),
        dimple_radius, dimple_radius,
        theta1=right_theta1, theta2=right_theta2,
        color="#d1ccff", linewidth=5 * face_scale, fill=False
    ))
    
    return dimple_elements

def animate_smile(frame):
    global patches_objs, eye_distance, mouth_distance, eye_size, mouth_size, eye_vert, \
           dimple_h, dimple_v, dimple_dist, left_dimple_rot, right_dimple_rot, face_scale
    for p in patches_objs:
        p.remove()
    patches_objs.clear()

    # Update parameters from sliders
    face_scale = face_size_slider.val
    eye_distance = eye_distance_slider.val
    mouth_distance = mouth_distance_slider.val
    eye_size = eye_size_slider.val
    mouth_size = mouth_size_slider.val
    eye_vert = eye_vert_slider.val
    dimple_h = dimple_h_slider.val
    dimple_v = dimple_v_slider.val
    dimple_dist = dimple_dist_slider.val
    left_dimple_rot = left_dimple_rot_slider.val
    right_dimple_rot = right_dimple_rot_slider.val

    blink_phase = frame % 60
    blink = False
    blink_progress = 0
    if blink_phase < 10:
        blink = True
        blink_progress = (10 - blink_phase) * 0.3 * eye_size
    elif blink_phase > 50:
        blink = True
        blink_progress = (blink_phase - 50) * 0.3 * eye_size

    left_eye = draw_eye(-eye_distance/2, 0.5 + eye_vert, eye_size, blink, blink_progress, face_scale)
    right_eye = draw_eye(eye_distance/2, 0.5 + eye_vert, eye_size, blink, blink_progress, face_scale)
    mouth = draw_realistic_smile(frame, mouth_size, face_scale)
    dimples = draw_dimples(mouth_distance, mouth_size, face_scale)

    # Draw stars in the upper corners
    left_star = patches.RegularPolygon((-1600 * face_scale, 900 * face_scale), numVertices=5, 
                                      radius=50 * face_scale, orientation=np.radians(90), color='#e6f9ff')
    right_star = patches.RegularPolygon((1600 * face_scale, 900 * face_scale), numVertices=5, 
                                       radius=50 * face_scale, orientation=np.radians(90), color='#e6f9ff')

    for item in left_eye + right_eye + mouth + dimples + [left_star, right_star]:
        ax.add_patch(item)
        patches_objs.append(item)
    
    return patches_objs

def save_parameters(event):
    params = {
        'face_size': face_size_slider.val,
        'eye_distance': eye_distance_slider.val,
        'mouth_distance': mouth_distance_slider.val,
        'eye_size': eye_size_slider.val,
        'mouth_size': mouth_size_slider.val,
        'eye_vert': eye_vert_slider.val,
        'dimple_h': dimple_h_slider.val,
        'dimple_v': dimple_v_slider.val,
        'dimple_dist': dimple_dist_slider.val,
        'left_dimple_rot': left_dimple_rot_slider.val,
        'right_dimple_rot': right_dimple_rot_slider.val
    }
    with open('parameters3.json', 'w') as f:
        json.dump(params, f)
    print("Parameters saved to parameters.json")

save_button.on_clicked(save_parameters)

ani = animation.FuncAnimation(fig, animate_smile, frames=1000, interval=16, blit=True)

plt.subplots_adjust(top=0.9)  # Make space for sliders
plt.show()