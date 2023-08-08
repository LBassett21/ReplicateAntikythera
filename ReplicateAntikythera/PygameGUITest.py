#import ButtonDemo
#import LayoutDemo

from cgitb import text
import pygame
import pygame_gui
import pygame.font

pygame.font.init()

from pygame_gui.elements import UIPanel
from pygame import Rect
from pygame_gui.elements import UIVerticalScrollBar
from pygame_gui.elements import UIButton
from pygame_gui.elements import UIScrollingContainer

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()

pygame.display.set_caption("Pygame-gui Event Window Demo")
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
background.fill(pygame.Color('#000000'))

ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))



class event_window():

    events=[]
    manager=None
    events_panel=None
    events_subpanel=None

    event_window_width = 270 
    event_window_height = 400

    class event_button():
        ui_panel = None

        button_width = 220 
        button_height = 50
        button_padding = 5

        def __init__(self, manager, container, event, relative_to = None):
            button_label = event[0] + " - " + event[1]

            if (relative_to == None):
                self.ui_panel = UIButton(relative_rect=Rect(0, self.button_padding, self.button_width, self.button_height),
                                       manager=manager,
                                       text=button_label,
                                       container=container,
                                       anchors={'centerx': 'centerx'},
                                       visible=True)
            else:
                self.ui_panel = UIButton(relative_rect=Rect(0, self.button_padding, self.button_width, self.button_height),
                                       manager=manager,
                                       text=button_label,
                                       container=container,
                                       anchors={'centerx': 'centerx',
                                                'top_target': relative_to},
                                       visible=True)


    def __init__(self, manager):

        self.manager = manager

        self.events_panel = UIPanel(relative_rect=Rect(0, 150, self.event_window_width, self.event_window_height),
                               manager=manager,
                               visible=True)

        subpanel_rect = Rect(5, 50, self.event_button.button_width + 30, 340)

        self.events_subpanel = UIScrollingContainer(relative_rect=subpanel_rect,
                                  manager=ui_manager,
                                  container=self.events_panel,
                                  anchors={'centerx': 'centerx'},
                                  visible=True)


    def add_event_to_list(self, event):
        """
        event[0]: name
        event[1]: date
        event[2]: additional data
        """

        # if this is the first event in the list, position it relative to the top of the subpanel
        if len(self.events) == 0:
            self.events.append(self.event_button(self.manager, self.events_subpanel.get_container(), event))
        else:
            self.events.append(self.event_button(self.manager, self.events_subpanel.get_container(), event, self.events[-1].ui_panel))

        self.events_subpanel.set_scrollable_area_dimensions((self.event_button.button_width, len(self.events) * (self.event_button.button_height + self.event_button.button_padding)))

    def remove_event_from_list(self, event):
        pass

    def update_event_list(self, events):
        pass


clock = pygame.time.Clock()
is_running = True

ewindow = event_window(ui_manager)

for i in range(0, 10):
    ewindow.add_event_to_list([f"Test Event {i}", "7/19/2023"])

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
