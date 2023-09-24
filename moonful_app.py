import dataclasses
import pygame
import sys
import math
import agen
import breath_predictor
from breath_predictor import User
import cv2
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Constants for screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB format)
WHITE = (255, 255, 255)
BACK = (43, 30, 74)
BUTTON_COLOR = (0, 0, 0)
BUTTON_CLICKED_COLOR = (65, 48, 92) 


#SCREENS
WELCOME = 0
QUEST = 1
BREATH1 = 2
BREATH2 = 3
BREATH3 = 4
BREATH4 = 5
BREATH5 = 6
BREATH6 = 7
BREATH7 = 8
BREATH8 = 9
BREATH9 = 10
BREATH10 = 11
END = 12
BREATH = 13

qnum = 0

current_state = WELCOME

moon_image = pygame.image.load("moon.png")  # Replace "moon.png" with your image file path
moon_image = pygame.transform.scale(moon_image,(270,270))

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("moonful")

# Function to draw circular text
def welcome():
    screen.fill(BACK)

    num_stars = 100  # Adjust this as needed
    stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars

    # Draw circular text
    text = 'moonful'
    radius = 100
    font = pygame.font.Font('fo.ttf', 30)
    angle = 30
    step = (3 * (math.pi) / 2) / len(text)
    screen.blit(moon_image, (270, 70))
    for char in text:
        text_surface = font.render(char, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        x = SCREEN_WIDTH // 2 - text_rect.width // 2 + radius * math.cos(angle)
        y = SCREEN_HEIGHT // 3 - text_rect.height // 2 + radius * math.sin(angle)
        angle += step
        screen.blit(text_surface, (x, y))
    

welcome_button_rect = pygame.Rect(300, 500, 200, 50)
welcome_button_color = BUTTON_COLOR
welcome_button_font = pygame.font.Font('fo.ttf', 30)
welcome_button_text = "begin"  # Text to be displayed on the button
welcome_text_surface = welcome_button_font.render(welcome_button_text, True, (255, 255, 255))  # Render the text
welcome_text_rect = welcome_text_surface.get_rect(center=welcome_button_rect.center)  # Center the text on the button

nums = []

def quest(nums):
    global qnum  # Declare qnum as a global variable
    screen.fill(BACK)
    num_stars = 100  # Adjust this as needed
    stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
    questions = [
        'How stressed do you feel? (1-10)',
        'How tense do you feel? (1-10)',
        'How relaxed do you feel? (1-10)',
        'Are you having trouble breathing? (1-10)',
        'How fast is your heart beating? (1-10)',
        'How depressed do you feel? (1-10)',
        'How hot (temperature) do you feel? (1-10)',
        'How frustrated do you feel? (1-10)',
        'How anxious do you feel? (1-10)',
        'How happy do you feel? (1-10)'
    ]

    # Display questions
    font = pygame.font.Font(None, 36)
    question_text = questions[qnum]
    text_surface = font.render(question_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    button_width = 50
    button_height = 30
    button_spacing = 10
    button_start_x = (SCREEN_WIDTH - (button_width + button_spacing) * 10) // 2
    button_y = SCREEN_HEIGHT // 2 + 20

    for number in range(1, 11):
        button_rect = pygame.Rect(
            button_start_x + (number - 1) * (button_width + button_spacing),
            button_y,
            button_width,
            button_height,
        )
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        number_text = str(number)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(number_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for number in range(1, 11):
                    button_rect = pygame.Rect(
                        button_start_x + (number - 1) * (button_width + button_spacing),
                        button_y,
                        button_width,
                        button_height,
                    )
                    if button_rect.collidepoint(event.pos):
                        if qnum < 9:
                            qnum += 1
                            question_text = questions[qnum]
                            text_surface = font.render(question_text, True, (255, 255, 255))
                            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                            screen.blit(text_surface, text_rect)
                            print(number)
                            nums.append(number)
                        else:
                            nums.append(number)
            


def br1():
    # Define the durations for breathing in and out
    inhale_duration = 3  # 5 seconds
    exhale_duration = 6  # 10 seconds
    num_cycles = 3  # Number of times to repeat the cycle

    current_cycle = 0  # Initialize the current cycle
    inhale_timer = inhale_duration  # Start with inhaling
    exhale_timer = exhale_duration
    inhaling = True  # Flag to track inhaling/exhaling phase
    clock = pygame.time.Clock()

    # Description of pursed lip breathing
    
    description_text = [
    "Pursed Lip Breathing:",
    "1. Inhale slowly through your nose for 3 seconds.",
    "2. Pucker your lips as if you're about to whistle.",
    "3. Exhale slowly and gently through pursed lips for 6 seconds.",
    "4. Repeat this cycle for 3 rounds."
]



    while current_cycle < num_cycles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BACK)
        num_stars = 100  # Adjust this as needed
        stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
        description_surfaces = []

    # Create font and render text surfaces
        font = pygame.font.Font(None, 27)
        for line in description_text:
            text_surface = font.render(line, True, (0, 0, 0))
            description_surfaces.append(text_surface)

        # Display text surfaces with line breaks
        y_position = 200  # Adjust this value for vertical positioning
        for surface in description_surfaces:
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(surface, text_rect)
            y_position += surface.get_height() + 10  # Add vertical spacing

        # Continue with the rest of your code

        # Calculate the current countdown percentage
        if inhaling:
            countdown_percentage = (inhale_timer / inhale_duration) * 100
        else:
            countdown_percentage = (exhale_timer / exhale_duration) * 100

        # Draw the progress bar
        progress_bar_rect = pygame.Rect(100, 450, countdown_percentage * 6, 30)
        if inhaling:
            pygame.draw.rect(screen, (0, 128, 0), progress_bar_rect)  # Green for inhaling
        else:
            pygame.draw.rect(screen, (0, 0, 128), progress_bar_rect)  # Blue for exhaling

        # Draw the countdown timer text
        font = pygame.font.Font(None, 36)
        if inhaling:
            countdown_text = f"Inhale: {inhale_timer} seconds (Cycle {current_cycle + 1})"
        else:
            countdown_text = f"Exhale: {exhale_timer} seconds (Cycle {current_cycle + 1})"
        text_surface = font.render(countdown_text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 100, 400))

        pygame.display.flip()
        pygame.time.delay(1000)

        # Decrement the timers only if they are greater than 0
        if inhale_timer > 0 and exhale_timer > 0:
            if inhaling:
                inhale_timer -= 1
            else:
                exhale_timer -= 1

        if inhale_timer == 0 and inhaling:
            # Switch to exhaling
            inhale_timer = inhale_duration
            inhaling = False

        if exhale_timer == 0 and not inhaling:
            # Switch to inhaling and move to the next cycle
            exhale_timer = exhale_duration
            current_cycle += 1
            inhaling = True

        clock.tick(1)  # Limit the loop to 1 frame per second

    # When all cycles are finished, change the scene
    global current_state
    current_state = END

def br2():
    # Define the durations for breathing in and out
    inhale_duration = 3  # 5 seconds
    exhale_duration = 6  # 10 seconds
    num_cycles = 5  # Number of times to repeat the cycle

    current_cycle = 0  # Initialize the current cycle
    inhale_timer = inhale_duration  # Start with inhaling
    exhale_timer = exhale_duration
    inhaling = True  # Flag to track inhaling/exhaling phase
    clock = pygame.time.Clock()

    # Description of pursed lip breathing
    
    description_text = [
    "Diaphragmatic Breathing:",
        "1. Find a comfortable sitting or lying position.",
        "2. Place one hand on your chest and the other on your abdomen.",
        "3. Inhale deeply through your nose, allowing your abdomen to rise for 3 seconds",
        "4. Exhale slowly through pursed lips, feeling your abdomen fall for 6 seconds",
        "5. Repeat this cycle 5 times"
    ]



    while current_cycle < num_cycles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BACK)
        num_stars = 100  # Adjust this as needed
        stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
        
        description_surfaces = []

    # Create font and render text surfaces
        font = pygame.font.Font(None, 27)
        for line in description_text:
            text_surface = font.render(line, True, (0, 0, 0))
            description_surfaces.append(text_surface)

        # Display text surfaces with line breaks
        y_position = 200  # Adjust this value for vertical positioning
        for surface in description_surfaces:
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(surface, text_rect)
            y_position += surface.get_height() + 10  # Add vertical spacing

        # Continue with the rest of your code

        # Calculate the current countdown percentage
        if inhaling:
            countdown_percentage = (inhale_timer / inhale_duration) * 100
        else:
            countdown_percentage = (exhale_timer / exhale_duration) * 100

        # Draw the progress bar
        progress_bar_rect = pygame.Rect(100, 450, countdown_percentage * 6, 30)
        if inhaling:
            pygame.draw.rect(screen, (0, 128, 0), progress_bar_rect)  # Green for inhaling
        else:
            pygame.draw.rect(screen, (0, 0, 128), progress_bar_rect)  # Blue for exhaling

        # Draw the countdown timer text
        font = pygame.font.Font(None, 36)
        if inhaling:
            countdown_text = f"Inhale: {inhale_timer} seconds (Cycle {current_cycle + 1})"
        else:
            countdown_text = f"Exhale: {exhale_timer} seconds (Cycle {current_cycle + 1})"
        text_surface = font.render(countdown_text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 100, 400))

        pygame.display.flip()
        pygame.time.delay(1000)

        # Decrement the timers only if they are greater than 0
        if inhale_timer > 0 and exhale_timer > 0:
            if inhaling:
                inhale_timer -= 1
            else:
                exhale_timer -= 1

        if inhale_timer == 0 and inhaling:
            # Switch to exhaling
            inhale_timer = inhale_duration
            inhaling = False

        if exhale_timer == 0 and not inhaling:
            # Switch to inhaling and move to the next cycle
            exhale_timer = exhale_duration
            current_cycle += 1
            inhaling = True

        clock.tick(1)  # Limit the loop to 1 frame per second

    # When all cycles are finished, change the scene
    global current_state
    current_state = END

