import sys
import pygame
import Config

pygame.init()
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 480
        self.TILE_SIZE = 64
        self.GRAVITY = 1
        self.JUMP_STRENGTH = 25
        self.scroll = 0
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Game")
        self.init_sounds()
        self.levels = self.create_levels()
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.player = Player(self)
        self.background_game = pygame.image.load(r'image\sky.png')
        self.background_game_cloud = pygame.image.load(r'image\cloud.png')
        self.bg_width = self.background_game_cloud.get_width()
        self.grass = pygame.image.load(r'image\grass.png')
        self.door = pygame.image.load(r'image\MainDoor.png')
        self.bush_side = pygame.image.load(r'image\bush_side.png')
        self.bush_side_r = pygame.image.load(r'image\bush_side_r.png')
        self.bush = pygame.image.load(r'image\bush.png')
        self.castle_wall = pygame.image.load(r'image\wall_castle.png')
        self.fence = pygame.image.load(r'image\fence.png')
        self.dirt = pygame.image.load(r'image\dirt.png')
        self.dirt2 = pygame.image.load(r'image\dirt_2.png')
        self.grass_left = pygame.image.load(r'image/grass_left.png')
        self.grass_right = pygame.image.load(r'image/grass_right.png')
        self.dirt_ins = pygame.image.load(r'image\dirt-ins.png')
        self.bridge = pygame.image.load(r'image\bridge.png')
        self.bush_forest = pygame.image.load(r'image\brush_forest.png')
        self.wood = pygame.image.load(r'image\wood.png')


        self.enemies = [Enemy(self, 1300, 640), Enemy(self, 1600, 450), Enemy(self, 2500, 640), Enemy(self, 5600, 640), Enemy(self, 5900, 640), Enemy(self, 6500, 640)]

        self.coin_sheet = pygame.image.load(r'image\red_crystal.png')
        self.coins = []
        self.coin_counter = 0

        pygame.mixer.music.load(r'Soundtrack\Yuka Kitamura - Firelink Shrine.mp3')
        pygame.mixer.music.set_volume(0.5)

    def init_sounds(self):
        self.step_sounds = [
            pygame.mixer.Sound(r'Soundtrack\blizkiy-odinarnyiy-chtkiy-shag-po-staromu-polu.mp3'),
            pygame.mixer.Sound(r'Soundtrack\nespeshnyiy-shag-po-osennemu-lesu.mp3')
        ]
        self.jump_sound = pygame.mixer.Sound(r'Soundtrack\6ef264c09005b61.mp3')
        self.land_sound = pygame.mixer.Sound(r'Soundtrack\gluhoe-padenie-v-pesok.mp3')
        self.open_door = pygame.mixer.Sound(r'Soundtrack\mixkit-old-church-door-open-193.wav')
        self.coin_pickup_sound = pygame.mixer.Sound(r'Soundtrack\coin.mp3')


    def create_levels(self):
        return [
            {
                "base": [
                    ".......C...................................................................................................................................................................C.....",
                    ".......C...................................................................................................................................................................C.....",
                    ".......C...................................................................................................................................................................C.....",
                    ".......C...................................................................................................................................................................C.....",
                    ".......C.............................................MMMM.....MMMM.................................M.MEM...................................................................C.....",
                    ".......C......................................S.....qGGGGw...qGGGGw....S..........S................qGGGGw..................................................................C.....",
                    ".......C...................................................................................................................................................................C.....",
                    ".......C................MMEMM.....................M.M.M.MEM.M.M.M.MEM.M.........E..............M.M......M.M.M..............................................................C.....",
                    ".......C...S...........qGGGGGw.......S......GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG.....S....qGGGGw....qGGGGw..S...........................................S..........S...C.....",
                    ".......C....................................iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiGG.....................................................................................C.....",
                    ".......C........MEM.M.M.M.........E......GGGiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii..........EM.M.M.M.M..........E........................................E.......E.....C.....",
                    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGQQQQQQQQQQQQQQQQQQQQQQQQQQQQGGGGGGGGGGGGGGGGGGGGGGGGGG",
                    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD............................DDDDDDDDDDDDDDDDDDDDDDDDDD",
                    "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII............................IIIIIIIIIIIIIIIIIIIIIIIIII"
                ],
                "overlay": [
                    "................................",
                    "................................",
                    "................................",
                    "................................",
                    "................................",
                    "................................",
                    "................................",
                    "................................",
                    "................................",
                    "................................",
                    "................................"
                ]
            }
        ]

    def load_level(self, index):
        self.current_level = self.levels[index]
        self.player.x, self.player.y = 100, 200
        self.player.velocity_y = 0

    def draw_map(self, screen, level, offset_x, offset_y):
        for y, row in enumerate(level["base"]):
            for x, col in enumerate(row):
                if col == "M":
                    screen.blit(self.coin_sheet, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "G":
                    screen.blit(self.grass, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "B":
                    screen.blit(self.bush, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "b":
                    screen.blit(self.bush_side, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "W":
                    screen.blit(self.castle_wall, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "D":
                    screen.blit(self.dirt, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "I":
                    screen.blit(self.dirt2, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "q":
                    screen.blit(self.grass_left, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "w":
                    screen.blit(self.grass_right, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "i":
                    screen.blit(self.dirt_ins, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "C":
                    transparent_surface = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE), pygame.SRCALPHA)
                    transparent_surface.fill((0, 0, 0, 0))
                    screen.blit(transparent_surface, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "Q":
                    screen.blit(self.bridge, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "E":
                    screen.blit(self.bush_forest, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "S":
                    screen.blit(self.wood, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))


        for y, row in enumerate(level["overlay"]):
            for x, col in enumerate(row):
                if col == "N":
                    screen.blit(self.door, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "n":
                    transparent_surface = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE), pygame.SRCALPHA)
                    transparent_surface.fill((0, 0, 0, 0))
                    screen.blit(transparent_surface, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))
                if col == "F":
                    screen.blit(self.fence, (x * self.TILE_SIZE - offset_x, y * self.TILE_SIZE - offset_y))

    def check_collision(self, player_rect, level):
        collisions = []
        for y, row in enumerate(level["base"]):
            for x, col in enumerate(row):
                if col in "GDIqwiCQ":
                    tile_rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                    if player_rect.colliderect(tile_rect):
                        collisions.append(tile_rect)
        return collisions
    def check_near_special_block(self, player_rect, level):
        for y, row in enumerate(level["overlay"]):
            for x, col in enumerate(row):
                if col == "N" or col == "n":
                    tile_rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                    if player_rect.colliderect(tile_rect):
                        return True
        return False

    def check_coin_collision(self, player_rect, level):
        collected_coins = []
        for y, row in enumerate(level["base"]):
            for x, col in enumerate(row):
                if col == "M":
                    tile_rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                    if player_rect.colliderect(tile_rect):
                        collected_coins.append((x, y))
        return collected_coins

    def run(self):
        running = True
        pygame.mixer.music.play(-1)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.player.update(keys)

            for enemy in self.enemies:
                enemy.update()

            self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]

            offset_x = self.player.x - self.SCREEN_WIDTH // 2
            offset_y = self.player.y - self.SCREEN_HEIGHT // 2

            self.screen.blit(self.background_game, (0, 0))
            self.screen.blit(self.background_game_cloud, (self.scroll, 0))
            self.screen.blit(self.background_game_cloud, (self.scroll + self.bg_width, 0))
            self.scroll -= 1
            if abs(self.scroll) > self.bg_width:
                self.scroll = 0

            self.draw_map(self.screen, self.current_level, offset_x, offset_y)

            for enemy in self.enemies:
                self.screen.blit(enemy.image, (enemy.rect.x - offset_x, enemy.rect.y - offset_y))


            self.screen.blit(self.player.image, (self.player.x - offset_x, self.player.y - offset_y))

            font = pygame.font.SysFont('Arial', 25)
            coin_text = font.render(f'Coins: {self.coin_counter}', True, (255, 255, 255))
            self.screen.blit(coin_text, (10, 10))
            self.player.draw_health_bar(self.screen)

            pygame.display.flip()
            pygame.time.Clock().tick(60)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        super().__init__()
        self.image = pygame.image.load(r'image\Spider_walk.png')
        self.rect = self.image.get_rect()
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.attack_radius = 100
        self.attack_damage = 10
        self.health = 50
        self.attack_timer = 0
        self.attack_interval = 1000


    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

        current_time = pygame.time.get_ticks()
        if current_time - self.attack_timer > self.attack_interval:
            if self.attack_player():
                self.game.player.health -= self.attack_damage
                if self.game.player.health <= 0:
                    self.game.player.health = 0
            self.attack_timer = current_time


        if self.health <= 0:
            self.kill()

    def attack_player(self):
        player_rect = pygame.Rect(self.game.player.x, self.game.player.y, self.game.player.width, self.game.player.height)
        if self.rect.colliderect(player_rect.inflate(self.attack_radius, self.attack_radius)):
            return True
        return False

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.image = pygame.image.load(r'image\Player_walk1.png')
        self.rect = self.image.get_rect()
        self.game = game
        self.x = 1000
        self.y = 500
        self.width = self.game.TILE_SIZE
        self.height = self.game.TILE_SIZE +45
        self.velocity_y = 0
        self.on_ground = False
        self.step_timer = 0
        self.step_interval = 400
        self.moving = False
        self.jumping = False
        self.jumping_started = False
        self.landing_sound_played = False
        self.step_sound_played = False
        self.health = 100
        self.attack_radius = 50
        self.attack_damage = 25
        self.walking_frame = 0
        self.attack_started = False

    def update(self, keys):
        next_x, next_y = self.x, self.y

        if keys[pygame.K_a]:
            next_x -= 10
            self.moving = True
        elif keys[pygame.K_d]:
            next_x += 10
            self.moving = True
        else:
            self.moving = False
            self.step_sound_played = False

        if keys[pygame.K_SPACE] and self.on_ground and not self.jumping_started:
            self.velocity_y = -self.game.JUMP_STRENGTH
            self.on_ground = False
            self.jumping = True
            self.jumping_started = True
            self.game.jump_sound.play()

        if pygame.mouse.get_pressed()[0]:
            self.attack()

        self.velocity_y += self.game.GRAVITY
        next_y += self.velocity_y

        player_rect = pygame.Rect(self.x, next_y, self.width, self.height)
        collisions = self.game.check_collision(player_rect, self.game.current_level)

        self.on_ground = False
        for tile in collisions:
            if self.velocity_y > 0 and player_rect.bottom > tile.top:
                next_y = tile.top - self.height
                self.velocity_y = 0
                self.on_ground = True
                self.jumping = False
                self.jumping_started = False
                if not self.landing_sound_played:
                    self.game.land_sound.play()
                    self.landing_sound_played = True
            elif self.velocity_y < 0:
                next_y = tile.bottom
                self.velocity_y = 0

        player_rect = pygame.Rect(next_x, self.y, self.width, self.height)
        collisions = self.game.check_collision(player_rect, self.game.current_level)

        collected_coins = self.game.check_coin_collision(player_rect, self.game.current_level)
        for x, y in collected_coins:
            self.game.current_level["base"][y] = self.game.current_level["base"][y][:x] + '.' + self.game.current_level["base"][y][x + 1:]
            self.game.coin_counter += 1
            self.game.coin_pickup_sound.play()

        for tile in collisions:
            if next_x > self.x:
                next_x = tile.left - self.width
            elif next_x < self.x:
                next_x = tile.right

        self.x, self.y = next_x, next_y

        if self.on_ground and self.moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.step_timer > self.step_interval:
                self.game.step_sounds[0].play()
                self.step_timer = current_time

        if not self.on_ground:
            self.landing_sound_played = False

        if self.game.check_near_special_block(player_rect, self.game.current_level) and keys[pygame.K_e]:
            self.game.open_door.play()
            self.game.current_level_index = (self.game.current_level_index + 1) % len(self.game.levels)
            self.game.load_level(self.game.current_level_index)



    def attack(self):
        for enemy in self.game.enemies:
            enemy_rect = pygame.Rect(enemy.rect.x, enemy.rect.y, enemy.image.get_width(), enemy.image.get_height())
            if pygame.Rect(self.x - self.attack_radius, self.y - self.attack_radius, self.attack_radius * 2, self.attack_radius * 2).colliderect(enemy_rect): enemy.take_damage(self.attack_damage)

    def draw_health_bar(self, screen):
        health_bar_width = 200
        health_bar_height = 20

        health_percentage = self.health / 100
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(580, 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(580, 10, health_bar_width * health_percentage, health_bar_height))



screen = pygame.display.set_mode(Config.screen_size)
pygame.display.set_caption("The curse of the Dark Moon")
pygame.mouse.set_cursor(pygame.cursors.tri_left)
background_menu = pygame.image.load(r'image\BackgroundMenu.png')
background_setting = pygame.image.load(r'image\backgroundSetting.png')


main_font = pygame.font.SysFont('algerian', 32)
menu_soundtrack = pygame.mixer.Sound(r'Soundtrack\Dark Souls CD 1 TRACK 21 (320).mp3')
def exit_game():
    """Вихід з гри"""
    pygame.quit()
    sys.exit()

def empty():
    return

def draw_text(text, font, color, screen, centerx, centery):
    """Виведення тексту на екран"""
    text_test = font.render(text, True, color)
    text_field = text_test.get_rect()
    text_field.centerx = centerx
    text_field.centery = centery
    screen.blit(text_test, text_field)


def start_screen():
    """Стартовий екран"""

    global menu_soundtrack
    if not pygame.mixer.get_busy():
        menu_soundtrack.play(-1)

    while Config.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_menu()

        screen.blit(background_setting, (0, 0))
        draw_text("Press SPACE to Start", main_font, Config.text_color, screen, Config.screen_size[0]//2, Config.screen_size[0]//2)
        pygame.display.flip()


def main_menu():
    """Головне меню гри"""

    while Config.running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(menu_items):
                    if Config.screen_size[1]/2+Config.vertical_offset+50*i-15 < my < Config.screen_size[1]/2+Config.vertical_offset+50*i+15:
                        menu_items_map[button]()
        screen.blit(background_menu, (0, 0))
        for i, button in enumerate(menu_items):
            if Config.screen_size[1]/2+Config.vertical_offset+50*i-15 < my < Config.screen_size[1]/2+Config.vertical_offset+50*i+15:
                draw_text(button, main_font, Config.text_hover_color, screen, Config.screen_size[0]/4.3, Config.screen_size[1]/2+Config.vertical_offset + 55*i)
            else:
                draw_text(button, main_font, Config.text_color, screen, Config.screen_size[0]/4.3, Config.screen_size[1]/2 + Config.vertical_offset + 55*i)
        pygame.display.flip()

def change_volume(step):
    """Збільшення та зменшення звуку"""
    global menu_soundtrack
    Config.volume += step
    if Config.volume < 0:
        Config.volume = 0
    elif Config.volume > 100:
        Config.volume = 100
    menu_soundtrack.set_volume(Config.volume / 100.0)

def change_fps(step):
    """Зміна FPS"""
    Config.fps += step
    if Config.fps < 30:
        Config.fps = 30
    elif Config.fps > 60:
        Config.fps = 60


def setting():
    """Налаштування гри"""
    while Config.running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Config.screen_size[0] // 3 < mx < Config.screen_size[0] // 3 + 100 and Config.screen_size[1] // 5 - 40 < my < Config.screen_size[1] // 5 + 40:
                    change_volume(-5)
                elif Config.screen_size[0] // 2 + 80 < mx < Config.screen_size[0] // 2 + 180 and Config.screen_size[1] // 5 - 30 < my < Config.screen_size[1] // 5 + 30:
                    change_volume(5)
                elif Config.screen_size[0] // 3 < mx < Config.screen_size[0] // 3 + 100 and Config.screen_size[1] // 2 - 20 < my < Config.screen_size[1] // 2 + 20:
                    change_fps(30)
                elif Config.screen_size[0] // 2 + 80 < mx < Config.screen_size[0] // 2 + 180 and Config.screen_size[1] // 2 - 20 < my < Config.screen_size[1] // 2 + 20:
                    change_fps(-30)
                elif Config.screen_size[0] // 2 - 50 < mx < Config.screen_size[0] // 3 + 200 and Config.screen_size[1] // 1 - 100 < my < Config.screen_size[1] // 2 + 190:
                    main_menu()

        screen.blit(background_setting, (0, 0))
        setting_button = [
            ("Volume", Config.screen_size[0] // 2, Config.screen_size[1] // 6 - 10),
            (f"{Config.volume}", Config.screen_size[0] // 2, Config.screen_size[1] // 4),
            ("<", Config.screen_size[0] // 3 + 30, Config.screen_size[1] // 5 + 20),
            (">", Config.screen_size[0] // 2 + 100, Config.screen_size[1] // 5 + 20),
            ("FPS", Config.screen_size[0] // 2, Config.screen_size[1] // 3 + 32),
            (f"{Config.fps}", Config.screen_size[0] // 2, Config.screen_size[1] // 2),
            ("<", Config.screen_size[0] // 3 + 30, Config.screen_size[1] // 2),
            (">", Config.screen_size[0] // 2 + 100, Config.screen_size[1] // 2),
            ("Back", Config.screen_size[0] // 2, Config.screen_size[1] // 1 - 100)
        ]


        for text, x, y in setting_button:
            if text == "Back" and Config.screen_size[0] // 2 - 50 < mx < Config.screen_size[0] // 3 + 200 and Config.screen_size[1] // 1 - 100 < my < Config.screen_size[1] // 2 + 190:
                draw_text(text, main_font, Config.text_hover_color, screen, x, y)
            else:
                draw_text(text, main_font, Config.text_color, screen, x, y)


        pygame.display.flip()


menu_items = ["Play", "Setting", "Exit"]
menu_items_map = {
    "Play": Game().run,
    "Setting": setting,
    "Exit": exit_game
}

if __name__ == "__main__":
    start_screen()