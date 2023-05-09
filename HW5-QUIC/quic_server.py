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
    server.send(1, b"ABCDEF123456abcdef123456" * 4)
    server.send(2, b"LOREM DATA, MAY EXCEED 1500 bytes")
    print('sent 1 & 2')
    recv_id, recv_data = server.recv()
    print('recv 1', recv_id, recv_data)
    recv_id, recv_data = server.recv()
    print('recv 2', recv_id, recv_data)
    print(recv_data.decode("utf-8")) # Hello Server!
    server.close()


if __name__ == "__main__":
    main()
