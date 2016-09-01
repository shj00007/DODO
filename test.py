import tornado.ioloop
import tornado.web
import tornado.websocket
import os

UPLOAD_FILE_PATH = "./tempfiles/"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./templates/main.html", title = "Main Page");

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    all_client = set()
    def open(self):
        print("WebSocket opened")
        EchoWebSocket.all_client.add(self)

    def on_message(self, message):
        print message
        for client in EchoWebSocket.all_client:
            client.write_message(u"You said: " + message)
        # self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
        EchoWebSocket.all_client.remove(self)

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        uploadFile = self.request.files['uploadFile'][0]
        filename = uploadFile['filename']
        fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
        fileObj.write(uploadFile['body'])
        for client in EchoWebSocket.all_client:
            client.write_message(u"You said: " + message)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", EchoWebSocket),
        (r'/upload', UploadHandler),
        (r"/tempfiles/(.*)", tornado.web.StaticFileHandler, {"path": UPLOAD_FILE_PATH}),
    ], static_path = os.path.join(os.path.dirname(__file__), "static"), debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
