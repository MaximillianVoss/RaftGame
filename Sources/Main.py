import sys, os, pygame, random
import time
from enum import Enum


def GetRootPath():
    return os.path.dirname(os.path.abspath(__file__))[:-len("Sources")]


class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4
    NoDirection = 5


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

    # Функция отображения картинок
    def loadImage(selft, name, colorkey=None):
        # Добавляем к имени картинки имя папки
        fullname = GetRootPath() + "Resources\\" + name
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

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        if not self.stand:
            self.modeDown(2)

    def drawStatus(self, screen):
        font = pygame.font.Font("freesansbold.ttf", 25)
        placeholder = [10, 10]
        titles = [("Здоровье:", self.health), ("Дерево:", self.wood), ("Камень:", self.stone)]
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    player = Player([250, 250], ["1.png"])
    shark = Shark([0, 300], ["Shark1.png", "Shark2.png"])
    stone = Stone([100, 400], ["Stone.png"])
    wood = Wood([300, 400], ["Wood.png"])
    raft = Raft([200, 125], ["Raft1.png"])
    background = Background([0, 0], ["background_image.png"])
    my_group = pygame.sprite.Group(background, player, shark, stone, wood, raft)

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        carryOn = True
        stoneCollected = False
        woodCollected = False
        clock = pygame.time.Clock()
        timerSeconds = 0
        while carryOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    carryOn = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # выохд во ESCAPE
                        carryOn = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.moveLeft(5)
            if keys[pygame.K_RIGHT]:
                player.moveRight(5)
            if keys[pygame.K_UP]:
                player.moveUp(5)
            if keys[pygame.K_DOWN]:
                player.modeDown(5)
            if player.checkCollision(shark):
                player.health -= 1
            if player.checkCollision(stone):
                player.stone += 1
                stoneCollected = True
                stone.moveRight(500)
            if player.checkCollision(wood):
                player.wood += 1
                woodCollected = True
                wood.moveRight(500)
            player.drawStatus(screen)

            if stoneCollected == True and timerSeconds % 300 == 0:
                stoneCollected = False
                stone.setCoords(random.randint(50, 500), 400)
            if woodCollected == True and timerSeconds % 300 == 0:
                woodCollected = False
                wood.setCoords(random.randint(50, 500), 400)
            # обновление спрайтов
            my_group.update()
            # отрисовка спрайтов
            my_group.draw(screen)
            # обновление экрана
            pygame.display.flip()
            # число кадров в сек.
            clock.tick(60)
            timerSeconds += 1
        pygame.quit()


if __name__ == '__main__':
    main()
