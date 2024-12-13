# pyright: reportOptionalMemberAccess = false
from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, player_pos) -> None: # pyright: ignore
        self.offset.x = -(player_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(player_pos[1] - WINDOW_HEIGHT / 2)

        ground_sprites = [x for x in self if hasattr(x, "ground")]
        object_sprites = [x for x in self if not hasattr(x, "ground")]

        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key = lambda x: x.rect.centery):
                self.surface.blit(
                    sprite.image,
                    sprite.rect.topleft + self.offset
                )

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)

class Player(Sprite):
    def __init__(self, pos, groups, collision_sprites):
        self.image = pygame.image.load(join("images", "player", "0.png")).convert_alpha()
        super().__init__(pos, self.image, groups)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 400
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def collide(self, direction):
        pass

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collide("horizontal")
        self.rect.y += self.direction.y * self.speed * dt
        self.collide("vertical")

    def update(self, dt):
        self.input()
        self.move(dt)
