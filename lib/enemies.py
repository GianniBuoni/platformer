# pyright: reportOptionalMemberAccess = false
from math import sin
from random import randint

from lib.sprites import AnimatedSprite
from settings import *

class Enemy(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def move(self, dt) -> None:
        raise NotImplemented(f"Child class missing method. DT: {dt}")

    def constraint(self) -> None:
        raise NotImplemented("Child class missing method")

    def update(self, dt):
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
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def move(self, dt):
        pass

    def constraint(self):
        pass
