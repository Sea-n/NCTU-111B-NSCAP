from setting import get_hosts, get_switches, get_links, get_ip, get_mac


def main():
    set_topology()
    run_net()


def set_topology():
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


def run_net():
    while True:
        argv = input(">> ").split()
        match argv:
            case [src, 'ping', dst]:
                ping(src, dst)
            case ['show_table', target]:
                show_table(target)
            case ['clear', target]:
                if target in all_dict:
                    all_dict[target].clear()
                else:
                    print(f'Target {target} not exists.')
            case _:
                print('a wrong command')


def ping(src, dst):  # initiate a ping between two hosts
    global host_dict, switch_dict
    print(f'{src=} -> {dst=}')
    if src not in host_dict or dst not in host_dict:
        return  # invalid command

    src, dst = host_dict[src], host_dict[dst]
    src.ping(dst.ip)


def show_table(target):  # display the ARP or MAC table of a node
    if target == 'all_hosts':
        [v.show_table() for k, v in host_dict.items()]
    elif target == 'all_switches':
        [v.show_table() for k, v in switch_dict.items()]
    elif target in all_dict:
        all_dict[target].show_table()
    else:
        print(f'{target = } not exists.')


class host:
    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.port_to = None
        self.arp_table = {}  # IP -> MAC

    def add(self, node):
        self.port_to = node

    def ping(self, dst_ip):  # handle a ping request
        self.send(dst_ip, 'ping')

    def show_table(self):
        print(f'host {self.name=}\n'
              f'{self.arp_table=}\n')

    def clear(self):
        self.arp_table = {}

    def send(self, dst_ip, content):
        dst_mac = self.arp_table.get(dst_ip, 'ff')
        self.port_to.handle_packet(self, self.mac, dst_mac,
                                   self.ip, dst_ip, content)

    def handle_packet(self, ingress, src_mac, dst_mac,
                      src_ip, dst_ip, content):
        if dst_ip != self.ip:
            return
        self.arp_table[src_ip] = src_mac  # Update ARP

        if 'ping' in content:
            self.send(src_ip, 'pong')


class switch:
    def __init__(self, name):
        self.name = name
        self.port_to = []
        self.mac_table = {}  # MAC -> Port

    def add(self, node):  # link with other hosts or switches
        self.port_to.append(node)

    def show_table(self):
        print(f'sw {self.name=}\n{self.mac_table=}\n')

    def clear(self):
        self.mac_table = {}

    def send(self, idx, src_mac, dst_mac, src_ip, dst_ip, content):
        node = self.port_to[idx]
        node.handle_packet(self, src_mac, dst_mac,
                           src_ip, dst_ip, content)

    def handle_packet(self, ingress, src_mac, dst_mac,
                      src_ip, dst_ip, content):
        content = content + '.'

        if dst_mac in self.mac_table:
            return self.send(self.mac_table[dst_mac], src_mac, dst_mac,
                             src_ip, dst_ip, content)
        if dst_mac != 'ff':
            self.mac_table[src_mac] = self.port_to.index(ingress)  # Update
        for p in range(len(self.port_to)):
            if self.port_to[p] != ingress:
                self.send(p, src_mac, dst_mac, src_ip, dst_ip, content)


if __name__ == '__main__':
    main()
