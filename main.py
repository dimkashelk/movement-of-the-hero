import pygame
import os
from copy import deepcopy

pygame.init()
MONITOR_width, MONITOR_height = 600, 600
size = (MONITOR_width, MONITOR_height)
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mario.png')
tile_width = tile_height = 50
width = height = 200


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, pos_x, pos_y):
        dop = self.image.get_rect()
        dop[0] = pos_x * tile_width + 15
        dop[1] = pos_y * tile_height + 5
        self.rect = dop


def generate_level(level, pr=True):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            if level[y][x] == '#':
                Tile('wall', x, y)
            if pr and level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            else:
                Tile('empty', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
fon = pygame.transform.scale(load_image('fon.jpg'), (MONITOR_width, MONITOR_height))
screen.blit(fon, (0, 0))
fps = 60
clock = pygame.time.Clock()
running = True
try:
    card = load_level(input())
except FileNotFoundError:
    print('File not found!')
    exit(0)
camera = Camera()
player, level_x, level_y = generate_level(card)
camera.update(player)
x, y = 90, 90
for sprite in all_sprites:
    camera.apply(sprite)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_DOWN:
                player.rect.y += 10
                y += 10
                if y >= height - height // 4:
                    dop = deepcopy(card[0])
                    del card[0]
                    card.append(dop)
                    y -= 100
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(player)
                    tiles_group = pygame.sprite.Group()
                    generate_level(card, pr=False)
            elif event.key == pygame.K_UP:
                player.rect.y -= 10
                y -= 10
                if y <= height // 4:
                    dop = deepcopy(card[-1])
                    del card[-1]
                    card.insert(0, dop)
                    y += 100
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(player)
                    tiles_group = pygame.sprite.Group()
                    generate_level(card, pr=False)
            elif event.key == pygame.K_RIGHT:
                player.rect.x += 10
                x += 10
                if x >= width - width // 4:
                    for i, value in enumerate(card):
                        card[i] = value[1:] + value[0]
                    x -= 100
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(player)
                    tiles_group = pygame.sprite.Group()
                    generate_level(card, pr=False)
            elif event.key == pygame.K_LEFT:
                player.rect.x -= 10
                x -= 10
                if x <= width // 4:
                    for i, value in enumerate(card):
                        card[i] = value[-1] + value[:-1]
                    x -= 100
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(player)
                    tiles_group = pygame.sprite.Group()
                    generate_level(card, pr=False)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
