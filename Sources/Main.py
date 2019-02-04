import datetime
import math
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
        if self.images.__len__() > 0:
            self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.location = location
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


class Label(BaseSprite):
    def __init__(self, title, size, location):
        font = pygame.font.Font("SegoeUI.ttf", size)
        text = font.render(title, True, (255, 255, 255))
        self.image = text
        self.rect = self.image.get_rect()
        super(Label, self).__init__(location, [])
        self.images = [self.image]


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
        placeholder = [10, 10]
        titles = [("Здоровье:", self.health), ("Дерево:", self.wood), ("Камень:", self.stone), ("Stand:", self.stand),
                  ("Swim:", self.swimming)]
        # for i in range(0, titles.__len__()):
        #     Label(screen, titles[i][0] + str(titles[i][1]), 25, placeholder)
        #     placeholder[1] += 30


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
        self.DEBUG = False
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
                self.seconds += (ticks % self.FPS) / 1000
                # обновление спрайтов
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
                if self.table.rect.collidepoint(pos):
                    self.started = False
                    table = Table()
                    table.start()
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
        self.labelWood1 = Label("Бревна, нужны", 12, [350, 350])
        self.labelWood2 = Label("для апгрейда корабля", 12, [350, 370])
        self.labelWood3 = Label("собирайте их!", 12, [350, 390])
        self.labelStone1 = Label("Камни тоже!", 12, [50, 390])
        self.labelControls1 = Label("Нажните P для паузы", 12, [170, 10])
        self.labelControls2 = Label("Нажните U для апгрейда корабля", 12, [170, 30])
        self.labelControls3 = Label("Нажните Esc для возврата в меню", 12, [170, 50])

        self.labelWarning1 = Label("", 12, [170, 70])

        self.labelsPlayer = []

        self.stoneCollected = False
        self.woodCollected = False
        self.stage = 0
        self.stages = [[10, 10], [20, 20]]
        self.myGroup = pygame.sprite.Group(
            self.sky,
            self.water,
            self.sand,
            self.player,
            self.shark,
            self.stone,
            self.wood,
            self.raft,
            self.labelWood1,
            self.labelWood2,
            self.labelWood3,
            self.labelStone1,
            self.labelControls1,
            self.labelControls2,
            self.labelControls3

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
            if keys[pygame.K_ESCAPE]:
                self.started = False
                menuScene = Menu()
                menuScene.start()
            if keys[pygame.K_LEFT]:
                self.player.moveLeft(5)
            if keys[pygame.K_RIGHT]:
                self.player.moveRight(5)
            if keys[pygame.K_UP]:
                self.player.moveUp(5)
            if keys[pygame.K_DOWN]:
                self.player.modeDown(5)
            if keys[pygame.K_u]:
                if self.player.wood >= self.stages[self.stage][0] and self.player.stone >= self.stages[self.stage][1]:
                    self.player.wood -= self.stages[self.stage][0]
                    self.player.stone -= self.stages[self.stage][1]
                    self.stage += 1
                    self.myGroup.remove([self.raft])
                    self.raft = Raft([200, self.levelConstants.Water - 50], ["Raft" + str(self.stage + 1) + ".png"])
                    self.myGroup.add(self.raft)
                else:
                    if self.player.wood < self.stages[self.stage][0] or \
                            self.player.stone < self.stages[self.stage][1]:
                        self.myGroup.remove(self.labelWarning1)
                        self.labelWarning1 = Label(
                            "Не хватает дерева:{0} камня:{1}".format(self.stages[self.stage][0] - self.player.wood,
                                                                     self.stages[self.stage][1] - self.player.stone),
                            12, self.labelWarning1.location)
                        self.myGroup.add(self.labelWarning1)

            if self.player.checkCollision(self.shark):
                self.player.health -= 1

            self.player.swimming = self.player.checkCollision(self.water)
            self.player.stand = self.player.checkCollision(self.raft) or self.player.checkCollision(self.sand)

            if self.player.checkCollision(self.stone):
                self.player.stone += 1
                self.stoneCollected = True
                self.stone.moveRight(500)
            if self.player.checkCollision(self.wood):
                self.player.wood += 1
                self.woodCollected = True
                self.wood.moveRight(500)

            placeholder = [10, 10]
            titles = [("Здоровье:", self.player.health), ("Дерево:", self.player.wood), ("Камень:", self.player.stone)]
            for i in range(0, self.labelsPlayer.__len__()):
                self.myGroup.remove(self.labelsPlayer[i])
            for i in range(0, titles.__len__()):
                label = Label(titles[i][0] + str(titles[i][1]), 20, placeholder)
                placeholder[1] += 30
                self.labelsPlayer.append(label)
                self.myGroup.add(label)

            if self.stage == 2:
                self.started = False
                success = Success(self.seconds)
                success.start()
            self.player.drawStatus(self.screen)

            if self.seconds > 5:
                self.myGroup.remove(self.labelWood1)
                self.myGroup.remove(self.labelWood2)
                self.myGroup.remove(self.labelWood3)
                self.myGroup.remove(self.labelStone1)

            if math.floor(self.seconds) % 2 == 0:
                self.myGroup.remove(self.labelWarning1)
            # print(math.floor(self.seconds))

            if self.stoneCollected == True and math.floor(self.seconds) % 3 == 0:
                self.stoneCollected = False
                self.stone.setCoords(random.randint(50, 500), 400)
            if self.woodCollected == True and math.floor(self.seconds) % 3 == 0:
                self.woodCollected = False
                self.wood.setCoords(random.randint(50, 500), 400)

            if self.player.health == 0:
                gameOver = GameOver()
                gameOver.start()
                self.started = False


class GameOver(BaseScene):
    def __init__(self):
        super(GameOver, self).__init__()
        self.background = BaseSprite([0, 0], ["GameOver.png"])
        self.tryAgain = BaseSprite([50, 300], ["TryAgainBtn.png"])
        self.myGroup = pygame.sprite.Group(
            self.background,
            self.tryAgain
        )

    def main(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.started = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # выохд во ESCAPE
                    self.started = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.tryAgain.rect.collidepoint(pos):
                    self.started = False
                    gameScene = GameScene()
                    gameScene.start()
        pygame.display.flip()


class Success(BaseScene):
    def __init__(self, score):
        super(Success, self).__init__()
        self.score = score
        self.background = BaseSprite([0, 0], ["Success.png"])
        self.tryAgain = BaseSprite([50, 300], ["TryAgainBtn.png"])
        self.labelScore = Label("{0:.2f} секунд".format(score), 25, [200, 200])
        self.myGroup = pygame.sprite.Group(
            self.background,
            self.tryAgain,
            self.labelScore
        )

    def main(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.started = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # выохд во ESCAPE
                    self.started = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.tryAgain.rect.collidepoint(pos):
                    self.started = False
                    with open("table.txt", "a") as myfile:
                        now = datetime.datetime.now()
                        myfile.write(
                            "дата:{0}.{1}.{2} счет(секунды):{3:.2f}\n".format(now.day, now.month, now.year, self.score))
                    gameScene = GameScene()
                    gameScene.start()
        pygame.display.flip()


class Table(BaseScene):
    def __init__(self):
        super(Table, self).__init__()
        self.background = BaseSprite([0, 0], ["Table.png"])
        self.back = BaseSprite([50, 400], ["BackToMenuBtn.png"])
        self.myGroup = pygame.sprite.Group(
            self.background,
            self.back
        )

    def main(self):
        with open("table.txt") as f:
            content = f.readlines()
        placeholder = [30, 150]
        for i in range(0, content.__len__()):
            self.myGroup.add(Label(content[i], 20, placeholder))
            placeholder[1] += 20
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.started = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.back.rect.collidepoint(pos):
                    self.started = False
                    Menu().start()
        pygame.display.flip()


if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load('Oxygene.mp3')
    pygame.mixer.music.play(-1)
    menuScene = Menu()
    menuScene.start()
    pygame.quit()
