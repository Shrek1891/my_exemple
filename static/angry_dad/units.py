import pygame

angry_dad_coordinates_kick = {
    'up': (200, 0),
    'middle': (490, 135),
    'down': (900, 290),
}

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
dark_gray = (80, 80, 80)

speed_angry_dad = {  # change 3 times
    "t": 40*3,
    "f": 5 * 3,
}

kick_speed = {  # change 3 times
    "t": 40 * 3,
    "f": 8*3
}

scared_speed = {  # change 3 times
    "t": 40 * 3,
    "f": 8 * 3
}


class AngryDad(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        pygame.init()
        self.animation = []
        self.angry_dad = pygame.image.load('img/angry_boss/0-fotor-bg-remover.png')
        self.angry_dad = pygame.transform.scale(self.angry_dad, (200, 300))
        self.count = 0
        self.count_frame = 0
        self.isRow = True
        self.animation_set_angry_cry = [pygame.image.load((f'img/angry_boss/{i}-fotor-bg-remover.png')) for i in
                                        range(0, 11)]
        self.animation_set_kick_left = [pygame.image.load((f'img/kick/left/{i}-left.png')) for i in range(0, 6)]
        self.animation_set_kick_right = [pygame.image.load((f'img/kick/right/{i}-right.png')) for i in range(0, 6)]
        self.count_animation_left = 0
        self.count_animation_right = 0
        self.is_kick = True
        self.is_kick_animation = True

    def draw_dad(self, screen, coordinates):
        screen.blit(self.angry_dad, coordinates)

    def angry_row(self, screen, coordinates, times):
        self.angry_dad = pygame.transform.scale(self.animation_set_angry_cry[self.count // speed_angry_dad["f"]],
                                                (200, 300))
        screen.blit(self.angry_dad, coordinates)
        self.count += 1
        if self.count == speed_angry_dad["t"]:
            self.count = 0
            self.count_frame += 1
        if self.count_frame >= times:
            self.count_frame = 0
            self.isRow = False

    def left_kick(self, screen, coordinates):
        self.angry_dad = pygame.transform.scale(self.animation_set_kick_left[self.count_animation_left // kick_speed["f"]],
                                                (200, 300))
        screen.blit(self.angry_dad, coordinates)
        self.count_animation_left += 1
        if self.count_animation_left == kick_speed["t"]:
            self.count_animation_left = 0
            self.is_kick_animation = False

    def right_kick(self, screen, coordinates):
        self.angry_dad = pygame.transform.scale(self.animation_set_kick_right[self.count_animation_right // kick_speed["f"]],
                                                (200, 300))
        screen.blit(self.angry_dad, coordinates)
        self.count_animation_right += 1
        if self.count_animation_right == kick_speed["t"]:
            self.count_animation_right = 0
            self.is_kick_animation = False


class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.catcher = pygame.image.load('img/catch/catch_left/0-catch-left.png')
        self.catcher = pygame.transform.scale(self.catcher, (200, 300))
        self.coordinates = {
            'x': 600,
            'y': 500
        }
        self.direction = 'directly'
        self.count = 0
        self.scored = 0
        self.count_scared = 0
        self.count_frame = 0
        self.animation_set_turn_right = [pygame.image.load((f'img/catch/catch_right/{i}-catch-right.png')) for i in
                                         range(0, 9)]
        self.animation_set_turn_left = [pygame.image.load((f'img/catch/catch_left/{i}-catch-left.png')) for i in
                                        range(0, 9)]
        self.animation_set_sacred = [pygame.image.load((f'img/loss/{i}-fear.png')) for i in range(0, 9)]

    def draw_catcher(self, screen):
        screen.blit(self.catcher, (self.coordinates['x'], self.coordinates['y']))

    def go_left(self, screen):
        self.coordinates['x'] -= 2
        screen.blit(self.catcher, (self.coordinates['x'], self.coordinates['y']))
        if self.coordinates['x'] <= 0:
            self.coordinates['x'] = 0

    def go_right(self, screen):
        self.coordinates['x'] += 2
        screen.blit(self.catcher, (self.coordinates['x'], self.coordinates['y']))
        if self.coordinates['x'] >= 1000:
            self.coordinates['x'] = 1000

    def turn_right(self, screen, i=0):
        self.catcher = pygame.transform.scale(self.animation_set_turn_right[i], (200, 300))
        screen.blit(self.catcher, (self.coordinates['x'], self.coordinates['y']))

    def update(self, screen):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.direction == 'directly':
                self.animation_left(screen)
            if self.direction == 'left':
                self.go_left(screen)
            if self.direction == 'right':
                self.animation_left(screen, -1)
        if keys[pygame.K_RIGHT]:
            if self.direction == 'right':
                self.go_right(screen)
            if self.direction == 'directly':
                self.animation_right(screen)
            if self.direction == 'left':
                self.animation_right(screen, -1)

    def animation_right(self, screen, direction=1):
        self.catcher = pygame.transform.scale(self.animation_set_turn_right[self.count], (200, 300))
        screen.blit(self.catcher, (self.coordinates['x'], self.coordinates['y']))
        self.count += direction
        if self.count >= 8:
            self.direction = 'right'
            self.count = 0
        if self.count < 0:
            self.direction = 'directly'
            self.count = 0

    def animation_left(self, screen, direction=1):
        self.catcher = pygame.transform.scale(self.animation_set_turn_left[self.count], (200, 300))
        screen.blit(self.catcher, (self.coordinates['x'], self.coordinates['y']))
        self.count += direction
        if self.count >= 8:
            self.direction = 'left'
            self.count = 0
        if self.count < 0:
            self.direction = 'directly'
            self.count = 0

    def scared(self, screen):
        self.catcher = pygame.transform.scale(self.animation_set_sacred[self.count_scared // scared_speed["f"]], (200, 300))
        screen.blit(self.catcher, (self.coordinates['x'], self.coordinates['y']))
        self.count_scared += 1
        if self.count_scared >= scared_speed["t"]:
            self.count_scared = 0


class Phone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.phone = pygame.image.load('img/cell-phone.png')
        self.phone = pygame.transform.scale(self.phone, (20, 30))
        self.coordinates = {
            'x': angry_dad_coordinates_kick['middle'][0] + 200,
            'y': angry_dad_coordinates_kick['middle'][1] + 100
        }

    def draw_phone(self, screen):
        screen.blit(self.phone, (self.coordinates['x'], self.coordinates['y']))

    def projectile_motion(self, v0, angle, speed, g=9.81):
        self.coordinates['x'] = self.coordinates['x'] + speed
        self.coordinates['y'] = int(self.coordinates['y'] + angle)


class Board(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def draw_text(self, screen, text, size, x, y, color):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

    def draw_button(self, screen, color, x, y, width, height, text, text_color):
        self.draw_text(screen, text, 20, x + width / 2, y + height / 2 - 10, text_color)
