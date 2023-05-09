import socket
from threading import Thread
from time import sleep
from struct import pack, unpack


class QUIC:
    def __init__(self):
        self.MTU = 13 - 12
        self.running = True
        self.stream_max = 10
        self.completed = list()
        self.ack = {k: set() for k in range(self.stream_max)}
        self.frag = {k: dict() for k in range(self.stream_max)}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.thrd = Thread(target = self.loop)
        self.sock.settimeout(0.1)
        self.thrd.start()

    def send(self, stream_id: int, data: bytes):
        frag_cnt = (len(data)-1) // self.MTU + 1
        for k in range(frag_cnt):
            self.sock.sendto(pack('III', stream_id, k, frag_cnt)
                             + data[self.MTU*k:self.MTU*(k+1)], self.addr)

    def recv(self) -> tuple[int, bytes]: # stream_id, data
        while not len(self.completed):
            sleep(0.1)
        return self.completed.pop()

    def loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(self.MTU + 12)
            except TimeoutError:
                continue

            if 'addr' not in vars(self):
                self.addr = addr
            elif self.addr != addr:
                print(f'Warning: received from {addr} rather than {self.addr}')

            stream_id, frag_id, frag_cnt = unpack('III', data[:12])
            self.frag[stream_id][frag_id] = data[12:]
            self.ack[stream_id].add(frag_id)
            if len(self.ack[stream_id]) == frag_cnt:
                buf = b''
                for i in range(frag_cnt):
                    buf = buf + self.frag[stream_id][i]
                self.ack[stream_id]
                self.completed.append((stream_id, buf))

    def close(self):
        print('closing...')
        self.running = False
        self.thrd.join()
        self.sock.close()
        print('close()')
