# pyright: reportOptionalMemberAccess = false
from random import randint
from settings import *

from lib.sprites import *
from lib.helpers import *
from lib.enemies import *
from lib.player import Player
from lib.timers import Timer

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()

        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # map setup
        self.load_assets()
        self.map_setup()

        # timers
        self.bee_timer = Timer(500, self.create_bee, autostart = True, repeat = True)

    def load_assets(self):
        # player
        self.player_frames = load_dir("images", "player")
        self.bullet_surface = load_img("images", "gun", "bullet")
        self.fire_surface = load_img("images", "gun", "fire")

        # enemies
        self.bee_frames = load_dir("images", "enemies", "bee")
        self.worm_frames = load_dir("images", "enemies", "worm")

        # audio
        self.audio = audio_import("audio")

    def map_setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))
        self.level_w = map.width * TILE_SIZE
        self.level_h = map.height * TILE_SIZE

        for x, y, image in map.get_layer_by_name("Main").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                image,
                (self.all_sprites, self.collision_sprites)
            )

        for x, y, image in map.get_layer_by_name("Decoration").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                image,
                self.all_sprites
            )

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player(
                    (obj.x, obj.y),
                    self.player_frames,
                    self.all_sprites,
                    self.collision_sprites,
                    self.create_bullet
                )
            if obj.name == "Worm":
                worm_rect = pygame.FRect(obj.x, obj.y, obj.width, obj.height)
                Worm(worm_rect, self.worm_frames, (self.all_sprites, self.enemy_sprites))

    def create_bee(self):
        Bee(
            (self.level_w + WINDOW_WIDTH / 2, randint(0, self.level_h)),
            self.bee_frames,
            (self.all_sprites, self.enemy_sprites)
        )

    def create_bullet(self, player_pos, direction):
        bullet_x = (
            player_pos[0] + direction * 34 if direction == 1
            else player_pos[0] + direction * 34 - self.bullet_surface.get_width()
        )
        Bullet(
            (bullet_x, player_pos[1]),
            self.bullet_surface,
            direction,
            (self.all_sprites, self.bullet_sprites)
        )
        Fire(
            player_pos,
            self.fire_surface,
            self.all_sprites,
            self.player
        )

    def collision(self):
        for bullet in self.bullet_sprites:
            sprite_collisions = pygame.sprite.spritecollide(
                bullet, self.enemy_sprites, False, pygame.sprite.collide_mask
            )
            if sprite_collisions:
                bullet.kill()
                for sprite in sprite_collisions:
                    sprite.destroy()

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collision()

            # draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
