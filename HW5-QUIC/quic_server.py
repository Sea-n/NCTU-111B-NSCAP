from socket import SOL_SOCKET, SO_REUSEADDR
from quic_base import QUIC


class QUICServer(QUIC):
    def listen(self, socket_addr: tuple[str, int]):
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(socket_addr)
        print('listen()')

    def accept(self):
        stream_id, data = self.recv()
        if stream_id != 0 or data != b'QUIC Hello':
            print(f'Warning: {stream_id=} and {data=} is not Hello')
            return self.accept()  # Try again
        print('accept()')


def main():
    server = QUICServer()
    server.listen(socket_addr=("127.0.0.1", 30001))
    server.accept()

    server.send(1, b"0123456789ABCDEF" * 42)
    print('sent 1')

    stream_id, data = server.recv()
    print('recv A', stream_id, data)

    stream_id, data = server.recv()
    print('recv B', stream_id, data)

    server.send(2, b"0123456789ABCDEF" * 42)
    print('sent 2')

    server.close()


if __name__ == "__main__":
    main()
