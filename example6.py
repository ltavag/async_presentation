import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
selector = DefaultSelector()

def accept():
    global sock, selector
    conn, addr = sock.accept()
    conn.setblocking(False)
    selector.register(conn, EVENT_READ, lambda: read(conn))

def read(conn):
    data = conn.recv(10)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        selector.unregister(conn)
        conn.close()


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
