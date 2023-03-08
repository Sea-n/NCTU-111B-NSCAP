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
                print(f'failed {argv=}')


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
    elif target == 'all_switchs':
        [v.show_table() for k, v in switch_dict.items()]
    else:
        all_dict[target].show_table()


class host:
    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.port_to = None
        self.arp_table = {}

    def add(self, node):
        self.port_to = node

    def ping(self, dst_ip):  # handle a ping request
        pass

    def show_table(self):
        print(f'sw {self.name=}, {self.ip=}, {self.mac=}\n'
              f'{self.port_to=}\n{self.arp_table=}\n')

    def clear(self):
        pass  # clear ARP table entries for this host

    def send(self, xxx):
        node = self.port_to  # get node connected to this host
        node.handle_packet(xxx)  # send packet to the connected node

    def handle_packet(self, xxx):  # handle incoming packets
        pass

    def update_arp(self, xxx):
        pass  # update ARP table with a new entry


class switch:
    def __init__(self, name):
        self.name = name
        self.port_to = []
        self.mac_table = {}

    def add(self, node):  # link with other hosts or switches
        self.port_to.append(node)

    def show_table(self):
        print(f'sw {self.name=}\n{self.port_to=}\n{self.mac_table=}\n')

    def clear(self):
        pass  # clear MAC table entries for this switch

    def send(self, idx, xxx):  # send to the specified port
        node = self.port_to[idx]
        node.handle_packet(xxx)

    def handle_packet(self, xxx):  # handle incoming packets
        pass

    def update_mac(self, xxx):
        pass  # update MAC table with a new entry


if __name__ == '__main__':
    main()