def br3():
    # Define the durations for breathing in and out
    inhale_duration = 4  # 5 seconds
    exhale_duration = 5  # 10 seconds
    num_cycles = 6  # Number of times to repeat the cycle

    current_cycle = 0  # Initialize the current cycle
    inhale_timer = inhale_duration  # Start with inhaling
    exhale_timer = exhale_duration
    inhaling = True  # Flag to track inhaling/exhaling phase
    clock = pygame.time.Clock()

    # Description of pursed lip breathing
    
    description_text = [
        "Focus Breathing:",
        "1. Sit or lie down in a quiet place.",
        "2. Close your eyes and take a deep inhale for 4 seconds",
        "3. Focus your attention solely on your breath. Exhale for 5 seconds",
        "4. Notice the sensation of the breath entering and leaving your body.",
        "5. If your mind wanders, gently bring your focus back to your breath. Repeat this cycle 6 times",

    ]



    while current_cycle < num_cycles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BACK)
        num_stars = 100  # Adjust this as needed
        stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
        description_surfaces = []

    # Create font and render text surfaces
        font = pygame.font.Font(None, 27)
        for line in description_text:
            text_surface = font.render(line, True, (0, 0, 0))
            description_surfaces.append(text_surface)

        # Display text surfaces with line breaks
        y_position = 200  # Adjust this value for vertical positioning
        for surface in description_surfaces:
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(surface, text_rect)
            y_position += surface.get_height() + 10  # Add vertical spacing

        # Continue with the rest of your code

        # Calculate the current countdown percentage
        if inhaling:
            countdown_percentage = (inhale_timer / inhale_duration) * 100
        else:
            countdown_percentage = (exhale_timer / exhale_duration) * 100

        # Draw the progress bar
        progress_bar_rect = pygame.Rect(100, 450, countdown_percentage * 6, 30)
        if inhaling:
            pygame.draw.rect(screen, (0, 128, 0), progress_bar_rect)  # Green for inhaling
        else:
            pygame.draw.rect(screen, (0, 0, 128), progress_bar_rect)  # Blue for exhaling

        # Draw the countdown timer text
        font = pygame.font.Font(None, 36)
        if inhaling:
            countdown_text = f"Inhale: {inhale_timer} seconds (Cycle {current_cycle + 1})"
        else:
            countdown_text = f"Exhale: {exhale_timer} seconds (Cycle {current_cycle + 1})"
        text_surface = font.render(countdown_text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 100, 400))

        pygame.display.flip()
        pygame.time.delay(1000)

        # Decrement the timers only if they are greater than 0
        if inhale_timer > 0 and exhale_timer > 0:
            if inhaling:
                inhale_timer -= 1
            else:
                exhale_timer -= 1

        if inhale_timer == 0 and inhaling:
            # Switch to exhaling
            inhale_timer = inhale_duration
            inhaling = False

        if exhale_timer == 0 and not inhaling:
            # Switch to inhaling and move to the next cycle
            exhale_timer = exhale_duration
            current_cycle += 1
            inhaling = True

        clock.tick(1)  # Limit the loop to 1 frame per second

    # When all cycles are finished, change the scene
    global current_state
    current_state = END


