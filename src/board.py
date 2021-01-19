import pygame
from pygame.math import Vector2
import random

# Board dimensions
WIDTH = 800
CELL_WIDTH = 40
NUM_OF_CELLS = WIDTH//CELL_WIDTH

class Food(object):
    def __init__(self):
        self.position = Vector2(NUM_OF_CELLS,NUM_OF_CELLS)
        self.randomize()
        APPLE_IMG = pygame.image.load('images/apple.png')
        self.apple_img = pygame.transform.scale(APPLE_IMG, (CELL_WIDTH, CELL_WIDTH))

    def randomize(self):
        x = random.randint(0, NUM_OF_CELLS-2)
        y = random.randint(0, NUM_OF_CELLS-2)
        self.position = Vector2(x, y)

    def draw(self, win):
        x_draw = self.position.x * CELL_WIDTH
        y_draw = self.position.y * CELL_WIDTH
        food_rect = pygame.Rect(x_draw, y_draw, CELL_WIDTH, CELL_WIDTH)
        win.blit(self.apple_img, food_rect)


class Snake(object):
    def __init__(self):
        self.body = [Vector2(NUM_OF_CELLS//2, NUM_OF_CELLS//2),
                     Vector2(NUM_OF_CELLS//2 - 1, NUM_OF_CELLS//2),
                     Vector2(NUM_OF_CELLS//2 - 2, NUM_OF_CELLS//2)
                     ]
        self.direction = Vector2(0,0)
        # images
        head_up = pygame.image.load('images/head_up.png').convert_alpha()
        self.head_up = pygame.transform.scale(head_up, (CELL_WIDTH, CELL_WIDTH))
        head_down = pygame.image.load('images/head_down.png').convert_alpha()
        self.head_down = pygame.transform.scale(head_down, (CELL_WIDTH, CELL_WIDTH))
        head_right = pygame.image.load('images/head_right.png').convert_alpha()
        self.head_right = pygame.transform.scale(head_right, (CELL_WIDTH, CELL_WIDTH))
        head_left = pygame.image.load('images/head_left.png').convert_alpha()
        self.head_left = pygame.transform.scale(head_left, (CELL_WIDTH, CELL_WIDTH))

        tail_up = pygame.image.load('images/tail_up.png').convert_alpha()
        self.tail_up = pygame.transform.scale(tail_up, (CELL_WIDTH, CELL_WIDTH))
        tail_down = pygame.image.load('images/tail_down.png').convert_alpha()
        self.tail_down = pygame.transform.scale(tail_down, (CELL_WIDTH, CELL_WIDTH))
        tail_right = pygame.image.load('images/tail_right.png').convert_alpha()
        self.tail_right = pygame.transform.scale(tail_right, (CELL_WIDTH, CELL_WIDTH))
        tail_left = pygame.image.load('images/tail_left.png').convert_alpha()
        self.tail_left = pygame.transform.scale(tail_left, (CELL_WIDTH, CELL_WIDTH))

        body_horizontal = pygame.image.load('images/body_horizontal.png').convert_alpha()
        self.body_horizontal = pygame.transform.scale(body_horizontal, (CELL_WIDTH, CELL_WIDTH))
        body_vertical = pygame.image.load('images/body_vertical.png').convert_alpha()
        self.body_vertical = pygame.transform.scale(body_vertical, (CELL_WIDTH, CELL_WIDTH))
        body_top_right = pygame.image.load('images/body_top_right.png').convert_alpha()
        self.body_top_right = pygame.transform.scale(body_top_right, (CELL_WIDTH, CELL_WIDTH))
        body_top_left = pygame.image.load('images/body_top_left.png').convert_alpha()
        self.body_top_left = pygame.transform.scale(body_top_left, (CELL_WIDTH, CELL_WIDTH))
        body_bottom_right = pygame.image.load('images/body_bottom_right.png').convert_alpha()
        self.body_bottom_right = pygame.transform.scale(body_bottom_right, (CELL_WIDTH, CELL_WIDTH))
        body_bottom_left = pygame.image.load('images/body_bottom_left.png').convert_alpha()
        self.body_bottom_left = pygame.transform.scale(body_bottom_left, (CELL_WIDTH, CELL_WIDTH))

    def move(self, add_block=False):
        if self.direction != Vector2(0,0):
            if add_block:
                temp_body = self.body[:]
            else:
                temp_body = self.body[:-1]
            temp_body.insert(0, temp_body[0] + self.direction)
            self.body = temp_body

    def draw(self, win):
        head = self.draw_head()
        tail = self.draw_tail()
        for index, block in enumerate(self.body):
            x_draw = block.x * CELL_WIDTH
            y_draw = block.y * CELL_WIDTH
            block_rect = pygame.Rect(x_draw, y_draw, CELL_WIDTH, CELL_WIDTH)
            if index == 0:
                win.blit(head, block_rect)
            elif index == len(self.body) - 1:
                win.blit(tail, block_rect)
            else:
                prev_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block

                if prev_block.x == next_block.x:
                    win.blit(self.body_vertical, block_rect)
                elif prev_block.y == next_block.y:
                    win.blit(self.body_horizontal, block_rect)
                else:
                    if next_block.y == -1 and prev_block.x == 1 or next_block.x == 1 and prev_block.y == -1:
                        win.blit(self.body_top_right, block_rect)
                    elif next_block.y == -1 and prev_block.x == -1 or next_block.x == -1 and prev_block.y == -1:
                        win.blit(self.body_top_left, block_rect)
                    elif next_block.x == 1 and prev_block.y == 1 or next_block.y == 1 and prev_block.x == 1:
                        win.blit(self.body_bottom_right, block_rect)
                    elif next_block.x == -1 and prev_block.y == 1 or next_block.y == 1 and prev_block.x == -1:
                        win.blit(self.body_bottom_left, block_rect)

    def draw_head(self):
        relative_pos = self.body[0] - self.body[1]
        if relative_pos == Vector2(0,-1): return self.head_up
        elif relative_pos == Vector2(0,1): return self.head_down
        elif relative_pos == Vector2(1,0): return self.head_right
        elif relative_pos == Vector2(-1,0): return self.head_left

    def draw_tail(self):
        relative_pos = self.body[-1] - self.body[-2]
        if relative_pos == Vector2(0,-1): return self.tail_up
        elif relative_pos == Vector2(0,1): return self.tail_down
        elif relative_pos == Vector2(1,0): return self.tail_right
        elif relative_pos == Vector2(-1,0): return self.tail_left
