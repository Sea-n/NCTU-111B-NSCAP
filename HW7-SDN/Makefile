ryu:
	ryu-manager controller.py --observe-links

mn1:
	service openvswitch-switch start
	mn --custom topo.py --topo=topo1 --controller=remote,ip=172.31.0.11

mn2:
	service openvswitch-switch start
	mn --custom topo.py --topo=topo2 --controller=remote,ip=172.31.0.11

gre1:
	ovs-vsctl add-port s1 gre0 -- set interface gre0 type=gre options:remote_ip=172.31.0.22

gre2:
	ovs-vsctl add-port s2 gre0 -- set interface gre0 type=gre options:remote_ip=172.31.0.11