def br4():
    # Define the durations for breathing in and out
    inhale_duration = 2  # 5 seconds
    exhale_duration = 3  # 10 seconds
    num_cycles = 6  # Number of times to repeat the cycle

    current_cycle = 0  # Initialize the current cycle
    inhale_timer = inhale_duration  # Start with inhaling
    exhale_timer = exhale_duration
    inhaling = True  # Flag to track inhaling/exhaling phase
    clock = pygame.time.Clock()

    # Description of pursed lip breathing
    
    description_text = [
        "Lion Breathing:",
        "1. Sit comfortably with your legs crossed.",
        "2. Inhale deeply through your nose for 2 seconds",
        "3. Exhale forcefully through your mouth while sticking out your tongue for 3 seconds",
        "4. Make a 'ha' sound as you exhale.",
        "5. Repeat 6 times, releasing tension and stress."

    ]



    while current_cycle < num_cycles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BACK)
        num_stars = 100  # Adjust this as needed
        stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
        description_surfaces = []

    # Create font and render text surfaces
        font = pygame.font.Font(None, 27)
        for line in description_text:
            text_surface = font.render(line, True, (0, 0, 0))
            description_surfaces.append(text_surface)

        # Display text surfaces with line breaks
        y_position = 200  # Adjust this value for vertical positioning
        for surface in description_surfaces:
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(surface, text_rect)
            y_position += surface.get_height() + 10  # Add vertical spacing

        # Continue with the rest of your code

        # Calculate the current countdown percentage
        if inhaling:
            countdown_percentage = (inhale_timer / inhale_duration) * 100
        else:
            countdown_percentage = (exhale_timer / exhale_duration) * 100

        # Draw the progress bar
        progress_bar_rect = pygame.Rect(100, 450, countdown_percentage * 6, 30)
        if inhaling:
            pygame.draw.rect(screen, (0, 128, 0), progress_bar_rect)  # Green for inhaling
        else:
            pygame.draw.rect(screen, (0, 0, 128), progress_bar_rect)  # Blue for exhaling

        # Draw the countdown timer text
        font = pygame.font.Font(None, 36)
        if inhaling:
            countdown_text = f"Inhale: {inhale_timer} seconds (Cycle {current_cycle + 1})"
        else:
            countdown_text = f"Exhale: {exhale_timer} seconds (Cycle {current_cycle + 1})"
        text_surface = font.render(countdown_text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 100, 400))

        pygame.display.flip()
        pygame.time.delay(1000)

        # Decrement the timers only if they are greater than 0
        if inhale_timer > 0 and exhale_timer > 0:
            if inhaling:
                inhale_timer -= 1
            else:
                exhale_timer -= 1

        if inhale_timer == 0 and inhaling:
            # Switch to exhaling
            inhale_timer = inhale_duration
            inhaling = False

        if exhale_timer == 0 and not inhaling:
            # Switch to inhaling and move to the next cycle
            exhale_timer = exhale_duration
            current_cycle += 1
            inhaling = True

        clock.tick(1)  # Limit the loop to 1 frame per second

    # When all cycles are finished, change the scene
    global current_state
    current_state = END

