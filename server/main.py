import tornado
import tornado.web
import tornado.httpserver
import tornadio2
import tornadio2.router
import tornadio2.server
import tornadio2.conn
from game import Game

http_app = tornado.web.Application([
        (r'/', tornado.web.RedirectHandler, {'url': 'index.html'}),
        (r'/(.*\.html)', tornado.web.StaticFileHandler, {'path': '../html/'}),
        (r'/(socket.io.js)', tornado.web.StaticFileHandler, {'path': '../socket.io/'}),
        (r'/(.*\.js)', tornado.web.StaticFileHandler, {'path': '../js/'})
])

game = Game()

class GameConnection(tornadio2.conn.SocketConnection):
    connections = set()
    def on_open(self, info):
        self.emit('board_size', game.size())
        snake = game.add_player(self)
        snake.add_observer(self)
        game.add_observer(self)
        self.connections.add(self)
 
    def on_close(self):
        game.remove_player(self)
        self.connections.remove(self)

    def on_message(self, data):
        pass

    @tornadio2.event
    def move(self, direction):
        game.move(self, direction)
    @tornadio2.event
    def update(self, direction):
        game.update()

    def case_freed(self, snake, pos):
        for c in self.connections:
            c.emit('free', pos)
    def new_case(self, snake, pos):
        for c in self.connections:
            c.emit('used', (pos, snake.color))
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
