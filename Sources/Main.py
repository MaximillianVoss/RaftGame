import sys, os, pygame, random


def GetRootPath():
    return os.path.dirname(os.path.abspath(__file__))[:-len("Sources")]


# Функция отображения картинок
def loadImage(name, colorkey=None):
    # Добавляем к имени картинки имя папки
    fullname = GetRootPath() + "Resources\\" + name
    # Загружаем картинку
    image = pygame.image.load(fullname)
    image = image.convert()
    # Если второй параметр =-1 делаем прозрачным
    # цвет из точки 0,0
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image


def checkCollision(sprite1, sprite2):
    return pygame.sprite.collide_rect(sprite1, sprite2)


class Background(pygame.sprite.Sprite):
    def __init__(self, imgFileName, location):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load(loadImage(image_file))
        self.images = []
        self.images.append(loadImage(imgFileName))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.images = []
        # анимаия
        self.images.append(loadImage('1.png'))
        self.images.append(loadImage('2.png'))
        # размер изображений 50х50
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 50, 50)
        self.health = 100
        self.wood = 0
        self.stone = 0

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveUp(self, pixels):
        self.rect.y -= pixels

    def modeDown(self, pixels):
        self.rect.y += pixels


class Shark(pygame.sprite.Sprite):
    def __init__(self, location):
        super(Shark, self, ).__init__()
        self.images = []
        # анимаия
        self.images.append(loadImage('Shark1.png'))
        self.images.append(loadImage('Shark2.png'))
        # размер изображений 50х50
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.direction = 1

    def update(self):
        if self.rect.x < 0 or self.rect.x > 420:
            self.direction *= -1
            self.index += 1
        self.moveRight(5 * self.direction)
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveUp(self, pixels):
        self.rect.y -= pixels

    def modeDown(self, pixels):
        self.rect.y += pixels


class Wood(pygame.sprite.Sprite):
    def __init__(self, location):
        super(Wood, self).__init__()
        self.images = []
        # анимаия
        self.images.append(loadImage('wood.png'))
        # размер изображений 50х50
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 50, 50)
        self.rect.left, self.rect.top = location

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


class Stone(pygame.sprite.Sprite):
    def __init__(self, location):
        super(Stone, self).__init__()
        self.images = []
        # анимаия
        self.images.append(loadImage('stone.png'))
        # размер изображений 50х50
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 50, 50)
        self.rect.left, self.rect.top = location

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("freesansbold.ttf", size)
        self.textSurf = self.font.render(text, 1, color)
        self.image = pygame.Surface((width, height))
        self.drawText(text, size, color, width, height)
        self.rect = pygame.Rect(5, 5, width, height)

    def drawText(self, text, size, color, width, height):
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width / 2 - W / 2, height / 2 - H / 2])

    def update(self, text=""):
        self.drawText(text, self.size, self.color, self.width, self.height)


def drawStatus(player, screen):
    font = pygame.font.Font("freesansbold.ttf", 25)
    healthTitle = font.render("Здоровье: " + str(player.health), True, (255, 255, 255))
    woodTitle = font.render("Дерево: " + str(player.wood), True, (255, 255, 255))
    stoneTitle = font.render("Камень: " + str(player.stone), True, (255, 255, 255))
    screen.blit(healthTitle, [10, 10])
    screen.blit(woodTitle, [10, 40])
    screen.blit(stoneTitle, [10, 70])
    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(60)

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    player = Player()
    shark = Shark([0, 300])
    stone = Stone([100, 400])
    wood = Wood([300, 400])
    healthTitle = Text(str(player.health), 25, (0, 0, 0), 100, 100)
    background = Background('background_image.png', [0, 0])
    my_group = pygame.sprite.Group(background, player, shark, stone, wood)

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        carryOn = True
        clock = pygame.time.Clock()

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

            if checkCollision(player, shark):
                player.health -= 1
            if checkCollision(player, stone):
                player.stone += 1
            if checkCollision(player, wood):
                player.wood += 1
            drawStatus(player, screen)
            # обновление спрайтов
            my_group.update()
            # отрисовка спрайтов
            my_group.draw(screen)
            # обновление экрана
            pygame.display.flip()
            # число кадров в сек.
            clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    main()
