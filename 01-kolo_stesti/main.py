import math
import random

import pygame
from PIL import Image, ImageDraw, ImageFont

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('../opensans.ttf', 20)
clock = pygame.time.Clock()
pygame.display.set_caption('Rota Fortunae')
screen = pygame.display.set_mode([1000, 1000])


class Wheel:
    def __init__(self, parent):
        self.parent = parent
        self.wheel_diameter = 600
        self.wheel = self.fnc_generate_wheel()

    def fnc_update(self):
        image = pygame.image.fromstring(self.wheel[2], self.wheel[1], self.wheel[0])
        self.fnc_draw(image)

    def fnc_draw(self, image):
        rotated_image = pygame.transform.rotate(image, self.parent.rotation)
        new_rect = rotated_image.get_rect(center=screen.get_rect().center)
        screen.blit(rotated_image, new_rect)

    def fnc_generate_wheel(self):
        radius = 360 / len(self.parent.file)

        __image = Image.new("RGBA", (self.wheel_diameter, self.wheel_diameter))
        __draw = ImageDraw.Draw(__image)

        for x in range(len(self.parent.file)):
            __draw.pieslice((0, 0, self.wheel_diameter - 1, self.wheel_diameter - 1), x * radius + self.parent.rotation, (x + 1) * radius + self.parent.rotation, fill=(random.randint(50, 200),random.randint(50, 200),random.randint(50, 200)))

        mode = __image.mode
        size = __image.size
        data = __image.tobytes()

        return mode, size, data, radius


class Options:
    def __init__(self, parent):
        self.parent = parent

    def fnc_update(self):
        for x in range(len(self.parent.file)):
            __text = font.render(self.parent.file[x], True, (255, 255, 255))
            __text = pygame.transform.rotate(__text, -self.parent.wheel.wheel[3] * (x + 1) + self.parent.rotation + 90)
            __text_rect = __text.get_rect(center=screen.get_rect().center)

            __angle_rad = math.radians(180 - self.parent.wheel.wheel[3] * (x + 1) + self.parent.rotation + 90)
            __text_rect.centerx += 200 * math.sin(__angle_rad)
            __text_rect.centery += 200 * math.cos(__angle_rad)
            self.fnc_draw(__text, __text_rect)

    def fnc_draw(self, __text, __text_rect):
        screen.blit(__text, __text_rect)


class App:
    def __init__(self):
        self.running = True
        self.rotating = False
        self.rotation = 0
        self.slow_down = 0
        self.result = ''
        self.file = fnc_read_file('input.txt')
        self.wheel = Wheel(self)
        self.options = Options(self)
        self.rotating = False
        self.text_surface = font.render('text button', True, (255, 255, 255))
        self.button_rect = self.text_surface.get_rect(topleft=(200, 200))

    def fnc_update(self):
        if self.rotating:
            self.fnc_spin()
        self.wheel.fnc_update()
        self.options.fnc_update()
        self.fnc_draw()

    def fnc_draw(self):
        self.text_surface = font.render('Spin the wheel', True, (255, 255, 255))
        self.button_rect = self.text_surface.get_rect(center=(500, 900))
        screen.blit(self.text_surface, self.button_rect)
        pygame.draw.line(screen, (255, 255, 255), (1000, 500), (850, 500), 5)
        if self.result != '':
            screen.blit(font.render(f'You got: {self.result}', True, (255, 255, 255)), (100, 800))

    def fnc_spin(self):
        if (random.randint(0, 200)) < 199 and self.slow_down == 0:
            self.rotation += 20
            pass
        elif self.slow_down <= 20:
            self.rotation += 20 - self.slow_down
            self.slow_down += .5
        else:
            self.rotating = False
            self.slow_down = 0
            self.fnc_print_result()

    def fnc_print_result(self):
        __res = ((self.rotation % 360) / (360 / len(self.file)))
        if __res > 5:
            __res = math.ceil(abs(__res) - 5)
        else:
            __res = math.ceil(__res + 4)
        print(f'You got: {self.file[__res - 1]}')
        self.result = self.file[__res - 1]


def fnc_read_file(file):
    with open(file, encoding='utf8') as f:
        t = f.read().split('\n')
        return t


def main():

    app = App()

    while app.running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if app.running:
                        if app.button_rect.collidepoint(event.pos):
                            app.rotating = True
            if event.type == pygame.QUIT:
                app.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    app.running = False

        screen.fill((20, 20, 20))

        app.fnc_update()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
