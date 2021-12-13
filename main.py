"""
Main module of our program.
"""
import pygame
from typing import Optional
from dataclasses import dataclass
import graphing as g
import bankruptcy as b


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
    time_mode = True
    button_previous = Button(5, 545, 200, 50, (0, 0, 0), 'Previous')
    button_switch = Button(300, 545, 200, 50, (200, 0, 0), 'Time Mode')
    button_next = Button(595, 545, 200, 50, (0, 0, 0), 'Next')

    image_list_by_time = []
    image_list_by_employee = []

    font: pygame.font.SysFont

    def __init__(self) -> None:
        """
        Initializes pygame and pygame.font. Also sets a default value
        for self.font.
        """
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Corbel', 24)

        # generate graphs for different lengths of time until bankruptcy
        for i in range(len(b.LENGTH_OF_TIME_STR)):
            img_name = g.generate_graph(i, 2)
            self.image_list_by_time.append(Image(55, 0, img_name))

        #generate graphs for different numbers of employees
        for i in range(len(b.EMPLOYEE_SIZE)):
            img_name = g.generate_graph(3, i)
            self.image_list_by_employee.append(Image(55, 0, img_name))


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

            if self.time_mode:
                current_img_list = self.image_list_by_time
            else:
                current_img_list = self.image_list_by_employee

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    # Update state if mouse click detected inside button bounds.
                    if self.button_clicked(self.button_previous, mouse):
                        self.state = (self.state - 1) % len(current_img_list)

                    elif self.button_clicked(self.button_next, mouse):
                        self.state = (self.state + 1) % len(current_img_list)

                    elif self.button_clicked(self.button_switch, mouse):
                        self.time_mode = not self.time_mode
                        self.state = 0

                        if self.time_mode:
                            self.button_switch.background_colour = (200, 0, 0)
                            self.button_switch.text = 'Time Mode'
                        else:
                            self.button_switch.background_colour = (0, 200, 0)
                            self.button_switch.text = 'Employee Mode'

            # Fill the screen and draw the button
            screen.fill(self.background_colour)
            self.draw_button(self.button_previous, screen)
            self.draw_button(self.button_next, screen)
            self.draw_button(self.button_switch, screen)

            self.draw_image(current_img_list[self.state], screen)

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
