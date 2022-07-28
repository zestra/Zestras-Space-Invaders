import pygame, pgzero, pgzrun
import math, random, time

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
lasers = []

car_images = {"them_ship": ["them_ship", "them_ship2", "them_ship3", "them_ship4", "them_ship5", "them_ship6", "them_ship7", "them_ship8"],
              "you_ship": ["you_ship", "you_ship2", "you_ship3", "you_ship4", "you_ship5", "you_ship6", "you_ship7", "you_ship8"],
              "us_ship": ["us_ship", "us_ship2", "us_ship3", "us_ship4", "us_ship5", "us_ship6", "us_ship7", "us_ship8"]}

norm_shooter = False
still_shooter = False
slider_shooter = False

game_over = False

background = {"start": [images.start1, images.start2],
              "play": [images.play],
              "end": [images.end]}
background["start"] = random.choice(background["start"])


class State:
    def __init__(self):
        self.states = ["start", "play", "end"]
        self.state = self.states[0]

state = State()


class ManualCar:
    def __init__(self, code, type, image2, images, x, y):
        self.code = code
        self.type = type

        self.image2 = image2
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
        self.timer = 0

    def update(self):

        if self.run is not True:
            return

        if self.timer != 0:
            self.timer += 1
            if self.timer == 10:
                self.timer = 0

        # Moving the car

        if slider_shooter is False:
            if keyboard.left:
                if still_shooter:
                    self.car.angle += 1
                else:
                    self.car.angle += 10
                self.shield.angle = self.car.angle
            elif keyboard.right:
                if still_shooter:
                    self.car.angle -= 1
                else:
                    self.car.angle -= 10
                self.shield.angle = self.car.angle
        else:
            if keyboard.left:
                self.car.x -= 10
                self.x = self.car.x
            if keyboard.right:
                self.car.x += 10
                self.x = self.car.x

        if keyboard.up and self.velocity <= 15:
            self.velocity += 1
        elif keyboard.down and self.velocity >= -15:
            self.velocity -= 1

        if still_shooter is False and slider_shooter is False:
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

        # Lasers
        if keyboard.space and self.timer == 0:
            lasers.append(Laser(len(lasers), "you", self.x, self.y, self.car.angle, self.velocity, False))
            sounds.player_laser.play()
            self.timer = 1

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
    def __init__(self, code, type, image2, images, x, y):
        self.code = code
        self.type = type

        self.image2 = image2
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
        self.timer = 0

    def update(self):

        if self.run is not True:
            return

        if self.timer != 0:
            self.timer += 1
            if self.timer == 15:
                self.timer = 0

        target = None

        distance_from_target = 20000
        if self.type in ["us", "you"]:
            kind = ["them"]
        elif self.type == "them":
            kind = ["us", "you"]
        elif self.type == "any":
            kind = ["them", "us", "you", "any"]
        for car in cars:
            if (car.run) and (self.run) and (car.type in kind) and (car.code != self.code):
                distance_from_target2 = math.sqrt(((car.x - self.x) ** 2) + ((car.y - self.y) ** 2))
                if distance_from_target2 < distance_from_target:
                    distance_from_target = distance_from_target2
                    target = car

        if target is None:
            return

        if (target.x - self.x) != 0:
            angle_to_target = int((math.degrees(math.atan2((target.y - self.y), (target.x - self.x))) + 90)/10) * 10
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
        # Lasers
        if distance_from_target <= 175 and self.timer == 0:
            if self.type == "us":
                lasers.append(Laser(len(lasers), "you", self.x, self.y, self.car.angle, self.velocity, False))
                sounds.player_laser.play()
                self.timer = 1
            elif self.type == "them":
                lasers.append(Laser(len(lasers), "them", self.x, self.y, self.car.angle, self.velocity, False))
                sounds.enemy_laser.play()
                self.timer = 1

        # CAR FADING TRAIL EFFECT
        if len(self.trace) > len(self.images) - 1:
            del self.trace[0]
        self.trace.append([self.x, self.y, self.car.angle])

        # Check collision
        self.check_collision()