def br5():
    # Define the durations for breathing in and out
    inhale_duration = 3 # 5 seconds
    exhale_duration = 4  # 10 seconds
    num_cycles = 20  # Number of times to repeat the cycle

    current_cycle = 0  # Initialize the current cycle
    inhale_timer = inhale_duration  # Start with inhaling
    exhale_timer = exhale_duration
    inhaling = True  # Flag to track inhaling/exhaling phase
    clock = pygame.time.Clock()

    # Description of pursed lip breathing
    
    description_text = [
        "Alternate Nostril Breathing:",
        "1. Sit comfortably with your spine straight.",
        "2. Use your right thumb to close your right nostril and inhale through the left nostril for 3 seconds",
        "3. Close your left nostril with your right ring finger and exhale through the right nostril for 4 seconds",
        "4. Inhale through the right nostril for 3 seconds, close it, and exhale through the left nostril for 4 seconds",
        "5. Repeat 10 times, balancing your energy."
    ]



    while current_cycle < num_cycles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BACK)
        num_stars = 100  # Adjust this as needed
        stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
        description_surfaces = []

    # Create font and render text surfaces
        font = pygame.font.Font(None, 20)
        for line in description_text:
            text_surface = font.render(line, True, (0, 0, 0))
            description_surfaces.append(text_surface)

        # Display text surfaces with line breaks
        y_position = 200  # Adjust this value for vertical positioning
        for surface in description_surfaces:
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(surface, text_rect)
            y_position += surface.get_height() + 10  # Add vertical spacing

        # Continue with the rest of your code

        # Calculate the current countdown percentage
        if inhaling:
            countdown_percentage = (inhale_timer / inhale_duration) * 100
        else:
            countdown_percentage = (exhale_timer / exhale_duration) * 100

        # Draw the progress bar
        progress_bar_rect = pygame.Rect(100, 450, countdown_percentage * 6, 30)
        if inhaling:
            pygame.draw.rect(screen, (0, 128, 0), progress_bar_rect)  # Green for inhaling
        else:
            pygame.draw.rect(screen, (0, 0, 128), progress_bar_rect)  # Blue for exhaling

        # Draw the countdown timer text
        font = pygame.font.Font(None, 36)
        if inhaling:
            countdown_text = f"Inhale: {inhale_timer} seconds (Cycle {(math.ceil(current_cycle + 1))})"
        else:
            countdown_text = f"Exhale: {exhale_timer} seconds (Cycle {(math.ceil(current_cycle + 1))})"
        text_surface = font.render(countdown_text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 100, 400))

        pygame.display.flip()
        pygame.time.delay(1000)

        # Decrement the timers only if they are greater than 0
        if inhale_timer > 0 and exhale_timer > 0:
            if inhaling:
                inhale_timer -= 1
            else:
                exhale_timer -= 1

        if inhale_timer == 0 and inhaling:
            # Switch to exhaling
            inhale_timer = inhale_duration
            inhaling = False

        if exhale_timer == 0 and not inhaling:
            # Switch to inhaling and move to the next cycle
            exhale_timer = exhale_duration
            current_cycle += 1
            inhaling = True

        clock.tick(1)  # Limit the loop to 1 frame per second

    # When all cycles are finished, change the scene
    global current_state
    current_state = END

