import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import urllib.request
import re
from async_request import AsyncHTTPRequest

selector = DefaultSelector()

def accept(sock):
    global selector
    conn, addr = sock.accept()
    conn.setblocking(False)
    selector.register(conn, EVENT_READ, lambda: read(conn))

def inline_callback(gen):
    def wrapper(*args):
        print(gen.__class__)
        running = gen(*args)
        x = running.__next__()

        def cb(x):
            try:
                running.send(x)
            except StopIteration:
                pass

        if isinstance(x, AsyncHTTPRequest):
            x.cb = cb
            x()

    return wrapper

RESULT = b'HTTP/1.0 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: 13\r\nConnection: close\r\n\r\nGot a result\n'
@inline_callback
def read(conn):
    data = conn.recv(1024)  # Should be ready
    try:
        if data:
            x = yield lookup()
            conn.send(RESULT)
    finally:
        selector.unregister(conn)
        conn.close()

def lookup():
    url = 'http://blockchain.info/rawblock/000000000000000000165fab1959a2575748085b635d867f4840f888d8f24e76'
    request = AsyncHTTPRequest(url, selector)
    return request

def listen_forever():
    sock = socket.socket()
    sock.bind(('localhost', 1235))
    sock.setblocking(False)
    sock.listen(100)
    selector.register(sock.fileno(), EVENT_READ, lambda:accept(sock))

    try:
        while True:
            events = selector.select()
            for event_key, event_mask in events:
                callback = event_key.data
                callback()

    finally:
        selector.unregister(sock.fileno())
        sock.close()

listen_forever()
