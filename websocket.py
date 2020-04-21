# coding:utf-8
import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import datetime

from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler

define("port", default=2222, type=int)
swearWord =[
    'retard',
    'bad',
]
class IndexHandler(RequestHandler):
    def get(self):
        self.render("chat-client.html")

class ChatHandler(WebSocketHandler):

    users = set()  

    def open(self):
        self.users.add(self)  
        for u in self.users:  
            u.write_message(u"[%s]-[%s]-has joined into the chat room!" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        # Bad words detection
        temp = message.split()
        for index, var in enumerate(temp):
            if var in swearWord:
                temp[index] = '****'
                message = ' '.join(temp) 
        for u in self.users:   
            u.write_message(u"[%s]-[%s]-：%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))
        # print(self.request.remote_ip)

    def on_close(self):
        self.users.remove(self) 
        for u in self.users:
            u.write_message(u"[%s]-[%s]-has left the chat room" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/", IndexHandler),
            (r"/chat", ChatHandler),
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True
        )
    http_server = tornado.httpserver.HTTPServer(app,xheaders = True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
