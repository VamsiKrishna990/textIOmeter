import pygame

# Initialize fonts
pygame.font.init()
font = pygame.font.Font(None, 36)
speed_font = pygame.font.Font(None, 72)
title_font = pygame.font.Font(None, 100)

# Set up colors
BLACK = (0, 0, 0)
NEON_GREEN = (57, 255, 20)
RED = (255, 0, 0)
DARK_GREY = (50, 50, 50)
ORANGE = (255, 140, 0)

# Digital speedometer theme settings
background_color = BLACK
text_color = NEON_GREEN
speed_color = RED

def interpolate_color(color1, color2, factor):
    return tuple(int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3))

def draw_segmented_progress_bar(screen, word_count):
    max_word_count = 1500
    segments = 30
    progress = min(1.0, word_count / max_word_count)
    segment_width = 20
    segment_height = 30
    gap = 2

    filled_segments = int(progress * segments)
    x = (screen.get_width() - (segments * (segment_width + gap))) // 2
    y = 250  # Adjust as needed

    for i in range(segments):
        if i < filled_segments:
            factor = i / segments
            color = interpolate_color(ORANGE, RED, factor)
        else:
            color = DARK_GREY
        pygame.draw.rect(screen, color, (x + i * (segment_width + gap), y, segment_width, segment_height))

def render_speed(screen, word_count):
    speed_text = speed_font.render(str(word_count), True, speed_color)
    screen.blit(speed_text, (screen.get_width() - speed_text.get_width() - 20, 350))

def render_title(screen, width):
    title_text = title_font.render("TextOMeter!", True, RED)
    title_x = (width - title_text.get_width()) // 2
    y_pos = 30  # Move up to the header section
    screen.blit(title_text, (title_x, y_pos))

def render_message(screen, word_count):
    if word_count <= 250:
        message = "Just started"
    elif word_count <= 500:
        message = "Work in progress"
    elif word_count <= 750:
        message = "Half way done!"
    elif word_count <= 1250:
        message = "Almost there!"
    elif word_count <= 1500:
        message = "Chapter completed!"
    else:
        message = "Over Achiever!!"
    message_text = font.render(message, True, text_color)
    message_x = (screen.get_width() - message_text.get_width()) // 2  # Center align the message
    screen.blit(message_text, (message_x, 300))

def render_word_count(screen, word_count, width):
    count_text = f"Word Count: {word_count}"
    count_rendered = font.render(count_text, True, text_color)
    screen.blit(count_rendered, (width - count_rendered.get_width() - 20, 450))

def render_fire_background(screen, word_count, fire_image, rotation_angle):
    screen_width, screen_height = screen.get_size()
    fire_scale = 1 + (word_count / 1500) * 0.5
    fire_width = int(screen_width * fire_scale)
    fire_height = int(fire_image.get_height() * fire_scale)
    scaled_fire = pygame.transform.scale(fire_image, (fire_width, fire_height))
    rotated_fire = pygame.transform.rotate(scaled_fire, rotation_angle)
    fire_x = (screen_width - rotated_fire.get_width()) // 2
    fire_y = (screen_height - rotated_fire.get_height()) // 2
    screen.blit(rotated_fire, (fire_x, fire_y))
