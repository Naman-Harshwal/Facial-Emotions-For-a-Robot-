#!/usr/bin/env python3
"""
Kawaii Face Animation with Realistic Eye Blinking and Emotions
=============================================================
Features:
- Natural eye blinking every 3-6 seconds
- Smooth mouse-tracking eye movement  
- 5 emotional expressions
- High-performance 60 FPS animation

Controls:
- Move mouse: Eye tracking
- Keys 1-5: Change emotions (Neutral, Happy, Sad, Surprise, Angry)
- Space: Manual blink
- ESC/Q: Exit

Created for enhanced kawaii face animation with realistic movement
"""

import pygame as pg
import numpy as np
import random
import math
import time
import sys

# Initialize Pygame
pg.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors - Kawaii palette
BACKGROUND_COLOR = (255, 240, 245)  # Light pink background
EYE_WHITE = (255, 255, 255)
EYE_BLUE = (70, 130, 180)          # Steel blue iris
PUPIL_BLACK = (25, 25, 112)        # Dark blue pupil
SPARKLE_WHITE = (255, 255, 255)
MOUTH_BLACK = (50, 50, 50)
MOUTH_RED = (220, 20, 60)          # Red for angry expression

# Eye settings
EYE_WIDTH = 120
EYE_HEIGHT = 80
EYE_SEPARATION = 200
PUPIL_RADIUS = 25
IRIS_RADIUS = 45

