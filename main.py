from random import randint, random

from time import sleep, time

from pygame.locals import *
import pygame


size = 40
BackgroundColor = (32, 99, 199)


class Apple:
    def __init__(self, parent_surface):
        self.parent_surface = parent_surface
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = 400
        self.y = 430

    def drawApple(self):
        self.parent_surface.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def jump(self):
        self.x = randint(0, 33)*size
        self.y = randint(0, 17)*size
        pygame.display.flip()


class Snake:
    def __init__(self, parent_surface, length):
        self.parent_surface = parent_surface
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [size]*self.length
        self.y = [size]*self.length
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def drawSnake(self):
        # self.parent_surface.fill(BackgroundColor)

        for i in range(self.length):
            # print(self.x, self.y)
            self.parent_surface.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def runUp(self):
        self.direction = "up"

    def runDown(self):
        self.direction = "down"

    def runRight(self):
        self.direction = "right"

    def runLeft(self):

        self.direction = "left"

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "up":
            self.y[0] = self.y[0]-size

        if self.direction == "down":
            self.y[0] = self.y[0]+size

        if self.direction == "left":
            self.x[0] = self.x[0]-size

        if self.direction == "right":
            self.x[0] = self.x[0]+size

        self.drawSnake()


class Game:
    def __init__(self):
        pygame.init()
        self. music_please()
        self.surface = pygame.display.set_mode((1360, 720))
        # self.surface.fill(BackgroundColor)
        self.renderBackground()
        self.snake = Snake(self.surface, 1)
        self.snake.drawSnake()
        self.apple = Apple(self.surface)
        self.apple.drawApple()

    def renderBackground(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def sound_please(self, soundName):
        sound = pygame.mixer.Sound(f"resources/{soundName}.mp3")
        pygame.mixer.Sound.play(sound)

    def music_please(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play(self):
        self.renderBackground()
        self.snake.walk()
        self.apple.drawApple()
        self.score()
        pygame.display.flip()
        if self.isCollision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.jump()

        for i in range(3, self.snake.length):
            if self.isCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over"
                exit(0)

        if(self.snake.x[0] == 0 or self.snake.x[0] == 1360 or self.snake.y[0] == 0 or self.snake.y[0] == 720):
            raise "Game Over"
            exit(0)

    def gameOver(self):
        self.sound_please("crash")
        # self.surface.fill(BackgroundColor)
        self.renderBackground()
        font = pygame.font.SysFont("arial", 40)
        line = font.render(f"game is over ", False, (0, 0, 0))
        line1 = font.render(
            f"press enter to play again and press escape for exit!! ", False, (0, 0, 0))
        self.surface.blit(line, (200, 300))
        self.surface.blit(line1, (200, 350))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def score(self):
        font = pygame.font.SysFont("arial", 20)
        score = font.render(f"Score: {self.snake.length-1}", False, (0, 0, 0))
        self.surface.blit(score, (1200, 20))

    def isCollision(self, snakex, snakey, applex, appley):
        if(snakex >= applex and snakex < applex+size):
            if(snakey >= appley and snakey < appley+size):
                self.sound_please("ding")
                return True
        return False

    def run(self):
        running = True
        PAUSE = False
        while running:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        PAUSE = False
                        pygame.mixer.music.unpause()

                    if not PAUSE:
                        if event.key == K_UP:
                            self.snake.runUp()

                        if event.key == K_DOWN:
                            self.snake.runDown()

                        if event.key == K_LEFT:
                            self.snake.runLeft()

                        if event.key == K_RIGHT:
                            self.snake.runRight()

                if event.type == QUIT:
                    running = False

            try:
                if not PAUSE:
                    self.play()
            except Exception as e:
                self.gameOver()
                pygame.mixer.music.pause()
                PAUSE = True
                self.reset()

            sleep(0.1)


if __name__ == "__main__":
    game = Game()
    game.run()