def br6():
    # Define the durations for breathing in and out
    inhale_duration = 4  # 5 seconds
    exhale_duration = 4  # 10 seconds
    num_cycles = 10  # Number of times to repeat the cycle

    current_cycle = 0  # Initialize the current cycle
    inhale_timer = inhale_duration  # Start with inhaling
    exhale_timer = exhale_duration
    inhaling = True  # Flag to track inhaling/exhaling phase
    clock = pygame.time.Clock()

    # Description of pursed lip breathing
    
    description_text = [
        "Equal Breathing:",
        "1. Sit or lie down in a relaxed position.",
        "2. Inhale through your nose for 4 seconds.",
        "3. Exhale through your nose for 4 seconds.",
        "4. Keep the inhale and exhale time equal.",
        "5. Focus on the steady rhythm of your breath and repeat 10 times."

    ]



    while current_cycle < num_cycles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BACK)
        num_stars = 100  # Adjust this as needed
        stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
        description_surfaces = []

    # Create font and render text surfaces
        font = pygame.font.Font(None, 27)
        for line in description_text:
            text_surface = font.render(line, True, (0, 0, 0))
            description_surfaces.append(text_surface)

        # Display text surfaces with line breaks
        y_position = 200  # Adjust this value for vertical positioning
        for surface in description_surfaces:
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(surface, text_rect)
            y_position += surface.get_height() + 10  # Add vertical spacing

        # Continue with the rest of your code

        # Calculate the current countdown percentage
        if inhaling:
            countdown_percentage = (inhale_timer / inhale_duration) * 100
        else:
            countdown_percentage = (exhale_timer / exhale_duration) * 100

        # Draw the progress bar
        progress_bar_rect = pygame.Rect(100, 450, countdown_percentage * 6, 30)
        if inhaling:
            pygame.draw.rect(screen, (0, 128, 0), progress_bar_rect)  # Green for inhaling
        else:
            pygame.draw.rect(screen, (0, 0, 128), progress_bar_rect)  # Blue for exhaling

        # Draw the countdown timer text
        font = pygame.font.Font(None, 36)
        if inhaling:
            countdown_text = f"Inhale: {inhale_timer} seconds (Cycle {current_cycle + 1})"
        else:
            countdown_text = f"Exhale: {exhale_timer} seconds (Cycle {current_cycle + 1})"
        text_surface = font.render(countdown_text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 100, 400))

        pygame.display.flip()
        pygame.time.delay(1000)

        # Decrement the timers only if they are greater than 0
        if inhale_timer > 0 and exhale_timer > 0:
            if inhaling:
                inhale_timer -= 1
            else:
                exhale_timer -= 1

        if inhale_timer == 0 and inhaling:
            # Switch to exhaling
            inhale_timer = inhale_duration
            inhaling = False

        if exhale_timer == 0 and not inhaling:
            # Switch to inhaling and move to the next cycle
            exhale_timer = exhale_duration
            current_cycle += 1
            inhaling = True

        clock.tick(1)  # Limit the loop to 1 frame per second

    # When all cycles are finished, change the scene
    global current_state
    current_state = END

def br7():
    # Define the durations for breathing in and out
    inhale_duration = 3 # 5 seconds
    exhale_duration = 4  # 10 seconds
    num_cycles = 10  # Number of times to repeat the cycle

    current_cycle = 0  # Initialize the current cycle
    inhale_timer = inhale_duration  # Start with inhaling
    exhale_timer = exhale_duration
    inhaling = True  # Flag to track inhaling/exhaling phase
    clock = pygame.time.Clock()

    # Description of pursed lip breathing
    
    description_text = [
        "Resonant Breathing:",
        "1. Sit comfortably with your back straight.",
        "2. Inhale slowly and deeply through your nose for 3 seconds",
        "3. Exhale slowly through your nose for 4 seconds",
        "5. Find a rhythm that feels calming and relaxing and repeat 10 times"
    ]



    while current_cycle < num_cycles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BACK)
        num_stars = 100  # Adjust this as needed
        stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
        description_surfaces = []

    # Create font and render text surfaces
        font = pygame.font.Font(None, 27)
        for line in description_text:
            text_surface = font.render(line, True, (0, 0, 0))
            description_surfaces.append(text_surface)

        # Display text surfaces with line breaks
        y_position = 200  # Adjust this value for vertical positioning
        for surface in description_surfaces:
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(surface, text_rect)
            y_position += surface.get_height() + 10  # Add vertical spacing

        # Continue with the rest of your code

        # Calculate the current countdown percentage
        if inhaling:
            countdown_percentage = (inhale_timer / inhale_duration) * 100
        else:
            countdown_percentage = (exhale_timer / exhale_duration) * 100

        # Draw the progress bar
        progress_bar_rect = pygame.Rect(100, 450, countdown_percentage * 6, 30)
        if inhaling:
            pygame.draw.rect(screen, (0, 128, 0), progress_bar_rect)  # Green for inhaling
        else:
            pygame.draw.rect(screen, (0, 0, 128), progress_bar_rect)  # Blue for exhaling

        # Draw the countdown timer text
        font = pygame.font.Font(None, 27)
        if inhaling:
            countdown_text = f"Inhale: {inhale_timer} seconds (Cycle {current_cycle + 1})"
        else:
            countdown_text = f"Exhale: {exhale_timer} seconds (Cycle {current_cycle + 1})"
        text_surface = font.render(countdown_text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 100, 400))

        pygame.display.flip()
        pygame.time.delay(1000)

        # Decrement the timers only if they are greater than 0
        if inhale_timer > 0 and exhale_timer > 0:
            if inhaling:
                inhale_timer -= 1
            else:
                exhale_timer -= 1

        if inhale_timer == 0 and inhaling:
            # Switch to exhaling
            inhale_timer = inhale_duration
            inhaling = False

        if exhale_timer == 0 and not inhaling:
            # Switch to inhaling and move to the next cycle
            exhale_timer = exhale_duration
            current_cycle += 1
            inhaling = True

        clock.tick(1)  # Limit the loop to 1 frame per second

    # When all cycles are finished, change the scene
    global current_state
    current_state = END


