import pygame
import random
import math
import time
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
import streamlit as st

st.set_page_config(layout="wide") #remove margins
screen_width = 1920
screen_height = 1080
max_distance = 400
min_distance = 230
#starting size of our quacken
QUACKEN_BASE_SIZE = 300
DUCKLING_SIZE = 50
NUCLEUS_CENTER_X = screen_width/2
NUCLEUS_CENTER_Y = screen_height/2
# Colors
water_blue = (255,236,242)
slider_bg = (255,124,178)
knob_color = (255,247,250)
pygame.font.init()
title_font = pygame.font.SysFont("Verdana", 32, bold=True)
label_font = pygame.font.SysFont("Verdana", 24)
instructions_font = pygame.font.SysFont("Verdana", 24, italic=True)
# Create the slider in the sidebar
st.sidebar.header("Controls")
#initialize pygame window
def intialize_pygame():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("The Quacken: Atomic Tug of War")

    font = pygame.font.SysFont("Arial", 24)
    return screen, font


#ui
def draw_ui_elements(screen, current_protons):
    text_color = (80, 40, 40)
    accent_color = (255, 124, 178)

    #title
    title_surf = title_font.render("The Quacken: Subatomic Tug-of-War", True, text_color)
    screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, 50))

    #description
    desc_text = "See how increasing protons decreases atomic radius by pulling electrons closer to the nucleus!"
    desc_surf = instructions_font.render(desc_text, True, text_color)
    screen.blit(desc_surf, (screen_width // 2 - desc_surf.get_width() // 2, 100))

    #slider label
    # Position this right above your slider bar
    # label_text = f"Number of Protons: {int(current_protons)}"
    # label_surf = label_font.render(label_text, True, text_color)
    #
    # screen.blit(label_surf, (screen_width // 2 - label_surf.get_width() // 2, screen_height -100))
    #instructions
    prompt_surf = instructions_font.render("Drag the slider to increase the number of protons (the muscle) " +
                                           "and watch the quacken (nucleus) pull the ducklings (electrons) with more force" + "\n"
                                           + "due to the stronger positive charge pulling the electrons inward!", True, text_color)
    screen.blit(prompt_surf, (screen_width // 2 - prompt_surf.get_width() // 2, screen_height-100))
#more protons => greater inclear charge => shorter distance
#formula: r = Max_Distance / sqrt(protons
#using sqrt to make the movement look more natural/satisfying.
def calculate_distance(protons):
    if protons == 0:
        return max_distance
    # calculate target distance
    target_r = max_distance / (protons ** 0.5)
    # can't pass the mix distance
    return max(target_r, min_distance)
#as protons increase, scale muscles by 0.15
def calculate_muscle_size_scale(protons):
    #safety net in case we have no protons for some reason
    if protons < 1:
        return 1.0
    scale = 1.0 + (protons - 1) * 0.15
    return scale


def draw_slider(current_protons):
    #the slider
    pygame.draw.rect(screen, slider_bg, (slider_x, slider_y, slider_width, slider_height))

    #knob position based on protons (1 to 10)
    #(1-10) to (0 to slider_width)
    relative_pos = (current_protons - 1) / 9
    knob_x = slider_x + (relative_pos * slider_width)

    # Draw the "Proton" Knob
    pygame.draw.circle(screen, knob_color, (int(knob_x), slider_y + 5), knob_radius)


def handle_input(protons, dragging, slider_x, slider_width, slider_y):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return protons, dragging, False  # Stop the game

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if slider_x <= mouse_x <= slider_x + slider_width and slider_y - 20 <= mouse_y <= slider_y + 20:
                dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    if dragging:
        mouse_x, _ = pygame.mouse.get_pos()
        clamped_x = max(slider_x, min(mouse_x, slider_x + slider_width))
        protons = round(1 + (clamped_x - slider_x) / slider_width * 9)

    return protons, dragging, True  # Keep the game running


def draw_ropes(screen, radius):
    #center of the nucleus
    cx, cy = NUCLEUS_CENTER_X, NUCLEUS_CENTER_Y
    rope_color = (150, 121, 105)  # A deeper, "Rich Academic" brown

    #4 ropes that look like they are pulling the circle inward
    angles = [-10, -15, 200, 190]

    for a in angles:
        rad = math.radians(a)

        #calc the point on the white orbit circle
        target_x = cx + radius * math.cos(rad)
        target_y = cy + radius * math.sin(rad)

        #draw center to the circle edge
        pygame.draw.line(screen, rope_color, (cx, cy), (int(target_x), int(target_y)), 2)

def draw_duckling(screen, protons, radius):
    #center
    nucleus_x = NUCLEUS_CENTER_X
    nucleus_y = NUCLEUS_CENTER_Y
    num_ducklings = int(protons)
    if(radius < min_distance):
        radius = min_distance
    #draw circle path to represent the sell
    #easier for students to see the radius literally shrink
    if num_ducklings > 0:
        pygame.draw.circle(screen, (255, 255, 255), (nucleus_x, nucleus_y), int(radius), 5)

    #make duckling much smaller than quacken, reduce clutter
    scaled_d = pygame.transform.smoothscale(duckling_img, (DUCKLING_SIZE, DUCKLING_SIZE))

    #make the ducklings go around in the circle
    rotation_speed = time.time() * 1.5
    #place ducklings in
    for i in range(num_ducklings):
        #evenly space ducklings along the circle
        angle = (2 * math.pi * i / num_ducklings) + rotation_speed

        #trigonometry finally paying off
        # x = center + radius * cos(angle)
        # y = center + radius * sin(angle)
        orbit_x = nucleus_x + radius * math.cos(angle)
        orbit_y = nucleus_y + radius * math.sin(angle)

        #make them jitter
        #the closer electrons are to the nucleus the more stable they are
        #as radius goes down, so should the jitter
        jitter = int(radius * 0.05)
        final_x = orbit_x + random.randint(-jitter, jitter)
        final_y = orbit_y + random.randint(-jitter, jitter)


        d_rect = scaled_d.get_rect(center=(int(final_x), int(final_y)))
        screen.blit(scaled_d, d_rect)
def draw_quacken(screen, protons):
    scale = calculate_muscle_size_scale(protons)

    # Calculate new dimensions
    new_w = int(QUACKEN_BASE_SIZE * scale)
    new_h = int(QUACKEN_BASE_SIZE * scale)

    # Smoothly scale the image
    scaled_quacken = pygame.transform.smoothscale(quacken_img, (new_w, new_h))

    # Center him on the left side of the screen
    q_rect = scaled_quacken.get_rect(center=(NUCLEUS_CENTER_X, NUCLEUS_CENTER_Y))
    screen.blit(scaled_quacken, q_rect)
    return q_rect


slider_x = 200
slider_y = 500
slider_width = 400
slider_height = 10
knob_radius = 15

# initialization
protons = 1
dragging = False
running = True
#initialize screen
screen, font = intialize_pygame()
#load images
quacken_img = pygame.image.load("quacken.png").convert_alpha()
duckling_img = pygame.image.load("duckling.png").convert_alpha()

# Get original dimensions for scaling
q_width, q_height = quacken_img.get_size()
d_width, d_height = duckling_img.get_size()
frame_placeholder = st.empty()
protons = st.sidebar.slider("Number of Protons", min_value=1, max_value=10, value=1)

while running:
    # check for clicks/events
    # protons, dragging, running = handle_input(protons, dragging, slider_x, slider_width, slider_y)

    # update distance and muscle size
    radius = calculate_distance(protons)
    scale = calculate_muscle_size_scale(protons)


    # draw everything
    screen.fill(water_blue)
    # ropes, quacken, ducklings
    draw_ropes(screen, radius)
    draw_quacken(screen, protons)
    draw_duckling(screen, protons, radius)
    draw_ui_elements(screen, protons)
    # draw_slider(protons)

    # pygame.display.flip()
    #getting the pixel data from pygame frame
    view = pygame.surfarray.array3d(screen)
    view = view.transpose([1, 0, 2])
    frame_placeholder.image(view, channels="RGB", use_container_width=False)
    # print(f"At {protons} proton(s):")
    # print(f"- The duckling is {radius:.2f} pixels away.")
    # print(f"- The quacken is at {scale:.2f}x size.")

pygame.quit()


