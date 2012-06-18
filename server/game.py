from board import Board
from threading import Timer

class Game():
    def __init__(self):
        self.board = Board(25, 25)
        self.players = {}
        self.running = False
    def size(self):
        return self.board.size()
    def add_observer(self, obs):
        self.board.add_observer(obs)
    def add_player(self, identifier):
        self.players[identifier] = self.board.spawn_snake()
        return self.players[identifier]
    def has_player(self, identifier):
        return identifier in self.players
    def remove_player(self, identifier):
        self.players[identifier].alive = False
        del self.players[identifier]
    def update(self):
        for snake in self.players.itervalues():
            snake.update(self.board)
    def move(self, identifier, direction):
        snake = self.players[identifier]
        if direction == 'left':
            snake.left()
        elif direction == 'right':
            snake.right()
        elif direction == 'up':
            snake.up()
        elif direction == 'down':
            snake.down()
    def run(self):
        if self.running:
            self.update()
            Timer(0.2, self.run).start()
    def start(self):
        self.running = True
        self.run()
    def stop(self):
        self.running = False

