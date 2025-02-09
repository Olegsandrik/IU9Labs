from time import sleep

import pygame

circle_positions = []
lines_positions = []
l_tree_pool = ["4", "5"]
n_tree_pool = ["11"]
m_tree_pool = ["9", "8"]
r_tree_pool = ["14"]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 128)

def init():
    pygame.init()
    display = (1500, 1100)
    screen = pygame.display.set_mode(display)

    return screen


def draw_lines(screen: pygame.Surface):
    for line in lines_positions:
        pygame.draw.line(screen, BLACK, (line[0], line[1]), (line[2], line[3]))

    return


def draw_circle_positions(screen: pygame.Surface):
    for pos in circle_positions:
        if pos[0] in l_tree_pool:
            draw_circle_with_text(pos[0], int(pos[1]), int(pos[2]), screen, (0, 0, 255))
            continue
        if pos[0] in m_tree_pool:
            draw_circle_with_text(pos[0], int(pos[1]), int(pos[2]), screen, (255, 0, 0))
            continue
        if pos[0] in r_tree_pool:
            draw_circle_with_text(pos[0], int(pos[1]), int(pos[2]), screen, (0, 255, 0))
            continue
        if pos[0] in n_tree_pool:
            draw_circle_with_text(pos[0], int(pos[1]), int(pos[2]), screen, (255, 255, 0))
            continue
        draw_circle_with_text(pos[0], int(pos[1]), int(pos[2]), screen)

    return


def draw_gradient_circle(screen, center, radius, color):
    for r in range(50, 48, -1):
        difference_0 = color[0] - (color[0] // radius) * r * 0.4
        difference_1 = color[1] - (color[1] // radius) * r * 0.4
        difference_2 = color[2] - (color[2] // radius) * r * 0.4
        new_color = (
            max(0, difference_0),
            max(0, difference_1),
            max(0, difference_2)
        )
        pygame.draw.circle(screen, new_color, center, r)

    for r in range(48, 45, -1):
        difference_0 = color[0] - (color[0] // radius) * r * 0.3
        difference_1 = color[1] - (color[1] // radius) * r * 0.3
        difference_2 = color[2] - (color[2] // radius) * r * 0.3
        new_color = (
            max(0, difference_0),
            max(0, difference_1),
            max(0, difference_2)
        )
        pygame.draw.circle(screen, new_color, center, r)

    for r in range(45, 40, -1):
        difference_0 = color[0] - (color[0] // radius) * r * 0.2
        difference_1 = color[1] - (color[1] // radius) * r * 0.2
        difference_2 = color[2] - (color[2] // radius) * r * 0.2
        new_color = (
            max(0, difference_0),
            max(0, difference_1),
            max(0, difference_2)
        )
        pygame.draw.circle(screen, new_color, center, r)

    for r in range(40, 0, -1):
        difference_0 = color[0] - (color[0] // radius) * r * 0.1
        difference_1 = color[1] - (color[1] // radius) * r * 0.1
        difference_2 = color[2] - (color[2] // radius) * r * 0.1
        new_color = (
            max(0, difference_0),
            max(0, difference_1),
            max(0, difference_2)
        )
        pygame.draw.circle(screen, new_color, center, r)


def draw_circle_with_text(textInCircle: str, x: int, y: int, screen: pygame.Surface, color=None):
    if color is None:
        color = (200, 200, 200)

    draw_gradient_circle(screen, (x, y), 50, color)

    font = pygame.font.Font(None, 36)
    text = font.render(textInCircle, True, WHITE)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

    return


def draw_first(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    circle_pos_1 = ["12", 200, 100]
    speed_x_1 = 6

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)

        draw_lines(screen)

        circle_pos_1[1] += speed_x_1

        if circle_pos_1[1] == 752:
            circle_positions.append(circle_pos_1)
            return

        draw_circle_with_text(circle_pos_1[0], int(circle_pos_1[1]), int(circle_pos_1[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def draw_second(screen: pygame.Surface, clock: pygame.time.Clock):
    circle_pos = ["14", 200, 100]
    speed_x_1 = 4.5
    speed_y_1 = 3
    running = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)
        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[1] > 500:
            speed_y_1 = 0
            speed_x_1 = 6

        if circle_pos[1] > 900:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[0][1]) + 35, int(circle_positions[0][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[0][1]) + 35, int(circle_positions[0][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return
        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen, (0, 255, 0))

        pygame.display.flip()
        clock.tick(60)


def draw_third(screen: pygame.Surface, clock: pygame.time.Clock):
    circle_pos = ["6", 200, 100]
    speed_x_1 = 6
    speed_y_1 = 4

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)
        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[1] > 500:
            speed_y_1 = 0
            # speed_x_1 = 6

        if circle_pos[1] > 600:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[0][1]) - 35, int(circle_positions[0][2]) + 35),
                             (int(circle_pos[1]) + 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[0][1]) - 35, int(circle_positions[0][2]) + 35,
                                    int(circle_pos[1]) + 35, int(circle_pos[2]) - 35])
            return
        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen)

        pygame.display.flip()
        clock.tick(60)


def draw_fourth(screen: pygame.Surface, clock: pygame.time.Clock):
    circle_pos = ["10", 200, 100]
    speed_x_1 = 3
    speed_y_1 = 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)
        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] > 500:
            speed_y_1 = 0
            speed_x_1 = 6

        if circle_pos[1] > 750:
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
    circle_pos = ["11", 200, 100]
    speed_x_1 = 3
    speed_y_1 = 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)
        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] > 700:
            speed_y_1 = 0
            speed_x_1 = 6

        if circle_pos[1] > 900:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[3][1]) + 35, int(circle_positions[3][2]) + 35),
                             (int(circle_pos[1]) - 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[3][1]) + 35, int(circle_positions[3][2]) + 35,
                                    int(circle_pos[1]) - 35, int(circle_pos[2]) - 35])
            return
        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen, (255, 255, 0))

        pygame.display.flip()
        clock.tick(60)


