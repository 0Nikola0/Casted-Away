#!/usr/bin/env python
import pygame
import pygame_gui

from scripts import settings as s


def main():
    pygame.init()

    pygame.display.set_caption('Quick Start')

    # TODO Screen size is hardcoded, we may want a dynamic UI in the future
    window_surface = pygame.display.set_mode(s.SCREEN_SIZE)

    background = pygame.Surface(s.SCREEN_SIZE)
    background.fill(pygame.Color('#000000'))

    manager = pygame_gui.UIManager(s.SCREEN_SIZE)

    # --- GUI: CREATE A BUTTON ---
    hello_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 275), (100, 50)),
        text='Say Hello',
        manager=manager)

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(s.FPS)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # --- GUI: HANDLE THE BUTTON ---
                    if event.ui_element == hello_button:
                        print('Hello World!')

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()


if __name__ == '__main__':
    main()
