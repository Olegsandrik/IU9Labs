import time
from time import sleep

import pygame

circle_positions = []
lines_positions = []

WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 128)

delete_tree_pool = []
delete_lines_pool = []
delete_circle_pool = []


def init():
    pygame.init()
    display = (1500, 1000)
    screen = pygame.display.set_mode(display)

    return screen


def draw_lines(screen: pygame.Surface, color=None, lines_positions_func=None):
    if lines_positions_func is None:
        lines_positions_func = lines_positions
    if color is None:
        color = BLACK
    for i in range(len(lines_positions_func)):
        if i in delete_lines_pool:
            continue
        pygame.draw.line(screen, color, (lines_positions_func[i][0], lines_positions_func[i][1]),
                         (lines_positions_func[i][2], lines_positions_func[i][3]))

    return


def draw_circle_positions(screen: pygame.Surface):
    for pos in circle_positions:
        if pos[0] in delete_circle_pool:
            continue
        if pos[0] in delete_tree_pool:
            draw_circle_with_text(pos[0], int(pos[1]), int(pos[2]), screen, (255, 0, 0))
        else:
            draw_circle_with_text(pos[0], int(pos[1]), int(pos[2]), screen)
    return


def draw_gradient_circle(screen, center, color):
    def draw_circles_with_differences(start_radius, end_radius, step, factor):
        for r in range(start_radius, end_radius, step):
            difference_0 = color[0] - (color[0] // 50) * r * factor
            difference_1 = color[1] - (color[1] // 50) * r * factor
            difference_2 = color[2] - (color[2] // 50) * r * factor
            new_color = (
                max(0, difference_0),
                max(0, difference_1),
                max(0, difference_2)
            )
            pygame.draw.circle(screen, new_color, center, r)

    draw_circles_with_differences(50, 48, -1, 0.4)
    draw_circles_with_differences(48, 45, -1, 0.3)
    draw_circles_with_differences(45, 40, -1, 0.2)
    draw_circles_with_differences(40, 0, -1, 0.1)


def draw_circle_with_text(textInCircle: str, x: int, y: int, screen: pygame.Surface, color=None):
    if color is None:
        color = (200, 200, 200)

    draw_gradient_circle(screen, (x, y), color)

    font = pygame.font.Font(None, 36)
    text = font.render(textInCircle, True, WHITE)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

    return


def draw_first(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos_1 = ["1", 200, 100]
    speed_x_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos_1[1] += speed_x_1

        if circle_pos_1[1] == 750:
            circle_positions.append(circle_pos_1)
            return

        draw_circle_with_text(circle_pos_1[0], int(circle_pos_1[1]), int(circle_pos_1[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def draw_second(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["2", 200, 100]
    speed_x_1 = 5
    speed_y_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 210:
            speed_y_1 = 0

        if circle_pos[1] == 860:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[0][1]) + 35, int(circle_positions[0][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[0][1]) + 35, int(circle_positions[0][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def draw_third(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["3", 200, 100]
    speed_x_1 = 5
    speed_y_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 320:
            speed_y_1 = 0

        if circle_pos[1] == 970:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[1][1]) + 35, int(circle_positions[1][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[1][1]) + 35, int(circle_positions[1][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def first_balance(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            if circle_positions[0][2] == 210:
                lines_positions[0][1] -= 70
                lines_positions[0][3] += 70
                break
            circle_positions[0][2] += speed
            lines_positions[0][1] += speed
            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[0][2] == 320:
                break

            circle_positions[0][2] += speed
            lines_positions[0][1] += speed
            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[1][2] == 100:
                break
            for pos in circle_positions:
                pos[1] -= speed
                pos[2] -= speed

            for line in lines_positions:
                line[0] -= speed
                line[2] -= speed
                line[1] -= speed
                line[3] -= speed

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        return


def draw_fourth(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["4", 200, 100]
    speed_x_1 = 5
    speed_y_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 320:
            speed_y_1 = 0

        if circle_pos[1] == 970:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[2][1]) + 35, int(circle_positions[2][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[2][1]) + 35, int(circle_positions[2][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def draw_fifth(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["5", 200, 100]
    speed_x_1 = 5
    speed_y_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 430:
            speed_y_1 = 0

        if circle_pos[1] == 1080:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[3][1]) + 35, int(circle_positions[3][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[3][1]) + 35, int(circle_positions[3][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def second_balance(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            if circle_positions[2][2] == 320:
                lines_positions[2][1] -= 70
                lines_positions[2][3] += 70
                lines_positions[1][2] = circle_positions[3][1] - 35
                lines_positions[1][3] = circle_positions[3][2] - 35
                break
            circle_positions[2][2] += speed
            lines_positions[2][1] += speed
            lines_positions[1][3] += speed
            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[2][2] == 430:
                break

            circle_positions[2][2] += speed
            lines_positions[2][1] += speed
            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[2][2] == 320:
                break
            for i in range(len(circle_positions)):
                if i <= 1:
                    continue
                circle_positions[i][1] -= speed
                circle_positions[i][2] -= speed

            for i in range(len(lines_positions)):
                if i <= 1:
                    continue
                lines_positions[i][0] -= speed
                lines_positions[i][2] -= speed
                lines_positions[i][1] -= speed
                lines_positions[i][3] -= speed

            lines_positions[1][2] -= speed
            lines_positions[1][3] -= speed

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        return


def draw_sixth(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["6", 200, 100]
    speed_x_1 = 5
    speed_y_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 430:
            speed_y_1 = 0

        if circle_pos[1] == 1080:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[4][1]) + 35, int(circle_positions[4][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[4][1]) + 35, int(circle_positions[4][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def third_balance(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            if circle_positions[1][2] == 210:
                lines_positions[1][1] -= 70
                lines_positions[1][3] += 70

                lines_positions[2][0] -= 70
                lines_positions[2][2] = circle_positions[1][1] + 35
                break
            circle_positions[0][2] += speed
            circle_positions[1][2] += speed

            lines_positions[0][1] += speed
            lines_positions[0][3] += speed

            lines_positions[1][1] += speed

            circle_positions[0][1] -= speed
            circle_positions[1][1] -= speed

            lines_positions[0][0] -= speed
            lines_positions[0][2] -= speed

            lines_positions[1][0] -= speed

            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[1][2] == 320:
                break

            circle_positions[0][2] += speed
            circle_positions[1][2] += speed
            circle_positions[2][2] += speed

            lines_positions[0][1] += speed
            lines_positions[0][3] += speed

            lines_positions[2][1] += speed
            lines_positions[2][3] += speed

            lines_positions[1][1] += speed


            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)


        while True:
            if circle_positions[2][2] == 320:
                break
            for i in range(len(circle_positions)):
                if i == 4 or i == 5:
                    circle_positions[i][2] -= speed
                    continue
                circle_positions[i][1] -= speed
                circle_positions[i][2] -= speed

            for i in range(len(lines_positions)):
                if i == 3:
                    lines_positions[i][0] -= speed
                    lines_positions[i][1] -= speed
                    lines_positions[i][3] -= speed
                    continue
                if i == 4:
                    lines_positions[i][1] -= speed
                    lines_positions[i][3] -= speed
                    continue
                lines_positions[i][0] -= speed
                lines_positions[i][2] -= speed
                lines_positions[i][1] -= speed
                lines_positions[i][3] -= speed

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)
        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
        return


def draw_seventh(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["7", 200, 100]
    speed_x_1 = 0
    speed_y_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 430:
            speed_x_1 = 5
            speed_y_1 = 0

        if circle_pos[1] == 1190:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[5][1]) + 35, int(circle_positions[5][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[5][1]) + 35, int(circle_positions[5][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def fourth_balance(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            if circle_positions[4][2] == 320:
                lines_positions[3][2] = circle_positions[5][1] - 35
                lines_positions[4][1] -= 70
                lines_positions[4][3] += 70
                break

            circle_positions[4][2] += speed
            lines_positions[3][3] += speed
            lines_positions[4][1] += speed

            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[4][2] == 430:
                break

            circle_positions[4][2] += speed
            lines_positions[4][1] += speed

            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[5][2] == 210:
                break

            circle_positions[5][1] -= speed
            circle_positions[5][2] -= speed

            circle_positions[6][1] -= speed
            circle_positions[6][2] -= speed

            circle_positions[4][1] -= speed
            circle_positions[4][2] -= speed

            lines_positions[4][0] -= speed
            lines_positions[4][1] -= speed
            lines_positions[4][2] -= speed
            lines_positions[4][3] -= speed

            lines_positions[5][0] -= speed
            lines_positions[5][1] -= speed
            lines_positions[5][2] -= speed
            lines_positions[5][3] -= speed

            lines_positions[3][2] -= speed
            lines_positions[3][3] -= speed

            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
        return


def draw_eighth(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["8", 200, 100]
    speed_x_1 = 0
    speed_y_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 430:
            speed_x_1 = 5
            speed_y_1 = 0

        if circle_pos[1] == 1190:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[6][1]) + 35, int(circle_positions[6][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[6][1]) + 35, int(circle_positions[6][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def draw_ninth(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["9", 200, 100]
    speed_x_1 = 0
    speed_y_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 540:
            speed_x_1 = 5
            speed_y_1 = 0

        if circle_pos[1] == 1300:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[7][1]) + 35, int(circle_positions[7][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[7][1]) + 35, int(circle_positions[7][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def fifth_balance(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            circle_positions[6][2] += speed
            lines_positions[5][3] += speed
            lines_positions[6][1] += speed
            if circle_positions[6][2] == 430:
                lines_positions[6][1] -= 70
                lines_positions[6][3] += 70
                lines_positions[5][2] = circle_positions[7][1] - 35
                break

            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            circle_positions[6][2] += speed
            lines_positions[6][1] += speed
            if circle_positions[6][2] == 540:
                break
            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[7][2] == 320:
                break
            circle_positions[6][1] -= speed
            circle_positions[6][2] -= speed
            
            circle_positions[7][1] -= speed
            circle_positions[7][2] -= speed
            
            circle_positions[8][1] -= speed
            circle_positions[8][2] -= speed
            
            lines_positions[6][0] -= speed
            lines_positions[6][1] -= speed
            lines_positions[6][2] -= speed
            lines_positions[6][3] -= speed

            lines_positions[7][0] -= speed
            lines_positions[7][1] -= speed
            lines_positions[7][2] -= speed
            lines_positions[7][3] -= speed

            lines_positions[5][2] -= speed
            lines_positions[5][3] -= speed

            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        return


def draw_tenth(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["10", 200, 100]
    speed_x_1 = 0
    speed_y_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 540:
            speed_x_1 = 5
            speed_y_1 = 0

        if circle_pos[1] == 1300:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[8][1]) + 35, int(circle_positions[8][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[8][1]) + 35, int(circle_positions[8][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def sixth_balance(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            if circle_positions[5][2] == 320:
                lines_positions[5][1] -= 70
                lines_positions[5][3] += 70
                lines_positions[3][2] = circle_positions[7][1] - 35
                lines_positions[6][2] = circle_positions[5][1] + 35

                break
            circle_positions[5][2] += speed
            circle_positions[4][2] += speed
            lines_positions[4][1] += speed
            lines_positions[4][3] += speed
            lines_positions[3][3] += speed
            lines_positions[5][1] += speed

            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[5][2] == 430:
                lines_positions[6][0] -= 70
                break
            circle_positions[4][2] += speed
            circle_positions[6][2] += speed
            circle_positions[5][2] += speed
            circle_positions[6][1] += speed

            lines_positions[4][1] += speed
            lines_positions[4][3] += speed

            lines_positions[6][1] += speed
            lines_positions[6][3] += speed
            lines_positions[6][0] += speed

            lines_positions[5][1] += speed

            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)


        while True:
            if circle_positions[7][2] == 210:
                break

            for i in range(4, 10):
                for j in range(1, 3):
                    circle_positions[i][j] -= speed

            for i in range(4, 9):
                for j in range(0, 4):
                    lines_positions[i][j] -= speed
            lines_positions[3][2] -= speed
            lines_positions[3][3] -= speed

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)


        while True:
            if circle_positions[5][1] == 750:
                break

            circle_positions[6][1] -= speed
            circle_positions[5][1] -= speed
            circle_positions[4][1] -= speed

            lines_positions[4][0] -= speed
            lines_positions[4][2] -= speed

            lines_positions[6][0] -= speed
            lines_positions[6][2] -= speed

            lines_positions[5][0] -= speed

            circle_positions[9][1] += speed
            circle_positions[8][1] += speed

            lines_positions[8][0] += speed
            lines_positions[8][2] += speed

            lines_positions[7][2] += speed

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)
        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
        return


def draw_eleventh(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["11", 200, 100]
    speed_x_1 = 0
    speed_y_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 540:
            speed_x_1 = 5
            speed_y_1 = 0

        if circle_pos[1] == 1410:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[9][1]) + 35, int(circle_positions[9][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[9][1]) + 35, int(circle_positions[9][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def seventh_balance(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            if circle_positions[8][2] == 430:
                lines_positions[8][1] -= 70
                lines_positions[8][3] += 70
                lines_positions[7][2] = circle_positions[9][1] - 35
                break
            circle_positions[8][2] += speed
            lines_positions[7][3] += speed
            lines_positions[8][1] += speed
            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[8][2] == 540:
                break
            circle_positions[8][2] += speed
            lines_positions[8][1] += speed
            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)
        while True:
            if circle_positions[9][2] == 320:
                break

            for i in range(8, 11):
                for j in range(1, 3):
                    circle_positions[i][j] -= speed

            for i in range(8, 10):
                for j in range(0, 4):
                    lines_positions[i][j] -= speed
            lines_positions[7][2] -= speed
            lines_positions[7][3] -= speed

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)
        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
        return


def draw_twelfth(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["12", 200, 100]
    speed_x_1 = 0
    speed_y_1 = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 540:
            speed_x_1 = 5
            speed_y_1 = 0

        if circle_pos[1] == 1410:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[10][1]) + 35, int(circle_positions[10][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[10][1]) + 35, int(circle_positions[10][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def eighth_balance(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            if circle_positions[3][1] == 640:

                break
            circle_positions[3][1] -= speed
            circle_positions[2][1] -= speed
            circle_positions[1][1] -= speed
            circle_positions[0][1] -= speed

            lines_positions[0][0] -= speed
            lines_positions[0][2] -= speed

            lines_positions[1][0] -= speed
            lines_positions[1][2] -= speed

            lines_positions[2][0] -= speed
            lines_positions[2][2] -= speed

            lines_positions[3][0] -= speed


            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[3][2] == 210:
                lines_positions[3][1] -= 70
                lines_positions[3][3] += 70
                lines_positions[5][2] = circle_positions[3][1] + 35
                lines_positions[5][0] -= 70
                break
            circle_positions[3][2] += speed
            circle_positions[2][2] += speed
            circle_positions[1][2] += speed
            circle_positions[0][2] += speed

            lines_positions[0][1] += speed
            lines_positions[0][3] += speed

            lines_positions[1][1] += speed
            lines_positions[1][3] += speed

            lines_positions[2][1] += speed
            lines_positions[2][3] += speed

            lines_positions[3][1] += speed

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[3][2] == 320:
                break
            for i in range(7):
                circle_positions[i][2] += speed

            for i in range(7):
                if i == 3:
                    continue
                lines_positions[i][1] += speed
                lines_positions[i][3] += speed

            lines_positions[3][1] += speed
            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[7][2] == 200:
                break
            for pos in circle_positions:
                pos[1] -= speed
                pos[2] -= speed

            for line in lines_positions:
                line[1] -= speed
                line[2] -= speed
                line[3] -= speed
                line[0] -= speed

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)
        while True:
            if circle_positions[7][1] == 750:
                break
            for pos in circle_positions:
                pos[1] -= speed

            for line in lines_positions:
                line[2] -= speed
                line[0] -= speed

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)
        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
        return


def draw_thirteenth(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["13", 200, 100]
    speed_x_1 = 5
    speed_y_1 = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 650:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[11][1]) + 35, int(circle_positions[11][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[11][1]) + 35, int(circle_positions[11][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return


        if circle_pos[1] == 1300:
            speed_x_1 = 0
            speed_y_1 = 5

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def ninth_balance(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            if circle_positions[10][2] == 530:
                lines_positions[10][1] -= 70
                lines_positions[10][3] += 70
                lines_positions[9][2] = circle_positions[11][1] - 35
                break
            circle_positions[10][2] += speed
            lines_positions[9][3] += speed
            lines_positions[10][1] += speed
            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[10][2] == 640:
                break
            circle_positions[10][2] += speed
            lines_positions[10][1] += speed
            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[11][2] == 420:
                break
            for i in range(10, 13):
                circle_positions[i][2] -= speed
                circle_positions[i][1] -= speed
            for i in range(10, 12):
                for j in range(4):
                    lines_positions[i][j] -= speed
            lines_positions[9][2] -= speed
            lines_positions[9][3] -= speed

            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)


        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
        return


def tenth_balance(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            if circle_positions[9][2] == 420:
                lines_positions[9][1] -= 70
                lines_positions[9][3] += 70
                lines_positions[7][2] = circle_positions[11][1] - 35
                lines_positions[10][2] = circle_positions[9][1] + 35
                break
            circle_positions[9][2] += speed
            circle_positions[8][2] += speed

            lines_positions[8][1] += speed
            lines_positions[8][3] += speed

            lines_positions[7][3] += speed

            lines_positions[9][1] += speed

            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)


        while True:
            if circle_positions[9][2] == 530:
                lines_positions[10][0] -= 70
                break
            circle_positions[10][2] += speed
            circle_positions[9][2] += speed
            circle_positions[8][2] += speed

            lines_positions[8][1] += speed
            lines_positions[8][3] += speed

            lines_positions[9][1] += speed

            lines_positions[10][1] += speed
            lines_positions[10][3] += speed

            circle_positions[10][1] += speed
            lines_positions[10][0] += speed

            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)


        while True:
            if circle_positions[11][2] == 310:

                for i in range(10):
                    circle_positions[12][2] -= 1
                    circle_positions[13][2] -= 1
                    lines_positions[12][1] -= 1
                    lines_positions[12][3] -= 1
                    lines_positions[11][3] -= 1
                    screen.fill(WHITE)

                    draw_circle_positions(screen)
                    draw_lines(screen)

                    pygame.display.flip()
                    clock.tick(60)
                break

            for i in range(8, 14):
                circle_positions[i][2] -= speed
                circle_positions[i][1] -= speed

            for i in range(8, 13):
                for j in range(4):
                    lines_positions[i][j] -= speed

            lines_positions[7][2] -= speed
            lines_positions[7][3] -= speed
            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)
        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
        return


def draw_fourteenth(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["14", 200, 100]
    speed_x_1 = 5
    speed_y_1 = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 650:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[12][1]) + 35, int(circle_positions[12][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[12][1]) + 35, int(circle_positions[12][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return


        if circle_pos[1] == 1300:
            speed_x_1 = 0
            speed_y_1 = 5

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def draw_fifteenth(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos = ["15", 200, 100]
    speed_x_1 = 5
    speed_y_1 = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] == 650:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[13][1]) + 35, int(circle_positions[13][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[13][1]) + 35, int(circle_positions[13][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return


        if circle_pos[1] == 1300:
            speed_x_1 = 0
            speed_y_1 = 5

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def eleventh_balance(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            if circle_positions[13][2] == 420:
                lines_positions[11][2] = circle_positions[13][1] - 35
                lines_positions[11][3] = circle_positions[13][2] - 35
                break
            if circle_positions[12][2] == 475:
                lines_positions[12][1] -= 70
                lines_positions[12][3] += 70
            circle_positions[12][2] += speed

            lines_positions[11][3] += speed
            lines_positions[12][1] += speed

            circle_positions[13][2] -= speed
            circle_positions[14][2] -= speed

            lines_positions[13][1] -= speed
            lines_positions[13][3] -= speed

            lines_positions[12][3] -= speed


            screen.fill(WHITE)

            draw_circle_positions(screen)

            draw_lines(screen)
            pygame.display.flip()
            clock.tick(60)

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
        return


def delete_first(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("2")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("2")

    delete_lines_pool.append(0)

    lines_positions[2][2] = circle_positions[0][1] + 35
    lines_positions[2][3] = circle_positions[0][2] + 35

    lines_positions[1][0] = circle_positions[0][1] + 35
    lines_positions[1][1] = circle_positions[0][2] - 35

    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(WHITE)

        circle_positions[0][1] += speed
        circle_positions[0][2] -= speed

        lines_positions[1][0] += speed
        lines_positions[2][2] += speed
        lines_positions[1][1] -= speed
        lines_positions[2][3] -= speed

        if circle_positions[0][1] == 200:
            break

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
    return


def delete_second(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("3")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("3")
    delete_lines_pool.append(2)

    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    return


def delete_third(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("4")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("4")

    delete_lines_pool.append(5)

    lines_positions[4][2] = circle_positions[0][1] + 35
    lines_positions[4][3] = circle_positions[0][2] + 35
    lines_positions[4][0] -= 70

    lines_positions[3][0] = circle_positions[5][1] + 35
    lines_positions[3][1] = circle_positions[5][2] - 35

    lines_positions[1][2] = circle_positions[5][1] - 35
    lines_positions[1][3] = circle_positions[5][2] + 35

    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    running = True
    speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            circle_positions[5][1] -= speed
            circle_positions[5][2] -= speed

            circle_positions[6][1] -= speed
            circle_positions[6][2] -= speed

            lines_positions[3][0] -= speed
            lines_positions[3][1] -= speed

            lines_positions[1][2] -= speed
            lines_positions[1][3] -= speed

            lines_positions[6][0] -= speed
            lines_positions[6][1] -= speed
            lines_positions[6][2] -= speed
            lines_positions[6][3] -= speed

            if circle_positions[5][1] == 420:
                break

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        while True:
            circle_positions[4][1] -= speed

            lines_positions[4][0] -= speed

            if circle_positions[4][1] == 310:
                break

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)
        return


def delete_fourth(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("5")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("5")
    delete_lines_pool.append(4)

    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)


    return


def delete_fifth(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("6")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("6")
    delete_lines_pool.append(1)

    lines_positions[3][0] = circle_positions[0][1] + 35
    lines_positions[3][1] = circle_positions[0][2] - 35

    lines_positions[6][2] = circle_positions[0][1] + 35
    lines_positions[6][3] = circle_positions[0][2] + 35

    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)


    speed = 5
    while True:
        circle_positions[0][1] += speed
        circle_positions[0][2] -= speed * 0.5

        lines_positions[3][0] += speed
        lines_positions[3][1] -= speed * 0.5

        lines_positions[6][2] += speed
        lines_positions[6][3] -= speed * 0.5

        if circle_positions[0][1] == 420:
            break

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)

    return


def delete_sixth(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("7")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("7")
    delete_lines_pool.append(6)

    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)


    running = True
    speed = 5
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while True:
            circle_positions[0][1] += speed
            lines_positions[3][0] += speed

            if circle_positions[0][1] == 640:
                break

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        while True:
            circle_positions[0][2] += speed
            circle_positions[7][2] += speed
            lines_positions[3][1] += speed
            lines_positions[3][3] += speed

            lines_positions[7][1] += speed

            if circle_positions[7][2] == 310:
                lines_positions[7][1] -= 70
                lines_positions[7][3] += 70
                lines_positions[9][2] = circle_positions[7][1] + 35
                lines_positions[9][3] = circle_positions[7][2] + 35
                lines_positions[9][0] -= 70
                break

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        while True:
            circle_positions[0][2] += speed
            circle_positions[7][2] += speed
            circle_positions[8][2] += speed
            circle_positions[9][2] += speed
            circle_positions[10][2] += speed

            lines_positions[3][1] += speed
            lines_positions[3][3] += speed

            lines_positions[8][1] += speed
            lines_positions[8][3] += speed

            lines_positions[9][1] += speed
            lines_positions[9][3] += speed

            lines_positions[10][1] += speed
            lines_positions[10][3] += speed

            lines_positions[7][1] += speed

            if circle_positions[7][2] == 420:
                break

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        while True:
            for pos in circle_positions:
                pos[1] -= speed
                pos[2] -= speed

            for line in lines_positions:
                line[0] -= speed
                line[1] -= speed
                line[2] -= speed
                line[3] -= speed

            if circle_positions[11][2] == 100:
                for i in range(2):
                    for pos in circle_positions:
                        pos[1] -= speed

                    for line in lines_positions:
                        line[0] -= speed
                        line[2] -= speed
                    screen.fill(WHITE)

                    draw_circle_positions(screen)
                    draw_lines(screen)

                    pygame.display.flip()
                    clock.tick(60)
                break
            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)
        return


def delete_seventh(screen: pygame.Surface, clock: pygame.time.Clock):
    sleep(0.1)
    delete_tree_pool.append("8")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("8")
    delete_lines_pool.append(9)

    lines_positions[7][0] = circle_positions[9][1] + 35
    lines_positions[7][1] = circle_positions[9][2] - 35

    lines_positions[8][2] = circle_positions[0][1] + 35
    lines_positions[8][3] = circle_positions[0][2] + 35

    lines_positions[3][2] = circle_positions[9][1] - 35
    lines_positions[3][3] = circle_positions[9][2] + 35

    lines_positions[8][0] -= 70

    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    speed = 5
    while True:
        circle_positions[9][1] -= speed
        circle_positions[9][2] -= speed

        circle_positions[10][1] -= speed
        circle_positions[10][2] -= speed

        lines_positions[10][0] -= speed
        lines_positions[10][1] -= speed
        lines_positions[10][2] -= speed
        lines_positions[10][3] -= speed

        lines_positions[3][2] -= speed
        lines_positions[3][3] -= speed

        lines_positions[7][0] -= speed
        lines_positions[7][1] -= speed

        if circle_positions[9][2] == 210:
            break

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
    return


def delete_eighth(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("9")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("9")
    delete_lines_pool.append(8)

    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    return


def delete_ninth(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("10")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("10")
    delete_lines_pool.append(3)

    lines_positions[7][0] = circle_positions[0][1] + 35
    lines_positions[7][1] = circle_positions[0][2] - 35

    lines_positions[10][2] = circle_positions[0][1] + 35
    lines_positions[10][3] = circle_positions[0][2] + 35

    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    speed = 5
    while True:
        circle_positions[0][1] += speed
        circle_positions[0][2] -= speed

        lines_positions[7][0] += speed
        lines_positions[7][1] -= speed

        lines_positions[10][2] += speed
        lines_positions[10][3] -= speed

        if circle_positions[0][2] == 210:
            break

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    return


def delete_tenth(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("11")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("11")
    delete_lines_pool.append(10)

    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    return


def delete_eleventh(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("12")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("12")
    delete_lines_pool.append(7)

    lines_positions[11][0] = circle_positions[0][1] + 35
    lines_positions[11][1] = circle_positions[0][2] - 35

    lines_positions[12][2] = circle_positions[0][1] + 35
    lines_positions[12][3] = circle_positions[0][2] + 35
    lines_positions[12][0] -= 70

    speed = 5
    while True:
        if circle_positions[0][1] == 750:
            lines_positions[11][3] += 70
            break
        circle_positions[0][1] += speed
        lines_positions[11][0] += speed
        lines_positions[12][2] += speed

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)

    while True:
        if circle_positions[0][2] == 320:
            break

        circle_positions[0][2] += speed
        circle_positions[12][2] += speed
        lines_positions[12][1] += speed
        lines_positions[12][3] += speed

        lines_positions[11][1] += speed



        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
    while True:
        if circle_positions[13][2] == 100:
            break
        for pos in circle_positions:
            pos[1] -= speed
            pos[2] -= speed

        for line in lines_positions:
            line[0] -= speed
            line[2] -= speed
            line[1] -= speed
            line[3] -= speed
        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)

    while True:
        if circle_positions[13][1] == 750:
            break
        for pos in circle_positions:
            pos[1] -= speed

        for line in lines_positions:
            line[0] -= speed
            line[2] -= speed
        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    return


def delete_twelfth(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("13")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("13")
    delete_lines_pool.append(12)
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    speed = 5
    while True:
        if circle_positions[0][1] == 640:
            break
        circle_positions[0][1] += speed
        lines_positions[11][0] += speed
        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)

    return


def delete_thirteenth(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("14")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("14")
    delete_lines_pool.append(11)

    lines_positions[13][0] = circle_positions[0][1] + 35
    lines_positions[13][1] = circle_positions[0][2] + 35
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    speed = 5
    while True:
        if circle_positions[0][1] == 750:
            break
        circle_positions[0][1] += speed
        circle_positions[0][2] -= speed

        lines_positions[13][0] += speed
        lines_positions[13][1] -= speed

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)

    return


def delete_fourteenth(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("15")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("15")
    delete_lines_pool.append(13)
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    return


def delete_fifteenth(screen: pygame.Surface, clock: pygame.time.Clock):
    delete_tree_pool.append("1")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)
    time.sleep(3)

    delete_circle_pool.append("1")
    screen.fill(WHITE)

    draw_circle_positions(screen)
    draw_lines(screen)

    pygame.display.flip()
    clock.tick(60)

    return


def final_demonstration():
    screen = init()
    clock = pygame.time.Clock()
    draw_first(screen, clock)
    draw_second(screen, clock)
    draw_third(screen, clock)
    first_balance(screen, clock)
    draw_fourth(screen, clock)
    draw_fifth(screen, clock)
    second_balance(screen, clock)
    draw_sixth(screen, clock)
    third_balance(screen, clock)
    draw_seventh(screen, clock)
    fourth_balance(screen, clock)
    draw_eighth(screen, clock)
    draw_ninth(screen, clock)
    fifth_balance(screen, clock)
    draw_tenth(screen, clock)
    sixth_balance(screen, clock)
    draw_eleventh(screen, clock)
    seventh_balance(screen, clock)
    draw_twelfth(screen, clock)
    eighth_balance(screen, clock)
    draw_thirteenth(screen, clock)
    ninth_balance(screen, clock)
    draw_fourteenth(screen, clock)
    tenth_balance(screen, clock)
    draw_fifteenth(screen, clock)
    eleventh_balance(screen, clock)
    sleep(3)
    delete_first(screen, clock)
    delete_second(screen, clock)
    delete_third(screen, clock)
    delete_fourth(screen, clock)
    delete_fifth(screen, clock)
    delete_sixth(screen, clock)
    delete_seventh(screen, clock)
    delete_eighth(screen, clock)
    delete_ninth(screen, clock)
    delete_tenth(screen, clock)
    delete_eleventh(screen, clock)
    delete_twelfth(screen, clock)
    delete_thirteenth(screen, clock)
    delete_fourteenth(screen, clock)
    delete_fifteenth(screen, clock)
    sleep(2)
    pygame.quit()


if __name__ == "__main__":
    final_demonstration()