def draw_sixth(screen: pygame.Surface, clock: pygame.time.Clock):
    circle_pos = ["9", 200, 100]
    speed_x_1 = 3
    speed_y_1 = 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)
        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] > 700:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[3][1]) - 35, int(circle_positions[3][2]) + 35),
                             (int(circle_pos[1]) + 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[3][1]) - 35, int(circle_positions[3][2]) + 35,
                                    int(circle_pos[1]) + 35, int(circle_pos[2]) - 35])
            return

        if circle_pos[1] > 600:
            speed_x_1 = 0
            speed_y_1 = 6


        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen, (255, 0, 0))

        pygame.display.flip()
        clock.tick(60)


def draw_seventh(screen: pygame.Surface, clock: pygame.time.Clock):
    circle_pos = ["8", 200, 100]
    speed_x_1 = 3
    speed_y_1 = 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)
        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] > 900:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[5][1]) - 35, int(circle_positions[5][2]) + 35),
                             (int(circle_pos[1]) + 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[5][1]) - 35, int(circle_positions[5][2]) + 35,
                                    int(circle_pos[1]) + 35, int(circle_pos[2]) - 35])
            return

        if circle_pos[1] > 450:
            speed_x_1 = 0
            speed_y_1 = 6

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen, (255, 0, 0))

        pygame.display.flip()
        clock.tick(60)


def draw_eighth(screen: pygame.Surface, clock: pygame.time.Clock):
    circle_pos = ["5", 200, 100]
    speed_x_1 = 3
    speed_y_1 = 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)
        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] > 500:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[2][1]) - 35, int(circle_positions[2][2]) + 35),
                             (int(circle_pos[1]) + 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[2][1]) - 35, int(circle_positions[2][2]) + 35,
                                    int(circle_pos[1]) + 35, int(circle_pos[2]) - 35])
            return

        if circle_pos[1] > 450:
            speed_x_1 = 0
            speed_y_1 = 6

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen, (0, 0, 255))

        pygame.display.flip()
        clock.tick(60)


def draw_ninth(screen: pygame.Surface, clock: pygame.time.Clock):
    circle_pos = ["4", 200, 100]
    speed_x_1 = 3
    speed_y_1 = 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)
        circle_pos[1] += speed_x_1
        circle_pos[2] += speed_y_1

        if circle_pos[2] > 700:
            circle_positions.append(circle_pos)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(circle_positions[7][1]) - 35, int(circle_positions[7][2]) + 35),
                             (int(circle_pos[1]) + 35, int(circle_pos[2]) - 35), 1)
            lines_positions.append([int(circle_positions[7][1]) - 35, int(circle_positions[7][2]) + 35,
                                    int(circle_pos[1]) + 35, int(circle_pos[2]) - 35])
            return

        if circle_pos[1] > 300:
            speed_x_1 = 0
            speed_y_1 = 6

        draw_circle_with_text(circle_pos[0], int(circle_pos[1]), int(circle_pos[2]), screen, (0, 0, 255))

        pygame.display.flip()
        clock.tick(60)


def wait(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)
        sleep(10)
        return