class Laser:
    def __init__(self, code, type, x, y, angle, speed, auto=False):
        self.code = code
        self.type = type

        self.angle = angle
        self.x = x - 25*math.cos(math.radians(self.angle - 90))
        self.y = y + 25*math.sin(math.radians(self.angle - 90))

        self.speed = 10 + speed

        self.auto = auto

        if self.type == "you":
            self.image = "you_pellet"
            self.image2 = images.you_pellet
        elif self.type == "us":
            self.image = "us_pellet"
            self.image2 = images.us_pellet
        elif self.type == "them":
            self.image = "them_pellet"
            self.image2 = images.them_pellet
        else:
            self.image = "them_pellet"
            self.image2 = images.them_pellet

        self.laser = Actor(self.image, center=(self.x, self.y))
        self.laser.angle = self.angle

        self.run = True
        self.death_timer = random.randint(20, 50)

    def norm(self):
        self.x -= self.speed * math.cos(math.radians(self.laser.angle - 90))
        self.laser.x = self.x

        self.y += self.speed * math.sin(math.radians(self.laser.angle - 90))
        self.laser.y = self.y

        # MAGIC SPACE EFFECT
        if (self.x > WIDTH or self.x < 0) \
                or (self.y > HEIGHT or self.y < 0):

            if self.x > WIDTH:
                self.laser.x = 0
                self.x = 0
            elif self.x < 0:
                self.laser.x = WIDTH
                self.x = WIDTH

            if self.y > HEIGHT:
                self.laser.y = 0
                self.y = 0
            elif self.y < 0:
                self.laser.y = HEIGHT
                self.y = HEIGHT

    def automatic(self):
        pass

    def check_collision(self):
        global cars, lasers

        if self.run is False:
            return

        collided = False
        index = 0
        for object in cars + lasers:
            if object.run is True:
                # if (car.x == self.car.x) and (car.y == self.car.y):  # If car too near another car...
                if (object.x - int(object.image2.get_width()/2) < self.x < object.x + int(object.image2.get_width()/2)) \
                        and (object.y - int(object.image2.get_height()/2) < self.y < object.y + int(object.image2.get_height()/2))\
                        and object.code != self.code:
                    # ... there has been a collision.
                    object.run = False  # Destroy both cars.
                    self.run = False
                    collided = True

                    sounds.collision.play()  # Run sound effect
            if collided:
                break
            index += 1

    def update(self):

        if self.run is False:
            return

        self.death_timer -= 1
        if self.death_timer == 0:
            self.run = False
            return

        if self.auto is False:
            self.norm()
        else:
            self.automatic()

        self.check_collision()

    def draw(self):
        if self.run is False:
            return

        self.laser.draw()

if norm_shooter:
    cars.append(ManualCar(0, "you", images.you_ship, car_images["you_ship"], 0, 0))
elif still_shooter:
    cars.append(ManualCar(0, "you", images.you_ship, car_images["you_ship"], 0, 400))
elif slider_shooter:
    cars.append(ManualCar(0, "you", images.you_ship, car_images["you_ship"], 0, 300))


def initialize():
    global cars

    if len(cars) >= 35:
        return

    for num in range(random.randint(5, 10)):
        cars.append(AutoCar(len(cars), "them", images.them_ship, car_images["them_ship"], random.randint(-10, 10)*70, 70 - HEIGHT/2 + 75))
        cars[len(cars) - 1].velocity = 1


initialize()

color = (0, 0, 255)
index = 0
dim = False

selection = 0
options = ["NORM SHOOTER", "STILL SHOOTER", "SLIDER SHOOTER"]


