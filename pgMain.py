import pygame
import pygame.locals
from uiShortcut import handle_shortcuts
import styling
from threading import Thread, Event
from saveScheduler import autosave, shared_data
import os
import sys

def toggle_scheduler(event, active, main_file_path, staging_file_path):
    """Toggle the autosave scheduler using an Event for thread management."""
    if active:
        event.clear()  # Clear any existing stop signals
        t = Thread(target=autosave, args=(event, main_file_path, staging_file_path))
        t.start()
        return t
    else:
        event.set()  # Signal the thread to stop
        return None

def restart_program():
    """Restarts the current program."""
    python = sys.executable
    os.execl(python, python, *sys.argv)

main_file_path = 'C:/Users/fight/OneDrive/Documents/Literature/[Ramayana]/Chapter1/draft.txt'
staging_file_path = 'C:/Users/fight/OneDrive/Documents/Literature/py scripts/stagingFile.txt'

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TextOMeter!")

text = ""
lines = text.split('\n')

# Load symbols
run_symbol = pygame.image.load('run.png')
stop_symbol = pygame.image.load('stop.png')
exit_symbol = pygame.image.load('exit.png')
reset_symbol = pygame.image.load('reset.png')

# Resize symbols to fit buttons
button_width, button_height = 80, 50
run_symbol = pygame.transform.scale(run_symbol, (button_width, button_height))
stop_symbol = pygame.transform.scale(stop_symbol, (button_width, button_height))
exit_symbol = pygame.transform.scale(exit_symbol, (button_width, button_height))
reset_symbol = pygame.transform.scale(reset_symbol, (button_width, button_height))

# Buttons setup, aligned to the right
screen_width = 800
button_spacing = 10

reset_button = pygame.Rect(screen_width - button_width - button_spacing, 520, button_width, button_height)
exit_button = pygame.Rect(reset_button.x - button_width - button_spacing, 520, button_width, button_height)
autosave_button = pygame.Rect(exit_button.x - button_width - button_spacing, 520, button_width, button_height)

scheduler_active = False
scheduler_thread = None
stop_event = Event()

# Load and scale fire image
fire_image = pygame.image.load('fire.png')

# Variable to keep track of rotation angle
rotation_angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if autosave_button.collidepoint(event.pos):
                scheduler_active = not scheduler_active
                scheduler_thread = toggle_scheduler(stop_event, scheduler_active, main_file_path, staging_file_path)
            elif exit_button.collidepoint(event.pos):
                running = False  # Set running to False to exit the main loop
            elif reset_button.collidepoint(event.pos):
                restart_program()  # Restart the program
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            handle_shortcuts(event, text, event.type == pygame.KEYDOWN)

    word_count = shared_data['word_count']
    screen.fill(styling.background_color)

    # Update rotation angle based on word count
    rotation_angle = (word_count / 1500) * 360

    # Render fire background for the whole window with rotation
    styling.render_fire_background(screen, word_count, fire_image, rotation_angle)

    # Render header
    styling.render_title(screen, 800)

    # Render body sections
    styling.draw_segmented_progress_bar(screen, word_count)
    styling.render_message(screen, word_count)

    # Render footer section
    styling.render_word_count(screen, word_count, 800)
    if scheduler_active:
        screen.blit(stop_symbol, (autosave_button.x, autosave_button.y))
    else:
        screen.blit(run_symbol, (autosave_button.x, autosave_button.y))
    
    screen.blit(exit_symbol, (exit_button.x, exit_button.y))
    screen.blit(reset_symbol, (reset_button.x, reset_button.y))

    pygame.display.flip()

if scheduler_thread:
    stop_event.set()
    scheduler_thread.join()

pygame.quit()
