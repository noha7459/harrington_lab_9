# Import the pygame library
import pygame
import math  # For particle effects and calculations

# Initialize pygame (gets it ready to work)
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Not a Game About an Italian Plumber")

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# SOUND EFFECTS

try:
    jump_sound = pygame.mixer.Sound("jumpSound.wav.wav")
    coin_sound = pygame.mixer.Sound("coinCollect.wav.wav")
    enemy_defeat_sound = pygame.mixer.Sound("enemyDeath.wav")
    death_sound = pygame.mixer.Sound("playerDeath.wav")
    pygame.mixer.music.load("backgroundMusic.wav.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    print("Sound files not found - continuing without sound")
    jump_sound = None
    coin_sound = None
    enemy_defeat_sound = None
    death_sound = None

# BACKGROUND IMAGE
try:
    background_image = pygame.image.load("backgroundImage.png.png")  # YOUR BACKGROUND IMAGE FILENAME HERE
    background_image = pygame.transform.scale(background_image, (800, 600))
except:
    print("Background image not found - using solid color instead")
    background_image = None

# PLATFORM IMAGE
# Replace this filename with your own platform texture!
try:
    platform_image = pygame.image.load("platform.jpg")  # YOUR PLATFORM IMAGE FILENAME HERE
    # We'll scale this for each platform individually
except:
    print("Platform image not found - using solid color rectangles instead")
    platform_image = None

# EXIT DOOR IMAGE
try:
    door_image = pygame.image.load("castledoors.png")  # YOUR DOOR IMAGE FILENAME HERE
    door_image = pygame.transform.scale(door_image, (60, 80))  # Scale to door size
except:
    print("Door image not found - using colored rectangle instead")
    door_image = None

# ENEMY IMAGE
try:
    enemy_image = pygame.image.load("skull_copy.gif")  # YOUR ENEMY IMAGE FILENAME HERE
    # We'll scale this for each enemy individually
except:
    print("Enemy image not found - using colored rectangle instead")
    enemy_image = None

# PLAYER IMAGE
try:
    player_image = pygame.image.load("playerCharacter.png")  # YOUR PLAYER IMAGE FILENAME HERE
    # We'll scale this for the player size
except:
    print("Player image not found - using colored rectangle instead")
    player_image = None

# PLAYER VARIABLES
player_x = 100
player_y = 100
player_width = 40
player_height = 60
player_lives = 3  # NEW: Player starts with 3 lives

# CAMERA/SCROLL VARIABLES - For side-scrolling
camera_x = 0  # How far the camera has scrolled right
level_width = 3200  # How wide the level is. Change for longer/shorter levels!

# SMOOTH MOVEMENT VARIABLES
player_velocity_x = 0
player_acceleration = 2.0
player_max_speed = 6
player_friction = 0.85

# PHYSICS VARIABLES
player_velocity_y = 0
gravity = 0.8
jump_strength = -15
on_ground = False

# COYOTE TIME
coyote_timer = 0
coyote_time = 8

# GROUND LEVEL
ground_y = 500

# LEVEL VARIABLES
current_level = 1
total_levels = 5

# GAME STATE
game_state = "start_screen"

# LEVEL TRANSITION FADE
transition_alpha = 0
transitioning = False

# RESPAWN - When player dies, briefly show death then respawn
respawning = False
respawn_timer = 0
respawn_duration = 60  # Frames to wait before respawning (1 second at 60 FPS)

# COIN VARIABLES
coin_radius = 15
score = 0

# PARTICLE EFFECTS
particles = []

# MATH CHALLENGE VARIABLES - For levels 3, 4, 5
asking_math_question = False  # Are we currently asking a math question?
math_question = ""  # The question text
math_answer = 0  # The correct answer
player_math_input = ""  # What the player is typing
math_feedback = ""  # "Correct!" or "Try again!"
math_feedback_timer = 0  # How long to show feedback

# SETTINGS VARIABLES
volume_level = 5  # Volume from 0-10 (5 = 50%)
colorblind_mode = False  # Is colorblind mode enabled?
game_paused = False  # Is the game paused?

# COLOR VARIABLES - Normal Mode
player_color_normal = (0, 255, 0)  # Green
background_color_normal = (135, 206, 235)  # Sky blue
ground_color_normal = (101, 67, 33)  # Brown
platform_color_normal = (139, 90, 43)  # Dark brown
coin_color_normal = (255, 215, 0)  # Gold
enemy_color_normal = (255, 0, 0)  # Red
door_color_normal = (139, 69, 19)  # Brown
door_locked_color_normal = (100, 100, 100)  # Gray

# COLOR VARIABLES - Colorblind Mode (uses blue/orange/yellow instead of red/green)
player_color_colorblind = (0, 150, 255)  # Bright blue
background_color_colorblind = (200, 220, 240)  # Light gray-blue
ground_color_colorblind = (80, 80, 80)  # Dark gray
platform_color_colorblind = (120, 120, 120)  # Medium gray
coin_color_colorblind = (255, 200, 0)  # Bright yellow
enemy_color_colorblind = (255, 100, 0)  # Orange
door_color_colorblind = (100, 100, 150)  # Blue-gray
door_locked_color_colorblind = (60, 60, 60)  # Very dark gray

# Current active colors (will change based on colorblind mode)
player_color = player_color_normal
background_color = background_color_normal
ground_color = ground_color_normal
platform_color = platform_color_normal
coin_color = coin_color_normal
enemy_color = enemy_color_normal
door_color = door_color_normal
door_locked_color = door_locked_color_normal

# FONT for displaying text
font = pygame.font.Font(None, 25)
big_font = pygame.font.Font(None, 72)

# BUTTON CLASS - Simple buttons for start screen
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        if self.rect.collidepoint(mouse_pos) and mouse_clicked:
            return True
        return False
    
    def draw(self, screen):
        # Choose color based on hover state
        draw_color = self.hover_color if self.is_hovered else self.color
        
        # Draw button
        pygame.draw.rect(screen, draw_color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)
        
        # Draw text
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_x = self.rect.centerx - text_surface.get_width() / 2
        text_y = self.rect.centery - text_surface.get_height() / 2
        screen.blit(text_surface, (text_x, text_y))

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, start_val, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.label = label
        self.dragging = False
        self.handle_rect = pygame.Rect(0, 0, 20, height + 10)
        self.update_handle_position()
    
    def update_handle_position(self):
        # Calculate handle position based on value
        if self.max_val == self.min_val:
            ratio = 0  # Avoid division by zero
        else:
            ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        ratio = max(0, min(1, ratio))  # Clamp between 0 and 1
        handle_x = self.rect.x + ratio * self.rect.width - 10
        self.handle_rect.centerx = handle_x + 10
        self.handle_rect.centery = self.rect.centery
    
    def draw(self, screen):
        # Draw label
        label_text = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_text, (self.rect.x, self.rect.y - 35))
        
        # Draw slider track
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        # Draw filled portion
        if self.max_val == self.min_val:
            filled_width = 0  # Avoid division by zero
        else:
            filled_width = ((self.value - self.min_val) / (self.max_val - self.min_val)) * self.rect.width
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, filled_width, self.rect.height)
        pygame.draw.rect(screen, (0, 200, 0), filled_rect)
        
        # Draw handle
        pygame.draw.rect(screen, (200, 200, 200), self.handle_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.handle_rect, 2)
        
        # Draw value
        value_text = font.render(str(self.value), True, (255, 255, 255))
        screen.blit(value_text, (self.rect.x + self.rect.width + 15, self.rect.y))
    
    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(mouse_pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Update value based on mouse position
                relative_x = mouse_pos[0] - self.rect.x
                ratio = relative_x / self.rect.width
                ratio = max(0, min(1, ratio))  # Clamp between 0 and 1
                self.value = int(self.min_val + ratio * (self.max_val - self.min_val))
                self.update_handle_position()
                return True
        return False

# TOGGLE BUTTON CLASS - For colorblind mode
class ToggleButton:
    def __init__(self, x, y, width, height, label, start_state=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.is_on = start_state
        self.is_hovered = False
    
    def draw(self, screen):
        # Draw label
        label_text = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_text, (self.rect.x, self.rect.y - 35))
        
        # Choose color based on state
        if self.is_on:
            color = (0, 200, 0) if not self.is_hovered else (0, 255, 0)
            state_text = "ON"
        else:
            color = (200, 0, 0) if not self.is_hovered else (255, 0, 0)
            state_text = "OFF"
        
        # Draw button
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)
        
        # Draw state text
        text_surface = font.render(state_text, True, (255, 255, 255))
        text_x = self.rect.centerx - text_surface.get_width() / 2
        text_y = self.rect.centery - text_surface.get_height() / 2
        screen.blit(text_surface, (text_x, text_y))
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    
    def is_clicked(self, mouse_pos, mouse_clicked):
        if self.rect.collidepoint(mouse_pos) and mouse_clicked:
            self.is_on = not self.is_on  # Toggle state
            return True
        return False