def br8():
    # Define the durations for breathing in and out
    inhale_duration = 3  # 5 seconds
    exhale_duration = 4  # 10 seconds
    num_cycles = 10  # Number of times to repeat the cycle

    current_cycle = 0  # Initialize the current cycle
    inhale_timer = inhale_duration  # Start with inhaling
    exhale_timer = exhale_duration
    inhaling = True  # Flag to track inhaling/exhaling phase
    clock = pygame.time.Clock()

    # Description of pursed lip breathing
    
    description_text = [
        "Sitali Breathing:",
        "1. Sit with your back straight and shoulders relaxed.",
        "2. Curl your tongue like a 'U' and protrude it slightly from your mouth.",
        "3. Inhale deeply through your curled tongue for 3 seconds.",
        "4. Exhale slowly through your nose for 4 seconds.",
        "5. Feel the cooling sensation as you breathe and repeat 10 times."

    ]



    while current_cycle < num_cycles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BACK)
        num_stars = 100  # Adjust this as needed
        stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
        description_surfaces = []

    # Create font and render text surfaces
        font = pygame.font.Font(None, 27)
        for line in description_text:
            text_surface = font.render(line, True, (0, 0, 0))
            description_surfaces.append(text_surface)

        # Display text surfaces with line breaks
        y_position = 200  # Adjust this value for vertical positioning
        for surface in description_surfaces:
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(surface, text_rect)
            y_position += surface.get_height() + 10  # Add vertical spacing

        # Continue with the rest of your code

        # Calculate the current countdown percentage
        if inhaling:
            countdown_percentage = (inhale_timer / inhale_duration) * 100
        else:
            countdown_percentage = (exhale_timer / exhale_duration) * 100

        # Draw the progress bar
        progress_bar_rect = pygame.Rect(100, 450, countdown_percentage * 6, 30)
        if inhaling:
            pygame.draw.rect(screen, (0, 128, 0), progress_bar_rect)  # Green for inhaling
        else:
            pygame.draw.rect(screen, (0, 0, 128), progress_bar_rect)  # Blue for exhaling

        # Draw the countdown timer text
        font = pygame.font.Font(None, 36)
        if inhaling:
            countdown_text = f"Inhale: {inhale_timer} seconds (Cycle {current_cycle + 1})"
        else:
            countdown_text = f"Exhale: {exhale_timer} seconds (Cycle {current_cycle + 1})"
        text_surface = font.render(countdown_text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 100, 400))

        pygame.display.flip()
        pygame.time.delay(1000)

        # Decrement the timers only if they are greater than 0
        if inhale_timer > 0 and exhale_timer > 0:
            if inhaling:
                inhale_timer -= 1
            else:
                exhale_timer -= 1

        if inhale_timer == 0 and inhaling:
            # Switch to exhaling
            inhale_timer = inhale_duration
            inhaling = False

        if exhale_timer == 0 and not inhaling:
            # Switch to inhaling and move to the next cycle
            exhale_timer = exhale_duration
            current_cycle += 1
            inhaling = True

        clock.tick(1)  # Limit the loop to 1 frame per second

    # When all cycles are finished, change the scene
    global current_state
    current_state = END

