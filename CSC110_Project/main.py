"""
Main module of our program.
"""
import pygame
from typing import Optional
from dataclasses import dataclass


@dataclass
class Button:
    """
    Class that stores information about a button.

    Instance Attributes:
    - x: The x position of the top-left of the button
    - y: The y position of the top-left of the button
    - width: The width of the button
    - height: The height of the button
    - background_colour: The colour of the button
    - text: Text to be displayed on the button
    """
    x: int
    y: int
    width: int
    height: int
    background_colour: tuple[int, int, int]
    text: Optional[str] = None


class App:
    """
    Manager class of our app.

    Instance Attributes:
    - background_colour: The colour of the screen
    - width: The width of the screen
    - height: The height of the screen
    - running: Whether the app is running or not
    - state: Determines which graph should be shown, is either 1 or 0
    - button: A button to be displayed on the screen
    - font: A default font for text rendering
    """
    background_colour = (255, 255, 255)
    width, height = (800, 600)
    running = True
    state = 0
    # TODO: Fill in the button parameters
    button = Button(100, 50, 200, 50, (0, 0, 0), 'Press Me')
    font: pygame.font.SysFont

    def __init__(self):
        """
        Initializes pygame and pygame.font. Also sets a default value
        for self.font.
        """
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Corbel', 24)

    def run(self) -> None:
        """
        Runs the app.

        The main function of the class, calling this function will open a pygame window
        with the app inside it.
        """
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('CS Final Project')
        screen.fill(self.background_colour)
        pygame.display.flip()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    # Update state if mouse click detected inside button bounds.
                    if (self.button.x <= mouse[0] <= self.button.x + self.button.width) and \
                       (self.button.y <= mouse[1] <= self.button.y + self.button.height):
                        self.state = not self.state

            # Fill the screen and draw the button
            screen.fill(self.background_colour)
            button_rect = pygame.Rect(
                self.button.x,
                self.button.y,
                self.button.width,
                self.button.height
            )
            pygame.draw.rect(screen, self.button.background_colour, button_rect)

            # To change the x, y position of the text, change the parameters of screen.blit
            # which are the x, y of the top-left corner of the text.
            # Be careful! The y-axis increases downwards in pygame, i.e. 100 is **lower** than 0
            # To change the text colour,
            # change the tuple in self.font.render(...)
            if self.button.text is not None:
                text = self.font.render(self.button.text, True, (255, 255, 255))
                screen.blit(
                    text,
                    (
                        self.button.x + self.button.width / 4,
                        self.button.y + self.button.height / 4
                    )
                )

            if self.state == 0:
                # Display the original graph
                # Dummy text to fill the screen, delete when done
                screen.blit(
                    self.font.render('Hello!', True, (0, 0, 0)),
                    (self.width / 4, self.height / 4)
                )
            elif self.state == 1:
                # Display whatever should change after the button is pressed.
                # Dummy text to fill the screen, delete when done
                screen.blit(
                    self.font.render('Goodbye!', True, (0, 0, 0)),
                    (self.width / 4, self.height / 4)
                )

            pygame.display.update()


if __name__ == '__main__':
    app = App()
    app.run()