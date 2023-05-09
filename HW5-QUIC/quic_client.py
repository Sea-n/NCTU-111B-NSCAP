from quic_base import QUIC


class QUICClient(QUIC):
    def connect(self, socket_addr: tuple[str, int]):
        self.addr = socket_addr
        self.send(0, b'QUIC Hello')
        print('connect()')


def main():
    client = QUICClient()
    client.connect(("127.0.0.1", 30001))

    stream_id, data = client.recv()
    print('recv A', stream_id, data)

    client.send(3, b"Hey There!")
    print('sent 3')

    client.send(4, b"Nice to meet you.")
    print('sent 4')

    stream_id, data = client.recv()
    print('recv B', stream_id, data)

    client.close()


if __name__ == "__main__":
    main()
