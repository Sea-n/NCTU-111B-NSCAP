from mininet.topo import Topo


class Topo1(Topo):
    def build(self):
        # Add hosts and switches
        s1 = self.addSwitch('s1', mac='00:00:00:11:ff:ff')
        h1 = self.addHost('h1', ip='10.42.1.1', mac='00:00:00:11:00:11')
        h2 = self.addHost('h2', ip='10.42.1.2', mac='00:00:00:11:00:22')
        h3 = self.addHost('h3', ip='10.42.1.3', mac='00:00:00:11:00:33')
        h4 = self.addHost('h4', ip='10.42.1.4', mac='00:00:00:11:00:44')

        # Add links
        self.addLink(s1, h1)
        self.addLink(s1, h2)
        self.addLink(s1, h3)
        self.addLink(s1, h4)


class Topo2(Topo):
    def build(self):
        # Add hosts and switches
        s2 = self.addSwitch('s2', mac='00:00:00:22:ff:ff')
        h5 = self.addHost('h5', ip='10.42.2.5', mac='00:00:00:22:00:11')
        h6 = self.addHost('h6', ip='10.42.2.6', mac='00:00:00:22:00:22')
        h7 = self.addHost('h7', ip='10.42.2.7', mac='00:00:00:22:00:33')
        h8 = self.addHost('h8', ip='10.42.2.8', mac='00:00:00:22:00:44')

        # Add links
        self.addLink(s2, h5)
        self.addLink(s2, h6)
        self.addLink(s2, h7)
        self.addLink(s2, h8)


topos = {
        'topo1': (lambda: Topo1()),
        'topo2': (lambda: Topo2()),
        }
