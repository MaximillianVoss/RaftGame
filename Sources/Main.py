import sys, os, pygame, random
import time
from enum import Enum


class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4
    NoDirection = 5


class LevelConstans():
    def __init__(self):
        self.Height = 500
        self.Width = 500
        self.Sky = 50
        self.Water = 125
        self.Bottom = 400


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, location, imgFileNames):
        super(BaseSprite, self, ).__init__()
        # анимаия
        self.index = 0
        self.images = []
        for i in range(0, len(imgFileNames)):
            self.images.append(self.loadImage(imgFileNames[i]))
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.direction = 1

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.image.set_colorkey((255, 255, 255))

    def setCoords(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveUp(self, pixels):
        self.rect.y -= pixels

    def modeDown(self, pixels):
        self.rect.y += pixels

    def GetRootPath(self):
        return os.path.dirname(os.path.abspath(__file__))[:-len("Sources")]

    # Функция отображения картинок
    def loadImage(self, name, colorkey=None):
        # Добавляем к имени картинки имя папки
        fullname = self.GetRootPath() + "Resources\\" + name
        # Загружаем картинку
        image = pygame.image.load(fullname).convert_alpha()
        return image

    def checkCollision(self, sprite):
        return pygame.sprite.collide_rect(self, sprite)

    def getCollisionDirection(self, sprite):
        rect1 = self.image.get_rect()
        rect2 = sprite.image.get_rect()
        if rect1.midtop[1] > rect2.midtop[1]:
            return Direction.Up
        elif rect1.midleft[0] > rect2.midleft[0]:
            return Direction.Left
        elif rect1.midright[0] < rect2.midright[0]:
            return Direction.Right
        else:
            return Direction.Down


class Background(BaseSprite):
    def __init__(self, location, imgFileNames):
        super(Background, self).__init__(location, imgFileNames)


class Player(BaseSprite):
    def __init__(self, location, imgFileNames):
        super(Player, self).__init__(location, imgFileNames)
        self.health = 100
        self.wood = 0
        self.stone = 0
        self.stand = False;
        self.swimming = False;

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        if not self.stand:
            self.modeDown(2)
        if not self.stand and self.swimming:
            self.moveUp(1)

    def drawStatus(self, screen):
        font = pygame.font.Font("freesansbold.ttf", 25)
        placeholder = [10, 10]
        titles = [("Здоровье:", self.health), ("Дерево:", self.wood), ("Камень:", self.stone), ("Stand:", self.stand),
                  ("Swim:", self.swimming)]
        for i in range(0, titles.__len__()):
            title = font.render(titles[i][0] + str(titles[i][1]), True, (255, 255, 255))
            screen.blit(title, placeholder)
            placeholder[1] += 30
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(60)


class Shark(BaseSprite):
    def __init__(self, location, imgFileNames):
        super(Shark, self).__init__(location, imgFileNames)
        self.direction = 1

    def update(self):
        if self.rect.x < 0 or self.rect.x > 420:
            self.direction *= -1
            self.index += 1
        self.moveRight(5 * self.direction)
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.image.set_colorkey((255, 255, 255))


class Raft(BaseSprite):
    def __init__(self, location, imgFileNames):
        super(Raft, self).__init__(location, imgFileNames)

    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


class Wood(BaseSprite):
    def __init__(self, location, imgFileNames):
        super(Wood, self).__init__(location, imgFileNames)


class Stone(BaseSprite):
    def __init__(self, location, imgFileNames):
        super(Stone, self).__init__(location, imgFileNames)


class BaseScene:

    def __init__(self):
        self.started = False
        # число кадров в сек.
        self.FPS = 60
        self.seconds = 0
        self.clock = pygame.time.Clock()
        self.levelConstants = LevelConstans()
        self.paused = False
        self.screen = pygame.display.set_mode((self.levelConstants.Width, self.levelConstants.Height))
        pygame.init()

    def main(self):
        self.started = False

    def start(self):
        self.started = True
        ticks = 0
        while self.started:
            self.main()
            if not self.paused:
                ticks += 1
                self.clock.tick(self.FPS)
                self.seconds += ticks % self.FPS
                # обновление спрайтовp
                self.myGroup.update()
                # отрисовка спрайтов
                self.myGroup.draw(self.screen)
                # обновление экрана
                pygame.display.flip()


class Menu(BaseScene):
    def __init__(self):
        super(Menu, self).__init__()
        self.background = BaseSprite([0, 0], ["Menu.png"])
        self.newGame = BaseSprite([50, 150], ["NewGameBtn.png"])
        self.table = BaseSprite([50, 250], ["TableBtn.png"])
        self.exit = BaseSprite([50, 350], ["ExitBtn.png"])
        self.myGroup = pygame.sprite.Group(
            self.background,
            self.newGame,
            self.table,
            self.exit
        )

    def main(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.exit.rect.collidepoint(pos):
                    self.started = False
                if self.newGame.rect.collidepoint(pos):
                    self.started = False
                    gameScene = GameScene()
                    gameScene.start()
        pygame.display.flip()


class GameScene(BaseScene):
    def __init__(self):
        super(GameScene, self).__init__()
        self.water = BaseSprite([0, self.levelConstants.Water + 50], ["Water.png"])
        self.sand = BaseSprite([0, self.levelConstants.Bottom + 40], ["Bottom.png"])
        self.sky = BaseSprite([0, 0], ["Sky.png"])
        self.raft = Raft([200, self.levelConstants.Water], ["Raft1.png"])
        self.player = Player([250, self.levelConstants.Water], ["1.png"])
        self.shark = Shark([0, 250], ["Shark1.png", "Shark2.png"])
        self.stone = Stone([100, self.levelConstants.Bottom], ["Stone.png"])
        self.wood = Wood([300, self.levelConstants.Bottom], ["Wood.png"])
        self.myGroup = pygame.sprite.Group(
            self.sky,
            self.water,
            self.sand,
            self.player,
            self.shark,
            self.stone,
            self.wood,
            self.raft
        )

    def main(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.started = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # выохд во ESCAPE
                    self.started = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
        if not self.paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.moveLeft(5)
            if keys[pygame.K_RIGHT]:
                self.player.moveRight(5)
            if keys[pygame.K_UP]:
                self.player.moveUp(5)
            if keys[pygame.K_DOWN]:
                self.player.modeDown(5)
            if self.player.checkCollision(self.shark):
                self.player.health -= 1

            self.player.swimming = self.player.checkCollision(self.water)
            self.player.stand = self.player.checkCollision(self.raft) or self.player.checkCollision(self.sand)
            stoneCollected = False
            woodCollected = False
            if self.player.checkCollision(self.stone):
                self.player.stone += 1
                stoneCollected = True
                self.stone.moveRight(500)
            if self.player.checkCollision(self.wood):
                self.player.wood += 1
                woodCollected = True
                self.wood.moveRight(500)
            self.player.drawStatus(self.screen)

            if stoneCollected == True and self.seconds % 3 == 0:
                stoneCollected = False
                self.stone.setCoords(random.randint(50, 500), 400)
            if woodCollected == True and self.seconds % 3 == 0:
                woodCollected = False
                self.wood.setCoords(random.randint(50, 500), 400)

            if self.player.health == 0:
                gameOver = GameOver()
                gameOver.start()
                self.started = False


class GameOver(BaseScene):
    def __init__(self):
        super(GameOver, self).__init__()
        self.over = BaseSprite([0, 0], ["GameOver.png"])
        self.myGroup = pygame.sprite.Group(self.over)

    def main(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.started = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # выохд во ESCAPE
                    self.started = False
        pygame.display.flip()

if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load('Oxygene.mp3')
    pygame.mixer.music.play(-1)
    menuScene = Menu()
    menuScene.start()
    pygame.quit()
