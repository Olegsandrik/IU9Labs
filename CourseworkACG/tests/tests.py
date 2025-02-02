import unittest
import pygame
from Final import draw_circle_with_text, draw_gradient_circle, draw_lines, draw_first, draw_second, draw_third, draw_fourth
from Final import draw_fifth, draw_sixth, draw_seventh, draw_eighth, draw_ninth, draw_tenth, draw_eleventh
from Final import draw_twelfth,draw_thirteenth, draw_fourteenth, draw_fifteenth


class TestDrawingFunctions(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        display = (1500, 1000)
        self.screen = pygame.display.set_mode(display)

    def test_draw_circle_with_text(self):
        draw_circle_with_text("Test", 100, 100, self.screen, (255, 0, 0))
        draw_circle_with_text("Test", 300, 100, self.screen, (0, 255, 0))
        draw_circle_with_text("Test", 500, 100, self.screen, (0, 0, 255))
        pygame.image.save(self.screen, "red_green_blue_circle.png")

    def test_gradient_circle_without_text(self):
        draw_gradient_circle(self.screen, (100, 100), 50, (200, 200, 200))
        draw_gradient_circle(self.screen, (200, 100), 50, (255, 0, 0))
        draw_gradient_circle(self.screen, (300, 100), 50, (0, 255, 0))
        draw_gradient_circle(self.screen, (400, 100), 50, (0, 0, 255))
        pygame.image.save(self.screen, "gradient_without_text.png")

    def test_draw_lines(self):
        lines_positions = [[100, 100, 100, 200], [200, 100, 200, 200], [300, 100, 300, 200], [400, 100, 400, 200], [100, 100, 400, 200]]
        draw_lines(self.screen, (255, 255, 255), lines_positions)
        pygame.image.save(self.screen, "lines_positions.png")

    def test_draw_first(self):
        draw_first(self.screen, self.clock)

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()
