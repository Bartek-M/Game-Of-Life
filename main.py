import random
import pygame

pygame.init()

WIDTH = 1800
HEIGHT = 900
TILE_SIZE = 15

GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

FPS = 60


class Drawing:
    BLACK = 13, 17, 23
    WHITE = 220, 227, 233
    CYAN = 0, 255, 255
    BACKGROUND = BLACK

    def __init__(self, nodes):
        self.nodes = nodes
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))

    def draw_grid(self):
        self.window.fill(self.BACKGROUND)

        for cell_x, cell_y in self.nodes:
            cords = (cell_x * TILE_SIZE, cell_y * TILE_SIZE)
            pygame.draw.rect(self.window, self.CYAN, (*cords, TILE_SIZE, TILE_SIZE))

        for row in range(1, GRID_HEIGHT):
            pygame.draw.line(self.window, self.BACKGROUND, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

        for col in range(1, GRID_WIDTH):
            pygame.draw.line(self.window, self.BACKGROUND, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []

        for dx in [-1, 0, 1]:
            if x + dx < 0 or x + dx > GRID_WIDTH:
                continue

            for dy in [-1, 0, 1]:
                if y + dy < 0 or y + dy > GRID_HEIGHT:
                    continue

                if dx == 0 and dy == 0:
                    continue

                neighbors.append((x + dx, y + dy))

        return neighbors

    def adjust_grid(self):
        all_neighbors = set()
        new_nodes = set()

        for pos in self.nodes:
            neighbors = self.get_neighbors(pos)
            all_neighbors.update(neighbors)

            neighbors = list(filter(lambda x: x in self.nodes, neighbors))

            if len(neighbors) in [2, 3]:
                new_nodes.add(pos)

        for pos in all_neighbors:
            neighbors = list(filter(lambda x: x in self.nodes, self.get_neighbors(pos)))

            if len(neighbors) == 3:
                new_nodes.add(pos)

        self.set_nodes(new_nodes)

    def set_nodes(self, nodes):
        self.nodes = nodes

    def set_node(self, pos):
        if pos in self.nodes:
            self.nodes.remove(pos)
        else:
            self.nodes.add(pos)


def gen_list():
    num = random.randrange(15, 20) * GRID_WIDTH + 1
    return set([(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(num)])


def main():
    run = True
    playing = False

    count = 0
    update_freq = 10

    clock = pygame.time.Clock()
    drawing = Drawing(gen_list())

    while run:
        clock.tick(FPS)
        pygame.display.set_caption(f"Game of Life [{'PLAYING' if playing else 'PAUSED'}]")

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            drawing.adjust_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                pos = (x // TILE_SIZE, y // TILE_SIZE)
                drawing.set_node(pos)

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_SPACE:
                playing = not playing
            elif event.key == pygame.K_r and not playing:
                drawing.set_nodes(gen_list())
                count = 0

        drawing.draw_grid()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
