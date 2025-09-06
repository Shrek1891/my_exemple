import random
import pygame
import sys
from units import AngryDad, Catcher, Phone, Board

angry_dad_coordinates = {
    'up': (200, 0),
    'middle': (480, 170),
    'down': (900, 290),
}

angry_dad_coordinates_kick = {
    'up': (210, -35),
    'middle': (490, 135),
    'down': (910, 255),
}

black = (0, 0, 0)
white = (255, 255, 255)
darkness_color = (0, 0, 0, 128)

screen_width = 1200
screen_height = 800

menu_objects = []
button_width = 100
button_height = 50
button_x = screen_width // 2 - 50
button_y = screen_height // 2 + 150

play_button = {
    'rect': pygame.Rect(button_x, button_y, button_width, button_height),
    'text': 'Play',
    'text_color': white,
    'color': black,
    'action': 'play'
}

exit_button = {
    'rect': pygame.Rect(button_x, button_y + 100, button_width, button_height),
    'text': 'Exit',
    'text_color': white,
    'color': black,
    'action': 'exit'
}

menu_objects.append(play_button)
menu_objects.append(exit_button)

pygame.init()
pygame.mixer.music.load('music/pixel-love.ogg')

screen = pygame.display.set_mode((screen_width, screen_height))
bg = pygame.image.load('img/bg-2.jpg')
bg = pygame.transform.scale(bg, (screen_width + 40, screen_height + 160))
bg = bg.convert_alpha()
dad = AngryDad()
catcher = Catcher()
mobile_phone = Phone()
board = Board()
clock = pygame.time.Clock()
start = True
isRow = True
is_game_running = True
time = 1
direction = 1
angle = 2
"""angle,speed"""
time_speed = [(1, 2), (2, 4), (3, 6)] #3 times
game_difficulty = 0

angry_dad_coordinate = random.choice(list(angry_dad_coordinates_kick.keys()))

while start:

    if angry_dad_coordinate == 'up':
        direction = 1
    if angry_dad_coordinate == 'down':
        direction = -1

    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    board.draw_text(screen, 'Score: ' + str(catcher.scored), 20, 100, 10, white)
    if is_game_running:
        pygame.mixer.music.play(-1)
        s = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        s.fill(darkness_color)
        screen.blit(s, (0, 0))
        board.draw_text(screen, 'ANGRY DAD', 100, 600, 400, white)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for obj in menu_objects:
                if obj['rect'].collidepoint(mouse_pos):
                    if obj['action'] == 'play':
                        is_game_running = False
                    if obj['action'] == 'exit':
                        start = False
        for obj in menu_objects:
            board.draw_button(screen, obj['color'], obj['rect'].x, obj['rect'].y, obj['rect'].w, obj['rect'].h,
                              obj['text'], obj['text_color'])
    else:
        if dad.isRow:
            dad.angry_row(screen, angry_dad_coordinates[angry_dad_coordinate], 3)
            catcher.scared(screen)
        else:
            catcher.draw_catcher(screen)
            if dad.is_kick_animation:
                if direction == -1:
                    dad.left_kick(screen, angry_dad_coordinates_kick[angry_dad_coordinate])
                    mobile_phone.coordinates = {
                        'x': angry_dad_coordinates[angry_dad_coordinate][0],
                        'y': angry_dad_coordinates[angry_dad_coordinate][1] + 100
                    }
                else:
                    dad.right_kick(screen, angry_dad_coordinates_kick[angry_dad_coordinate])
                    mobile_phone.coordinates = {
                        'x': angry_dad_coordinates[angry_dad_coordinate][0] + 200,
                        'y': angry_dad_coordinates[angry_dad_coordinate][1] + 100
                    }
            else:
                dad.draw_dad(screen, angry_dad_coordinates_kick[angry_dad_coordinate])
                if dad.is_kick:
                    mobile_phone.draw_phone(screen)
                    if time % time_speed[angle][1] - game_difficulty == 0:
                        mobile_phone.projectile_motion(20, time_speed[angle][0], direction, g=9.81)
                    time += 1
                    if mobile_phone.coordinates['y'] > catcher.coordinates['y'] + 100 and catcher.coordinates['x'] < \
                            mobile_phone.coordinates['x'] < catcher.coordinates['x'] + 100:
                        catcher.scored += 1
                        if catcher.scored % 10 == 0:
                            time_speed=[(1, 1), (2, 2), (3, 3)]
                            dad.isRow = True
                        direction = random.choice([-1, 1])
                        angle = random.choice([0, 1, 2])
                        dad.is_kick_animation = True
                        angry_dad_coordinate = random.choice(list(angry_dad_coordinates.keys()))

                    if mobile_phone.coordinates['y'] > 700:
                        dad.isRow = True
                        mobile_phone.coordinates = {
                            'x': angry_dad_coordinates[angry_dad_coordinate][0],
                            'y': angry_dad_coordinates[angry_dad_coordinate][1]
                        }
                        dad.is_kick_animation = True
                        catcher.scored = 0
                        screen.blit(s, (0, 0))
                        board.draw_text(screen, 'YOU LOSE', 100, 600, 400, white)
                        pygame.display.flip()
                        is_key_pressed = True
                        while is_key_pressed:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    is_key_pressed = False
                        is_game_running = True
            catcher.update(screen)

    pygame.display.flip()