# CREATE BUTTONS for start screen
play_button = Button(300, 200, 200, 60, "PLAY", (0, 150, 0), (0, 200, 0))
how_to_play_button = Button(300, 280, 200, 60, "HOW TO PLAY", (0, 100, 150), (0, 150, 200))
settings_button = Button(300, 360, 200, 60, "SETTINGS", (100, 100, 0), (150, 150, 0))
back_button = Button(300, 500, 200, 60, "BACK", (150, 0, 0), (200, 0, 0))

# CREATE BUTTONS for pause screen
resume_button = Button(300, 200, 200, 60, "RESUME", (0, 150, 0), (0, 200, 0))
pause_settings_button = Button(300, 280, 200, 60, "SETTINGS", (100, 100, 0), (150, 150, 0))
quit_to_menu_button = Button(300, 360, 200, 60, "QUIT TO MENU", (150, 0, 0), (200, 0, 0))

# CREATE SETTINGS CONTROLS
volume_slider = Slider(250, 250, 300, 20, 0, 10, volume_level, "Volume:")
colorblind_toggle = ToggleButton(300, 350, 200, 60, "Colorblind Mode:", colorblind_mode)

# Variables that will be set by setup_level()
platforms = []  # Static platforms: [x, y, width, height]
moving_platforms = []  # Moving platforms: [x, y, width, height, start_x, end_x, speed, direction]
pits = []  # Death pits: [x, y, width, height]
coins = []
enemies = []  # Enemies: [x, y, width, height, start_x, end_x, speed, direction]
exit_door = []  # Exit door: [x, y, width, height]

# FUNCTION TO RESET PLAYER TO START OF CURRENT LEVEL (when dying)
def respawn_player():
    global player_x, player_y, player_velocity_x, player_velocity_y, camera_x, respawning, respawn_timer
    player_x = 100
    player_y = 100
    player_velocity_x = 0
    player_velocity_y = 0
    camera_x = 0  # Reset camera to start
    respawning = False
    respawn_timer = 0


# FUNCTION TO UPDATE COLORS BASED ON COLORBLIND MODE
def update_colors():
    global player_color, background_color, ground_color, platform_color, coin_color, enemy_color, door_color, door_locked_color
    
    if colorblind_mode:
        player_color = player_color_colorblind
        background_color = background_color_colorblind
        ground_color = ground_color_colorblind
        platform_color = platform_color_colorblind
        coin_color = coin_color_colorblind
        enemy_color = enemy_color_colorblind
        door_color = door_color_colorblind
        door_locked_color = door_locked_color_colorblind
    else:
        player_color = player_color_normal
        background_color = background_color_normal
        ground_color = ground_color_normal
        platform_color = platform_color_normal
        coin_color = coin_color_normal
        enemy_color = enemy_color_normal
        door_color = door_color_normal
        door_locked_color = door_locked_color_normal


# FUNCTION TO UPDATE SOUND VOLUMES
def update_volume():
    volume_float = volume_level / 10.0  # Convert 0-10 to 0.0-1.0
    
    # Update sound effects volume
    if jump_sound:
        jump_sound.set_volume(volume_float)
    if coin_sound:
        coin_sound.set_volume(volume_float)
    if enemy_defeat_sound:
        enemy_defeat_sound.set_volume(volume_float)
    if death_sound:
        death_sound.set_volume(volume_float)
    
    # Update music volume
    pygame.mixer.music.set_volume(volume_float * 0.5)  # Music at 50% of sound effects




# FUNCTION TO GENERATE RANDOM MATH QUESTION
def generate_math_question():
    import random
    
    # Pick random numbers for the question
    num1 = random.randint(5, 20)
    num2 = random.randint(2, 10)
    
    # Pick random operation (1 = addition, 2 = subtraction, 3 = multiplication)
    operation = random.randint(1, 3)
    
    if operation == 1:
        # Addition: x + num2 = answer
        answer = num1 + num2
        question = f"Solve: x + {num2} = {answer}"
        correct_answer = num1
    elif operation == 2:
        # Subtraction: x - num2 = answer
        answer = num1 - num2
        question = f"Solve: x - {num2} = {answer}"
        correct_answer = num1
    else:
        # Multiplication: x * num2 = answer
        answer = num1 * num2
        question = f"Solve: x * {num2} = {answer}"
        correct_answer = num1
    
    return question, correct_answer


