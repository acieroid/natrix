class Snake():
    def __init__(self, position, direction, color):
        self.size = 1
        self.positions = [position]
        self.direction = direction
        self.color = color
        self.alive = True
        self.observers = []
        self.to_grow = 0
    def add_observer(self, observer):
        self.observers.append(observer)
        for pos in self.positions:
            observer.new_case(self, pos)
    def update(self, board):
        last_pos = self.positions[0]
        new_pos = (last_pos[0] + self.direction[0],
                   last_pos[1] + self.direction[1])
        if board.is_free(new_pos):
            if self.to_grow > 0:
                self.to_grow -= 1
            else:
                # remove the oldest position since we don't grow
                old_pos = self.positions.pop()
                for obs in self.observers:
                    obs.case_freed(self, old_pos)

            self.positions = [new_pos] + self.positions
            for obs in self.observers:
                obs.new_case(self, new_pos)

            if board.has_food(new_pos):
                board.spawn_food()
                self.to_grow += 1
        else:
            self.alive = False
    def left(self):
        self.direction = (-1, 0)
    def right(self):
        self.direction = (1, 0)
    def up(self):
        self.direction = (0, -1)
    def down(self):
        self.direction = (0, 1)
