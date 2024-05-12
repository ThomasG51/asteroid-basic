import pygame
import sys
from random import randint, uniform

# Init
pygame.init()

# Property
window_width = 1280
window_height = 720
title_font = pygame.font.Font("fonts/subatomic.ttf", 50)
clock = pygame.time.Clock()
can_shoot = True
last_shoot_time = 0
pop_meteor_event = pygame.event.custom_type()
pygame.time.set_timer(pop_meteor_event, 1000)
laser_sound = pygame.mixer.Sound("sounds/laser.ogg")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
background_sound = pygame.mixer.Sound("sounds/music.wav")

# Settings
pygame.display.set_caption("Asteroid Shooter")
background_sound.play(loops=-1)

# Surface
display_surface = pygame.display.set_mode((window_width, window_height))
background_surface = pygame.image.load("images/background.png").convert()
ship_surface = pygame.image.load("images/ship.png").convert_alpha()
laser_surface = pygame.image.load("images/laser.png").convert_alpha()
meteor_surface = pygame.image.load("images/meteor.png").convert_alpha()

# Rectangle
ship_rect = ship_surface.get_rect(center=(300, 500))

# List
laser_list = []
meteor_list = []

# Function
def laser_move(laser_list: list):
    for laser_rect in laser_list:
        laser_rect.y -= round(200 * dt)
        if laser_rect.bottom < 0:
            laser_list.remove(laser_rect)

def laser_timer(can_shoot) -> bool:
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if (current_time - last_shoot_time) > 200:
            can_shoot = True
        return can_shoot

def laser_collision(laser_list,meteor_list):
    for laser_rect in laser_list:
        for meteor_tuple in meteor_list:
            meteor_rect = meteor_tuple[0]
            if laser_rect.colliderect(meteor_rect):
                explosion_sound.play()
                meteor_list.remove(meteor_tuple)
                laser_list.remove(laser_rect)

def meteor_move(meteor_list, speed = 100):
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        meteor_direction = meteor_tuple[1]
        meteor_rect.center += round(meteor_direction * speed * dt)
        if meteor_rect.top > window_height:
            meteor_list.remove(meteor_tuple)

def meteor_collision(meteor_list, ship_rect):
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        if ship_rect.colliderect(meteor_rect):
            pygame.quit()
            sys.exit()

def display_score():
    score_surface = title_font.render(f"Score: {pygame.time.get_ticks() // 1000}", True, "White").convert_alpha()
    score_rect = score_surface.get_rect(midbottom=(window_width / 2, window_height - 60))
    display_surface.blit(score_surface, score_rect)
    pygame.draw.rect(display_surface, (255, 255, 255), score_rect.inflate(40, 40), width=8, border_radius=12)

# Game Loop
while True:
    # Delta Time
    dt = clock.tick(120) / 1000

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            laser_list.append(laser_surface.get_rect(midbottom=ship_rect.midtop))
            laser_sound.play()
            can_shoot = False
            last_shoot_time = pygame.time.get_ticks()
        if event.type == pop_meteor_event:
            rand_x_pos = randint(-100, window_width + 100)
            rand_y_pos = randint(-200, -100)
            direction = pygame.math.Vector2(uniform(-2, 2), 1)
            meteor_list.append((meteor_surface.get_rect(center=(rand_x_pos,rand_y_pos)),direction))

    ship_rect.center = pygame.mouse.get_pos()

    # Update
    laser_move(laser_list)
    can_shoot = laser_timer(can_shoot)
    meteor_move(meteor_list)
    meteor_collision(meteor_list, ship_rect)

    laser_collision(laser_list, meteor_list)

    # Draw surface
    display_surface.blit(background_surface, (0, 0))
    display_score()

    for laser_rect in laser_list:
        display_surface.blit(laser_surface, laser_rect)

    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        display_surface.blit(meteor_surface, meteor_rect)

    display_surface.blit(ship_surface, ship_rect)

    # Display the final frame (display surface)
    pygame.display.update()