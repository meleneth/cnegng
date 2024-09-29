import pygame

from cnegng.generations.two.log_widget import LogWidget

# Example usage of LogWidget
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    log_widget = LogWidget(10, 10, 780, 200)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Example: Adding a log message every second
        log_widget(f"Log message {pygame.time.get_ticks()}")

        screen.fill((30, 30, 30))  # Clear the screen
        log_widget.draw(screen)  # Draw the log widget

        pygame.display.flip()
        clock.tick(60)  # Cap to 60 FPS

    pygame.quit()
