import pygame
import pygame_gui

from pygame_gui.elements import UIButton
from pygame_gui.elements import UIWindow

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()

pygame.display.set_caption("Pygame-gui Layout Demo")
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

uiwindow = UIWindow(rect=pygame.Rect(10, 10, 400, 360),
                                         manager=manager,
                                         resizable=True,
                                         visible=True)

"""
# Anchors

b1_layout_rect = pygame.Rect(30, 20, 100, 60)

b2_layout_rect = pygame.Rect(0, 0, 150, 60)
b2_layout_rect.bottomright = (-30, -20)

b3_layout_rect = pygame.Rect(0, 0, 100, 20)

UIButton(relative_rect=b1_layout_rect,
        text = 'Top Left',
        manager = manager)

UIButton(relative_rect=b2_layout_rect,
        text = 'Bottom Right',
        manager = manager,
        anchors={'right': 'right',
                 'bottom': 'bottom'})

UIButton(relative_rect=b3_layout_rect,
         text = 'Center',
         manager = manager,
        anchors={'center': 'center'})
"""

"""
# Couldn't get this to work - button should be centered and should resize with the window

b4_layout_rect = pygame.Rect(30, 20, 100, 60)

UIButton(relative_rect=b4_layout_rect,
        text='Resizable',
        manager = manager,
        container=uiwindow,
        anchors={'left': 'left',
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'})
"""

# Anchor targets

b5_layout_rect = pygame.Rect(0, 20, 100, 60)

b5 = UIButton(relative_rect = b5_layout_rect,
       text='Button A',
       manager = manager,
       container=uiwindow,
       anchors={'centerx': 'centerx'})

b6_layout_rect = pygame.Rect(0, 20, 100, 60)

UIButton(relative_rect=b6_layout_rect,
         text='Button B',
         manager = manager,
         container = uiwindow,
         anchors = {'top_target': b5,
                    'centerx': 'centerx'})

manager.set_visual_debug_mode(True)

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

