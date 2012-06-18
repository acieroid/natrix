from random import choice
from snake import Snake

def random_color():
    chars = '0123456789ABCDEF'
    return '#' + choice(chars) + choice(chars) + choice(chars)

class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cases = [[None for _ in xrange(height)] for _ in xrange(width)]
        self.observers = []
        self.food = (0, 0)
        self.spawn_food()
    def add_observer(self, observer):
        self.observers.append(observer)
        observer.new_food(self.food)
    def size(self):
        return (self.width, self.height)
    def has_food(self, pos):
        return self.food == pos
    def is_free(self, pos):
        (x, y) = pos
        return (x >= 0 and x < self.width and 
                y >= 0 and y < self.height and
                not self.cases[x][y])
    def free_positions(self):
        for x in xrange(self.width):
            for y in xrange(self.height):
                if self.is_free((x, y)):
                    yield (x, y)
    def free_directions(self, position):
        (x, y) = position
        if self.is_free((x-1, y)):
            yield (-1, 0)
        if self.is_free((x+1, y)):
            yield (1, 0)
        if self.is_free((x, y-1)):
            yield (0, -1)
        if self.is_free((x, y+1)):
            yield (0, 1)
    def random_position(self):
        return choice([_ for _ in self.free_positions()])
    def random_direction(self, pos):
        return choice([_ for _ in self.free_directions(pos)])
    def used_cases(self):
        for x in xrange(self.width):
            for y in xrange(self.height):
                if not self.is_free((x, y)):
                    yield ((x, y), self.cases[x][y])
    def spawn_snake(self):
        pos = self.random_position()
        direction = self.random_direction(pos)
        snake = Snake(pos, direction, random_color())
        snake.add_observer(self)
        return snake
    def spawn_food(self):
        self.food = self.random_position()
        print('Spawing food at {0}'.format(self.food))
        for obs in self.observers:
            obs.new_food(self.food)
    def case_freed(self, snake, pos):
        (x, y) = pos
        self.cases[x][y] = None
    def new_case(self, snake, pos):
        (x, y) = pos
        self.cases[x][y] = snake.color
