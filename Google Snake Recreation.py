import time
import sys
from PIL import Image, ImageFilter
import random
import pygame

pygame.init()


def draw_circle(color, coordinates):
    pygame.draw.circle(screen, color, (border_w + checker_size / 2 + checker_size * coordinates[1],
                                       bar_h + border_h + checker_size / 2 + checker_size * coordinates[0]),
                       snake_w / 2)


def draw_rect(a, b):
    try:
        if current_direction([a] + [b]) == 'right' or current_direction([a] + [b]) == 'left':
            pygame.draw.rect(screen, snake_color, (int(border_w + min([a[1]] + [b[1]]) * checker_size + checker_size / 2),
                                                   int(border_h + bar_h + min(
                                                       [a[0]] + [b[0]]) * checker_size + checker_size / 2 - snake_w / 2),
                                                   int(abs(a[1] - b[1]) * checker_size), int(snake_w)))
        else:
            pygame.draw.rect(screen, snake_color,
                             (int(border_w + min([a[1]] + [b[1]]) * checker_size + checker_size / 2 - snake_w / 2),
                              int(border_h + bar_h + min([a[0]] + [b[0]]) * checker_size + checker_size / 2), int(snake_w),
                              int(abs(a[0] - b[0]) * checker_size)))
    except:
        pass


def draw_snake():
    turns_and_ends = [[last_tail_pos[0] + (snake[0][0] - last_tail_pos[0]) * (time_after_last_move / delay), last_tail_pos[1] + (snake[0][1] - last_tail_pos[1]) * (time_after_last_move / delay)]] + [snake[0]] + find_turns() + [[snake[-2][0] + (snake[-1][0] - snake[-2][0]) * (time_after_last_move / delay), snake[-2][1] + (snake[-1][1] - snake[-2][1]) * (time_after_last_move / delay)]]

    for i in range(len(turns_and_ends) - 1):
        point_a = turns_and_ends[i]
        point_b = turns_and_ends[i + 1]
        draw_rect(point_a, point_b)

    for part in turns_and_ends:
        draw_circle(snake_color, part)

    draw_circle((222, 80, 80), apple_pos)

    pygame.display.update()


def find_turns():
    turns = []
    for i in range(len(snake) - 2):
        section = snake[i:i + 3]
        if current_direction(section[:-1]) != current_direction(section[1:]):
            turns.append(section[1])
    return turns


def new_apple_pos():
    apple = [random.randint(0, h - 1), random.randint(0, w - 1)]
    while apple in snake:
        apple = [random.randint(0, h - 1), random.randint(0, w - 1)]
    return apple


def current_direction(lst):
    head = lst[-1]
    second = lst[-2]
    y_difference = head[0] - second[0]
    x_difference = head[1] - second[1]
    if y_difference > 0:
        return 'down'
    elif y_difference < 0:
        return 'up'
    elif x_difference > 0:
        return 'right'
    elif x_difference < 0:
        return 'left'
    else:
        return 'Error'


def backwards_or_straight(maybe):
    direction = current_direction(snake)
    if maybe in ['up', 'down'] and direction in ['up', 'down'] or maybe in ['left', 'right'] and direction in ['left',
                                                                                                               'right']:
        return True


def set_direction_and_x_button():
    global head_direction
    global running
    global x_color

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.name(event.key)
            if pressed in list('wasd'):
                temp = ['up', 'left', 'down', 'right'][list('wasd').index(pressed)]
                if not backwards_or_straight(temp):
                    head_direction = temp
            elif pressed in ['up', 'left', 'down', 'right']:
                temp = pressed
                if not backwards_or_straight(temp):
                    head_direction = temp

        if x_button_x <= mouse[0] <= x_button_x + x_button_w and x_button_y <= mouse[1] <= x_button_y + x_button_h:
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                pygame.quit()
                sys.exit()

            x_color = (200, 200, 200)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        else:
            x_color = (255, 255, 255)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    screen.blit(x_font.render('×', True, x_color), (x_button_x, x_button_y - x_size / 4))
    pygame.display.update()


def draw_board():
    pygame.draw.rect(screen, bar_color, (0, 0, checker_size * (checker_board_w + 2), bar_h))

    pygame.draw.rect(screen, light_checker,
                     (border_w, border_h + bar_h, checker_size * checker_board_w, checker_size * checker_board_h))
    for a in range(checker_board_w):
        for b in range(checker_board_h):
            if a % 2 == 0 and b % 2 == 1 or a % 2 == 1 and b % 2 == 0:
                pygame.draw.rect(screen, dark_checker, (
                border_w + a * checker_size, border_h + bar_h + b * checker_size, checker_size, checker_size))


def new_head_pos():
    head = snake[-1].copy()
    if head_direction == 'up':
        head[0] -= 1
    elif head_direction == 'left':
        head[1] -= 1
    elif head_direction == 'down':
        head[0] += 1
    else:
        head[1] += 1
    return head


