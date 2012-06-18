import tornado
import tornado.web
import tornado.httpserver
import tornadio2
import tornadio2.router
import tornadio2.server
import tornadio2.conn
from game import Game
from threading import Lock

http_app = tornado.web.Application([
        (r'/', tornado.web.RedirectHandler, {'url': 'index.html'}),
        (r'/(.*\.html)', tornado.web.StaticFileHandler, {'path': '../html/'}),
        (r'/(socket.io.js)', tornado.web.StaticFileHandler, {'path': '../socket.io/'}),
        (r'/(.*\.js)', tornado.web.StaticFileHandler, {'path': '../js/'})
])

game = Game()

class GameConnection(tornadio2.conn.SocketConnection):
    connections = set()
    lock = Lock()
    def on_open(self, info):
        if not self in self.connections:
            self.emit('board_size', game.size())
            for info in game.used_cases():
                self.emit('used', info)
            game.add_observer(self)
            self.lock.acquire()
            self.connections.add(self)
            self.lock.release()
 
    def on_close(self):
        if game.has_player(self):
            game.remove_player(self)
        self.lock.acquire()
        self.connections.remove(self)
        self.lock.release()

    def on_message(self, data):
        pass

    @tornadio2.event
    def move(self, direction):
        if game.has_player(self):
            game.move(self, direction)
    @tornadio2.event
    def join(self, name):
        if not game.has_player(self):
            snake = game.add_player(self, name)
            snake.add_observer(self)
            self.lock.acquire()
            for c in self.connections:
                c.emit('join', (name, snake.color))
            self.lock.release()

    def case_freed(self, snake, pos):
        self.lock.acquire()
        for c in self.connections:
            c.emit('free', pos)
        self.lock.release()
    def new_case(self, snake, pos):
        self.lock.acquire()
        for c in self.connections:
            c.emit('used', (pos, snake.color))
        self.lock.release()
    def snake_died(self, snake):
        self.lock.acquire()
        for c in self.connections:
            c.emit('died', (snake.name, snake.color))
        self.lock.release()
    def new_food(self, pos):
        self.emit('food', pos)

GameRouter = tornadio2.router.TornadioRouter(GameConnection)

sock_app = tornado.web.Application(
    GameRouter.urls,
    #flash_policy_port = 843,
    #flash_policy_file = '../socket.io/flashpolicy.xml'),
    socket_io_port = 8002
)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(http_app)
    http_server.listen(8001)

    tornadio2.server.SocketServer(sock_app, auto_start=False)
    try:
        game.start()
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        game.stop()
