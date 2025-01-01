from Vectors import *
import pygame
pygame.init()


class App:
    def __init__(self):
        self.size = self.width, self.height = (1000, 800)
        self.screen = pygame.display.set_mode(self.size)
        self.center_screen = (self.width / 2, self.height / 2)
        self.clock = pygame.time.Clock()
        self.time = 0

        self.G = 6.67430151515 * (10 ** (-11))
        self.light_speed = 299_792_458
        self.AU = 1.496 * (10 ** 11)
        self.mass_solar = 1.98847 * (10 ** 30)

        self.fix = 1000
        self.quantity_docs = 1000
        self.delta_time = 0.001
        self.docs_objects = []
        self.color_tails = [(90, 40, 78), (200, 40, 100), (200, 10, 40), (200, 10, 40)]
        self.color_objects = [(200, 40, 90), (200, 30, 0), (20, 200, 30), (20, 200, 30)]

        self.mass_objects = [10 ** 20, 10 ** 20]
        self.radius_objects = [50, 50]
        self.u_objects = [(0, 1000), (0, -1000)]
        self.pos_objects = [(1000, 0), (-1000, 0)]
        self.objects_influence = [True, False]
        self.quantity_objects = 2

        self.object_index = 1
        self.pause = True
        self.fastening = False
        self.see_orbits = True
        self.scape_move = False

        self.past_mouse_pos = (0, 0)
        self.pos_camera = self.center_screen

        self.scale = 1

        for index_object in range(self.quantity_objects):
            self.docs_objects.append([self.pos_objects[index_object]])

    def append_docs(self):
        for index_object in range(self.quantity_objects):
            self.docs_objects[index_object].append(self.pos_objects[index_object])
            if len(self.docs_objects[index_object]) == self.quantity_docs:
                del self.docs_objects[index_object][0]

    def pos_on_screen(self, pos: tuple):
        pos2 = (pos[0] + self.pos_camera[0], -pos[1] + self.pos_camera[1])
        return sum_vectors(self.center_screen,
                           multiply_vectors(minus_vectors(pos2, self.center_screen), 1 / self.scale))

    def update_pos(self):
        for index_object in range(self.quantity_objects):
            for index_object2 in range(self.quantity_objects):
                if index_object2 != index_object and self.objects_influence[index_object]:
                    r = len_line(self.pos_objects[index_object], self.pos_objects[index_object2])
                    a = (self.G * self.mass_objects[index_object2]) / (r ** 2)
                    gv_normal = minus_vectors(self.pos_objects[index_object2], self.pos_objects[index_object])
                    n = a / r
                    self.u_objects[index_object] = sum_vectors(self.u_objects[index_object],
                                                               multiply_vectors(gv_normal, n / self.fix))
            con = len_vector(self.u_objects[index_object]) / self.light_speed
            if con > 1:
                self.u_objects[index_object] = multiply_vectors(self.u_objects[index_object], self.light_speed /
                                                                len_vector(self.u_objects[index_object]))
        for index_object in range(self.quantity_objects):
            self.pos_objects[index_object] = sum_vectors(self.pos_objects[index_object],
                                                         multiply_vectors(self.u_objects[index_object], 1 / self.fix))
        self.time += 1
        if self.time % (self.fix * self.delta_time) == 0:
            self.append_docs()

    def render(self):
        for index_object in range(self.quantity_objects):
            pos_object = self.pos_on_screen(self.pos_objects[index_object])
            pygame.draw.circle(self.screen, self.color_objects[index_object], pos_object,
                               self.radius_objects[index_object] / self.scale)
            if self.see_orbits:
                doc = self.pos_on_screen(self.docs_objects[index_object][0])
                for i in self.docs_objects[index_object]:
                    doc2 = self.pos_on_screen(i)
                    pygame.draw.line(self.screen, self.color_tails[index_object], doc, doc2)
                    doc = doc2
        pygame.draw.circle(self.screen, (0, 0, 200), self.pos_on_screen((0, 0)), 4)

    def run(self):
        while True:
            self.clock.tick()
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause
                    if event.key == pygame.K_LEFT:
                        self.object_index -= 1
                        if self.object_index == -1:
                            self.object_index = self.quantity_objects - 1
                    if event.key == pygame.K_RIGHT:
                        self.object_index += 1
                        if self.object_index == self.quantity_objects:
                            self.object_index = 0
                    if event.key == pygame.K_TAB:
                        self.fastening = not self.fastening
                    if event.key == pygame.K_LSHIFT:
                        self.see_orbits = not self.see_orbits
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.scape_move = True
                        self.past_mouse_pos = mouse
                    if event.button == 5:
                        self.scale *= 2
                    if event.button == 4:
                        self.scale /= 2
                        if self.scale == 0:
                            self.scale = 1
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.scape_move = False
            if self.scape_move:
                self.pos_camera = sum_vectors(self.pos_camera,
                                              multiply_vectors(minus_vectors(mouse, self.past_mouse_pos), self.scale))
                self.past_mouse_pos = mouse
            self.screen.fill((0, 0, 0))
            if not self.pause:
                self.update_pos()
            if self.fastening:
                self.pos_camera = (-self.pos_objects[self.object_index][0] + self.center_screen[0],
                                   self.pos_objects[self.object_index][1] + self.center_screen[1])
            self.render()
            pygame.display.update()
            pygame.display.set_caption(f'fps: {int(self.clock.get_fps())}; pause: {not self.pause};'
                                       f' second:{self.time / self.fix}; scale: {self.scale}')


if __name__ == '__main__':
    app = App()
    app.run()
