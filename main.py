import pygame
import os

pygame.init()
MONITOR_width, MONITOR_height = 500, 500
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


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                player_x, player_y = x, y
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, player_x, player_y


player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
fon = pygame.transform.scale(load_image('fon.jpg'), (MONITOR_width, MONITOR_height))
screen.blit(fon, (0, 0))
fps = 60
clock = pygame.time.Clock()
running = True
card = load_level('level.txt')
player, level_x, level_y, player_x, player_y = generate_level(card)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_DOWN:
                player_y += 1
                if player_y >= level_y:
                    player_y -= 1
                if card[player_x][player_y] == '#':
                    player_y -= 1
                print(player_x, player_y)
            elif event.key == pygame.K_UP:
                player_y -= 1
                if player_y >= level_y:
                    player_y += 1
                if card[player_x][player_y] == '#':
                    player_y += 1
                print(player_x, player_y, player)
            elif event.key == pygame.K_RIGHT:
                player_x += 1
                if player_x >= level_x:
                    player_x -= 1
                if card[player_x][player_y] == '#':
                    player_x -= 1
                print(player_x, player_y)
            elif event.key == pygame.K_LEFT:
                player_x -= 1
                if player_x >= level_x:
                    player_x += 1
                if card[player_x][player_y] == '#':
                    player_x += 1
                print(player_x, player_y, player)
            player.move(player_x, player_y)
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()