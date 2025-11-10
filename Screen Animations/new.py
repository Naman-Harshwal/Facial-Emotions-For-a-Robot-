import pygame
import math
import random
import sys
import time

# Initialize pygame
pygame.init()

# Screen dimensions - Full HD for robot display
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Facial Expressions")

# Colors
BACKGROUND = (10, 20, 30)
PRIMARY = (0, 180, 216)
SECONDARY = (238, 242, 255)
ACCENT = (252, 163, 17)
HAPPY = (50, 200, 50)
SAD = (100, 100, 255)
SPARKLE = (255, 255, 200)
ANGRY_RED = (255, 50, 50)
CONFUSED_PURPLE = (180, 100, 220)
CURIOUS_BLUE = (100, 150, 255)
CRYING_BLUE = (100, 200, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()

class RobotFace:
    def __init__(self):
        # Face properties
        self.face_center = (WIDTH // 2, HEIGHT // 2)
        self.face_radius = 400
        
        # Eye properties
        self.eye_base_x = [WIDTH // 2 - 200, WIDTH // 2 + 200]
        self.eye_base_y = HEIGHT // 2 - 100
        self.eye_offset_x = 0
        self.eye_offset_y = 0
        self.eye_width = 120
        self.eye_height = 160
        self.pupil_size = 45
        
        # Eye state tracking
        self.eye_state = "neutral"
        self.eye_state_timer = 0
        self.eye_state_duration = 0
        
        # Blinking
        self.blink_timer = 0
        self.blink_duration = 0
        self.is_blinking = False
        self.blink_height = 0
        
        # Mouth properties
        self.mouth_openness = 0
        self.mouth_change = 1
        self.current_expression = "neutral"
        self.mouth_expression_timer = 0
        self.mouth_expression_duration = 0
        
        # Emotion-specific properties
        self.tears = []
        self.star_alpha = 0
        self.star_dir = 1
        self.angry_stars = []
        self.confused_jitter = 0
        self.curious_shift = 0
        
        # Antenna properties
        self.antenna_angle = 0
        
        # Sparkle properties
        self.sparkle_timer = 0
        self.sparkle_duration = 0
        self.sparkle_positions = []
        self.sparkle_size = []
        
        # Status text
        self.status_text = "STATUS: OPERATIONAL"
        self.status_color = PRIMARY
        
        # Expression history for random expressions
        self.expression_timer = 0

    def set_expression(self, expression):
        """Set the facial expression"""
        self.current_expression = expression
        
        if expression == "smile":
            self.status_text = "STATUS: HAPPY"
            self.status_color = HAPPY
        elif expression == "sad":
            self.status_text = "STATUS: SAD"
            self.status_color = SAD
        elif expression == "angry":
            self.status_text = "STATUS: ANGRY"
            self.status_color = ANGRY_RED
            # Create angry stars
            self.angry_stars = []
            for _ in range(20):
                self.angry_stars.append([
                    random.randint(200, WIDTH-200),
                    random.randint(100, HEIGHT-100),
                    random.randint(2, 6),
                    random.uniform(0.1, 0.5)
                ])
        elif expression == "confused":
            self.status_text = "STATUS: CONFUSED"
            self.status_color = CONFUSED_PURPLE
        elif expression == "crying":
            self.status_text = "STATUS: CRYING"
            self.status_color = CRYING_BLUE
            # Create tears
            self.tears = []
            for i in range(20):
                side = "left" if random.random() > 0.5 else "right"
                x = self.eye_base_x[0] if side == "left" else self.eye_base_x[1]
                x += random.randint(-50, 50)
                self.tears.append([x, self.eye_base_y + 100, random.uniform(2, 5)])
        elif expression == "curious":
            self.status_text = "STATUS: CURIOUS"
            self.status_color = CURIOUS_BLUE
        else:  # neutral
            self.status_text = "STATUS: OPERATIONAL"
            self.status_color = PRIMARY
            
        self.mouth_expression_duration = random.randint(100, 300)
        self.mouth_expression_timer = 0

    def trigger_blink(self):
        """Trigger a blink animation"""
        self.is_blinking = True
        self.blink_duration = 10
        self.blink_timer = 0
        self.blink_height = self.eye_height

    def trigger_sparkle(self):
        """Trigger eye sparkle effect"""
        self.sparkle_duration = 30
        self.sparkle_timer = 0
        
        # Create random sparkles near the eyes
        self.sparkle_positions = []
        self.sparkle_size = []
        
        # Create sparkles for both eyes
        for eye in range(2):
            for _ in range(random.randint(3, 6)):
                x_offset = random.randint(-30, 30)
                y_offset = random.randint(-25, 25)
                self.sparkle_positions.append((self.eye_base_x[eye] + x_offset, 
                                             self.eye_base_y + y_offset))
                self.sparkle_size.append(random.randint(3, 8))

    def update(self):
        """Update animation states"""
        # Update timers
        self.blink_timer += 1
        self.eye_state_timer += 1
        self.mouth_expression_timer += 1
        self.sparkle_timer += 1
        self.expression_timer += 1
        
        # Update emotion-specific animations
        if self.current_expression == "angry":
            # Update angry stars
            for star in self.angry_stars:
                star[0] += random.randint(-2, 2)
                star[1] += random.randint(-2, 2)
                
            # Update star alpha effect
            self.star_alpha += 0.05 * self.star_dir
            if self.star_alpha > 1.0:
                self.star_alpha = 1.0
                self.star_dir = -1
            elif self.star_alpha < 0.3:
                self.star_alpha = 0.3
                self.star_dir = 1
                
        elif self.current_expression == "crying":
            # Update tears
            for tear in self.tears:
                tear[1] += tear[2]  # Move tear down
                tear[2] += 0.05  # Accelerate
                # Add some horizontal movement
                tear[0] += random.uniform(-0.5, 0.5)
                
            # Remove tears that are off screen
            self.tears = [tear for tear in self.tears if tear[1] < HEIGHT + 50]
            
            # Add new tears occasionally
            if random.random() < 0.1 and len(self.tears) < 30:
                side = "left" if random.random() > 0.5 else "right"
                x = self.eye_base_x[0] if side == "left" else self.eye_base_x[1]
                x += random.randint(-50, 50)
                self.tears.append([x, self.eye_base_y + 100, random.uniform(2, 5)])
                
        elif self.current_expression == "confused":
            # Jitter effect for confused expression
            self.confused_jitter = 5 * math.sin(pygame.time.get_ticks() * 0.01)
            
        elif self.current_expression == "curious":
            # Shifting effect for curious expression
            self.curious_shift = 10 * math.sin(pygame.time.get_ticks() * 0.02)
        
        # Handle blinking
        if self.is_blinking:
            # Close eyes
            if self.blink_timer < self.blink_duration // 2:
                self.blink_height = max(2, self.blink_height - 15)
            # Open eyes
            else:
                self.blink_height = min(self.eye_height, self.blink_height + 15)
            
            # End blink
            if self.blink_timer >= self.blink_duration:
                self.is_blinking = False
                self.blink_height = self.eye_height
        else:
            # Random blinking
            if random.random() < 0.01:
                self.trigger_blink()
        
        # Handle eye state changes
        if self.eye_state_timer >= self.eye_state_duration:
            # Return to neutral after a state
            if self.eye_state != "neutral":
                self.set_eye_state("neutral")
            else:
                # Choose a new random eye state
                states = ["left", "right", "up", "down", "neutral", "neutral", "neutral"]
                self.set_eye_state(random.choice(states))
        
        # Handle mouth expression changes
        if self.mouth_expression_timer >= self.mouth_expression_duration:
            # Return to neutral after an expression
            if self.current_expression != "neutral":
                self.set_expression("neutral")
            else:
                # Occasionally show expressions
                if random.random() < 0.05:
                    expressions = ["smile", "sad", "angry", "confused", "crying", "curious"]
                    self.set_expression(random.choice(expressions))
        
        # Handle automatic expression changes
        if self.expression_timer > 300:  # Change expression every 5 seconds
            self.expression_timer = 0
            expressions = ["smile", "sad", "angry", "confused", "crying", "curious", "neutral"]
            self.set_expression(random.choice(expressions))
        
        # Handle sparkles
        if self.sparkle_timer > 180 and random.random() < 0.02:
            self.trigger_sparkle()
        
        # Update antenna animation
        self.antenna_angle = (self.antenna_angle + 0.03) % (2 * math.pi)

    def set_eye_state(self, state):
        """Set the eye movement state"""
        self.eye_state = state
        self.eye_state_duration = random.randint(80, 150)
        self.eye_state_timer = 0
        
        if state == "left":
            self.eye_offset_x = -20
            self.eye_offset_y = 0
        elif state == "right":
            self.eye_offset_x = 20
            self.eye_offset_y = 0
        elif state == "up":
            self.eye_offset_x = 0
            self.eye_offset_y = -15
        elif state == "down":
            self.eye_offset_x = 0
            self.eye_offset_y = 15
        else:  # neutral
            self.eye_offset_x = 0
            self.eye_offset_y = 0

    def draw(self, surface):
        """Draw the entire robot face"""
        # Clear screen
        surface.fill(BACKGROUND)
        
        # Draw face outline
        pygame.draw.circle(surface, PRIMARY, self.face_center, self.face_radius)
        pygame.draw.circle(surface, SECONDARY, self.face_center, self.face_radius - 10)
        
        # Draw antennas
        antenna_offset = math.sin(self.antenna_angle) * 15
        pygame.draw.line(surface, PRIMARY, (self.face_center[0] - 100, self.face_center[1] - self.face_radius + 20), 
                         (self.face_center[0] - 150, self.face_center[1] - self.face_radius - 50 + antenna_offset), 15)
        pygame.draw.line(surface, PRIMARY, (self.face_center[0] + 100, self.face_center[1] - self.face_radius + 20), 
                         (self.face_center[0] + 150, self.face_center[1] - self.face_radius - 50 - antenna_offset), 15)
        pygame.draw.circle(surface, ACCENT, (self.face_center[0] - 150, self.face_center[1] - self.face_radius - 50 + antenna_offset), 20)
        pygame.draw.circle(surface, ACCENT, (self.face_center[0] + 150, self.face_center[1] - self.face_radius - 50 - antenna_offset), 20)
        
        # Draw eyes with current state
        for i, eye_x in enumerate(self.eye_base_x):
            # Apply expression-specific adjustments
            draw_x = eye_x
            draw_y = self.eye_base_y
            
            if self.current_expression == "confused":
                draw_x += self.confused_jitter
                draw_y += self.confused_jitter * 0.5
            elif self.current_expression == "curious":
                draw_x += self.curious_shift
            
            # Draw eye background
            eye_rect = (draw_x - self.eye_width//2, 
                        draw_y - self.blink_height//2 + self.eye_offset_y, 
                        self.eye_width, self.blink_height)
            pygame.draw.ellipse(surface, BACKGROUND, eye_rect)
            
            # Only draw pupil if not blinking
            if not self.is_blinking or self.blink_timer > self.blink_duration // 2:
                # Draw pupil
                pupil_x = draw_x + self.eye_offset_x
                pupil_y = draw_y + self.eye_offset_y
                
                # Apply expression-specific pupil adjustments
                if self.current_expression == "confused":
                    pupil_x += random.randint(-5, 5)
                    pupil_y += random.randint(-5, 5)
                
                pygame.draw.circle(surface, PRIMARY, (pupil_x, pupil_y), self.pupil_size)
                
                # Draw pupil highlight
                pygame.draw.circle(surface, SECONDARY, (pupil_x - 10, pupil_y - 10), 10)
        
        # Draw mouth based on expression
        mouth_y = self.face_center[1] + 100
        mouth_width = 300
        mouth_height = 60
        
        if self.current_expression == "smile":
            # Smile - upward curve
            pygame.draw.arc(surface, ACCENT, 
                           (self.face_center[0] - mouth_width//2, mouth_y - 20, mouth_width, mouth_height * 2),
                           0, math.pi, 15)
        elif self.current_expression == "sad":
            # Sad - downward curve
            pygame.draw.arc(surface, SAD, 
                           (self.face_center[0] - mouth_width//2, mouth_y + 20, mouth_width, mouth_height * 2),
                           math.pi, 2 * math.pi, 15)
        elif self.current_expression == "angry":
            # Angry mouth (frown)
            pygame.draw.arc(surface, ANGRY_RED, 
                           (self.face_center[0] - mouth_width//2, mouth_y + 30, mouth_width, mouth_height),
                           0, math.pi, 15)
        elif self.current_expression == "confused":
            # Confused mouth (wavy)
            points = []
            for i in range(21):
                x = self.face_center[0] - mouth_width//2 + i * (mouth_width // 20)
                y_offset = 20 * math.sin(i * 0.4 + pygame.time.get_ticks() * 0.005)
                points.append((x, mouth_y + y_offset))
            if len(points) > 1:
                pygame.draw.lines(surface, CONFUSED_PURPLE, False, points, 8)
        elif self.current_expression == "crying":
            # Crying mouth (open with tongue)
            # Mouth opening
            pygame.draw.ellipse(surface, (200, 200, 255), 
                              (self.face_center[0] - mouth_width//2, mouth_y, mouth_width, self.mouth_openness))
            # Tongue
            pygame.draw.ellipse(surface, (255, 150, 200), 
                              (self.face_center[0] - 60, mouth_y + self.mouth_openness - 40, 120, 60))
        elif self.current_expression == "curious":
            # Curious mouth (small circle)
            pygame.draw.circle(surface, CURIOUS_BLUE, (self.face_center[0], mouth_y + 20), 30)
        else:  # neutral
            # Straight line mouth
            pygame.draw.line(surface, ACCENT, 
                            (self.face_center[0] - mouth_width//2, mouth_y),
                            (self.face_center[0] + mouth_width//2, mouth_y), 8)
        
        # Draw expression-specific elements
        if self.current_expression == "angry":
            # Draw angry eyebrows
            for i, eye_x in enumerate(self.eye_base_x):
                direction = -1 if i == 0 else 1
                points = [
                    (eye_x - 100, self.eye_base_y - 80),
                    (eye_x, self.eye_base_y - 150),
                    (eye_x + 100, self.eye_base_y - 100)
                ]
                pygame.draw.lines(surface, ANGRY_RED, False, points, 12)
            
            # Draw angry stars
            for star in self.angry_stars:
                alpha_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
                pygame.draw.polygon(alpha_surface, (*ANGRY_RED, int(self.star_alpha * 255)), 
                                  [(15, 0), (20, 15), (30, 15), (22, 25), (25, 40), (15, 30), (5, 40), (8, 25), (0, 15), (10, 15)])
                surface.blit(alpha_surface, (star[0] - 15, star[1] - 20))
                
        elif self.current_expression == "crying":
            # Draw tears
            for tear in self.tears:
                pygame.draw.ellipse(surface, CRYING_BLUE, (tear[0], tear[1], 10, 20))
                
        elif self.current_expression == "confused":
            # Draw question mark
            font = pygame.font.SysFont(None, 150)
            text = font.render("?", True, CONFUSED_PURPLE)
            surface.blit(text, (self.face_center[0] - 40, self.face_center[1] + 150))
        
        # Draw sparkles if active
        if self.sparkle_timer < self.sparkle_duration:
            alpha = 255 * (1 - self.sparkle_timer / self.sparkle_duration)
            for pos, size in zip(self.sparkle_positions, self.sparkle_size):
                # Draw sparkle with fading effect
                sparkle_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(sparkle_surf, (*SPARKLE, int(alpha)), (size, size), size)
                surface.blit(sparkle_surf, (pos[0]-size, pos[1]-size))
                
                # Draw additional sparkle effect
                pygame.draw.line(surface, (*SPARKLE, int(alpha)), 
                                (pos[0]-size, pos[1]), (pos[0]+size, pos[1]), 2)
                pygame.draw.line(surface, (*SPARKLE, int(alpha)), 
                                (pos[0], pos[1]-size), (pos[0], pos[1]+size), 2)
                pygame.draw.line(surface, (*SPARKLE, int(alpha)), 
                                (pos[0]-size*0.7, pos[1]-size*0.7), 
                                (pos[0]+size*0.7, pos[1]+size*0.7), 2)
                pygame.draw.line(surface, (*SPARKLE, int(alpha)), 
                                (pos[0]-size*0.7, pos[1]+size*0.7), 
                                (pos[0]+size*0.7, pos[1]-size*0.7), 2)
        
        # Draw status text
        font = pygame.font.SysFont(None, 60)
        status = font.render(self.status_text, True, self.status_color)
        surface.blit(status, (self.face_center[0] - status.get_width()//2, 50))
        
        # Draw controls info
        controls_font = pygame.font.SysFont(None, 40)
        controls = [
            "CONTROLS: 1-Smile  2-Sad  3-Neutral  4-Angry  5-Crying  6-Confused  7-Curious",
            "EYES: ← → ↑ ↓ - Direction  B-Blink  N-Neutral Eyes   S-Sparkles"
        ]
        for i, text in enumerate(controls):
            ctrl_text = controls_font.render(text, True, SECONDARY)
            surface.blit(ctrl_text, (self.face_center[0] - ctrl_text.get_width()//2, HEIGHT - 100 + i*50))

# Create face instance
robot_face = RobotFace()

# Main animation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # Expression controls
            elif event.key == pygame.K_1:
                robot_face.set_expression("smile")
            elif event.key == pygame.K_2:
                robot_face.set_expression("sad")
            elif event.key == pygame.K_3:
                robot_face.set_expression("neutral")
            elif event.key == pygame.K_4:
                robot_face.set_expression("angry")
            elif event.key == pygame.K_5:
                robot_face.set_expression("crying")
            elif event.key == pygame.K_6:
                robot_face.set_expression("confused")
            elif event.key == pygame.K_7:
                robot_face.set_expression("curious")
            elif event.key == pygame.K_s:
                robot_face.trigger_sparkle()
            # Eye controls
            elif event.key == pygame.K_LEFT:
                robot_face.set_eye_state("left")
            elif event.key == pygame.K_RIGHT:
                robot_face.set_eye_state("right")
            elif event.key == pygame.K_UP:
                robot_face.set_eye_state("up")
            elif event.key == pygame.K_DOWN:
                robot_face.set_eye_state("down")
            elif event.key == pygame.K_b:
                robot_face.trigger_blink()
            elif event.key == pygame.K_n:
                robot_face.set_eye_state("neutral")
    
    # Update animation
    robot_face.update()
    
    # Draw everything
    robot_face.draw(screen)
    
    # Update display
    pygame.display.flip()
    
    # Maintain 60 FPS for smooth animation
    clock.tick(60)

pygame.quit()
sys.exit()