import pygame
from pygame.math import Vector2
from board import Food, Snake, WIDTH, NUM_OF_CELLS
import sys
import tkinter as tk
from tkinter import messagebox


pygame.init()
pygame.display.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
bg_img = pygame.image.load("images/grass_bg.jpg")

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.pause = False
        self.counter = 0

    def restart_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.pause = False
        self.counter = 0

    def draw_bg(self, win):
        bg = pygame.transform.scale(bg_img, (WIDTH, WIDTH))
        win.blit(bg, (0, 0))

    def display_score(self, win):
        font = pygame.font.Font('fonts/PoetsenOne-Regular.ttf', 32)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        win.blit(text, (WIDTH - text.get_width() - 15, 10))

    def display_pause_text(self, win):
        font = pygame.font.Font('fonts/PoetsenOne-Regular.ttf', 80)
        text = font.render("Paused", True, (255, 255, 255))
        win.blit(text, (WIDTH//2 - text.get_width()//2, WIDTH//2 - text.get_height()//2))

    def play_bg_music(self, stop=False):
        if stop:
            self.counter += 1
            if self.counter % 2 != 0:
                pygame.mixer.pause()
            else:
                pygame.mixer.unpause()
        else:
            bg_music = pygame.mixer.Sound('sounds/bg_music.mp3')
            bg_music.set_volume(0.02)
            bg_music.play(-1)

    def draw_objects(self, win):
        self.draw_bg(win)
        self.food.draw(win)
        self.snake.draw(win)
        if self.pause:
            self.display_pause_text(win)
        else:
            self.display_score(win)

    def check_collision(self):
        if self.snake.body[0] == self.food.position:
            self.food.randomize()
            if self.food.position in self.snake.body[1:]:
                self.food.randomize()
            self.snake.move(add_block=True)
            pygame.mixer.Sound('sounds/crunch.wav').play()
            self.score += 1

    def check_game_over(self):
        if not 0 <= self.snake.body[0].x < NUM_OF_CELLS or not 0 <= self.snake.body[0].y < NUM_OF_CELLS:
            self.game_over()
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                self.game_over()

    def game_over(self):
        pygame.mixer.Sound('sounds/game_over.wav').play()
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        subject = "Game over!"
        content = "Do you want to play again"
        MsgBox = tk.messagebox.askquestion(subject, content, icon='question')
        if MsgBox == 'yes':
            try:
                root.destroy()
                self.restart_game()
            except:
                pass
        else:
            pygame.quit()
            sys.exit()

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_game_over()


def main(win):
    game = Game()
    game.play_bg_music()
    clock = pygame.time.Clock()
    screen_update = pygame.USEREVENT
    pygame.time.set_timer(screen_update, 200)
    while True:
        if not game.pause:
            for event in pygame.event.get():
                if event.type == screen_update:
                    game.update()
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_p:
                        game.pause = True
                    elif event.key == pygame.K_m:
                        game.play_bg_music(stop=True)
                    elif event.key == pygame.K_r:
                        game.restart_game()
                    elif event.key == pygame.K_UP:
                        if game.snake.direction.y != 1:
                            game.snake.direction = Vector2(0, -1)
                    elif event.key == pygame.K_DOWN:
                        if game.snake.direction.y != -1:
                            game.snake.direction = Vector2(0, 1)
                    elif event.key == pygame.K_LEFT:
                        if game.snake.direction.x != 1:
                            game.snake.direction = Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        if game.snake.direction.x != -1:
                            game.snake.direction = Vector2(1, 0)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game.pause = False
        game.draw_objects(win)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main(WIN)