import pygame
import random

pygame.mixer.init()

paddle_sound = pygame.mixer.Sound("game/paddle_hit.wav")
wall_sound = pygame.mixer.Sound("game/wall_bounce.wav")
score_sound = pygame.mixer.Sound("game/score.wav")

class Ball:
    def __init__(self, x, y, speed_x, speed_y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = 10

        # ✅ Add both speed components
        self.speed_x = speed_x * random.choice((1, -1))
        self.speed_y = speed_y * random.choice((1, -1))

        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off top/bottom
        if self.y - self.radius <= 0 or self.y + self.radius >= self.screen_height:
            self.speed_y *= -1
            wall_sound.play()

    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def check_collision(self, player, ai):
        ball_rect = self.rect()

        # Player collision
        if ball_rect.colliderect(player.rect()):
            offset = (self.y - (player.y + player.height / 2)) / (player.height / 2)
            self.speed_y += offset * 5
            self.x = player.x + player.width + self.radius
            self.speed_x *= -1
            paddle_sound.play()

        # AI collision
        elif ball_rect.colliderect(ai.rect()):
            offset = (self.y - (ai.y + ai.height / 2)) / (ai.height / 2)
            self.speed_y += offset * 5
            self.x = ai.x - self.radius * 2
            self.speed_x *= -1
            paddle_sound.play()

    def reset(self):
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        self.speed_x *= random.choice((1, -1))
        self.speed_y *= random.choice((1, -1))
