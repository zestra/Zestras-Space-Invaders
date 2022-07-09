import pygame, pgzero, pgzrun
import math, random

BLACK = (0, 0, 0)
BLUE = (0, 155, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (128, 0, 0)

DARK_BLUE = (0, 100, 200)
BRIGHT_BLUE = (100, 255, 355)
PALE_BLUE = (0, 35, 135)

DARK_GREY = (50, 50, 50)
DARKER_GREY = (10, 10, 10)

WIDTH = 1920
HEIGHT = 1050

top_left_x = WIDTH / 2
top_left_y = HEIGHT / 2

cars = []

car_images = {"them_ship": ["them_ship", "them_ship2", "them_ship3", "them_ship4", "them_ship5", "them_ship6", "them_ship7", "them_ship8"],
              "you_ship": ["you_ship", "you_ship2", "you_ship3", "you_ship4", "you_ship5", "you_ship6", "you_ship7", "you_ship8"],
              "us_ship": ["us_ship", "us_ship2", "us_ship3", "us_ship4", "us_ship5", "us_ship6", "us_ship7", "us_ship8"]}

rule = 1
game_over = False


class ManualCar:
    def __init__(self, code, type, images, x, y):
        self.code = code
        self.type = type

        self.images = images
        self.image = self.images[0]

        self.x = x + top_left_x
        self.y = y + top_left_y

        self.velocity = 0

        self.car = Actor(self.image, center=(self.x, self.y))

        self.car2 = Actor(self.image, center=(self.x, self.y))

        self.shield = Actor("shield2", center=(self.x, self.y))

        self.trace = [  # parameters: x, y, angle
        ]

        self.run = True

        self.shield_on = True

    def update(self):

        if self.run is not True:
            return

        # Moving the car
        if keyboard.left:
            self.car.angle += 10
            self.shield.angle = self.car.angle
        elif keyboard.right:
            self.car.angle -= 10
            self.shield.angle = self.car.angle


        if keyboard.up and self.velocity <= 5:
            self.velocity += 1
        elif keyboard.down and self.velocity >= -5:
            self.velocity -= 1

        self.car.x -= self.velocity * math.cos(math.radians(self.car.angle - 90))
        self.shield.x = self.car.x
        self.x = self.car.x

        self.car.y += self.velocity * math.sin(math.radians(self.car.angle - 90))
        self.shield.y = self.car.y
        self.y = self.car.y

        # Magic space effect
        if (self.x > WIDTH or self.x < 0) \
                or (self.y > HEIGHT or self.y < 0):

            if self.x > WIDTH:
                self.car.x = 0
                self.x = 0
            elif self.x < 0:
                self.car.x = WIDTH
                self.x = WIDTH

            if self.y > HEIGHT:
                self.car.y = 0
                self.y = 0
            elif self.y < 0:
                self.car.y = HEIGHT
                self.y = HEIGHT

        # Check collision
        self.check_collision()

        # Car fading trail effect
        if len(self.trace) > len(self.images) - 1:
            del self.trace[0]
        self.trace.append([self.x, self.y, self.car.angle])

    def check_collision(self):
        global cars

        if self.run is False:
            return

        collided = False
        index = 0
        for car in cars:
            if car.code != self.code and car.run is True:
                # if (car.x == self.car.x) and (car.y == self.car.y):  # If car too near another car...
                if (car.x - 10 < self.car.x < car.x + 10) and (car.y - 20 < self.car.y < car.y + 20):
                    # ... there has been a collision.
                    car.run = False  # Destroy both cars.
                    self.run = False
                    collided = True

                    sounds.collision.play()  # Run sound effect
            if collided:
                break
            index += 1


    def draw(self):

        if self.run is not True:
            return

        # if self.shield_on:
        #     self.shield.draw()
        self.car.draw()

        index = len(self.images) - 1
        for info in self.trace:
            self.car2.x = int(info[0])
            self.car2.y = int(info[1])
            self.car2.image = self.images[index]
            self.car2.angle = info[2]
            self.car2.draw()
            index -= 1


class AutoCar(ManualCar):
    def __init__(self, code, type, images, x, y):
        self.code = code
        self.type = type

        self.images = images
        self.image = self.images[0]

        self.x = x + top_left_x
        self.y = y + top_left_y

        self.velocity = 5

        self.car = Actor(self.image, center=(self.x, self.y))

        self.car2 = Actor(self.image, center=(self.x, self.y))

        self.shield = Actor("shield2", center=(self.x, self.y))

        self.trace = [  # parameters: x, y, angle
        ]

        self.run = True

        self.shield_on = True
    def update(self):

        if self.run is not True:
            return

        target = None

        distance_from_target = 10000
        if self.type == "us":
            kind = ["them"]
        elif self.type == "them":
            kind = ["us"]
        elif self.type == "any":
            kind = ["them", "us", "any"]
        for car in cars:
            if car.run and car.type in kind and car.code != self.code:
                distance_from_target2 = math.sqrt(((car.x - self.x) ** 2) + ((car.y - self.y) ** 2))
                if distance_from_target2 < distance_from_target:
                    distance_from_target = distance_from_target2
                    target = car

        if target is None:
            return

        if (target.x - self.x) != 0:
            angle_to_target = math.degrees(math.atan2((target.y - self.y), (target.x - self.x))) + 90
        else:
            angle_to_target = 0

        self.car.angle = -angle_to_target
        self.shield.angle = self.car.angle

        self.car.x += self.velocity * math.cos(math.radians(angle_to_target - 90))
        self.shield.x = self.car.x
        self.x = self.car.x

        self.car.y += self.velocity * math.sin(math.radians(angle_to_target - 90))
        self.shield.y = self.car.y
        self.y = self.car.y

        # MAGIC SPACE EFFECT
        if (self.x > WIDTH or self.x < 0) \
                or (self.y > HEIGHT or self.y < 0):

            if self.x > WIDTH:
                self.car.x = 0
                self.x = 0
            elif self.x < 0:
                self.car.x = WIDTH
                self.x = WIDTH

            if self.y > HEIGHT:
                self.car.y = 0
                self.y = 0
            elif self.y < 0:
                self.car.y = HEIGHT
                self.y = HEIGHT

        # CAR FADING TRAIL EFFECT
        if len(self.trace) > len(self.images) - 1:
            del self.trace[0]
        self.trace.append([self.x, self.y, self.car.angle])

        # Check collision
        self.check_collision()


def initialize():
    global cars

    cars.append(ManualCar(0, "us", car_images["you_ship"], 0, 0))

    for i in range(0, 5):
        # cars.append(AutoCar(len(cars), "n", car_images["red"], random.choice([int(-top_left_x) + 100, int(top_left_x) - 100]),
        #                     random.randrange(int(-top_left_y), int(top_left_y), 1)))
        # cars.append(AutoCar(len(cars), "n", car_images["red"], random.randint(-top_left_x, top_left_x),
        #                     random.randint(-top_left_y, top_left_y)))
        cars.append(AutoCar(len(cars), "us", car_images["us_ship"], random.randint(-top_left_x, top_left_x),
                            500))
        # cars[len(cars) - 1].velocity = 1

    for i in range(0, 20):
        # cars.append(AutoCar(len(cars), "y", car_images["green"], random.choice([int(-top_left_x) + 100, int(top_left_x) - 100]),
        #                     random.randrange(int(-top_left_y), int(top_left_y), 1)))
        # cars.append(AutoCar(len(cars), "y", car_images["green"], random.randint(-top_left_x, top_left_x),
        #                     random.randint(-top_left_y, top_left_y)))
        cars.append(AutoCar(len(cars), "them", car_images["them_ship"], random.randint(-top_left_x, top_left_x),
                            -500))
        # cars[len(cars) - 1].velocity = 1


initialize()

color = (0, 0, 255)
index = 0
dim = False


def draw():
    global color, index, dim

    # Background
    screen.clear()

    draw_image(images.background, top_left_x, top_left_y)

    # Fading text effect
    if dim is False:
        index += 1
        if index == (255 / 5):
            dim = True
    else:
        index -= 1
        if index == 0:
            dim = False
    color = (0, 0, 255 - 5 * index)

    if game_over:
        show_text("GAME OVER", -450, -100, color, 200)
        show_text("press space to try again", -210, 50, color, 45)
        return

    show_text("Press UP and DOWN to ACCELERATE \n Press RIGHT and LEFT to TURN", -top_left_x + 50, -top_left_y + 50,
              color, 35)

    # Show cars
    for car in cars:
        car.draw()


def update():
    global game_over
    global cars

    if game_over:
        if keyboard.space:
            cars = []
            initialize()
            game_over = False
        return

    for car in cars:
        car.update()

    # If heroes are all killed, let the enemies kill one another.
    counter = 0
    for car in cars:
        if car.run and car.type == "us":
            counter += 1
    if counter == 0:
        for car in cars:
            if car.run and car.type == "them":
                car.type = "any"

    # If hero is alive, and enemies are all dead, game over.
    if counter > 0:
        counter2 = 0
        for car in cars:
            if car.run and car.type == "them":
                counter2 += 1
        if counter2 == 0:
            game_over = True

    # If all cars are dead, game over.
    counter3 = 0
    for car in cars:
        if car.run:
            counter3 += 1
    if counter3 in [0, 1]:
        game_over = True




def draw_image(image, x, y):
    screen.blit(image,
                (top_left_x + x - image.get_width(),
                 top_left_y + y - image.get_height()))


def draw_rect(x, y,
              width, height,
              colour=BLACK,
              outline=None):
    if outline is not None:
        BOX2 = Rect((top_left_x + x - int(width / 2) - 2, top_left_y + y - int(height / 2) - 2),
                    (width + 4, height + 4)
                    )
        screen.draw.rect(BOX2, outline)

    if colour is not None:
        BOX = Rect((top_left_x + x - int(width / 2), top_left_y + y - int(height / 2)),
                   (width, height)
                   )
        screen.draw.filled_rect(BOX, colour)


def show_text(text_to_show, x, y,
              colour=WHITE,
              size=75):
    screen.draw.text(text_to_show,
                     (top_left_x + x, top_left_y + y),
                     fontsize=size, color=colour)


def theme():
    sounds.theme.play()


theme()
clock.schedule_interval(theme, 96)


pgzrun.go()
