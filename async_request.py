import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import re

URL_REG = re.compile('https?:\/\/(.+?)(\/.*)')
class AsyncHTTPRequest():
    full_response = b''
    finished = False

    def __init__(self,
                    url,
                    cb,
                    selector):
        self.cb = cb
        match = URL_REG.match(url)
        self.host = match.groups()[0]
        self.path = match.groups()[1]
        self.selector = selector

    def __call__(self):
        self.connect_host()

    def connect_host(self):
        inner_sock = socket.socket()
        inner_sock.setblocking(False)
        try:
            inner_sock.connect((self.host,80))
            inner_sock.setblocking(False)
        except BlockingIOError:
            pass

        self.selector.register(inner_sock.fileno(),
                            EVENT_WRITE,
                            lambda:self.make_request(inner_sock))

    def make_request(self, inner_sock):
        self.selector.unregister(inner_sock.fileno())
        inner_sock.send('GET {path} HTTP/1.0 \r\nHost: {host}\r\n\r\n'.format(host=self.host, path=self.path).encode('ascii'))
        self.selector.register(inner_sock.fileno(),
                            EVENT_READ,
                            lambda:self.read_response(inner_sock))


    def read_response(self,
                      inner_sock):

        data = inner_sock.recv(8192)
        if data:
          self.full_response+= data
        else:
          self.selector.unregister(inner_sock.fileno())
          inner_sock.close()
          self.finished = True
          self.cb(self.full_response)