def br9():
    # Define the durations for breathing in and out
    inhale_duration = 4  # 5 seconds
    exhale_duration = 6  # 10 seconds
    num_cycles = 10  # Number of times to repeat the cycle

    current_cycle = 0  # Initialize the current cycle
    inhale_timer = inhale_duration  # Start with inhaling
    exhale_timer = exhale_duration
    inhaling = True  # Flag to track inhaling/exhaling phase
    clock = pygame.time.Clock()

    # Description of pursed lip breathing
    
    description_text = [
        "Deep Breathing:",
        "1. Find a quiet place to sit or lie down.",
        "2. Inhale deeply through your nose for 4 seconds.",
        "3. Exhale slowly through your mouth for 6 seconds",
        "4. Focus on the expansion of your abdomen and chest.",
        "5. Relax and repeat 10 times"
    ]



    while current_cycle < num_cycles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BACK)
        num_stars = 100  # Adjust this as needed
        stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
        description_surfaces = []

    # Create font and render text surfaces
        font = pygame.font.Font(None, 27)
        for line in description_text:
            text_surface = font.render(line, True, (0, 0, 0))
            description_surfaces.append(text_surface)

        # Display text surfaces with line breaks
        y_position = 200  # Adjust this value for vertical positioning
        for surface in description_surfaces:
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(surface, text_rect)
            y_position += surface.get_height() + 10  # Add vertical spacing

        # Continue with the rest of your code

        # Calculate the current countdown percentage
        if inhaling:
            countdown_percentage = (inhale_timer / inhale_duration) * 100
        else:
            countdown_percentage = (exhale_timer / exhale_duration) * 100

        # Draw the progress bar
        progress_bar_rect = pygame.Rect(100, 450, countdown_percentage * 6, 30)
        if inhaling:
            pygame.draw.rect(screen, (0, 128, 0), progress_bar_rect)  # Green for inhaling
        else:
            pygame.draw.rect(screen, (0, 0, 128), progress_bar_rect)  # Blue for exhaling

        # Draw the countdown timer text
        font = pygame.font.Font(None, 36)
        if inhaling:
            countdown_text = f"Inhale: {inhale_timer} seconds (Cycle {current_cycle + 1})"
        else:
            countdown_text = f"Exhale: {exhale_timer} seconds (Cycle {current_cycle + 1})"
        text_surface = font.render(countdown_text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 100, 400))

        pygame.display.flip()
        pygame.time.delay(1000)

        # Decrement the timers only if they are greater than 0
        if inhale_timer > 0 and exhale_timer > 0:
            if inhaling:
                inhale_timer -= 1
            else:
                exhale_timer -= 1

        if inhale_timer == 0 and inhaling:
            # Switch to exhaling
            inhale_timer = inhale_duration
            inhaling = False

        if exhale_timer == 0 and not inhaling:
            # Switch to inhaling and move to the next cycle
            exhale_timer = exhale_duration
            current_cycle += 1
            inhaling = True

        clock.tick(1)  # Limit the loop to 1 frame per second

    # When all cycles are finished, change the scene
    global current_state
    current_state = END

def br10():
    # Define the durations for breathing in and out
    inhale_duration = 3  # 5 seconds
    exhale_duration = 5  # 10 seconds
    num_cycles = 10  # Number of times to repeat the cycle

    current_cycle = 0  # Initialize the current cycle
    inhale_timer = inhale_duration  # Start with inhaling
    exhale_timer = exhale_duration
    inhaling = True  # Flag to track inhaling/exhaling phase
    clock = pygame.time.Clock()

    # Description of pursed lip breathing
    
    description_text = [
        "Bhramari Breathing:",
        "1. Sit comfortably and close your eyes.",
        "2. Place your index fingers on your ears' cartilage.",
        "3. Inhale deeply through your nose for 3 seconds",
        "4. Exhale slowly while making a humming sound like a bee for 5 seconds",
        "5. Feel the vibrations in your head and calm your mind. Repeat 10 times"

    ]



    while current_cycle < num_cycles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BACK)
        num_stars = 100  # Adjust this as needed
        stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
        for star in stars:
            pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
        description_surfaces = []

    # Create font and render text surfaces
        font = pygame.font.Font(None, 27)
        for line in description_text:
            text_surface = font.render(line, True, (0, 0, 0))
            description_surfaces.append(text_surface)

        # Display text surfaces with line breaks
        y_position = 200  # Adjust this value for vertical positioning
        for surface in description_surfaces:
            text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(surface, text_rect)
            y_position += surface.get_height() + 10  # Add vertical spacing

        # Continue with the rest of your code

        # Calculate the current countdown percentage
        if inhaling:
            countdown_percentage = (inhale_timer / inhale_duration) * 100
        else:
            countdown_percentage = (exhale_timer / exhale_duration) * 100

        # Draw the progress bar
        progress_bar_rect = pygame.Rect(100, 450, countdown_percentage * 6, 30)
        if inhaling:
            pygame.draw.rect(screen, (0, 128, 0), progress_bar_rect)  # Green for inhaling
        else:
            pygame.draw.rect(screen, (0, 0, 128), progress_bar_rect)  # Blue for exhaling

        # Draw the countdown timer text
        font = pygame.font.Font(None, 36)
        if inhaling:
            countdown_text = f"Inhale: {inhale_timer} seconds (Cycle {current_cycle + 1})"
        else:
            countdown_text = f"Exhale: {exhale_timer} seconds (Cycle {current_cycle + 1})"
        text_surface = font.render(countdown_text, True, (0, 0, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 100, 400))

        pygame.display.flip()
        pygame.time.delay(1000)

        # Decrement the timers only if they are greater than 0
        if inhale_timer > 0 and exhale_timer > 0:
            if inhaling:
                inhale_timer -= 1
            else:
                exhale_timer -= 1

        if inhale_timer == 0 and inhaling:
            # Switch to exhaling
            inhale_timer = inhale_duration
            inhaling = False

        if exhale_timer == 0 and not inhaling:
            # Switch to inhaling and move to the next cycle
            exhale_timer = exhale_duration
            current_cycle += 1
            inhaling = True

        clock.tick(1)  # Limit the loop to 1 frame per second

    # When all cycles are finished, change the scene
    global current_state
    current_state = END