if __name__ == "__main__":
    h = 16
    w = 17
    snake = [[2, 1], [2, 2], [2, 3]]
    head_direction = 'right'
    tail_direction = 'up'
    head_pos = snake[-1]

    apple_pos = new_apple_pos()

    snake_color = (78, 124, 246)
    bar_color = (74, 117, 44)
    light_checker = (170, 215, 81)
    dark_checker = (162, 209, 73)
    checker_size = 40
    checker_board_w = 17
    checker_board_h = 16
    checker_board_x = 200
    checker_board_y = 200
    bar_h = int(checker_size * 2.3)
    border_h = int(checker_size * (8 / 10))
    border_w = int(checker_size * (9 / 10))
    snake_w = checker_size * 0.7

    screen = pygame.display.set_mode(
        (checker_size * checker_board_w + border_w * 2, bar_h + checker_size * checker_board_h + border_h * 2),
        pygame.NOFRAME)
    pygame.display.set_caption("Snake")
    bg_color = (87, 138, 52)
    screen.fill(bg_color)

    x_color = (255, 255, 255)
    x_size = int(checker_size * 13 / 7)
    x_font = pygame.font.SysFont('Corbel', x_size)
    x_button_w, x_button_h = [x_size / 2] * 2
    x_button_y = (bar_h - x_button_h) // 2
    x_button_x = checker_size * checker_board_w + border_w * 2 - x_button_w - (bar_h - x_button_w) // 2

    delay = 0.1

    time_after_last_move = time.time() % delay
    additional_time = delay * time.time() // delay

    last_tail_pos = [2, 0]

    clock = pygame.time.Clock()
    running = True
    while running:
        draw_board()
        draw_snake()
        set_direction_and_x_button()
        pygame.display.update()

        time_after_last_move = time.time() - additional_time

        new_head = new_head_pos()

        if time_after_last_move >= delay:
            additional_time = delay * (time.time() // delay)
            time_after_last_move = time.time() - additional_time

            if (0 <= new_head[0] <= h - 1 and 0 <= new_head[1] <= w - 1) and (new_head not in snake[1:]):
                snake.append(new_head)
                head_pos = snake[-1]
                if not apple_pos == new_head:
                    last_tail_pos = snake[0]
                    del snake[0]
                else:
                    apple_pos = new_apple_pos()
            else:
                pil_string_image = pygame.image.tostring(screen, "RGBA", False)
                pil_image = Image.frombytes("RGBA", (
                checker_size * checker_board_w + border_w * 2, bar_h + checker_size * checker_board_h + border_h * 2),
                                            pil_string_image)
                image = pil_image.filter(ImageFilter.BoxBlur(2))
                mode = image.mode
                size = image.size
                data = image.tobytes()
                py_image = pygame.image.fromstring(data, size, mode)
                rect = screen.get_rect()
                screen.blit(py_image, rect)

                pygame.display.update()
                time.sleep(0.1)

                end_box_w = 10
                end_box_h = 6
                pygame.draw.rect(screen, bg_color, pygame.Rect((w / 2 - end_box_w / 2) * checker_size + border_w, (
                            h / 2 - end_box_h / 2) * checker_size + border_w + bar_h * 2 / 3, end_box_w * checker_size,
                                                               end_box_h * checker_size), checker_size * 5,
                                 int(checker_size * 1.5))

                score_font = pygame.font.SysFont('segoeuisemibold', int(checker_size * 5 / 4))
                score = score_font.render("Score: " + str(len(snake) - 3), True, (240, 240, 240))
                score_rect = score.get_rect(
                    center=((checker_size * checker_board_w + border_w * 2) / 2, checker_size * 9))
                screen.blit(score, score_rect)

                play_again_font = pygame.font.SysFont('segoeuisemibold', int(checker_size))

                press_enter_to_text = play_again_font.render("Press enter", True, (240, 240, 240))
                play_again_text = play_again_font.render("to play again", True, (240, 240, 240))

                press_enter_to_text_rect = press_enter_to_text.get_rect(
                    center=((checker_size * checker_board_w + border_w * 2) / 2, checker_size * 10.5))
                play_again_text_rect = play_again_text.get_rect(
                    center=((checker_size * checker_board_w + border_w * 2) / 2, checker_size * 11.5))

                screen.blit(press_enter_to_text, press_enter_to_text_rect)
                screen.blit(play_again_text, play_again_text_rect)

                pygame.display.update()

                not_restart = True
                while not_restart:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                snake = [[2, 1], [2, 2], [2, 3]]
                                head_direction = 'right'
                                tail_direction = 'up'
                                head_pos = snake[-1]

                                apple_pos = new_apple_pos()

                                screen.fill(bg_color)
                                time.sleep(0.25)

                                not_restart = False

                            if event.key == pygame.K_ESCAPE:
                                exit()
        clock.tick(60)
