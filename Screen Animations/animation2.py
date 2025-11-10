import pygame
import math
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Bellabot Animation")

# Colors
BACKGROUND = (10, 20, 30)
PRIMARY = (0, 180, 216)
SECONDARY = (238, 242, 255)
ACCENT = (252, 163, 17)
HAPPY = (50, 200, 50)
SAD = (100, 100, 255)
SPARKLE = (255, 255, 200)

# Clock for controlling frame rate
clock = pygame.time.Clock()

class BellabotFace:
    def __init__(self):
        # Eye properties
        self.eye_base_x = [WIDTH//2 - 70, WIDTH//2 + 70]  # Left and right eye centers
        self.eye_base_y = 180
        self.eye_offset_x = 0
        self.eye_offset_y = 0
        self.eye_move_direction = 1
        self.eye_width = 60
        self.eye_height = 80
        self.pupil_size = 15
        
        # Eye state tracking
        self.eye_state = "neutral"  # neutral, left, right, up, down
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
        self.mouth_expression = "neutral"  # neutral, smile, sad
        self.mouth_expression_timer = 0
        self.mouth_expression_duration = 0
        
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
        self.current_expression = "neutral"

    def set_expression(self, expression):
        """Set the facial expression"""
        self.current_expression = expression
        
        if expression == "smile":
            self.mouth_expression = "smile"
            self.status_text = "STATUS: HAPPY"
            self.status_color = HAPPY
        elif expression == "sad":
            self.mouth_expression = "sad"
            self.status_text = "STATUS: SAD"
            self.status_color = SAD
        else:  # neutral
            self.mouth_expression = "neutral"
            self.status_text = "STATUS: OPERATIONAL"
            self.status_color = PRIMARY
            
        self.mouth_expression_duration = random.randint(100, 300)
        self.mouth_expression_timer = 0

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

    def trigger_blink(self):
        """Trigger a blink animation"""
        self.is_blinking = True
        self.blink_duration = 10  # Short blink duration
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
            if random.random() < 0.01:  # 1% chance per frame to blink
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
            if self.mouth_expression != "neutral":
                self.set_expression("neutral")
            else:
                # Occasionally show expressions
                if random.random() < 0.05:  # 5% chance to show expression
                    self.set_expression(random.choice(["smile", "sad"]))
        
        # Handle automatic expression changes
        if self.expression_timer > 300:  # Change expression every 5 seconds
            self.expression_timer = 0
            expressions = ["smile", "sad", "neutral", "neutral", "neutral"]
            self.set_expression(random.choice(expressions))
        
        # Handle sparkles
        if self.sparkle_timer > 180 and random.random() < 0.02:  # Occasional sparkles
            self.trigger_sparkle()
        
        # Update antenna animation
        self.antenna_angle = (self.antenna_angle + 0.03) % (2 * math.pi)

    def draw(self, surface):
        """Draw the entire Bellabot face"""
        # Clear screen
        surface.fill(BACKGROUND)
        
        # Draw face outline
        pygame.draw.ellipse(surface, PRIMARY, (WIDTH//2-150, 80, 300, 300))
        pygame.draw.ellipse(surface, SECONDARY, (WIDTH//2-140, 90, 280, 280))
        
        # Draw antennas
        antenna_offset = math.sin(self.antenna_angle) * 5
        pygame.draw.line(surface, PRIMARY, (WIDTH//2-40, 80), (WIDTH//2-70, 20 + antenna_offset), 8)
        pygame.draw.line(surface, PRIMARY, (WIDTH//2+40, 80), (WIDTH//2+70, 20 - antenna_offset), 8)
        pygame.draw.circle(surface, ACCENT, (WIDTH//2-70, 20 + antenna_offset), 10)
        pygame.draw.circle(surface, ACCENT, (WIDTH//2+70, 20 - antenna_offset), 10)
        
        # Draw eyes with current state
        for i, eye_x in enumerate(self.eye_base_x):
            # Draw eye background
            eye_rect = (eye_x - self.eye_width//2, 
                        self.eye_base_y - self.blink_height//2 + self.eye_offset_y, 
                        self.eye_width, self.blink_height)
            pygame.draw.ellipse(surface, BACKGROUND, eye_rect)
            
            # Only draw pupil if not blinking
            if not self.is_blinking or self.blink_timer > self.blink_duration // 2:
                # Draw pupil
                pupil_x = eye_x + self.eye_offset_x
                pupil_y = self.eye_base_y + self.eye_offset_y
                pygame.draw.circle(surface, PRIMARY, (pupil_x, pupil_y), self.pupil_size)
                
                # Draw pupil highlight
                pygame.draw.circle(surface, SECONDARY, (pupil_x - 4, pupil_y - 4), 4)
        
        # Draw mouth based on expression
        mouth_y = 280
        mouth_height = 40
        
        if self.mouth_expression == "smile":
            # Smile - upward curve
            start_angle = 0.2
            end_angle = math.pi - 0.2
            curve_offset = -15
        elif self.mouth_expression == "sad":
            # Sad - downward curve
            start_angle = math.pi + 0.2
            end_angle = 2 * math.pi - 0.2
            curve_offset = 15
        else:  # neutral
            # Neutral - straight line
            start_angle = 0
            end_angle = math.pi
            curve_offset = 0
        
        # Draw mouth background
        pygame.draw.ellipse(surface, BACKGROUND, (WIDTH//2-70, mouth_y, 140, mouth_height))
        
        # Draw mouth curve
        if self.mouth_expression in ["smile", "sad"]:
            # Curved mouth
            rect = (WIDTH//2 - 70, mouth_y + curve_offset, 140, mouth_height)
            pygame.draw.arc(surface, ACCENT, rect, start_angle, end_angle, 5)
        else:
            # Straight mouth
            pygame.draw.line(surface, ACCENT, 
                            (WIDTH//2 - 60, mouth_y + mouth_height//2),
                            (WIDTH//2 + 60, mouth_y + mouth_height//2), 5)
        
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
        font = pygame.font.SysFont(None, 36)
        status = font.render(self.status_text, True, self.status_color)
        surface.blit(status, (WIDTH//2 - status.get_width()//2, 380))
        
        # Draw controls info
        controls_font = pygame.font.SysFont(None, 24)
        controls = [
            "CONTROLS: 1-Smile  2-Sad  3-Neutral  4-Sparkles",
            "EYES: ← → ↑ ↓ - Direction  B-Blink  N-Neutral"
        ]
        for i, text in enumerate(controls):
            ctrl_text = controls_font.render(text, True, SECONDARY)
            surface.blit(ctrl_text, (WIDTH//2 - ctrl_text.get_width()//2, 420 + i*25))

# Create face instance
bot_face = BellabotFace()

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
                bot_face.set_expression("smile")
            elif event.key == pygame.K_2:
                bot_face.set_expression("sad")
            elif event.key == pygame.K_3:
                bot_face.set_expression("neutral")
            elif event.key == pygame.K_4:
                bot_face.trigger_sparkle()
            # Eye controls
            elif event.key == pygame.K_LEFT:
                bot_face.set_eye_state("left")
            elif event.key == pygame.K_RIGHT:
                bot_face.set_eye_state("right")
            elif event.key == pygame.K_UP:
                bot_face.set_eye_state("up")
            elif event.key == pygame.K_DOWN:
                bot_face.set_eye_state("down")
            elif event.key == pygame.K_b:
                bot_face.trigger_blink()
            elif event.key == pygame.K_n:
                bot_face.set_eye_state("neutral")
    
    # Update animation
    bot_face.update()
    
    # Draw everything
    bot_face.draw(screen)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()