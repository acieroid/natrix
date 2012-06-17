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
    def add_player(self, id):
        self.players[id] = self.board.spawn_snake()
        return self.players[id]
    def remove_player(self, id):
        self.players[id].alive = False
        del self.players[id]
    def update(self):
        for snake in self.players.itervalues():
            snake.update(self.board)
    def move(self, id, direction):
        snake = self.players[id]
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

