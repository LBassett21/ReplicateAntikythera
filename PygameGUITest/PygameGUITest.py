#import ButtonDemo
#import LayoutDemo

import pygame
import pygame_gui

from pygame_gui.elements import UIPanel
from pygame import Rect

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()

pygame.display.set_caption("Pygame-gui Event Window Demo")
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
background.fill(pygame.Color('#000000'))

ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

subpanel_rect = Rect(0, 50, 190, 340)


class events_panel():

    class event_button():
       def __init__(self, manager):
           pass

    def __init__(self, manager):
        events_panel = UIPanel(relative_rect=Rect(10, 150, 200, 400),
                               manager=manager,
                               visible=True)

        events_subpanel = UIPanel(relative_rect=subpanel_rect,
                                  manager=ui_manager,
                                  container=events_panel,
                                  anchors={'centerx': 'centerx'},
                                  visible=True)

    def add_event_to_list(self, event):
        pass

    def remove_event_from_list(self, event):
        pass

    def update_event_list(self, events):
        pass


clock = pygame.time.Clock()
is_running = True

events_panel(ui_manager)

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

#        if event.type == pygame_gui.UI_BUTTON_PRESSED:
#            if event.ui_element == hello_button:
#                print("Hello world!")

    ui_manager.process_events(event)
    ui_manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    ui_manager.draw_ui(window_surface)

    pygame.display.update()
