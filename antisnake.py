from random import randint
import pygame
pygame.init()

class Theme(object):
    def __init__(self, bg, snake, food, font):
        self.bg = bg
        self.snake = snake
        self.food = food
        self.font = font

class SnakeGame(object):
    """Snake Game."""


    def __init__(self):
        self.width = 50
        self.height = 50
        self.scale = 10

        self.themes = [
            Theme(
                bg=(0,0,0),
                snake=(100,255,100),
                food=(255,100,100),
                font=(205,205,205)
            ),
            Theme(
                bg=(30, 50, 200),
                snake=(233, 233, 10),
                food=(40, 10, 10),
                font=(255, 255, 255)
            ),
            Theme(
                bg=(255,200,200),
                snake=(255,10,10),
                food=(255,255,255),
                font=(0,0,0)
            ),
            Theme(
                bg=(230,230,230),
                snake=(0,0,0),
                food=(75,75,75),
                font=(100,100,100)
            ),
            Theme(
                bg=(200,230,10),
                snake=(255,150,0),
                food=(100,140,0),
                font=(0,0,0)
            ),
            Theme(
                bg=(200,0,255),
                snake=(100,0,255),
                food=(255,0,200),
                font=(200,150,255)
            ),
            Theme(
                bg=(255,255,255),
                snake=(0,90,0),
                food=(0,0,90),
                font=(0,0,0)
            ),
            Theme(
                bg=(255,0,0),
                snake=(0,0,0),
                food=(255,255,255),
                font=(255,200,200)
            ),
        ]

        size = self.width*self.scale, self.height*self.scale
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("~ ANTISNAKE ~")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("misterpixelregular.otf", 16)

        self.gameover = False
        self.opening = True
        self.pause = False
        self.special = False
        self.special_image = pygame.image.load("snake.png")

        self.tail = []

    def play(self):
        self.setup()
        quit = False
        while not quit:
            self.special = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                if event.type == pygame.KEYDOWN:
                    self.opening = False
                    if event.key == pygame.K_s:
                        self.special = True
                    if event.key == pygame.K_ESCAPE:
                        quit = True
                    elif event.key == pygame.K_r:
                        self.setup()
                        self.gameover = False
                    elif event.key == pygame.K_p:
                        self.pause = not self.pause
                    else:
                        self.controls(event.key)

            if not (self.gameover or self.pause or self.opening):
                self.update()

            self.draw()
            pygame.display.update()

            speed = 10 + (self.score * 2 if self.score < 10 else self.score)
            self.clock.tick(speed)

    def setup(self):
        self.random_food()
        self.tail = [(self.width//2,self.height//2)]
        self.direction = self.next_direction = (1,0) #(+1, 0)
        self.score = 0

    def controls(self, key):
        d = None
        if key == pygame.K_UP:
            d = (0, -1)
        elif key == pygame.K_DOWN:
            d = (0, +1)
        elif key == pygame.K_LEFT:
            d = (-1, 0)
        elif key == pygame.K_RIGHT:
            d = (+1, 0)

        if d and (self.direction[0]+d[0], self.direction[1]+d[1]) != (0, 0):
            self.next_direction = d

    def draw(self):
        theme = self.themes[self.score//5%len(self.themes)]
        score = "Score = {} ".format(self.score)+"!"*(self.score//5)
        self.screen.fill(theme.bg)
        if self.special:
            self.screen.blit(self.special_image, (0,0))
        if self.opening:
            label_text = [
                "Antisnake", "~"*7, "",
                "Touches fléchées = Se déplacer",
                "R = Recommencer une partie",
                "P = Mettre le jeu en pause",
                "",
                "Le jeu est fait en 2018 par Léon Lenclos (leonlenclos.net)",
                "La font est Mister Pixel de Christophe Badani (velvetyne.fr)",
                "",
                "N'importe quelle touche pour commencer."
            ]
        elif self.pause:
            label_text = [
                "Le jeu est en Pause...", score,
                "Appuie sur P pour reprendre.",
            ]
        elif self.gameover:
            label_text = [
                "Perdu !", score,
                "Appuie sur R pour recommencer.",
            ]
        else:
            for box in self.tail:
                self.draw_box(box, theme.snake)
            self.draw_box(self.food, theme.food)
            label_text = [score]

        for i, txt in enumerate(label_text):
            i = len(label_text) - i
            label = self.font.render(txt.upper(), True, theme.font)
            pos = (5, self.screen.get_rect().height-20*i)
            self.screen.blit(label, pos)



    def update(self):
        # Move
        self.direction = self.next_direction

        head = (self.tail[-1][0] + self.direction[0],
                self.tail[-1][1] + self.direction[1])

        if head[0] >= self.width :
            head = head[0]-self.width, head[1]
        if head[0] < 0 :
            head = head[0]+self.width, head[1]
        if head[1] >= self.height:
            head = head[0], head[1]-self.height
        if head[1] < 0 :
            head = head[0], head[1]+self.height

        # Contact
        if head in self.tail:
            self.gameover = True

        if head == self.food or self.food == ():
            self.random_food()
            self.tail = [head]
            self.score += 1

        else:
            self.tail.append(head)

    def random_food(self):
        place_found = False
        while not place_found:
            pos = (randint(0, self.width-1), randint(0, self.height-1))
            place_found = True
            for b in self.tail:
                if b == pos:
                    place_found = False
                    break
        self.food = pos

    def draw_box(self, pos, col):
        scl = self.scale
        rect = (pos[0]*scl, pos[1]*scl, scl, scl)
        pygame.draw.rect(self.screen, col, rect)

SnakeGame().play()
