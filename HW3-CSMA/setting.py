import random


class Setting():
    def __init__(self, host_num=3, total_time=10000, packet_num=500,
                 packet_size=5, max_colision_wait_time=None, p_resend=None,
                 coefficient=8, link_delay=1, seed=None) -> None:
        self.host_num = host_num  # host 數量
        self.total_time = total_time  # 模擬時間總長，時間以 1 為最小時間單位
        self.packet_num = packet_num  # 每個 host 生成的封包數量
        self.packet_size = packet_size
        # packet time 是完成一個封包所需的時間，包含了送 packet 的 link delay 和 ack 的 link delay
        # 假設等待 ack 的時間等同於 link delay
        self.packet_time = packet_size + 2*link_delay
        # 每個封包完成所需要的時間，等同於 slotted aloha 的 slot size
        if max_colision_wait_time is None:
            self.max_colision_wait_time = int(
                (host_num * (packet_size + 2)) * coefficient)
        else:
            self.max_colision_wait_time = max_colision_wait_time
        # ALOHA, CSMA, CSMA/CD 重新發送封包的最大等待時間
        if p_resend is None:
            self.p_resend = (1 / host_num) / coefficient
        else:
            self.p_resend = p_resend  # slotted aloha 每個 slot 開始時，重送封包的機率
        self.link_delay = link_delay  # link delay
        if seed is None:
            self.seed = random.randint(1, 10000)
        else:
            self.seed = seed  # seed 用於 random，同樣的 seed 會有相同的結果

    # hosts 產生封包的時間
    # e.g.
    #   [[10, 20, 30],  # host 0
    #    [20, 30, 50],  # host 1
    #    [30, 50, 60]]  # host 2
    def gen_packets(self):
        random.seed(self.seed)
        packets = [[] for i in range(self.host_num)]
        for i in range(self.host_num):
            rng = range(1, self.total_time - self.packet_size)
            packets[i] = random.sample(rng, self.packet_num)
            packets[i].sort()
        return packets
