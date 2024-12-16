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
        self.image: pygame.Surface = surface
        self.rect = self.image.get_frect(topleft = pos)

class Bullet(Sprite):
    def __init__(self, pos, surface, direction, groups):
        super().__init__(pos, surface, groups)

        # flip with player
        self.image = pygame.transform.flip(self.image, direction == -1, False)

        # movement
        self.direction = direction
        self.speed = 850

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups):
        self.frames, self.frames_idx, self.animation_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frames_idx], groups)

    def animate(self, dt):
        self.frames_idx += self.animation_speed * dt
        self.image = self.frames[int(self.frames_idx) % len(self.frames)]

class Bee(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def update(self, dt):
        self.animate(dt)

class Worm(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def update(self, dt):
        self.animate(dt)
