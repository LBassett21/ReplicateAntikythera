#import ButtonDemo
#import LayoutDemo

import pygame
import pygame_gui

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()

pygame.display.set_caption("Pygame-gui Event Window Demo")
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

#        if event.type == pygame_gui.UI_BUTTON_PRESSED:
#            if event.ui_element == hello_button:
#                print("Hello world!")

    manager.process_events(event)
    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
