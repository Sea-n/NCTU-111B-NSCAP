FROM ubuntu:20.04

RUN apt update
RUN apt install -y git tmux sudo tcpdump python3.8 python3-pip iputils-ping
RUN pip3 install eventlet==0.30.2 wheel ryu

RUN git clone --depth=1 https://github.com/mininet/mininet.git /opt/mininet
RUN /opt/mininet/util/install.sh -3nv

WORKDIR /srv

CMD ["sleep", "86400"]
