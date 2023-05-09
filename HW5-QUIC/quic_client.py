from quic_base import QUIC


class QUICClient(QUIC):
    def connect(self, socket_addr: tuple[str, int]):
        self.addr = socket_addr
        self.send(0, b'QUIC Hello')
        print('connect()')


def main():
    client = QUICClient()
    client.connect(("127.0.0.1", 30001))
    recv_id, recv_data = client.recv()
    print(recv_data.decode("utf-8")) # SOME DATA, MAY EXCEED 1500 bytes
    client.send(3, b"Hey Server!")
    print('sent 3')
    client.send(4, b"Hi Server!")
    print('sent 4')
    recv_id, recv_data = client.recv()
    print(recv_data.decode("utf-8")) # LOREM DATA, MAY EXCEED 1500 bytes
    client.close()


if __name__ == "__main__":
    main()