def small_left_rotate(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_circle_positions(screen)
        draw_lines(screen)

        pygame.display.flip()
        clock.tick(60)

        speed_x_1 = 2
        speed_y_1 = 2
        ok = True
        while ok:
            circle_positions[3][2] -= speed_y_1
            lines_positions[3][1] -= speed_y_1
            lines_positions[4][1] -= speed_y_1
            lines_positions[2][3] -= speed_y_1

            circle_positions[4][2] -= speed_y_1
            circle_positions[5][2] -= speed_y_1
            circle_positions[6][2] -= speed_y_1

            lines_positions[3][3] -= speed_y_1

            lines_positions[4][3] -= speed_y_1

            lines_positions[5][1] -= speed_y_1
            lines_positions[5][3] -= speed_y_1

            if circle_positions[3][2] <= 300:
                lines_positions[4][0] = circle_positions[2][1] + 35
                lines_positions[4][1] = circle_positions[2][2] + 35

                lines_positions[1][2] = circle_positions[3][1] + 35
                lines_positions[1][3] = circle_positions[3][2] - 35

                lines_positions[2][1] -= 70

                lines_positions[4][2] -= 70

                break

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        speed_x_2 = 2
        speed_y_2 = 4

        while ok:
            circle_positions[2][1] -= speed_x_2
            circle_positions[7][1] -= speed_x_2
            circle_positions[8][1] -= speed_x_2

            lines_positions[6][0] -= speed_x_1
            lines_positions[6][2] -= speed_x_1

            lines_positions[7][0] -= speed_x_1
            lines_positions[7][2] -= speed_x_1

            lines_positions[2][0] -= speed_x_1
            lines_positions[4][0] -= speed_x_2

            if circle_positions[2][1] == 450:
                speed_x_2 = 0

            circle_positions[2][2] += speed_y_2
            circle_positions[5][2] += speed_y_2
            circle_positions[6][2] += speed_y_2
            circle_positions[7][2] += speed_y_2
            circle_positions[8][2] += speed_y_2

            lines_positions[4][1] += speed_y_2
            lines_positions[5][1] += speed_y_2
            lines_positions[6][1] += speed_y_2
            lines_positions[7][1] += speed_y_2
            lines_positions[4][3] += speed_y_2
            lines_positions[5][3] += speed_y_2
            lines_positions[6][3] += speed_y_2
            lines_positions[7][3] += speed_y_2
            lines_positions[2][1] += speed_y_2

            if circle_positions[2][2] > 500:
                speed_y_2 = 0

            if speed_y_2 == 0 and speed_x_2 == 0:
                lines_positions[2][3] += 70
                break
            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        speed_x_3 = 4

        while ok:
            circle_positions[3][1] -= speed_x_3
            circle_positions[4][1] -= speed_x_3

            lines_positions[3][0] -= speed_x_3
            lines_positions[3][2] -= speed_x_3

            lines_positions[2][2] -= speed_x_3

            lines_positions[1][2] -= speed_x_3

            if circle_positions[3][1] == 600:
                break
            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        return


def small_right_rotate(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        speed_1 = 4
        while True:
            for pos in circle_positions:
                pos[1] += speed_1

            for line in lines_positions:
                line[0] += speed_1
                line[2] += speed_1

            if circle_positions[0][1] == 900:
                break
            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        while True:
            if circle_positions[2][1] == 450:
                break
            circle_positions[2][1] -= speed_1
            circle_positions[5][1] -= speed_1
            circle_positions[6][1] -= speed_1
            circle_positions[7][1] -= speed_1
            circle_positions[8][1] -= speed_1

            lines_positions[4][0] -= speed_1
            lines_positions[5][0] -= speed_1
            lines_positions[6][0] -= speed_1
            lines_positions[7][0] -= speed_1
            lines_positions[4][2] -= speed_1
            lines_positions[5][2] -= speed_1
            lines_positions[6][2] -= speed_1
            lines_positions[7][2] -= speed_1
            lines_positions[2][0] -= speed_1

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        while True:

            circle_positions[0][2] += speed_1
            circle_positions[1][2] += speed_1

            lines_positions[0][1] += speed_1
            lines_positions[0][3] += speed_1

            lines_positions[1][1] += speed_1

            if circle_positions[0][2] == 300:
                lines_positions[1][1] -= 70
                lines_positions[1][3] += 70
                lines_positions[3][0] = circle_positions[0][1] - 35
                lines_positions[3][1] = circle_positions[0][2] + 35
                lines_positions[3][2] += 70
                break

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        speed_x_1 = 3
        speed_y_1 = 4
        while True:
            circle_positions[4][1] -= speed_x_1
            lines_positions[3][2] -= speed_x_1

            circle_positions[0][2] += speed_y_1
            circle_positions[1][2] += speed_y_1
            circle_positions[4][2] += speed_y_1

            lines_positions[0][1] += speed_y_1
            lines_positions[0][3] += speed_y_1

            lines_positions[3][1] += speed_y_1
            lines_positions[3][3] += speed_y_1

            lines_positions[1][1] += speed_y_1

            if circle_positions[0][2] == 500:
                break

            screen.fill(WHITE)

            draw_circle_positions(screen)
            draw_lines(screen)

            pygame.display.flip()
            clock.tick(60)

        speed_3 = 4
        while True:
            for pos in circle_positions:
                pos[2] -= speed_3

            for line in lines_positions:
                line[1] -= speed_3
                line[3] -= speed_3

            if circle_positions[0][2] == 300:
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


def big_right_rotate():
    screen = init()
    clock = pygame.time.Clock()
    # play_sound()
    draw_first(screen, clock)
    draw_second(screen, clock)
    draw_third(screen, clock)
    draw_fourth(screen, clock)
    draw_fifth(screen, clock)
    draw_sixth(screen, clock)
    draw_seventh(screen, clock)
    draw_eighth(screen, clock)
    draw_ninth(screen, clock)
    wait(screen, clock)
    small_left_rotate(screen, clock)
    small_right_rotate(screen, clock)
    wait(screen, clock)
    pygame.quit()


if __name__ == "__main__":
    big_right_rotate()