# FUNCTION TO SET UP EACH LEVEL
def setup_level(level_number):
    global platforms, moving_platforms, pits, coins, enemies, exit_door, player_x, player_y, player_velocity_y, player_velocity_x, camera_x
    
    # Reset player position and physics
    player_x = 100
    player_y = 100
    player_velocity_y = 0
    player_velocity_x = 0
    camera_x = 0  # Reset camera
    
    # LEVEL 1 - Tutorial level with all mechanics
    if level_number == 1:
        # Static platforms: [x, y, width, height]
        platforms = [
            [200, 400, 150, 20],
            [450, 300, 120, 20],
            [100, 200, 100, 20],
            [800, 350, 150, 20],
            [1100, 400, 200, 20],
            [1500, 300, 150, 20],
            [1800, 400, 150, 20],
            [2200, 350, 200, 20],
            [2600, 300, 150, 20],
            [2900, 450, 200, 20]
        ]
        
        # Moving platforms: [x, y, width, height, start_x, end_x, speed, direction]
        # direction: 1 = moving right, -1 = moving left
        moving_platforms = [
            [650, 250, 100, 20, 650, 900, 2, 1],  # Moves between x=650 and x=900
            [1350, 200, 100, 20, 1350, 1600, 1.5, 1],
            [2000, 250, 120, 20, 2000, 2400, 2.5, 1]
        ]
        
        # Pits: [x, y, width, height] - These kill the player!
        pits = [
            [350, 500, 100, 100],  # Small pit
            [1300, 500, 150, 100],  # Medium pit
            [2450, 500, 200, 100]  # Large pit
        ]
        
        # Coins: [x, y]
        coins = [
            [275, 360],
            [500, 260],
            [140, 160],
            [875, 310],
            [1200, 360],
            [1575, 260],
            [2100, 310],
            [2275, 310],
            [2675, 260],
            [2975, 410]
        ]
        
        # Enemies: [x, y, width, height, start_x, end_x, speed, direction]
        # Jump on top to defeat them! Touch sides = death!
        enemies = [
            [600, 460, 40, 40, 550, 750, 1, 1],  # Patrol on ground
            [1000, 360, 40, 40, 950, 1250, 1.5, 1],
            [1700, 360, 40, 40, 1650, 1900, 1, 1],
            [2500, 460, 40, 40, 2400, 2700, 2, 1]
        ]
        
        # Exit door: [x, y, width, height]
        exit_door = [3100, 370, 60, 80]  # At the end of the level
    
    # LEVEL 2 - Harder level
    elif level_number == 2:
        platforms = [
            [50, 450, 100, 20],
            [200, 380, 80, 20],
            [320, 310, 80, 20],
            [440, 240, 80, 20],
            [700, 400, 150, 20],
            [1000, 350, 120, 20],
            [1300, 280, 100, 20],
            [1600, 350, 150, 20],
            [2000, 400, 200, 20],
            [2400, 300, 150, 20],
            [2800, 400, 200, 20]
        ]
        
        moving_platforms = [
            [560, 200, 100, 20, 560, 850, 2, 1],
            [1450, 180, 100, 20, 1450, 1750, 2.5, 1],
            [2250, 250, 120, 20, 2250, 2550, 2, 1]
        ]
        
        pits = [
            [150, 500, 170, 100],
            [850, 500, 150, 100],
            [1750, 500, 250, 100],
            [2600, 500, 200, 100]
        ]
        
        coins = [
            [90, 410],
            [240, 340],
            [360, 270],
            [775, 360],
            [1070, 310],
            [1370, 240],
            [1670, 310],
            [2100, 360],
            [2470, 260],
            [2870, 360]
        ]
        
        enemies = [
            [500, 460, 40, 40, 450, 680, 1.5, 1],
            [900, 360, 40, 40, 850, 1150, 2, 1],
            [1500, 310, 40, 40, 1450, 1700, 1, 1],
            [2100, 360, 40, 40, 2050, 2350, 1.5, 1],
            [2600, 360, 40, 40, 2550, 2950, 2, 1]
        ]
        
        exit_door = [3000, 320, 60, 80]
    
    # LEVEL 3 - Math Challenge Level (No images, colored shapes only)
    elif level_number == 3:
        platforms = [
            [150, 450, 120, 20],
            [350, 380, 100, 20],
            [550, 320, 100, 20],
            [750, 380, 120, 20],
            [950, 450, 150, 20],
            [1200, 380, 100, 20],
            [1400, 300, 120, 20],
            [1650, 380, 100, 20],
            [1900, 450, 150, 20],
            [2150, 350, 120, 20],
            [2400, 280, 100, 20],
            [2650, 350, 150, 20],
            [2900, 420, 120, 20]
        ]
        
        moving_platforms = [
            [1100, 250, 100, 20, 1100, 1350, 2, 1],
            [1750, 220, 100, 20, 1750, 2000, 2.5, 1],
            [2500, 200, 100, 20, 2500, 2750, 2, 1]
        ]
        
        pits = [
            [280, 500, 70, 100],
            [470, 500, 80, 100],
            [1550, 500, 100, 100],
            [2050, 500, 100, 100],
            [2800, 500, 100, 100]
        ]
        
        coins = [
            [200, 410],
            [400, 340],
            [600, 280],
            [800, 340],
            [1000, 410],
            [1250, 340],
            [1450, 260],
            [1700, 340],
            [1950, 410],
            [2200, 310],
            [2450, 240],
            [2700, 310],
            [2950, 380]
        ]
        
        # TWICE AS MANY ENEMIES (8 total for level 3)
        enemies = [
            [250, 460, 40, 40, 200, 350, 1.5, 1],
            [500, 370, 40, 40, 450, 650, 1, 1],
            [800, 370, 40, 40, 750, 950, 1.5, 1],
            [1100, 410, 40, 40, 1050, 1200, 2, 1],
            [1500, 340, 40, 40, 1450, 1700, 1, 1],
            [1800, 410, 40, 40, 1750, 2000, 1.5, 1],
            [2250, 380, 40, 40, 2200, 2500, 2, 1],
            [2750, 380, 40, 40, 2700, 3000, 1.5, 1]
        ]
        
        exit_door = [3100, 340, 60, 80]
    
    # LEVEL 4 - Harder Math Challenge Level
    elif level_number == 4:
        platforms = [
            [100, 450, 100, 20],
            [280, 380, 90, 20],
            [450, 310, 90, 20],
            [620, 240, 90, 20],
            [850, 350, 120, 20],
            [1050, 280, 100, 20],
            [1250, 380, 100, 20],
            [1450, 300, 100, 20],
            [1700, 400, 120, 20],
            [1950, 320, 100, 20],
            [2200, 400, 120, 20],
            [2450, 300, 100, 20],
            [2700, 380, 120, 20],
            [2950, 450, 150, 20]
        ]
        
        moving_platforms = [
            [750, 200, 100, 20, 750, 1000, 2.5, 1],
            [1550, 180, 100, 20, 1550, 1850, 3, 1],
            [2350, 220, 100, 20, 2350, 2600, 2, 1]
        ]
        
        pits = [
            [200, 500, 80, 100],
            [370, 500, 80, 100],
            [540, 500, 80, 100],
            [1350, 500, 100, 100],
            [1850, 500, 100, 100],
            [2600, 500, 100, 100]
        ]
        
        coins = [
            [150, 410],
            [330, 340],
            [500, 270],
            [670, 200],
            [900, 310],
            [1100, 240],
            [1300, 340],
            [1500, 260],
            [1750, 360],
            [2000, 280],
            [2250, 360],
            [2500, 260],
            [2750, 340],
            [3000, 410]
        ]
        
        # TWICE AS MANY ENEMIES (10 total for level 4)
        enemies = [
            [200, 460, 40, 40, 150, 350, 2, 1],
            [400, 340, 40, 40, 350, 550, 1.5, 1],
            [650, 270, 40, 40, 600, 850, 1, 1],
            [950, 380, 40, 40, 900, 1150, 2, 1],
            [1150, 310, 40, 40, 1100, 1350, 1.5, 1],
            [1400, 330, 40, 40, 1350, 1600, 2, 1],
            [1650, 430, 40, 40, 1600, 1850, 1.5, 1],
            [1900, 350, 40, 40, 1850, 2100, 2, 1],
            [2300, 430, 40, 40, 2250, 2550, 1.5, 1],
            [2800, 410, 40, 40, 2750, 3050, 2, 1]
        ]
        
        exit_door = [3200, 370, 60, 80]
    
    # LEVEL 5 - Final Challenge Level
    elif level_number == 5:
        platforms = [
            [80, 450, 100, 20],
            [250, 400, 80, 20],
            [400, 340, 80, 20],
            [550, 280, 80, 20],
            [700, 220, 80, 20],
            [900, 320, 120, 20],
            [1100, 250, 100, 20],
            [1300, 350, 100, 20],
            [1550, 280, 100, 20],
            [1800, 380, 120, 20],
            [2050, 300, 100, 20],
            [2300, 400, 120, 20],
            [2550, 320, 100, 20],
            [2800, 400, 120, 20],
            [3050, 450, 150, 20]
        ]
        
        moving_platforms = [
            [800, 150, 100, 20, 800, 1050, 3, 1],
            [1450, 180, 100, 20, 1450, 1750, 2.5, 1],
            [1950, 200, 100, 20, 1950, 2250, 3, 1],
            [2650, 220, 100, 20, 2650, 2950, 2.5, 1]
        ]
        
        pits = [
            [180, 500, 70, 100],
            [330, 500, 70, 100],
            [480, 500, 70, 100],
            [630, 500, 70, 100],
            [1200, 500, 100, 100],
            [1700, 500, 100, 100],
            [2200, 500, 100, 100],
            [2700, 500, 100, 100]
        ]
        
        coins = [
            [130, 410],
            [300, 360],
            [450, 300],
            [600, 240],
            [750, 180],
            [950, 280],
            [1150, 210],
            [1350, 310],
            [1600, 240],
            [1850, 340],
            [2100, 260],
            [2350, 360],
            [2600, 280],
            [2850, 360],
            [3100, 410]
        ]
        
        # TWICE AS MANY ENEMIES (12 total for level 5 - hardest!)
        enemies = [
            [180, 460, 40, 40, 130, 320, 2, 1],
            [350, 370, 40, 40, 300, 500, 2, 1],
            [600, 310, 40, 40, 550, 750, 1.5, 1],
            [850, 250, 40, 40, 800, 1050, 2.5, 1],
            [1050, 350, 40, 40, 1000, 1250, 2, 1],
            [1250, 280, 40, 40, 1200, 1450, 1.5, 1],
            [1500, 310, 40, 40, 1450, 1700, 2, 1],
            [1750, 410, 40, 40, 1700, 1950, 2, 1],
            [2000, 330, 40, 40, 1950, 2200, 2.5, 1],
            [2400, 430, 40, 40, 2350, 2650, 1.5, 1],
            [2700, 350, 40, 40, 2650, 2950, 2, 1],
            [3000, 430, 40, 40, 2950, 3200, 2, 1]
        ]
        
        exit_door = [3300, 370, 60, 80]
    
    return platforms, moving_platforms, pits, coins, enemies, exit_door, player_x, player_y, player_velocity_y, player_velocity_x, camera_x

