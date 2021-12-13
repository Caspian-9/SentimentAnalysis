"""
Main module of our program.
"""
import pygame
from typing import Optional
from dataclasses import dataclass
import graphing as g


@dataclass
class Button:
    """
    Class that stores information about a button.

    Instance Attributes:
    - x: The x position of the button
    - y: The y position of the button
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


@dataclass
class Image:
    """
    Class that stores information about a button.

    Instance Attributes:
    - x: The x position of the image
    - y: The y position of the image
    - filename: The filename of the image
    """
    x: int
    y: int
    filename: str


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
    button_previous = Button(0, 0, 200, 50, (0, 0, 0), 'Previous')
    button_next = Button(300, 0, 200, 50, (0, 0, 0), 'Next')
    image_1 = Image(0, 100, 'graph1.png')
    image_2 = Image(0, 100, 'graph3.png')
    image_3 = Image(0, 100, 'graph6.png')
    image_4 = Image(0, 100, 'graph12.png')
    image_5 = Image(0, 100, 'graph999.png')
    font: pygame.font.SysFont

    def __init__(self) -> None:
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

        g.generate_graph(1)
        g.generate_graph(3)
        g.generate_graph(6)
        g.generate_graph(12)
        g.generate_graph(999)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    # Update state if mouse click detected inside button bounds.
                    if self.button_clicked(self.button_previous, mouse) is True:
                        self.state = (self.state - 1) % 5
                    elif self.button_clicked(self.button_next, mouse) is True:
                        self.state = (self.state + 1) % 5

            # Fill the screen and draw the button
            screen.fill(self.background_colour)
            self.draw_button(self.button_previous, screen)
            self.draw_button(self.button_next, screen)

            # To change the x, y position of the text, change the parameters of screen.blit
            # which are the x, y of the top-left corner of the text.
            # Be careful! The y-axis increases downwards in pygame, i.e. 100 is **lower** than 0
            # To change the text colour,
            # change the tuple in self.font.render(...)
            if self.state == 0:
                # Display the graph businesses that will go bankrupt in less than 1 months
                self.draw_image(self.image_1, screen)
            elif self.state == 1:
                # Display the graph of businesses that will go bankrupt in 1 - 3 months
                self.draw_image(self.image_2, screen)
            elif self.state == 2:
                # Display the graph of businesses that will go bankrupt in 3 - 6 months
                self.draw_image(self.image_3, screen)
            elif self.state == 3:
                # Display the graph of businesses that will go bankrupt in 6 - 12 months
                self.draw_image(self.image_4, screen)
            elif self.state == 4:
                # Display the graph businesses that will go bankrupt in more than 12 months
                self.draw_image(self.image_5, screen)

            pygame.display.update()

    def button_clicked(self, button: Button, mouse: tuple) -> bool:
        """
        Return whether the mouse click detected inside this button's bounds.
        """
        if (button.x <= mouse[0] <= button.x + button.width) and \
                (button.y <= mouse[1] <= button.y + button.height):
            return True
        else:
            return False

    def draw_button(self, button: Button, screen: pygame.Surface) -> None:
        """
        Draw the button and write on the button.
        """
        button_rect = pygame.Rect(
            button.x,
            button.y,
            button.width,
            button.height
        )
        pygame.draw.rect(screen, button.background_colour, button_rect)

        if button.text is not None:
            text = self.font.render(button.text, True, (255, 255, 255))
            screen.blit(
                text,
                (
                    button.x + button.width / 4,
                    button.y + button.height / 4
                )
            )

    def draw_image(self, image: Image, screen: pygame.Surface) -> None:
        """
        Load and display the image.
        """
        graph = pygame.image.load(image.filename)
        screen.blit(graph, (image.x, image.y))


if __name__ == '__main__':
    app = App()
    app.run()
