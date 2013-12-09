#!/usr/bin/python2.7

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.web import StaticFileHandler
from tornado.options import define,options

from WeiboMongo import WeiboMongo

define("port",default = 12345, help="run on the given port")

class Application(tornado.web.Application):
   def __init__(self):
      settings = dict(
          titile = u"Crime"
         # template_path = os.path.join())
          )

      handlers = [
          (r"/",MainHandler),
          (r"/data",DataHandler)
      ]

      tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class DataHandler(tornado.web.RequestHandler):
    import WeiboMongo
    def get(self):
        w = WeiboMongo()
        self.write(w.findUsers())
        #self.write(w.get_reposts_counts_from_file('smallDataset.txt'))

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()