class KawaiiFace:
    def __init__(self):
        # Eye positions (left and right eye centers)
        self.left_eye_pos = (SCREEN_WIDTH // 2 - EYE_SEPARATION // 2, SCREEN_HEIGHT // 2 - 50)
        self.right_eye_pos = (SCREEN_WIDTH // 2 + EYE_SEPARATION // 2, SCREEN_HEIGHT // 2 - 50)

        # Pupil tracking
        self.left_pupil_pos = np.array([0.0, 0.0])   # Offset from center
        self.right_pupil_pos = np.array([0.0, 0.0])
        self.pupil_velocity = np.array([0.0, 0.0])
        self.pupil_smooth_factor = 0.15

        # Blinking system
        self.blink_state = 0.0      # 0.0 = fully open, 1.0 = fully closed
        self.is_blinking = False
        self.blink_timer = 0.0
        self.next_blink_time = random.uniform(3.0, 6.0)
        self.blink_duration = 0.15  # Fast blink

        # Emotion system
        self.current_emotion = "neutral"
        self.emotions = {
            "neutral": self._draw_neutral_mouth,
            "happy": self._draw_happy_mouth,
            "sad": self._draw_sad_mouth, 
            "surprise": self._draw_surprise_mouth,
            "angry": self._draw_angry_mouth
        }

        print("🥰 Kawaii Face Animation Started!")
        print("Controls:")
        print("  🖱️  Move mouse: Eye tracking")  
        print("  1️⃣  Key 1: Neutral emotion")
        print("  😊 Key 2: Happy emotion")
        print("  😢 Key 3: Sad emotion") 
        print("  😮 Key 4: Surprise emotion")
        print("  😠 Key 5: Angry emotion")
        print("  ⏺️  Space: Manual blink")
        print("  🚪 ESC/Q: Exit")

    def update(self, dt, mouse_pos):
        """Update animation state"""
        self._update_pupil_tracking(mouse_pos, dt)
        self._update_blinking(dt)

    def _update_pupil_tracking(self, mouse_pos, dt):
        """Smooth pupil tracking with physics"""
        # Calculate target positions for both eyes
        left_target = self._calculate_pupil_target(mouse_pos, self.left_eye_pos)
        right_target = self._calculate_pupil_target(mouse_pos, self.right_eye_pos)

        # Smooth interpolation with physics
        left_diff = left_target - self.left_pupil_pos
        right_diff = right_target - self.right_pupil_pos

        self.left_pupil_pos += left_diff * self.pupil_smooth_factor
        self.right_pupil_pos += right_diff * self.pupil_smooth_factor

    def _calculate_pupil_target(self, mouse_pos, eye_center):
        """Calculate pupil offset within eye bounds"""
        # Vector from eye center to mouse
        dx = mouse_pos[0] - eye_center[0] 
        dy = mouse_pos[1] - eye_center[1]

        # Normalize and constrain within iris bounds
        distance = math.sqrt(dx*dx + dy*dy)
        max_offset = IRIS_RADIUS - PUPIL_RADIUS - 5  # Leave some margin

        if distance > 0:
            # Normalize direction and apply max constraint
            scale = min(distance / 100.0, 1.0) * max_offset
            return np.array([dx/distance * scale, dy/distance * scale])
        return np.array([0.0, 0.0])

    def _update_blinking(self, dt):
        """Natural blinking system"""
        self.blink_timer += dt

        if not self.is_blinking and self.blink_timer >= self.next_blink_time:
            # Start new blink
            self.is_blinking = True
            self.blink_timer = 0.0

        if self.is_blinking:
            # Calculate blink progress with easing
            progress = self.blink_timer / self.blink_duration

            if progress <= 0.5:
                # Closing phase (fast)
                self.blink_state = self._ease_in_cubic(progress * 2.0)
            elif progress <= 1.0:
                # Opening phase (slower) 
                self.blink_state = 1.0 - self._ease_out_cubic((progress - 0.5) * 2.0)
            else:
                # Blink complete
                self.is_blinking = False
                self.blink_state = 0.0
                self.next_blink_time = random.uniform(3.0, 6.0)  # Next blink in 3-6 seconds
                self.blink_timer = 0.0

    def _ease_in_cubic(self, t):
        """Smooth acceleration easing"""
        return t * t * t

    def _ease_out_cubic(self, t):
        """Smooth deceleration easing"""  
        return 1 - (1 - t) ** 3

    def manual_blink(self):
        """Trigger immediate blink"""
        if not self.is_blinking:
            self.is_blinking = True
            self.blink_timer = 0.0

    def set_emotion(self, emotion):
        """Change facial expression"""
        if emotion in self.emotions:
            self.current_emotion = emotion
            print(f"😊 Emotion changed to: {emotion}")

    def draw(self, screen):
        """Draw the complete kawaii face"""
        # Clear background
        screen.fill(BACKGROUND_COLOR)

        # Draw both eyes
        self._draw_eye(screen, self.left_eye_pos, self.left_pupil_pos)
        self._draw_eye(screen, self.right_eye_pos, self.right_pupil_pos)

        # Draw mouth with current emotion
        mouth_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
        self.emotions[self.current_emotion](screen, mouth_pos)

    def _draw_eye(self, screen, center, pupil_offset):
        """Draw a single eye with blinking animation"""
        x, y = center

        # Calculate blink effect on eye height
        current_eye_height = EYE_HEIGHT * (1.0 - self.blink_state)

        if current_eye_height < 5:  # Eye essentially closed
            # Draw closed eye as a thin line
            pg.draw.ellipse(screen, MOUTH_BLACK, 
                          (x - EYE_WIDTH//2, y - 2, EYE_WIDTH, 4))
            return

        # Draw eye white (oval shape)
        eye_rect = pg.Rect(x - EYE_WIDTH//2, y - current_eye_height//2, 
                          EYE_WIDTH, int(current_eye_height))
        pg.draw.ellipse(screen, EYE_WHITE, eye_rect)

        # Draw iris (blue circle)
        iris_radius = int(IRIS_RADIUS * (current_eye_height / EYE_HEIGHT))
        if iris_radius > 5:
            pg.draw.circle(screen, EYE_BLUE, 
                         (int(x + pupil_offset[0]), int(y + pupil_offset[1])), 
                         iris_radius)

        # Draw pupil (dark center)
        pupil_radius = int(PUPIL_RADIUS * (current_eye_height / EYE_HEIGHT))
        if pupil_radius > 2:
            pg.draw.circle(screen, PUPIL_BLACK,
                         (int(x + pupil_offset[0]), int(y + pupil_offset[1])),
                         pupil_radius)

        # Draw sparkles (kawaii highlights)
        if current_eye_height > 20:
            sparkle_positions = [
                (int(x + pupil_offset[0] - 8), int(y + pupil_offset[1] - 8)),
                (int(x + pupil_offset[0] + 12), int(y + pupil_offset[1] - 15)),
                (int(x + pupil_offset[0] - 15), int(y + pupil_offset[1] + 10))
            ]

            for pos in sparkle_positions:
                pg.draw.circle(screen, SPARKLE_WHITE, pos, 3)

    # Emotion drawing methods
    def _draw_neutral_mouth(self, screen, pos):
        """Neutral expression - simple line"""
        x, y = pos
        pg.draw.line(screen, MOUTH_BLACK, (x - 30, y), (x + 30, y), 3)

    def _draw_happy_mouth(self, screen, pos):
        """Happy expression - upward curve"""
        x, y = pos
        points = []
        for i in range(-30, 31, 5):
            curve_y = y + int(15 * math.sin(math.pi * i / 60))
            points.append((x + i, curve_y))
        if len(points) > 1:
            pg.draw.lines(screen, MOUTH_BLACK, False, points, 4)

    def _draw_sad_mouth(self, screen, pos):
        """Sad expression - downward curve""" 
        x, y = pos
        points = []
        for i in range(-30, 31, 5):
            curve_y = y - int(15 * math.sin(math.pi * i / 60))
            points.append((x + i, curve_y))
        if len(points) > 1:
            pg.draw.lines(screen, MOUTH_BLACK, False, points, 4)

    def _draw_surprise_mouth(self, screen, pos):
        """Surprise expression - small O shape"""
        x, y = pos
        pg.draw.circle(screen, MOUTH_BLACK, pos, 15, 4)

    def _draw_angry_mouth(self, screen, pos):
        """Angry expression - jagged line"""
        x, y = pos
        points = [
            (x - 25, y + 10),
            (x - 10, y - 5), 
            (x, y + 5),
            (x + 10, y - 5),
            (x + 25, y + 10)
        ]
        pg.draw.lines(screen, MOUTH_RED, False, points, 4)

def main():
    """Main game loop"""
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("🥰 Kawaii Face Animation - Realistic Eye Blinking")
    clock = pg.time.Clock()

    # Create kawaii face
    face = KawaiiFace()

    # Main loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_ESCAPE, pg.K_q]:
                    running = False
                elif event.key == pg.K_SPACE:
                    face.manual_blink()
                elif event.key == pg.K_1:
                    face.set_emotion("neutral")
                elif event.key == pg.K_2:
                    face.set_emotion("happy")
                elif event.key == pg.K_3:
                    face.set_emotion("sad")
                elif event.key == pg.K_4:
                    face.set_emotion("surprise") 
                elif event.key == pg.K_5:
                    face.set_emotion("angry")

        # Update animation
        mouse_pos = pg.mouse.get_pos()
        face.update(dt, mouse_pos)

        # Render
        face.draw(screen)
        pg.display.flip()

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()