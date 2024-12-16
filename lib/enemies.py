# pyright: reportOptionalMemberAccess = false
from math import sin
from random import randint

from lib.sprites import AnimatedSprite
from lib.timers import Timer
from settings import *

class Enemy(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.death_timer = Timer(200, func = self.kill)

    def move(self, dt) -> None:
        raise NotImplemented(f"Child class missing method. DT: {dt}")

    def constraint(self) -> None:
        raise NotImplemented("Child class missing method")

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey("black")

    def update(self, dt):
        self.death_timer.update()
        if not self.death_timer:
            self.move(dt)
            self.animate(dt)
        self.constraint()

class Bee(Enemy):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.speed = randint(300, 500)
        self.amplitude = randint(500, 600)
        self.frequency = randint(300, 600)

    def move(self, dt):
        self.rect.x -= self.speed * dt
        self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt

    def constraint(self) -> None:
        if self.rect.right <= -WINDOW_WIDTH / 2:
            self.kill()

class Worm(Enemy):
    def __init__(self, rect, frames, groups):
        super().__init__(rect.topleft, frames, groups)
        self.rect.bottomleft = rect.bottomleft
        self.level_rect = rect

        # movement
        self.speed = 160
        self.direction = 1

    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt

    def constraint(self):
        if not self.level_rect.contains(self.rect):
            self.direction *= -1
            self.frames = [pygame.transform.flip(x, True, False) for x in self.frames]
