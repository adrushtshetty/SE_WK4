import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.winning_score=5

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            pygame.mixer.Sound("game/score.wav").play() 
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()
            pygame.mixer.Sound("game/score.wav").play() 

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        if self.player_score >= self.winning_score:
            return self.show_winner(screen, "Player Wins!")
        elif self.ai_score >= self.winning_score:
            return self.show_winner(screen, "AI Wins!")
        return False
    
    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2

    def show_winner(self, screen, message):
        screen.fill((0, 0, 0))
        text = self.font.render(message, True, (255, 255, 255))
        rect = text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(text, rect)

        # Display replay options
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]

        for i, opt in enumerate(options):
            opt_text = self.font.render(opt, True, (200, 200, 200))
            opt_rect = opt_text.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
            screen.blit(opt_text, opt_rect)

        pygame.display.flip()

        # Wait for player input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return False
                    elif event.key == pygame.K_3:
                        self.winning_score = 2  # Best of 3 => first to 2
                        self.reset_game()
                        return True
                    elif event.key == pygame.K_5:
                        self.winning_score = 3  # Best of 5 => first to 3
                        self.reset_game()
                        return True
                    elif event.key == pygame.K_7:
                        self.winning_score = 4  # Best of 7 => first to 4
                        self.reset_game()
                        return True
