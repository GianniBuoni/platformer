# pyright: reportOptionalMemberAccess = false
from settings import *
from lib.sprites import *
from lib.helpers import *
from lib.player import Player

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

        # map setup
        self.load_assets()
        self.map_setup()

    def load_assets(self):
        # player
        self.player_frames = load_dir("images", "player")
        self.bullet_surface = load_img("images", "gun", "bullet")
        self.fire_surface = load_img("images", "gun", "fire")

        # enemies
        self.bee_frames = load_dir("images", "enemies", "bee")
        self.worm_frames = load_dir("images", "enemies", "worm")

    def map_setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))

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
                    self.collision_sprites
                )

        Bee((500, 600), self.bee_frames, self.all_sprites)
        Worm((500, 800), self.worm_frames, self.all_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
