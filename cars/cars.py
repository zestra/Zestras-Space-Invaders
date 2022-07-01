import pygame, pgzero, pgzrun
import math, random

BLACK = (0, 0, 0)
BLUE = (0, 155, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (128, 0, 0) #

DARK_BLUE = (0, 100, 200)
BRIGHT_BLUE = (100, 255, 355)
PALE_BLUE = (0, 35, 135)

DARK_GREY = (50, 50, 50)
DARKER_GREY = (10, 10, 10)

WIDTH = 1920
HEIGHT = 1050

top_left_x = WIDTH / 2
top_left_y = HEIGHT / 2

cars1 = {}
cars2 = {}
cars = {}

info = {}

car_images = ["blue", "green", "red"]


class ManualCar:
    def __init__(self, name, images, x, y):
        self.name = name

        self.images = images
        self.image = self.images[0]

        self.x = x + top_left_x
        self.y = y + top_left_y

        self.velocity = 0

        self.car = Actor(self.image, center=(self.x, self.y))

        self.car2 = Actor(self.image, center=(self.x, self.y))

        self.trace = [  # parameters: x, y, angle
                     ]

    def update(self):
        global cars, cars1

        if keyboard.left:
            self.car.angle += 10
        elif keyboard.right:
            self.car.angle -= 10

        if keyboard.up:
            self.velocity += 0.5
        elif keyboard.down:
            self.velocity -= 0.5

        self.car.x -= self.velocity*math.cos(math.radians(self.car.angle - 90))
        self.x -= self.velocity*math.cos(math.radians(self.car.angle - 90))

        self.car.y += self.velocity*math.sin(math.radians(self.car.angle - 90))
        self.y += self.velocity*math.sin(math.radians(self.car.angle - 90))

        if (self.x > WIDTH or self.x < 0)\
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

        # image2 = random.choice(car_images)
        # while image2 == self.image:
        #     image2 = random.choice(car_images)
        # self.image = image2
        # angle = self.car.angle
        # self.car.image = self.image
        # self.car.angle = angle

        if len(self.trace) > 5:
            del self.trace[0]
        self.trace.append([self.x, self.y, self.car.angle])

        return self.x, self.y


    def draw(self):
        self.car.draw()
        show_text(str(self.velocity), self.x - top_left_x + 3, self.y - top_left_y - 50, WHITE, 25)

        if int(self.velocity) <= 75:
            index = len(self.images) - 1
            for info in self.trace:
                x, y, angle = info[0], info[1], info[2]
                self.car2.x = x
                self.car2.y = y
                self.car2.image = self.images[index]
                self.car2.angle = angle
                self.car2.draw()

                index -= 1


cars["Car 101"] = ManualCar("Car 101", ["blue",
                                      "blue2",
                                      "blue3",
                                      "blue4",
                                      "blue5",
                                      "blue6"],
                           0, 0)
cars1["Car 101"] = cars["Car 101"]
info["Car 101"] = [0, 0]

color = (0,  0, 255)
index = 0
dim = False

def draw():
    global color, index, dim

    screen.clear()

    draw_image(images.background, top_left_x, top_left_y)
    # screen.fill(BLACK)
    #
    # for y in range(HEIGHT):
    #     for x in range(0, 10*int(WIDTH/30), 10):
    #         if (100 - int(x/5)) >= 0:
    #             colour = (0, 0, 100 - int(x/5))
    #         else:
    #             colour = (0, 0, 0)
    #         draw_rect(x - top_left_x, y - top_left_y, 30, 30, colour, None)
    #
    #     for x in range(1400, 1400 + 10*int(WIDTH/30), 10):
    #         if (int((x - 1400)/5)) <= 255:
    #             colour = (int((x - 1400)/5), 0, 0)
    #         else:
    #             colour = (0, 0, 0)
    #         draw_rect(x - top_left_x, y - top_left_y, 30, 30, colour, None)

    if dim is False:
        index += 1
        if index == (255 / 5):
            dim = True
    else:
        index -= 1
        if index == 0:
            dim = False
    color = (0, 0, 255 - 5 * index)
    show_text("CRAZY SPACE", -500, -100, color, 200)

    show_text("Press UP and DOWN to ACCELERATE \n Press RIGHT and LEFT to TURN", -top_left_x + 50, -top_left_y + 50, color, 35)

    for car in cars:
        cars[car].draw()


def update():
    global info

    for name in info:
        x, y = cars[name].update()
        info[name] = [x, y]

    pass


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

# for car in cars:
#     clock.schedule_interval(cars[car].update, 0.1)

pgzrun.go()