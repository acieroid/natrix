class Snake():
    def __init__(self, position, direction, color, name):
        self.respawn(position, direction)
        self.alive = False
        self.color = color
        self.name = name
        self.observers = []
        self.score = 0
    def respawn(self, position, direction):
        self.positions = [position]
        self.direction = direction
        self.alive = True
        self.to_grow = 2
        self.changed_direction = False
    def add_observer(self, observer):
        self.observers.append(observer)
        if self.is_alive():
            for pos in self.positions:
                observer.new_case(self, pos)
    def update(self, board):
        self.changed_direction = False
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
                self.to_grow += 3
                self.increase_score()
        else:
            self.die()
    def set_direction(self, direction):
        if (self.direction[0] == -direction[0] and
            self.direction[1] == -direction[1]):
            return
        elif not self.changed_direction:
            self.direction = direction
            self.changed_direction = True
    def left(self):
        self.set_direction((-1, 0))
    def right(self):
        self.set_direction((1, 0))
    def up(self):
        self.set_direction((0, -1))
    def down(self):
        self.set_direction((0, 1))
    def is_alive(self):
        return self.alive
    def die(self):
        self.alive = False
        for obs in self.observers:
            obs.snake_died(self)
            for pos in self.positions:
                obs.case_freed(self, pos)
    def set_score(self, score):
        self.score = score
        for obs in self.observers:
            obs.score_changed(self)
    def reset_score(self):
        self.set_score(0)
    def increase_score(self):
        self.set_score(self.score+1)
