import socket
from threading import Thread
from time import sleep
from struct import pack, unpack


class QUIC:
    def __init__(self):
        self.MTU = 22 - 12
        self.itrv = 0.1
        self.running = True
        self.stream_max = 10
        self.recv_completed = list()
        self.send_ack = {k: set() for k in range(self.stream_max)}
        self.recv_ack = {k: set() for k in range(self.stream_max)}
        self.send_frag = {k: dict() for k in range(self.stream_max)}  # header and data
        self.recv_frag = {k: dict() for k in range(self.stream_max)}  # data only

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_thrd = Thread(target = self.send_loop)
        self.recv_thrd = Thread(target = self.recv_loop)
        self.sock.settimeout(0.01)
        self.send_thrd.start()
        self.recv_thrd.start()

    def send(self, stream_id: int, data: bytes):
        frag_cnt = (len(data)-1) // self.MTU + 1
        for k in range(frag_cnt):
            self.send_frag[stream_id][k] = pack('iii', stream_id, k, frag_cnt) \
                                           + data[self.MTU*k:self.MTU*(k+1)]

    def recv(self) -> tuple[int, bytes]: # stream_id, data
        while not len(self.recv_completed):
            sleep(0.01)
        return self.recv_completed.pop()

    def send_loop(self):
        while self.running:
            for k in range(self.stream_max):
                for frag_id, data in self.send_frag[k].items():
                    self.sock.sendto(data, self.addr)
                    sleep(self.itrv)
                for frag_id in self.send_ack[k]:
                    del self.send_frag[k][frag_id]
                self.send_ack[k].clear()
            sleep(0.01)

    def recv_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(self.MTU + 12)
            except TimeoutError:
                continue

            if 'addr' not in vars(self):
                self.addr = addr
            elif self.addr != addr:
                print(f'Warning: received from {addr} rather than {self.addr}')

            stream_id, frag_id, frag_cnt = unpack('iii', data[:12])

            if stream_id == -42:  # Received ACK
                self.send_ack[frag_id].add(frag_cnt)
                continue

            self.recv_frag[stream_id][frag_id] = data[12:]
            self.recv_ack[stream_id].add(frag_id)
            if len(self.recv_ack[stream_id]) == frag_cnt:
                buf = b''
                for i in range(frag_cnt):
                    buf = buf + self.recv_frag[stream_id][i]
                self.recv_ack[stream_id].clear()
                self.recv_completed.append((stream_id, buf))
            self.sock.sendto(pack('iii', -42, stream_id, frag_id), self.addr)  # ACK

    def close(self):
        print('closing...', end='')
        while self.running:
            self.running = False
            for k in range(self.stream_max):
                if len(self.send_frag[k]):
                    self.running = True
                    print('.', end='', flush=True)
                    sleep(0.5)
        print('')

        self.send_thrd.join()
        self.recv_thrd.join()
        self.sock.close()
        print('closed')
