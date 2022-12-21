import os.path
import pprint
import sys
from PIL import Image

import pygame

FPS = 50
pygame.init()
pygame.display.set_caption("Перемещение героя. Новый уровень")
screen = pygame.display.set_mode((550, 550))
WIDTH, HEIGHT = 500, 500
clock = pygame.time.Clock()

pos1 = [-1, -1]



# LEVEL = "...###....." \
#         "..##.#.####" \
#         ".##..###..#" \
#         "##........#" \
#         "#...@..#..#" \
#         "###..###..#" \
#         "..#..#....#" \
#         ".##.##.#.##" \
#         ".#......##." \
#         ".#.....##.." \
#         ".#######..."


def terminate():
    pygame.quit()
    sys.exit()


def load_image(filename: str, colorkey=None):
    fullname = os.path.join('Data/' + filename)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


pprint.pprint(level := load_level('level.txt'))

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

player_image = load_image("player.png")
tile_width = tile_height = 50

player = None


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super(Tile, self).__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super(Player, self).__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos = [pos_x, pos_y]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move_player(self, coords):
        if level[(self.pos[1] + coords[1]) % level.__len__()][(self.pos[0] + coords[0]) % level[0].__len__()] != '#':
            self.rect = self.rect.move(coords[0] * 50, coords[1] * 50)
            self.pos[0] += coords[0]
            self.pos[1] += coords[1]


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
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


player, level_x, level_y = generate_level(load_level('level.txt'))


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Пампампам",
                  "НЕДО SOUL KNIGHT"]

    fon = pygame.transform.scale(pygame.image.load('Data/img.png'), (550, 550))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def start_game():
    running = True
    camera = Camera()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.move_player((0, -1))
                if event.key == pygame.K_d:
                    player.move_player((1, 0))
                if event.key == pygame.K_a:
                    player.move_player((-1, 0))
                if event.key == pygame.K_s:
                    player.move_player((0, 1))

        screen.fill((255, 255, 255))

        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        camera.update(player)
        #обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.x %= 500
        obj.rect.y += self.dy
        obj.rect.y %= 500

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()
start_game()
