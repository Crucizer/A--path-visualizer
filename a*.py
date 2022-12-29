# Importing Stuff
import pygame
import math
from queue import PriorityQueue

# Pygame window
WIDTH = 700
ROWS = 40
WIN = pygame.display.set_mode((WIDTH-WIDTH//ROWS, WIDTH-WIDTH//ROWS))
pygame.display.set_caption("A* Path Finding Algorithm")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GREY = (168, 159, 158)
RED = (255, 0, 0)
BLUE = (50, 119, 168)
ORANGE = (245, 185, 66)
PURPLE = (87, 76, 245)
TURQUOISE = (76, 217, 245)


# Frame
frame = 60
clock = pygame.time.Clock()


# Class which takes care of each node
class Node:
    # taking args
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    # the current position of the node
    def get_pos(self):
        return self.row, self.col

    # check if node is closed (already looked through)
    def is_closed(self):
        return self.color == RED

    # checking if node is open (we can still check)
    def is_open(self):
        return self.color == GREEN

    # checking if the node is a barrier
    def is_barrier(self):
        return self.color == BLACK

    # checking if the node is the start node
    def is_start(self):
        return self.color == ORANGE

    # checking if node is the end node
    def is_end(self):
        return self.color == TURQUOISE

    # changing node to white (default color)
    def reset(self):
        self.color = WHITE

    # making the current node closed (already looked through)
    def make_closed(self):
        self.color = RED

    # making the node a barrier (black node)
    def make_barrier(self):
        self.color = BLACK

    # making the node the start node
    def make_start(self):
        self.color = ORANGE

    def make_open(self):
        self.color = GREEN

    # def making the node the end node
    def make_end(self):
        self.color = TURQUOISE

    # making the node to a color of the path
    def make_path(self):
        self.color = PURPLE

    # to draw rectangle on the screen
    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    # These are all the neighbours of the current node

    def update_neighbours(self, grid):
        self.neighbours = []
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])

        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])

        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbours.append(grid[self.row][self.col+1])

        # Left
        if self.row > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbours.append(grid[self.row][self.col-1])

    def __lt__(self, other):
        return False


# Estimated distance between two nodes (Manhattan distance)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1-y2)


# Draws the path between the start point and end point
def reconstruct_path(came_from, current, start, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

    start.make_start()


def algorithm(draw, grid, start, end):
    # var to keep count of queue
    count = 0
    print(count)
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    # print(open_set_hash)

    # looping runnning untlt the priorityqueue is empty
    while not open_set.empty():
        # option to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        # print(current.row, current.col)
        open_set_hash.remove(current)

        # Found the path
        if current == end:
            end.make_end()
            start.make_start()
            reconstruct_path(came_from, end, start, draw)
            return True

        for neighbour in current.neighbours:

            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + \
                    h(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


# making the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


# drawing the grid
def draw_grid(win, rows, width):
    # width of each node
    gap = width // rows
    for i in range(rows):
        # for vertical lines
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        # for horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))


# draws all the stuff on the screen
def draw(win, grid, rows, width):
    # refilling white color on screen every frame
    win.fill(WHITE)

    # drawing each node
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    clock.tick(frame)
    pygame.display.update()


# getting the position
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


# main loop
def main(win, width):
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start = end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