def draw():
    global color, index, dim

    # Background
    screen.clear()

    if state.state == "start":
        draw_image(background["start"], top_left_x, top_left_y)

        if dim is False:
            index += 1
            if index == (255 / 5):
                dim = True
        else:
            index -= 1
            if index == 0:
                dim = False
        color = (0, 0, 255 - 5 * index)
        show_text("SPACE INVADERS", -635, -100, color, 200)
        show_text("which variation would you like to play?", -270, 15, color, 35)
        for y in range(1, len(options) + 1):
            show_text(options[y - 1], -265, y*60, color, 75)

        draw_rect(-50, (selection + 1)*60 + 20, 500, 60, None, "white")

    if state.state == "play":
        draw_image(background["play"][0], top_left_x, top_left_y)

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

        # Show cars
        for sprite in cars + lasers:
            sprite.draw()

    if state.state == "end":
        draw_image(background["end"][0], top_left_x, top_left_y)

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
        show_text("GAME OVER", -450, -100, color, 200)
        show_text("fancy another go?", -150, 15, color, 35)
        for y in range(1, len(options) + 1):
            show_text(options[y - 1], -265, y * 60, color, 75)

        draw_rect(-50, (selection + 1) * 60 + 20, 500, 60, None, "white")
        pass


def update():
    global game_over
    global cars, lasers
    global state, selection
    global norm_shooter, still_shooter, slider_shooter

    if state.state == "start":
        if keyboard.up:
            if selection == 0:
                selection = len(options) - 1
            else:
                selection -= 1
            time.sleep(0.1)

        if keyboard.down:
            if selection == len(options) - 1:
                selection = 0
            else:
                selection += 1
            time.sleep(0.1)

        if keyboard.space:
            state.state = state.states[1]

            if selection == 0:
                norm_shooter = True
            elif selection == 1:
                still_shooter = True
            elif selection == 2:
                slider_shooter = True

            if norm_shooter:
                cars.append(ManualCar(0, "you", images.you_ship, car_images["you_ship"], 0, 0))
            elif still_shooter:
                cars.append(ManualCar(0, "you", images.you_ship, car_images["you_ship"], 0, 400))
            elif slider_shooter:
                cars.append(ManualCar(0, "you", images.you_ship, car_images["you_ship"], 0, 300))

            clock.schedule_interval(initialize, 1)


    if state.state == "play":
        for sprite in cars + lasers:
            sprite.update()

        # If heroes are all killed, let the enemies kill one another.
        counter = 0
        for car in cars:
            if car.run and car.type in ["us", "you"]:
                counter += 1
        if counter == 0:
            for car in cars:
                if car.run and car.type == "them":
                    car.type = "any"
                car.velocity = 5

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

        if game_over:
            state.state = state.states[2]

            cars = []
            lasers = []

            selection = 0

            norm_shooter = False
            still_shooter = False
            slider_shooter = False

            clock.unschedule(initialize)

    if state.state == "end":
        if keyboard.up:
            if selection == 0:
                selection = len(options) - 1
            else:
                selection -= 1
            time.sleep(0.1)

        if keyboard.down:
            if selection == len(options) - 1:
                selection = 0
            else:
                selection += 1
            time.sleep(0.1)

        if keyboard.space:
            game_over = False
            state.state = state.states[1]

            if selection == 0:
                norm_shooter = True
            elif selection == 1:
                still_shooter = True
            elif selection == 2:
                slider_shooter = True

            if norm_shooter:
                cars.append(ManualCar(0, "you", images.you_ship, car_images["you_ship"], 0, 0))
            elif still_shooter:
                cars.append(ManualCar(0, "you", images.you_ship, car_images["you_ship"], 0, 400))
            elif slider_shooter:
                cars.append(ManualCar(0, "you", images.you_ship, car_images["you_ship"], 0, 300))

            initialize()
            clock.schedule_interval(initialize, 1)


def draw_image(image, x, y):
    screen.blit(image,
                (top_left_x + x - image.get_width(),
                 top_left_y + y - image.get_height()))


def draw_rect(x, y,
              width, height,
              colour=BLACK,
              outline=None):
    if outline is not None:
        BOX2 = Rect((top_left_x + x - int(width / 2) - 4, top_left_y + y - int(height / 2) - 4),
                    (width + 8, height + 8)
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
clock.schedule_interval(update, 0.1)

pgzrun.go()
