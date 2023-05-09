import socket
from time import time, sleep
from threading import Thread
from struct import pack, unpack


class QUIC:
    def __init__(self):
        self.ts = 0
        self.speed = 500
        self.snd_cnt = 0
        self.ack_cnt = 0
        self.recv_wnd = 3
        self.send_wnd = 0
        self.MTU = 1400 - 12
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
                    if (frag_id >= list(self.send_frag[k].keys())[0] + self.wnd):
                        continue  # Exceed sliding window
                    self.sock.sendto(data, self.addr)
                    self.snd_cnt += 1
                    sleep(1.0 / self.speed)

                for frag_id in self.send_ack[k]:
                    if frag_id in self.send_frag[k].keys():
                        del self.send_frag[k][frag_id]
                self.send_ack[k].clear()

            if self.snd_cnt > self.speed:  # About every second
                if self.ack_cnt / self.snd_cnt < 0.5:
                    self.speed = min(10, self.speed / 2)
                else:
                    self.speed += 50
            sleep(max(0.01, self.ts - time()))
            self.ts = time() + 0.5  # Resend timer

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
                self.ack_cnt += 1
                continue
            self.sock.sendto(pack('iii', -42, stream_id, frag_id), self.addr)  # ACK

            self.recv_frag[stream_id][frag_id] = data[12:]
            self.recv_ack[stream_id].add(frag_id)
            if len(self.recv_ack[stream_id]) == frag_cnt:
                buf = b''.join([self.recv_frag[stream_id][i] for i in range(frag_cnt)])
                self.recv_completed.append((stream_id, buf))
                # self.recv_ack[stream_id].clear()  # don't reuse stream_id
                self.recv_ack[stream_id].add(-1)    # mark as completed

    def close(self):
        print('closing...', end='')
        while self.running:
            self.running = False
            for k in range(self.stream_max):
                if len(self.send_frag[k]):
                    self.running = True
                    print('.', end='', flush=True)
                    sleep(0.3)
        print('')

        self.send_thrd.join()
        self.recv_thrd.join()
        self.sock.close()
        print('closed')
