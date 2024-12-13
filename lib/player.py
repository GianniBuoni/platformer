# pyright: reportOptionalMemberAccess = false
from lib.sprites import *

class Player(AnimatedSprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(pos, frames, groups)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 400
        self.gravity = 50
        self.collision_sprites = collision_sprites
        self.on_ground = False

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = -20

    def collide(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.direction.x > 0: self.rect.right = sprite.rect.left # moving left -> right
                    if self.direction.x < 0: self.rect.left = sprite.rect.right # moving right -> left
                else:
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom # moving down -> up
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top # moving up -> down
                    self.direction.y = 0

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collide("horizontal")

        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collide("vertical")

    def check_floor(self):
        bottom_rect = pygame.FRect((0,0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
        collide_rects = [x.rect for x in self.collision_sprites]

        self.on_ground = True if bottom_rect.collidelist(collide_rects) >= 0 else False

    def update(self, dt):
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)
