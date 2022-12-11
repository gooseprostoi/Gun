import math
import time
from random import *

import pygame, fontTools

FPS = 50

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
ay = 0.5

global score

score = 0

hit = 1


class Ball:
    def __init__(self, screen: pygame.Surface, gun_x=40, gun_y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = gun_x
        self.y = gun_y
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.dietick = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= ay
        self.x += self.vx
        self.y -= self.vy
        # FIXED
        if self.y >= HEIGHT - 50:
            self.vy = -self.vy * 0.8
            self.y = 550
            self.dietick += 1
        if self.x >= WIDTH:
            self.vx = -self.vx * 0.8
            self.x = WIDTH - 10
        if self.x <= 0:
            self.vx = -self.vx * 0.8
            self.x = 10
            
        

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXED
        if (((obj.x + obj.r) - (self.x + self.r)) ** 2 + ((obj.y + obj.r) - (self.y + self.r)) ** 2) < (obj.r + self.r) ** 2:
            return True
        else:
            return False



class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 5
        self.f2_on = 0
        self.cos = 1
        self.sin = 0
        self.color = GREY
        self.vx = 0
        self.vy = 0
        self.x = 40
        self.y = 440
        self.v = 5

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        vec_len = ((event.pos[1] - self.y) ** 2 + (event.pos[0] - self.x) ** 2) ** 0.5
        self.cos = (event.pos[0] - self.x) / vec_len # cos
        self.sin = (event.pos[1] - self.y) / vec_len # sin

        new_ball.vx = self.f2_power * self.cos
        new_ball.vy = - self.f2_power * self.sin
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            vec_len = ((event.pos[1] - self.y) ** 2 + (event.pos[0] - self.x) ** 2) ** 0.5
            self.cos = (event.pos[0] - self.x) / vec_len # cos
            self.sin = (event.pos[1] - self.y) / vec_len # sin
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXED
        pygame.draw.polygon(self.screen, self.color, ([self.x, self.y + 10],
                                                      [self.x, self.y],
                                                      [self.x + 40 * self.cos * (1 + self.f2_power / 100),
                                                       self.y + 40 * self.sin * (1 + self.f2_power / 100), ],
                                                      [self.x + 40 * self.cos * (1 + self.f2_power / 100),
                                                       self.y + 10 + 40 * self.sin * (1 + self.f2_power / 100), ]
                                                      ))
                                                
    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x >= WIDTH:
            self.x = WIDTH
        if self.x <= 0:
            self.x = 0
        if self.y >= (HEIGHT - 50):
            self.y = (HEIGHT - 50)
        if self.y <= 0:
            self.y = 0

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        self.points = 0
        self.live = 1  # непонятно вообщзе зачем это нужно
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(15, 50)
        self.color = RED
        self.new_target()
        self.screen = screen


    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(15, 50)
        self.live = 1


    def move(self):
        """Движение цели"""
        self.x += self.vx
        self.y += self.vy
        if self.x >= WIDTH or self.x <= 0:
            self.vx *= -1
        if self.y >= (HEIGHT - 50) or self.y <= 0:
            self.vy *= -1


    def hit(self, points=1):
        """Попадание шарика в цель."""
        global score
        self.points += points
        score += points

    def draw(self):
        """ Рисует цель """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target()
target2 = Target()

finished = False
textfont = pygame.font.SysFont('monospace', 27)

ticker = 0

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target1.draw()
    target2.draw()
    target1.move()
    target2.move()
    for b in balls:
        b.draw()

    textTBD = textfont.render("Счёт: " + str(target1.points + target2.points) + ", количество выстрелов: " + str(bullet), 10, (0, 0, 0))  # Displaying score counter
    screen.blit(textTBD, (30, 10))

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                gun.vy -= gun.v
            if event.key == pygame.K_s:
                gun.vy += gun.v
            if event.key == pygame.K_a:
                gun.vx -= gun.v
            if event.key == pygame.K_d:
                gun.vx += gun.v

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                gun.vy += gun.v
            if event.key == pygame.K_s:
                gun.vy -= gun.v
            if event.key == pygame.K_a:
                gun.vx += gun.v
            if event.key == pygame.K_d:
                gun.vx -= gun.v
        
    gun.move()

    for b in balls:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1.new_target()
        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()
        if b.dietick == 10:
            balls.remove(b)

    gun.power_up()
    pygame.display.update()

pygame.quit()