def end():
    global current_state, done, sec, nums, qnum, ndone
    screen.fill(BACK)
    num_stars = 100  # Adjust this as needed
    stars = generate_stars(num_stars, SCREEN_WIDTH, SCREEN_HEIGHT)
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), star, 1)  # White stars
    # Display the final blurb
    font = pygame.font.Font(None, 30)
    end_text = "If you ever feel alone, dont be afraid to talk to the man on the moon."
    end_text_surface = font.render(end_text, True, (0, 0, 0))
    end_text_rect = end_text_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(end_text_surface, end_text_rect)

    # Define the "Done" and "Not Done" buttons
    done_button_rect = pygame.Rect(150, 400, 150, 50)
    not_done_button_rect = pygame.Rect(SCREEN_WIDTH - 300, 400, 150, 50)

    # Button colors and text surfaces
    button_color = (0, 128, 255)
    font = pygame.font.Font(None, 36)
    done_text_surface = font.render("Done", True, (255, 255, 255))
    done_text_rect = done_text_surface.get_rect(center=done_button_rect.center)
    not_done_text_surface = font.render("Not Done", True, (255, 255, 255))
    not_done_text_rect = not_done_text_surface.get_rect(center=not_done_button_rect.center)

    # Draw the buttons
    pygame.draw.rect(screen, button_color, done_button_rect)
    pygame.draw.rect(screen, button_color, not_done_button_rect)

    # Draw button text
    screen.blit(done_text_surface, done_text_rect)
    screen.blit(not_done_text_surface, not_done_text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if done_button_rect.collidepoint(event.pos):
                    # User is done, exit the program
                    done = True
                    current_state = END
                    return
                elif not_done_button_rect.collidepoint(event.pos):
                    # User is not done, go back to the main menu
                    nums = []
                    qnum = 0
                    ndone = True
                    current_state = END
                    sec = True
                    return


def generate_stars(num_stars, screen_width, screen_height):
    stars = [(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(num_stars)]
    return stars

# Pygame main loop
running = True
agent = agen.Agent()
user = User(nums)
done = False
en= False
enc = True
sec = False
ndone = False

while running:
    if current_state == WELCOME:
        welcome()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if welcome_button_rect.collidepoint(event.pos):
                    welcome_button_color = BUTTON_CLICKED_COLOR
                    current_state = QUEST
            if event.type == pygame.MOUSEBUTTONUP:
                # Reset button color when mouse button released
                welcome_button_color = BUTTON_COLOR

        pygame.draw.rect(screen, welcome_button_color, welcome_button_rect, border_radius=25)
        screen.blit(welcome_text_surface, welcome_text_rect)


    elif current_state == QUEST:
        quest(nums)
            
        if len(nums) == 10:
            if en:
                current_state = END
                enc = False
            else:
                current_state = BREATH
        
            


    elif current_state == BREATH:
        ostate = agent.get_state(user)

        ftech = agent.get_action(ostate)

        current_state = BREATH - (13-ftech)


    elif current_state == END:
        en = True
        if enc:
            nums = []
            qnum = 0
            current_state = QUEST
        else:
            user.state = nums
            reward, dond = user.suggest(ftech)
            nstate = nums
            agent.train_short_memory(ostate,ftech,reward,nstate,done)
            agent.remember(ostate,ftech,reward,nstate,done)
            end()

            if ndone:
                current_state = WELCOME
                en = False

            if done:
                agent.train_long_memory()
                agent.model.save()
                agent.memory_save('mems.csv')
                agent.n_opens +=1
                print(nums)
                pygame.quit()
                sys.exit()

    
    elif current_state == BREATH1:
        br1()

    elif current_state == BREATH2:
        br2()

    elif current_state == BREATH3:
        br3()

    elif current_state == BREATH4:
        br4()

    elif current_state == BREATH5:
        br5()

    elif current_state == BREATH6:
        br6()

    elif current_state == BREATH7:
        br7()

    elif current_state == BREATH8:
        br8()

    elif current_state == BREATH9:
        br9()

    elif current_state == BREATH10:
        br10()

    # Update the display
    pygame.display.flip()
    pygame.time.delay(100)

# Quit Pygame
pygame.quit()
sys.exit()