# pyright: reportOptionalMemberAccess = false
from lib.sprites import *
from lib.timers import Timer

class Player(AnimatedSprite):
    def __init__(self, pos, frames, groups, collision_sprites, bullet_func):
        super().__init__(pos, frames, groups)
        self.create_bullet = bullet_func

        # movement
        self.direction = pygame.Vector2()
        self.speed = 400
        self.gravity = 50
        self.collision_sprites = collision_sprites
        self.on_ground = False
        self.flip = False

        # timers
        self.shoot_timer = Timer(500)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = -20

        if keys[pygame.K_f] and not self.shoot_timer:
            self.create_bullet(
                self.rect.center,
                -1 if self.flip else 1
            )
            self.shoot_timer.activate()

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

    def animate(self, dt):
        if self.direction.x:
            self.frames_idx += self.animation_speed * dt
            self.flip = self.direction.x < 0
        else: self.frames_idx = 0

        self.frames_idx = 1 if not self.on_ground else self.frames_idx
        self.image = self.frames[int(self.frames_idx) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def update(self, dt):
        self.shoot_timer.update()
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)