# FUNCTION TO RESET THE ENTIRE GAME
def reset_game():
    global current_level, score, game_state, player_x, player_y, player_velocity_y, player_velocity_x, particles, transition_alpha, transitioning, player_lives, camera_x
    current_level = 1
    score = 0
    game_state = "playing"
    player_lives = 3  # Reset lives
    player_x = 100
    player_y = 100
    player_velocity_y = 0
    player_velocity_x = 0
    camera_x = 0
    particles = []
    transition_alpha = 0
    transitioning = False
    platforms, moving_platforms, pits, coins, enemies, exit_door, player_x, player_y, player_velocity_y, player_velocity_x, camera_x = setup_level(1)
    return platforms, moving_platforms, pits, coins, enemies, exit_door


# Initialize volume
update_volume()

# Set up the first level when the game starts (but don't run it yet - start screen first!)
# We'll set this up when the player clicks PLAY
platforms = []
moving_platforms = []
pits = []
coins = []
enemies = []
exit_door = []

# Variable to control level transition display
show_level_text = True
level_text_timer = 0
level_text_duration = 120

# Game loop
running = True
while running:
    
    # Event handling
    mouse_clicked = False  # Track if mouse was clicked this frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True
        # Handle slider events when in settings screen
        if game_state == "settings":
            volume_changed = volume_slider.handle_event(event, pygame.mouse.get_pos())
            if volume_changed:
                volume_level = volume_slider.value
                update_volume()
        # Handle math question input (for levels 3, 4, 5)
        if asking_math_question and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter key
                # Check if answer is correct
                try:
                    player_answer = int(player_math_input)
                    if player_answer == math_answer:
                        math_feedback = "Correct! Starting level..."
                        math_feedback_timer = 60  # Show for 1 second
                        asking_math_question = False
                        show_level_text = True
                        level_text_timer = 0
                    else:
                        math_feedback = "Wrong! Try again."
                        math_feedback_timer = 60
                        player_math_input = ""  # Clear input
                except ValueError:
                    math_feedback = "Please enter a number!"
                    math_feedback_timer = 60
                    player_math_input = ""
            elif event.key == pygame.K_BACKSPACE:
                # Delete last character
                player_math_input = player_math_input[:-1]
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                # Allow negative numbers
                if len(player_math_input) == 0:
                    player_math_input += "-"
            else:
                # Add typed number to input
                if event.unicode.isdigit():
                    player_math_input += event.unicode
    
    # Get mouse position for buttons
    mouse_pos = pygame.mouse.get_pos()
    # KEYBOARD INPUT
    keys = pygame.key.get_pressed()
    
    # HANDLE START SCREEN
    if game_state == "start_screen":
        # Update button hover states
        play_button.check_hover(mouse_pos)
        how_to_play_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        
        # Check if play button clicked
        if play_button.is_clicked(mouse_pos, mouse_clicked):
            game_state = "playing"
            # Set up first level
            platforms, moving_platforms, pits, coins, enemies, exit_door, player_x, player_y, player_velocity_y, player_velocity_x, camera_x = setup_level(current_level)
            show_level_text = True
            level_text_timer = 0
        
        # Check if how to play button clicked
        if how_to_play_button.is_clicked(mouse_pos, mouse_clicked):
            game_state = "how_to_play"
        
        # Check if settings button clicked
        if settings_button.is_clicked(mouse_pos, mouse_clicked):
            game_state = "settings"
    
    # HANDLE SETTINGS SCREEN
    elif game_state == "settings":
        # Update back button hover state
        back_button.check_hover(mouse_pos)
        colorblind_toggle.check_hover(mouse_pos)
        
        # Check if colorblind toggle clicked
        if colorblind_toggle.is_clicked(mouse_pos, mouse_clicked):
            colorblind_mode = colorblind_toggle.is_on
            update_colors()
        
        # Check if back button clicked
        if back_button.is_clicked(mouse_pos, mouse_clicked):
            if game_paused:
                game_state = "paused"
            else:
                game_state = "start_screen"
    
    # HANDLE HOW TO PLAY SCREEN
    elif game_state == "how_to_play":
        # Update back button hover state
        back_button.check_hover(mouse_pos)
        
        # Check if back button clicked
        if back_button.is_clicked(mouse_pos, mouse_clicked):
            game_state = "start_screen"

    # Check for restart key (R) on win or game over screens
    if (game_state == "won" or game_state == "game_over") and keys[pygame.K_r]:
        platforms, moving_platforms, pits, coins, enemies, exit_door = reset_game()
        show_level_text = True
        level_text_timer = 0
    
    # HANDLE RESPAWNING AFTER DEATH
    if respawning:
        respawn_timer += 1
        if respawn_timer >= respawn_duration:
            respawn_player()
    
    # Count down math question feedback timer
    if math_feedback_timer > 0:
        math_feedback_timer -= 1
        if math_feedback_timer == 0:
            math_feedback = ""

    # Check for ESC key to pause game
    if game_state == "playing" and keys[pygame.K_ESCAPE]:
        game_state = "paused"
        game_paused = True
    
    # HANDLE PAUSE SCREEN
    if game_state == "paused":
        resume_button.check_hover(mouse_pos)
        pause_settings_button.check_hover(mouse_pos)
        quit_to_menu_button.check_hover(mouse_pos)
        
        # Check if resume button clicked
        if resume_button.is_clicked(mouse_pos, mouse_clicked):
            game_state = "playing"
            game_paused = False
        
        # Check if settings button clicked
        if pause_settings_button.is_clicked(mouse_pos, mouse_clicked):
            game_state = "settings"
        
        # Check if quit to menu button clicked
        if quit_to_menu_button.is_clicked(mouse_pos, mouse_clicked):
            game_state = "start_screen"
            game_paused = False
            # Reset game
            platforms, moving_platforms, pits, coins, enemies, exit_door = reset_game()

    
    # ONLY UPDATE GAME LOGIC IF WE'RE PLAYING (and not respawning or answering math)
    if game_state == "playing" and not respawning and not asking_math_question:
        # SMOOTH MOVEMENT
        if keys[pygame.K_LEFT]:
            player_velocity_x -= player_acceleration
        if keys[pygame.K_RIGHT]:
            player_velocity_x += player_acceleration
        
        player_velocity_x *= player_friction
        
        if player_velocity_x > player_max_speed:
            player_velocity_x = player_max_speed
        if player_velocity_x < -player_max_speed:
            player_velocity_x = -player_max_speed
        
        player_x += player_velocity_x
        
        # SCREEN BOUNDARIES - But allow moving forward infinitely
        if player_x < 0:
            player_x = 0
            player_velocity_x = 0
        # No right boundary! Player can go as far as level_width
        
        # JUMP with COYOTE TIME
        if keys[pygame.K_SPACE] and (on_ground or coyote_timer > 0):
            player_velocity_y = jump_strength
            on_ground = False
            coyote_timer = 0
            if jump_sound:
                jump_sound.play()
        
        # APPLY GRAVITY
        player_velocity_y += gravity
        
        # UPDATE VERTICAL POSITION
        player_y += player_velocity_y
        
        # ASSUME PLAYER IS IN THE AIR
        on_ground = False
        
        # CHECK COLLISION WITH GROUND
        if player_y + player_height >= ground_y:
            player_y = ground_y - player_height
            player_velocity_y = 0
            on_ground = True
        
        # UPDATE COYOTE TIMER
        if on_ground:
            coyote_timer = coyote_time
        else:
            coyote_timer -= 1
            if coyote_timer < 0:
                coyote_timer = 0
        
        # CHECK IF PLAYER FELL OFF THE SCREEN
        if player_y > 600:
            # Player dies - lose a life
            player_lives -= 1
            if death_sound:
                death_sound.play()
            
            if player_lives <= 0:
                game_state = "game_over"
            else:
                # Start respawn process
                respawning = True
                respawn_timer = 0
        
        # UPDATE CAMERA - Follow player (smooth scrolling)
        # Keep player roughly in center of screen
        target_camera_x = player_x - 400  # 400 is half screen width
        
        # Don't scroll past level boundaries
        if target_camera_x < 0:
            target_camera_x = 0
        if target_camera_x > level_width - 800:  # 800 is screen width
            target_camera_x = level_width - 800
        
        # Smooth camera movement
        camera_x += (target_camera_x - camera_x) * 0.1  # 0.1 = smoothness. Try 0.05 for slower, 0.2 for faster!
        
        # UPDATE MOVING PLATFORMS
        for platform in moving_platforms:
            # platform = [x, y, width, height, start_x, end_x, speed, direction]
            platform[0] += platform[6] * platform[7]  # Move by speed * direction
            
            # Reverse direction at boundaries
            if platform[0] <= platform[4]:  # Reached start
                platform[0] = platform[4]
                platform[7] = 1  # Move right
            elif platform[0] >= platform[5]:  # Reached end
                platform[0] = platform[5]
                platform[7] = -1  # Move left
        
        # CHECK COLLISION WITH STATIC PLATFORMS
        for platform in platforms:
            platform_x = platform[0]
            platform_y = platform[1]
            platform_width = platform[2]
            platform_height = platform[3]
            
            horizontal_overlap = (player_x + player_width > platform_x and 
                                 player_x < platform_x + platform_width)
            
            vertical_collision = (player_y + player_height >= platform_y and 
                                 player_y + player_height <= platform_y + platform_height and
                                 player_velocity_y >= 0)
            
            if horizontal_overlap and vertical_collision:
                player_y = platform_y - player_height
                player_velocity_y = 0
                on_ground = True
        
        # CHECK COLLISION WITH MOVING PLATFORMS
        for platform in moving_platforms:
            platform_x = platform[0]
            platform_y = platform[1]
            platform_width = platform[2]
            platform_height = platform[3]
            
            horizontal_overlap = (player_x + player_width > platform_x and 
                                 player_x < platform_x + platform_width)
            
            vertical_collision = (player_y + player_height >= platform_y and 
                                 player_y + player_height <= platform_y + platform_height and
                                 player_velocity_y >= 0)
            
            if horizontal_overlap and vertical_collision:
                player_y = platform_y - player_height
                player_velocity_y = 0
                on_ground = True
                # Move player with platform!
                player_x += platform[6] * platform[7]
        
        # CHECK COLLISION WITH PITS (instant death)
        for pit in pits:
            pit_x = pit[0]
            pit_y = pit[1]
            pit_width = pit[2]
            pit_height = pit[3]
            
            # Check if player overlaps with pit
            if (player_x + player_width > pit_x and 
                player_x < pit_x + pit_width and
                player_y + player_height > pit_y and
                player_y < pit_y + pit_height):
                # Player fell in pit - die!
                player_lives -= 1
                if death_sound:
                    death_sound.play()
                
                if player_lives <= 0:
                    game_state = "game_over"
                else:
                    respawning = True
                    respawn_timer = 0
        
        # UPDATE ENEMIES (move back and forth)
        for enemy in enemies[:]:  # Use copy so we can remove defeated enemies
            # enemy = [x, y, width, height, start_x, end_x, speed, direction]
            enemy[0] += enemy[6] * enemy[7]  # Move by speed * direction
            
            # Reverse direction at boundaries
            if enemy[0] <= enemy[4]:  # Reached start
                enemy[0] = enemy[4]
                enemy[7] = 1  # Move right
            elif enemy[0] >= enemy[5]:  # Reached end
                enemy[0] = enemy[5]
                enemy[7] = -1  # Move left
        
        # CHECK COLLISION WITH ENEMIES
        for enemy in enemies[:]:
            enemy_x = enemy[0]
            enemy_y = enemy[1]
            enemy_width = enemy[2]
            enemy_height = enemy[3]
            
            # Check if player overlaps with enemy
            if (player_x + player_width > enemy_x and 
                player_x < enemy_x + enemy_width and
                player_y + player_height > enemy_y and
                player_y < enemy_y + enemy_height):
                
                # Check if player jumped on top of enemy
                # Player's bottom was above enemy's top in previous frame
                if player_velocity_y > 0 and player_y + player_height - player_velocity_y <= enemy_y + 10:
                    # Player defeated enemy!
                    enemies.remove(enemy)
                    player_velocity_y = -10  # Bounce up
                    if enemy_defeat_sound:
                        enemy_defeat_sound.play()
                    
                    # Create particles for defeated enemy
                    for i in range(12):
                        angle = i * 30
                        angle_rad = math.radians(angle)
                        particle_vel_x = math.cos(angle_rad) * 4
                        particle_vel_y = math.sin(angle_rad) * 4
                        particles.append([enemy_x + enemy_width/2, enemy_y + enemy_height/2, 
                                        particle_vel_x, particle_vel_y, 25])
                else:
                    # Player touched enemy from side - die!
                    player_lives -= 1
                    if death_sound:
                        death_sound.play()
                    
                    if player_lives <= 0:
                        game_state = "game_over"
                    else:
                        respawning = True
                        respawn_timer = 0
        
        # CHECK COIN COLLECTION WITH PARTICLE EFFECTS
        for coin in coins[:]:
            coin_x = coin[0]
            coin_y = coin[1]
            
            player_center_x = player_x + player_width / 2
            player_center_y = player_y + player_height / 2
            
            distance_x = player_center_x - coin_x
            distance_y = player_center_y - coin_y
            
            if (abs(distance_x) < coin_radius + player_width / 2 and 
                abs(distance_y) < coin_radius + player_height / 2):
                coins.remove(coin)
                score += 1
                
                if coin_sound:
                    coin_sound.play()
                
                # CREATE PARTICLE EFFECT
                for i in range(8):
                    angle = i * 45
                    angle_rad = math.radians(angle)
                    particle_vel_x = math.cos(angle_rad) * 3
                    particle_vel_y = math.sin(angle_rad) * 3
                    particles.append([coin_x, coin_y, particle_vel_x, particle_vel_y, 20])
        
        # UPDATE PARTICLES
        for particle in particles[:]:
            particle[0] += particle[2]
            particle[1] += particle[3]
            particle[4] -= 1
            
            if particle[4] <= 0:
                particles.remove(particle)
        
        # CHECK EXIT DOOR INTERACTION
        # Door is only accessible if all coins collected
        if len(coins) == 0 and exit_door and len(exit_door) > 0:
            door_x = exit_door[0]
            door_y = exit_door[1]
            door_width = exit_door[2]
            door_height = exit_door[3]
            
            # Check if player overlaps with door
            if (player_x + player_width > door_x and 
                player_x < door_x + door_width and
                player_y + player_height > door_y and
                player_y < door_y + door_height):
                # Player entered door - go to next level!
                transitioning = True
        
        # HANDLE LEVEL TRANSITION FADE
        if transitioning:
            transition_alpha += 10
            if transition_alpha >= 255:
                transition_alpha = 255
                current_level += 1
                
                if current_level <= total_levels:
                    platforms, moving_platforms, pits, coins, enemies, exit_door, player_x, player_y, player_velocity_y, player_velocity_x, camera_x = setup_level(current_level)
                    
                    # Check if this is a math challenge level (3, 4, or 5)
                    if current_level >= 3:
                        # Generate math question
                        math_question, math_answer = generate_math_question()
                        asking_math_question = True
                        player_math_input = ""
                        math_feedback = ""
                        transition_alpha = 0  # Clear transition so math question is visible
                    else:
                        show_level_text = True
                        level_text_timer = 0
                    
                    transitioning = False
                    if current_level < 3:
                        transition_alpha = 255  # Only fade for non-math levels
                else:
                    game_state = "won"
                    transitioning = False
                    transition_alpha = 0
        
        # Fade out after level loads
        if not transitioning and transition_alpha > 0:
            transition_alpha -= 10
            if transition_alpha < 0:
                transition_alpha = 0
        
        # UPDATE LEVEL TEXT TIMER
        if show_level_text:
            level_text_timer += 1
            if level_text_timer >= level_text_duration:
                show_level_text = False
    
    # DRAWING - This happens regardless of game state
    
    # Draw background image or solid color
    # Use images for levels 1-2, solid color for levels 3-5
    if background_image and current_level <= 2:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(background_color)
    
    # DRAW THE GROUND (adjusted for camera)
    pygame.draw.rect(screen, ground_color, (-camera_x, ground_y, level_width, 100))
    
    # DRAW ALL STATIC PLATFORMS (adjusted for camera)
    for platform in platforms:
        # Use images for levels 1-2, colored shapes for levels 3-5
        if platform_image and current_level <= 2:
            # Scale platform image to fit platform size
            scaled_image = pygame.transform.scale(platform_image, (platform[2], platform[3]))
            screen.blit(scaled_image, (platform[0] - camera_x, platform[1]))
        else:
            pygame.draw.rect(screen, platform_color, (platform[0] - camera_x, platform[1], platform[2], platform[3]))
    
    # DRAW ALL MOVING PLATFORMS (adjusted for camera)
    for platform in moving_platforms:
        # Use images for levels 1-2, colored shapes for levels 3-5
        if platform_image and current_level <= 2:
            scaled_image = pygame.transform.scale(platform_image, (platform[2], platform[3]))
            screen.blit(scaled_image, (platform[0] - camera_x, platform[1]))
        else:
            # Draw with different color to distinguish from static
            pygame.draw.rect(screen, (100, 150, 200), (platform[0] - camera_x, platform[1], platform[2], platform[3]))
    
    # DRAW ALL PITS (adjusted for camera)
    for pit in pits:
        # Draw pits as dark holes
        pygame.draw.rect(screen, (20, 20, 20), (pit[0] - camera_x, pit[1], pit[2], pit[3]))
    
    # DRAW ALL COINS (adjusted for camera)
    for coin in coins:
        pygame.draw.circle(screen, coin_color, (int(coin[0] - camera_x), coin[1]), coin_radius)
    
    # DRAW ALL ENEMIES (adjusted for camera)
    for enemy in enemies:
        # Use images for levels 1-2, colored shapes for levels 3-5
        if enemy_image and current_level <= 2:
            scaled_image = pygame.transform.scale(enemy_image, (enemy[2], enemy[3]))
            screen.blit(scaled_image, (enemy[0] - camera_x, enemy[1]))
        else:
            pygame.draw.rect(screen, enemy_color, (enemy[0] - camera_x, enemy[1], enemy[2], enemy[3]))
    
    # DRAW EXIT DOOR (adjusted for camera)
    # Only draw if exit_door exists (not empty)
    if exit_door and len(exit_door) > 0:
        # Change color based on whether door is unlocked (all coins collected)
        if len(coins) == 0:
            door_draw_color = door_color  # Unlocked (brown)
        else:
            door_draw_color = door_locked_color  # Locked (gray)
        
        # Use images for levels 1-2, colored shapes for levels 3-5
        if door_image and current_level <= 2:
            screen.blit(door_image, (exit_door[0] - camera_x, exit_door[1]))
        else:
            pygame.draw.rect(screen, door_draw_color, (exit_door[0] - camera_x, exit_door[1], exit_door[2], exit_door[3]))
    
    # DRAW PARTICLES (adjusted for camera)
    for particle in particles:
        pygame.draw.circle(screen, coin_color, (int(particle[0] - camera_x), int(particle[1])), 4)
    
    # DRAW THE PLAYER (adjusted for camera) - only if not respawning
    if not respawning:
        if player_image:
            # Scale player image to fit player size
            scaled_player_image = pygame.transform.scale(player_image, (player_width, player_height))
            screen.blit(scaled_player_image, (int(player_x - camera_x), int(player_y)))
        else:
            # Fallback to rectangle if image not found
            pygame.draw.rect(screen, player_color, (int(player_x - camera_x), int(player_y), player_width, player_height))
    
    # DRAW THE SCORE, LEVEL, and LIVES (UI - not affected by camera)
    score_text = font.render(f"Coins: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    level_display_text = font.render(f"Level: {current_level}", True, (255, 255, 255))
    screen.blit(level_display_text, (10, 50))
    
    # NEW: Draw lives as hearts or numbers
    lives_text = font.render(f"Lives: {player_lives}", True, (255, 0, 0))
    screen.blit(lives_text, (10, 90))
    
    # Draw indicator if door is unlocked
    if len(coins) == 0:
        unlock_text = font.render("Door Unlocked!", True, (0, 255, 0))
        screen.blit(unlock_text, (10, 130))
    
    # DRAW RESPAWN MESSAGE
    if respawning:
        respawn_text = big_font.render("RESPAWNING...", True, (255, 255, 0))
        respawn_x = 400 - respawn_text.get_width() / 2
        screen.blit(respawn_text, (respawn_x, 250))
    
    # DRAW LEVEL TRANSITION TEXT
    if show_level_text and game_state == "playing" and not transitioning:
        level_text = big_font.render(f"LEVEL {current_level}", True, (255, 255, 0))
        text_x = 400 - level_text.get_width() / 2
        text_y = 250
        screen.blit(level_text, (text_x, text_y))
    
    # DRAW TRANSITION FADE OVERLAY
    if transition_alpha > 0:
        fade_surface = pygame.Surface((800, 600))
        fade_surface.set_alpha(transition_alpha)
        fade_surface.fill((0, 0, 0))
        screen.blit(fade_surface, (0, 0))
    
    # DRAW START SCREEN
    if game_state == "start_screen":
        # Draw semi-transparent overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 50))  # Dark blue tint
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = big_font.render("MY PLATFORMER", True, (255, 255, 0))
        title_x = 400 - title_text.get_width() / 2
        screen.blit(title_text, (title_x, 100))
        
        # Draw subtitle
        subtitle_text = font.render("A Side-Scrolling Adventure", True, (200, 200, 200))
        subtitle_x = 400 - subtitle_text.get_width() / 2
        screen.blit(subtitle_text, (subtitle_x, 180))
        
        # Draw buttons
        play_button.draw(screen)
        how_to_play_button.draw(screen)
        settings_button.draw(screen)


    # DRAW SETTINGS SCREEN
    elif game_state == "settings":
        # Draw semi-transparent overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = big_font.render("SETTINGS", True, (255, 255, 0))
        title_x = 400 - title_text.get_width() / 2
        screen.blit(title_text, (title_x, 80))
        
        # Draw volume slider
        volume_slider.draw(screen)
        
        # Draw colorblind toggle
        colorblind_toggle.draw(screen)
        
        # Draw back button
        back_button.draw(screen)

    
    # DRAW HOW TO PLAY SCREEN
    elif game_state == "how_to_play":
        # Draw semi-transparent overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = big_font.render("HOW TO PLAY", True, (255, 255, 0))
        title_x = 400 - title_text.get_width() / 2
        screen.blit(title_text, (title_x, 50))
        
        # Draw controls
        controls = [
            "CONTROLS:",
           
            "LEFT ARROW - Move Left",
            "RIGHT ARROW - Move Right",
            "SPACEBAR - Jump",
           
            "OBJECTIVE:",
            
            "Collect all coins to unlock the exit door",
            "Avoid pits and enemies",
            "Jump on enemies to defeat them",
            "You have 3 lives - don't run out!",
        ]
        
        y_position = 150
        for line in controls:
            if line == "CONTROLS:" or line == "OBJECTIVE:":
                # Draw section headers in yellow
                text_surface = font.render(line, True, (255, 255, 0))
            else:
                # Draw regular text in white
                text_surface = font.render(line, True, (255, 255, 255))
            
            text_x = 400 - text_surface.get_width() / 2
            screen.blit(text_surface, (text_x, y_position))
            y_position += 35
        
        # Draw back button
        back_button.draw(screen)


    # DRAW PAUSE SCREEN
    if game_state == "paused":
        # Draw semi-transparent overlay over the game
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 50))
        screen.blit(overlay, (0, 0))
        
        # Draw pause title
        pause_text = big_font.render("PAUSED", True, (255, 255, 0))
        pause_x = 400 - pause_text.get_width() / 2
        screen.blit(pause_text, (pause_x, 100))
        
        # Draw buttons
        resume_button.draw(screen)
        pause_settings_button.draw(screen)
        quit_to_menu_button.draw(screen)
        
        # Draw instruction
        instruction_text = font.render("Press ESC to resume", True, (150, 150, 150))
        instruction_x = 400 - instruction_text.get_width() / 2
        screen.blit(instruction_text, (instruction_x, 480))


    # DRAW WIN SCREEN
    if game_state == "won":
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        win_text = big_font.render("YOU WIN!", True, (255, 215, 0))
        win_x = 400 - win_text.get_width() / 2
        screen.blit(win_text, (win_x, 200))
        final_score_text = font.render(f"Total Coins: {score}", True, (255, 255, 255))
        score_x = 400 - final_score_text.get_width() / 2
        screen.blit(final_score_text, (score_x, 300))
        
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        restart_x = 400 - restart_text.get_width() / 2
        screen.blit(restart_text, (restart_x, 400))
    
    # DRAW GAME OVER SCREEN
    if game_state == "game_over":
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
        game_over_x = 400 - game_over_text.get_width() / 2
        screen.blit(game_over_text, (game_over_x, 200))
        
        lives_text = font.render("You ran out of lives!", True, (255, 255, 255))
        lives_x = 400 - lives_text.get_width() / 2
        screen.blit(lives_text, (lives_x, 300))
        
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        restart_x = 400 - restart_text.get_width() / 2
        screen.blit(restart_text, (restart_x, 400))
    
    # DRAW MATH QUESTION SCREEN (for levels 3, 4, 5)
    if asking_math_question:
        # Draw dark overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(230)
        overlay.fill((0, 0, 50))
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = big_font.render(f"LEVEL {current_level} CHALLENGE", True, (255, 215, 0))
        title_x = 400 - title_text.get_width() / 2
        screen.blit(title_text, (title_x, 100))
        
        # Draw instructions
        instruction_text = font.render("Solve the equation to continue:", True, (200, 200, 200))
        instruction_x = 400 - instruction_text.get_width() / 2
        screen.blit(instruction_text, (instruction_x, 180))
        
        # Draw math question
        question_text = big_font.render(math_question, True, (255, 255, 255))
        question_x = 400 - question_text.get_width() / 2
        screen.blit(question_text, (question_x, 250))
        
        # Draw input prompt
        prompt_text = font.render("Your answer:", True, (200, 200, 200))
        prompt_x = 400 - prompt_text.get_width() / 2
        screen.blit(prompt_text, (prompt_x, 350))
        
        # Draw input box
        input_box = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(screen, (50, 50, 100), input_box)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 3)
        
        # Draw player's typed answer
        answer_text = font.render(player_math_input, True, (255, 255, 255))
        answer_x = input_box.centerx - answer_text.get_width() / 2
        screen.blit(answer_text, (answer_x, 410))
        
        # Draw enter instruction
        enter_text = font.render("Press ENTER to submit", True, (150, 150, 150))
        enter_x = 400 - enter_text.get_width() / 2
        screen.blit(enter_text, (enter_x, 480))
        
        # Draw feedback (if any)
        if math_feedback:
            if "Correct" in math_feedback:
                feedback_color = (0, 255, 0)
            else:
                feedback_color = (255, 0, 0)
            feedback_text = big_font.render(math_feedback, True, feedback_color)
            feedback_x = 400 - feedback_text.get_width() / 2
            screen.blit(feedback_text, (feedback_x, 520))

    # Update the display
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()