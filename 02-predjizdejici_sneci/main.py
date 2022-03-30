import time
import pygame

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('../opensans.ttf', 30)
clock = pygame.time.Clock()
pygame.display.set_caption('Snail race')
screen = pygame.display.set_mode([1500, 800])


class Snail:
    def __init__(self, parent, x, speed, file):
        self.parent = parent
        self.x = float(x) + 80
        self.y = (600 / file) * self.parent.index + (600 / file / 2 - 10)
        self.parent.index += 1
        self.width = 20
        self.height = 20
        self.speed = float(speed) * (1730 / (self.parent.max_distance))

    def fnc_update(self):
        if self.parent.race:
            self.x += (self.speed / 30)
        self.fnc_draw()

    def fnc_draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
        # screen.blit(font.render(f'mm', True, (200, 200, 200)), (self.x, self.y))


class App:
    def __init__(self):
        self.running = True
        self.race = True
        self.file = fnc_read_file('input.txt')
        self.time = float(self.file.pop(0)[0])
        self.max_distance = self.fnc_get_max_distance()
        self.timestamp = time.time()
        self.time_rem = round(time.time() - self.timestamp, 2)
        self.index = 0
        self.snails = [Snail(self, x[0], x[1], len(self.file)) for x in self.file]

    def fnc_update(self):
        if self.time - (time.time() - self.timestamp) <= 0:
            self.race = False
            self.time_rem = self.time
            self.fnc_end()
        else:
            self.time_rem = str(round(time.time() - self.timestamp, 2))
        __text = font.render(f'{self.time_rem} / {self.time} s', True, (255, 255, 255))
        self.fnc_draw(__text)
        for snail in self.snails:
            snail.fnc_update()

    def fnc_draw(self, __text):
        screen.blit(__text, (750, 720))
        pygame.draw.line(screen, (155, 155, 155), (100, 0), (100, 700), 3)
        pygame.draw.line(screen, (155, 155, 155), (1400, 0), (1400, 700), 3)
        screen.blit(font.render('START', True, (200, 200, 200)), (100, 700))
        screen.blit(font.render(f'{self.max_distance}mm', True, (200, 200, 200)), (1400, 700))

    def fnc_get_max_distance(self):
        return max([(float(x[1]) * self.time + float(x[0])) for x in self.file])

    def fnc_end(self):
        order = []
        difference = 0
        for index, snail in enumerate(self.file):
            order.append([index, float(snail[1]) * float(self.time) + float(snail[0])])
        order.sort(key=lambda x: x[1], reverse=True)
        for idx, x in enumerate(order):
            if order[idx-1][1] != x[1]:
                print(f'{idx + 1 - difference}. place:')
            else:
                difference += 1
            print(f'Snail no.{x[0]} with {x[1]}mm')


def fnc_read_file(file):
    with open(file, encoding='utf8') as f:
        t = [i.split(' ') for i in f.read().split('\n')]
        return t


def main():

    app = App()

    while app.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    app.running = False

        if app.race:
            screen.fill((20, 20, 20))
            app.fnc_update()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
