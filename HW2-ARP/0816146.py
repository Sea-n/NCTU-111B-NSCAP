from setting import get_hosts, get_switches, get_links, get_ip, get_mac


def main():
    __author__ = 'Sean Wei <me@sean.cat>, 0816146'
    setup_topology()
    while True:
        menu()


def setup_topology():
    global all_dict, host_dict, switch_dict
    host_dict, switch_dict = {}, {}
    ip_dict, mac_dict = get_ip(), get_mac()

    for name in get_hosts().split():
        host_dict[name] = host(name, ip_dict[name], mac_dict[name])
    for name in get_switches().split():
        switch_dict[name] = switch(name)
    all_dict = host_dict | switch_dict  # Merge two dict

    for p1, p2 in [i.split(',') for i in get_links().split()]:
        all_dict[p1].add(all_dict[p2]), all_dict[p2].add(all_dict[p1])


def menu():
    match input(">> ").split():
        case [src, 'ping', dst] if src in host_dict and dst in host_dict:
            src, dst = host_dict[src], host_dict[dst]
            src.ping(dst.ip)

        case ['show_table', 'all_hosts']:
            [v.show_table() for k, v in host_dict.items()]
        case ['show_table', 'all_switches']:
            [v.show_table() for k, v in switch_dict.items()]
        case ['show_table', target] if target in all_dict:
            all_dict[target].show_table()

        case ['clear', target] if target in all_dict:
            all_dict[target].clear()

        case _:
            print('a wrong command')


class host:
    def __init__(self, name, ip, mac):
        self.name = name
        self.ip, self.mac = ip, mac
        self.port_to = None
        self.arp_table = {}  # IP -> MAC

    def clear(self):
        self.arp_table = {}

    def add(self, node):
        self.port_to = node

    def show_table(self):
        print(f'{self.name:->20}:',
              *[f'{k} : {v}' for k, v in self.arp_table.items()], sep='\n')

    def ping(self, dst_ip):
        if dst_ip not in self.arp_table:
            self.send(dst_ip, 'ARP request')
        self.send(dst_ip, 'ICMP ping')

    def send(self, dst_ip, content):
        dst_mac = self.arp_table.get(dst_ip, 'ffff')
        self.port_to.handle_packet(self, self.mac, dst_mac,
                                   self.ip, dst_ip, content)

    def handle_packet(self, ingress, src_mac, dst_mac,
                      src_ip, dst_ip, content):
        if dst_ip != self.ip:
            return
        self.arp_table[src_ip] = src_mac  # Update ARP

        if 'request' in content:
            self.send(src_ip, 'ARP response')
        if 'ping' in content:
            self.send(src_ip, 'ICMP pong')


class switch:
    def __init__(self, name):
        self.name = name
        self.port_to = []
        self.mac_table = {}  # MAC -> Port

    def clear(self):
        self.mac_table = {}

    def add(self, node):
        self.port_to.append(node)

    def show_table(self):
        print(f'{self.name:->20}:',
              *[f'{k} : {v}' for k, v in self.mac_table.items()], sep='\n')

    def send(self, idx, src_mac, dst_mac, src_ip, dst_ip, content):
        node = self.port_to[idx]
        node.handle_packet(self, src_mac, dst_mac,
                           src_ip, dst_ip, content)

    def handle_packet(self, ingress, src_mac, dst_mac,
                      src_ip, dst_ip, content):
        self.mac_table[src_mac] = self.port_to.index(ingress)  # Update
        if dst_mac in self.mac_table:
            return self.send(self.mac_table[dst_mac], src_mac, dst_mac,
                             src_ip, dst_ip, content)
        for p in range(len(self.port_to)):
            if self.port_to[p] != ingress:
                self.send(p, src_mac, dst_mac, src_ip, dst_ip, content)


if __name__ == '__main__':
    main()
