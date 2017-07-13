import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import urllib.request
selector = DefaultSelector()

def accept():
    global sock, selector
    conn, addr = sock.accept()
    conn.setblocking(False)
    selector.register(conn, EVENT_READ, lambda: read(conn))

def read(conn):
    data = conn.recv(10)  # Should be ready
    if data:
        lookup()
        #bad_lookup()
    else:
        print('closing', conn)
        selector.unregister(conn)
        conn.close()

def bad_lookup():
    request = urllib.request.Request('http://jsonp.moatads.com/adunitlevel/TURNERDFP1/la/100394077')
    print(urllib.request.urlopen(request).read())

def lookup():
    inner_sock = socket.socket()
    inner_sock.setblocking(False)
    try:
        inner_sock.connect(('jsonp.moatads.com',80))
    except BlockingIOError:
        pass

    selector.register(inner_sock.fileno(), EVENT_WRITE, lambda:read_response(inner_sock))

def read_response(inner_sock):
    selector.unregister(inner_sock.fileno())
    inner_sock.send('GET /adunitlevel/TURNERDFP1/la/100394077 HTTP/1.0 \r\nHost: jsonp.moatads.com\r\n\r\n'.encode('ascii'))
    selector.register(inner_sock.fileno(), EVENT_READ, lambda:get_jsonp_value(inner_sock))

def get_jsonp_value(inner_sock):
    data = inner_sock.recv(1024)
    if data:
      print(data)
    else:
      selector.unregister(inner_sock.fileno())
      inner_sock.close()

sock = socket.socket()
sock.bind(('localhost', 1234))
sock.setblocking(False)
sock.listen(100)
selector.register(sock.fileno(), EVENT_READ, accept)

def loop():
    while True:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()

loop()
