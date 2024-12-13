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

        for sprite in self:
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
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.direction.x > 0: self.rect.right = sprite.rect.left # moving left -> right
                    if self.direction.x < 0: self.rect.left = sprite.rect.right # moving right -> left
                else:
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom # moving down -> up
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top # moving up -> down

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collide("horizontal")
        self.rect.y += self.direction.y * self.speed * dt
        self.collide("vertical")

    def update(self, dt):
        self.input()
        self.move(dt)
