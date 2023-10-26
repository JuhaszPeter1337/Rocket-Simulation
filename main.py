import pygame
from pygame import font, Surface
import math

pygame.init()

WIDTH, HEIGHT = 1200, 1000

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect")

PLANET_MASS = 100
SHIP_MASS = 5
G = 10
FPS = 1000
PLANET_SIZE = 250
OBJ_SIZE = 5
VEL_SCALE = 300

BACKGROUND = pygame.transform.scale(pygame.image.load("background_image.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("Jupiter-modified.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class Spacecraft():
    def __init__(self, x, y, x_vel, y_vel, mass) -> None:
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass

    def move(self, planet):
        distance = math.sqrt((planet.x - self.x)**2 + (planet.y - self.y)**2)
        force = (G * self.mass * planet.mass) / distance**2
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.x_vel += acceleration_x
        self.y_vel += acceleration_y

        self.x += self.x_vel
        self.y += self.y_vel

    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)

class Planet():
    def __init__(self, x, y, mass) -> None:
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self) -> None:
        win.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))

class Text():
    def __init__(self, font_type, font_size, text) -> None:
        self.font_type = font_type
        self.font_size = font_size
        self.text = text

    def create_font(self) -> font:
        font = pygame.font.Font(self.font_type, self.font_size)
        return font
    
    def create_text_surface(self, font) -> Surface:
        text = font.render(self.text, True, WHITE, BLACK)
        return text

def create_ship(location, mouse) -> Spacecraft:
    x, y = location
    m_x, m_y = mouse
    x_vel = (m_x - x) / VEL_SCALE
    y_vel = (m_y - y) / VEL_SCALE
    obj = Spacecraft(x, y, x_vel, y_vel, SHIP_MASS)
    return obj

def main():
    running = True

    clock = pygame.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)

    objects = []
    tmp_obj_pos = None

    while(running):
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if tmp_obj_pos:
                    obj = create_ship(tmp_obj_pos, mouse_pos)
                    objects.append(obj)
                    tmp_obj_pos = None
                else:
                    tmp_obj_pos = mouse_pos

        win.blit(BACKGROUND, (0, 0))

        if tmp_obj_pos:
            pygame.draw.line(win, WHITE, tmp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, tmp_obj_pos, OBJ_SIZE)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            # Distance between 2 points: sqrt((b1-a1)^2 + (b2-a2)^2)
            collision = math.sqrt((planet.x - obj.x)**2 + (planet.y - obj.y)**2) < PLANET_SIZE
            if off_screen or collision:
                objects.remove(obj)

        planet.draw()

        # FPS counter
        fps = clock.get_fps()
        fps = f"{str(round(fps))}" + " ms"
        text = Text('freesansbold.ttf', 25, fps)
        font = text.create_font()
        surface = text.create_text_surface(font)
        textRect = surface.get_rect()
        textRect.center = (50, 25)
        win.blit(surface, textRect)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()