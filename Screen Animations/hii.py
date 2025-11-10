#!/usr/bin/env python3
"""
Ultra-Smooth Kawaii Face Animation - Pygame Version (120 FPS)
High-performance solution with physics-based eye movement
"""
import pygame
import numpy as np
import math
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FACE_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
FACE_RADIUS = 200
EYE_RADIUS = 60
PUPIL_RADIUS = 18

# Colors
PINK_FACE = (255, 228, 225)
PINK_BORDER = (255, 105, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_PINK = (255, 20, 147)
GOLD = (255, 215, 0)
BACKGROUND = (30, 30, 30)

class UltraKawaiiFace:
    def __init__(self):
        # Eye positions
        self.left_eye_center = np.array([FACE_CENTER[0] - 80, FACE_CENTER[1] - 40], dtype=np.float64)
        self.right_eye_center = np.array([FACE_CENTER[0] + 80, FACE_CENTER[1] - 40], dtype=np.float64)

        # Physics-based pupil tracking
        self.pupil_pos = np.array([0.0, 0.0], dtype=np.float64)
        self.pupil_velocity = np.array([0.0, 0.0], dtype=np.float64)
        self.pupil_target = np.array([0.0, 0.0], dtype=np.float64)

        # Physics constants
        self.spring_force = 0.15
        self.damping = 0.85
        self.max_pupil_movement = 25

        # Advanced blinking system
        self.blink_timer = 0.0
        self.next_blink_time = random.uniform(3.0, 6.0)
        self.blink_progress = 0.0
        self.is_blinking = False
        self.blink_speed = 8.0

        # Micro-saccades (tiny eye movements)
        self.saccade_timer = 0.0
        self.next_saccade_time = random.uniform(1.0, 3.0)
        self.saccade_offset = np.array([0.0, 0.0], dtype=np.float64)

        # Sparkle animation
        self.sparkle_phase = 0.0

    def update(self, dt, mouse_pos):
        """Update all animations with physics-based movement"""
        self.blink_timer += dt
        self.saccade_timer += dt
        self.sparkle_phase += dt

        # Update pupil tracking with physics
        self.update_pupil_physics(mouse_pos, dt)

        # Update blinking
        self.update_blinking(dt)

        # Update micro-saccades
        self.update_saccades(dt)

    def update_pupil_physics(self, mouse_pos, dt):
        """Physics-based smooth pupil tracking"""
        # Calculate target position from mouse
        target_x = (mouse_pos[0] - FACE_CENTER[0]) / SCREEN_WIDTH * 2
        target_y = (mouse_pos[1] - FACE_CENTER[1]) / SCREEN_HEIGHT * 2

        # Limit target to realistic eye movement
        target_x = max(-1, min(1, target_x)) * self.max_pupil_movement
        target_y = max(-1, min(1, target_y)) * self.max_pupil_movement

        self.pupil_target = np.array([target_x, target_y], dtype=np.float64)

        # Spring-damper physics for smooth movement
        force = (self.pupil_target - self.pupil_pos) * self.spring_force
        self.pupil_velocity = self.pupil_velocity + force
        self.pupil_velocity = self.pupil_velocity * self.damping

        # Update position - FIXED: Use regular assignment
        self.pupil_pos = self.pupil_pos + self.pupil_velocity * dt * 60

    def update_blinking(self, dt):
        """Realistic blinking with natural timing"""
        if not self.is_blinking and self.blink_timer >= self.next_blink_time:
            # Start new blink
            self.is_blinking = True
            self.blink_timer = 0.0
            self.next_blink_time = random.uniform(3.0, 6.0)

        if self.is_blinking:
            # Smooth blink curve (fast close, slower open)
            self.blink_progress += self.blink_speed * dt

            if self.blink_progress >= 2 * math.pi:
                self.is_blinking = False
                self.blink_progress = 0.0

    def get_blink_factor(self):
        """Calculate how closed the eyes are (0=open, 1=closed)"""
        if not self.is_blinking:
            return 0.0

        # Use sine wave for natural blink motion
        return max(0, math.sin(self.blink_progress)) * 0.9

    def update_saccades(self, dt):
        """Add micro-saccades for realistic eye movement"""
        if self.saccade_timer >= self.next_saccade_time:
            # Create small random movement
            self.saccade_offset = np.array([
                random.uniform(-2, 2),
                random.uniform(-2, 2)
            ], dtype=np.float64)

            self.saccade_timer = 0.0
            self.next_saccade_time = random.uniform(1.0, 3.0)

        # Gradually return to center
        self.saccade_offset = self.saccade_offset * 0.95

    def draw(self, screen):
        """Draw the ultra-smooth kawaii face"""
        # Clear screen
        screen.fill(BACKGROUND)

        # Draw face circle
        pygame.draw.circle(screen, PINK_FACE, FACE_CENTER, FACE_RADIUS)
        pygame.draw.circle(screen, PINK_BORDER, FACE_CENTER, FACE_RADIUS, 4)

        # Draw eyes
        self.draw_eye(screen, self.left_eye_center)
        self.draw_eye(screen, self.right_eye_center)

        # Draw mouth
        self.draw_mouth(screen)

        # Draw sparkles
        self.draw_sparkles(screen)

    def draw_eye(self, screen, eye_center):
        """Draw individual eye with realistic blinking"""
        blink_factor = self.get_blink_factor()

        if blink_factor < 0.95:  # Eye is open
            # Calculate actual eye height with blinking
            eye_height = EYE_RADIUS * (1 - blink_factor)

            # Draw eye white (ellipse when blinking)
            if blink_factor > 0:
                pygame.draw.ellipse(screen, WHITE, 
                                  (eye_center[0] - EYE_RADIUS, 
                                   eye_center[1] - eye_height,
                                   EYE_RADIUS * 2, eye_height * 2))
                pygame.draw.ellipse(screen, BLACK, 
                                  (eye_center[0] - EYE_RADIUS, 
                                   eye_center[1] - eye_height,
                                   EYE_RADIUS * 2, eye_height * 2), 2)
            else:
                pygame.draw.circle(screen, WHITE, (int(eye_center[0]), int(eye_center[1])), EYE_RADIUS)
                pygame.draw.circle(screen, BLACK, (int(eye_center[0]), int(eye_center[1])), EYE_RADIUS, 2)

            # Calculate pupil position with saccades
            pupil_center = eye_center + self.pupil_pos + self.saccade_offset

            # Draw pupil
            pygame.draw.circle(screen, BLACK, 
                             (int(pupil_center[0]), int(pupil_center[1])), PUPIL_RADIUS)

            # Draw highlight
            highlight_pos = pupil_center + np.array([6, -6])
            pygame.draw.circle(screen, WHITE, 
                             (int(highlight_pos[0]), int(highlight_pos[1])), 6)
        else:
            # Draw closed eye line
            start_pos = (int(eye_center[0] - EYE_RADIUS * 0.8), int(eye_center[1]))
            end_pos = (int(eye_center[0] + EYE_RADIUS * 0.8), int(eye_center[1]))
            pygame.draw.line(screen, BLACK, start_pos, end_pos, 3)

    def draw_mouth(self, screen):
        """Draw kawaii smile"""
        mouth_center = (FACE_CENTER[0], FACE_CENTER[1] + 80)
        mouth_width = 80

        # Draw curved smile using multiple line segments
        points = []
        for i in range(21):
            t = i / 20.0
            x = mouth_center[0] + (t - 0.5) * mouth_width * 2
            y = mouth_center[1] + math.sin(math.pi * t) * 20
            points.append((x, y))

        if len(points) > 1:
            pygame.draw.lines(screen, DARK_PINK, False, points, 4)

    def draw_sparkles(self, screen):
        """Draw animated sparkles"""
        sparkle_positions = [
            (FACE_CENTER[0] - 250, FACE_CENTER[1] - 150),
            (FACE_CENTER[0] + 250, FACE_CENTER[1] - 150),
            (FACE_CENTER[0] - 280, FACE_CENTER[1]),
            (FACE_CENTER[0] + 280, FACE_CENTER[1]),
            (FACE_CENTER[0] - 200, FACE_CENTER[1] + 200),
            (FACE_CENTER[0] + 200, FACE_CENTER[1] + 200),
        ]

        for i, pos in enumerate(sparkle_positions):
            # Twinkling effect with phase offset
            alpha = 0.5 + 0.5 * math.sin(self.sparkle_phase * 3 + i)
            size = 12 + 4 * math.sin(self.sparkle_phase * 2 + i * 1.3)

            # Create surface for alpha blending
            sparkle_surf = pygame.Surface((size * 2, size * 2))
            sparkle_surf.set_alpha(int(alpha * 255))
            sparkle_surf.fill(BACKGROUND)

            # Draw 4-pointed star
            center = (size, size)
            pygame.draw.line(sparkle_surf, GOLD, (center[0] - size//2, center[1]), 
                           (center[0] + size//2, center[1]), 3)
            pygame.draw.line(sparkle_surf, GOLD, (center[0], center[1] - size//2), 
                           (center[0], center[1] + size//2), 3)

            screen.blit(sparkle_surf, (pos[0] - size, pos[1] - size))

def main():
    """Main game loop with 120 FPS"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ultra-Smooth Kawaii Face Animation - 120 FPS")
    clock = pygame.time.Clock()

    kawaii_face = UltraKawaiiFace()

    print("🚀 Ultra-Smooth Kawaii Animation Started!")
    print("✨ Running at 120 FPS for maximum smoothness")
    print("👁️ Move mouse for realistic eye tracking")
    print("⏰ Natural blinking every 3-6 seconds")
    print("🔬 Physics-based movement with micro-saccades")
    print("Press ESC or close window to exit")

    running = True
    while running:
        dt = clock.tick(120) / 1000.0  # 120 FPS target

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Update animations
        kawaii_face.update(dt, mouse_pos)

        # Draw everything
        kawaii_face.draw(screen)

        # Display FPS
        fps = clock.get_fps()
        font = pygame.font.Font(None, 36)
        fps_text = font.render(f"FPS: {fps:.1f}", True, WHITE)
        screen.blit(fps_text, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()