NSCAP_2023
===
###### tags: `nscap`
# Information
[Course outline](https://timetable.nctu.edu.tw/?r=main/crsoutline&Acy=111&Sem=2&CrsNo=515618&lang=zh-tw)
[Course website](https://people.cs.nctu.edu.tw/~shieyuan/course/nscap/2023/)
[Webex](https://nycu.webex.com/meet/nsl111.nscap)
[Google drive](https://drive.google.com/drive/folders/1co_2RCDzwWBvOJq2fTBZ-M0af7ya3u9d?usp=sharing)
Class time : T34
Classroom : ED202
# Homework 1 Specification

PPT: https://docs.google.com/presentation/d/1bLb27cYqEBAD_xiEFSAPcFLwNJycXxRF/edit?usp=sharing&ouid=107769609686930206462&rtpof=true&sd=true
Deadline: March 7, 11:59 PM.

## Overview
For this homework assignment, you need to write a C++ program that captures live network packets  and prints some information in the packet, similar to what the tcpdump utility does.
cification
### pcap
#### Environment (ubuntu 18.04)
- sudo apt-get install libpcap-dev
- g++ main.o -o main -lpcap (linking the object file with the libraries)
#### User manual
- Function
    - [pcap_findalldevs](https://linux.die.net/man/3/pcap_findalldevs)
    - [pcap_open_live](https://linux.die.net/man/3/pcap_open_live) 
    - [pcap_compile](https://linux.die.net/man/3/pcap_compile)
    - [pcap_setfilter](https://linux.die.net/man/3/pcap_setfilter)
    - [pcap_next](https://linux.die.net/man/3/pcap_next)
- Structure
    - [pcap_if_t](https://www.winpcap.org/docs/docs_40_2/html/group__wpcap__def.html#g3a6e7cbf8d9752da3add4676c7cd4c58)
    - [pcap_t](https://www.winpcap.org/docs/docs_40_2/html/group__wpcap__def.html#g3a6e7cbf8d9752da3add4676c7cd4c58)


### Program Arguments
Your program should correctly support the following arguments:
 - -\-interface {interface},  -i {interface} 
 - -\-count {number}, -c {number}  
default =  -1, which means that it will continuously capture packets until it is interrupted
 - -\-filter {udp, tcp, icmp, all}, -f {udp, tcp, icmp, all} 
 default = all
It should correctly filter out UDP, TCP, and ICMP packets.

### Print Format
:::success
Payload: You should print the first 16 bytes of the application data in the hexadecimal format. 
If there is nothing in the payload, don't print anything.

e.g.,
-    ASCII -> hex
a -> 61
b -> 62
1 -> 31
2 -> 32
a4bs5k1cdefg1257 -> 61 34 62 73 35 6B 31 63 64 65 66 67 31 32 35 37
:::
* ICMP
:::info
Transport type: ICMP
Source IP: 10.0.0.1
Destination IP: 10.0.0.8
ICMP type value: 8
:::
* TCP and UDP
:::info
Transport type: TCP (or UDP)
Source IP: 10.0.0.1
Destination IP: 10.0.0.2
Source port: 7777
Destination port: 8888
Payload: ... (If there is no payload, don’t print anything)
:::





### Testing Flow
We will compile your homework by simply typing 'make' in your homework directory, and run your program by typing `./main [argument] ...`
1. Compile
`make`
2. Run your program (an example)
- `./main --interface {interface} -c 3 --filter udp`
:::info
Transport type: UDP
Source IP: ...
Destination IP: ...
Source port: ...
Destination port: ...
Payload: ...

Transport type: UDP
Source IP: ...
Destination IP: ...
Source port: ...
Destination port: ...
Payload: ...

Transport type: UDP
Source IP: ...
Destination IP: ...
Source port: ...
Destination port: ...
Payload: ...

:::
- `./main `
:::info
wrong command
:::
   This error is caused because you did not specify the interface when running your program.
- The following is an example output when sending and receiving UDP, ICMP, and TCP packets with the filter option being set to 'all'. 
(You can see clearer images in the PPT presentation slides.)
![](https://i.imgur.com/Av3lMs3.png)

![](https://i.imgur.com/COFbUAj.png)
![](https://i.imgur.com/3sYoc7T.png)



## Report

- You need to prepare two virtual machines and configure them to be on the same VLAN, so that they can communicate using both UDP and TCP.
- Perform the following experiments and take screenshots of the results.
    - 1.
        - Run`./main --interface {interface} -c 4 --filter icmp` on VM1
        - Run `ping {VM2_IP} -c 3` on VM1   
    - 2. 
        - Run`./main --count 20 -f all -i {interface}` on VM1
        - Run `ping {VM2_IP} -c 1` on VM1 
        - VM1 should send three UDP packets to VM2, similar to the ones displayed in the "Testing Flow 2. examples".
            - First packet: 5555555555555555
            - Second packet: 7777777777777777
            - Third packet: 8888888888888888
        - VM1 should send the file **sample_file.txt** to VM2 using the python socket module and TCP protocol.
            - You can use Wireshark to verify whether the payload you present is correct.
            - Server port: 8888, Client port: 7777
                - It will make grading easier.
    - Note: Screenshots capturig the commands and what they print on two VMs are required.
### Image
:::warning
[Link](https://drive.google.com/file/d/18s2DXj8JkKwoHpxBhlWmMs5q1NZ8DGV2/view?usp=sharing)
User: nscap2
Password: nscap
:::
`$sudo ./main -i enp0s3`
This test is intended to indicate that the environment is capable of using the "pcap" package.
![](https://i.imgur.com/6v6yOoZ.png)

## Grading Policy
### Features

- -i argument: 10%
- -c argument: 10%
- -f argument: 10%
- Transport type: 5%
- Port and IP address: 20%
- UDP app_data: 10%
- TCP app_data: 20%  (Hint: There may be tcp options.)
- ICMP “type” value: 15% (echo request = 8, echo reply = 0) 


### Penalty
- Incorrect upload format (wrong directory structures, wrong file names, etc.): -10%
- Fail to `make`: -10%
- Late submission: final score = original score * (3/4) ^ #_late_days
- Cannot compile or run on the workstations: -20%

### Submission
{student_id}_hw1.zip
├──── cpp_file
├──── (other_files)   
├──── {student_id}_hw1.pdf
└──── Makefile  
# Homework 2 Specification
PPT: https://docs.google.com/presentation/d/1VoOLsJI4WJ9bD2m0-oIUjVnBPBEyPRQE/edit?usp=sharing&ouid=107769609686930206462&rtpof=true&sd=true
Deadline: March 21, 11:59 PM.
## Overview
For this homework, you are tasked with designing an interactive program that creates a virtual network, similar to what is done with Mininet. 

In the program, you need to research and understand how switches populate their switch table entries and how hosts populate their ARP table entries so that packets can be properly forwarded to their destinations.


## Topology
8 hosts + 7 switches 
The names of the hosts and switches may differ from those during the demonstration.
The red numbers in the topology map refer to the port numbers of those switches. 
![](https://i.imgur.com/oitVfSS.png)

- Import setting.py
    - hosts
    - switches
    - links
## Rules
- For the command `h1 ping h2`, the following actions will occur:

    - h1:

        -    h1 will check if the IP of h2 is in its ARP table.
        -    If it is, h1 will send an ICMP request to the MAC address of h2.
        -    If not, h1 will broadcast an ARP request to all hosts by setting the destination MAC address to 'ffff'. Switches will handle this.
        -    After receiving an ARP reply from h2, h1 will update its ARP table and send an ICMP request to h2.
    - h2:

        -    After receiving an ARP request, h2 will update its ARP table and send an ARP reply to h1 since the destination IP matches its own IP.
        -    After receiving an ICMP request, h2 will send an ICMP reply to h1.
    -    Other hosts:

            -    After receiving an ARP/ICMP request, they will drop the request since the destination IP does not match their own IP, .
    -    Switch:
            -    After receiving a packet, the switch will first update its MAC table with the source's MAC address.
            -    If the destination MAC address is 'ffff', the switch will recognize it as an ARP request and broadcast the packet.
            -    Otherwise, the switch will check if the MAC address of h2 is in its MAC table.
            -    If it is, the switch will send the packet on the specific port.
            -    If not, the switch will flood the packet by sending it on every other port **except the one it came from.**"




## Command
1. ping: 
    e.g. 
    `h1 ping h2` (No need to print anything)
2. show_table (for switches and hosts)
    -    show_table {host-name/switch-name}
    e.g. 
    `show_table h1` (show arp table in h1)
    `show_table s1` (show mac table in s1)
    - show_table {all_hosts/all_switches}
    `show_table all_hosts` (show all hosts' arp table)
    `show_table all_switches` (show all switches' arp table)
3. clear: 
    e.g. 
    `clear h1` (clear arp table in h1)
    `clear s1` (clear mac table in s1)
4. If the entered command is not “ping,” “show_table,” or “clear”  
    print "a wrong command"
## Print format
- show_table {host_name}
    - First line: `ip : mac`
    - Then: `---------------{host_name}:`
    - Then print every entry in its ARP table in the format `h1ip : h1mac`
 
- show_table {switch_name}
    - First line: `mac : port`
    - Then: `---------------{switch_name}:`
    - Then print every entry in its MAC table in the format `h1mac : 0`

## Examples
- 4 hosts + 3 switches
`python3 main.py`

\>> show_table all_hosts
:::info
ip : mac
---------------h1:
---------------h2:
---------------h3:
---------------h4:
:::
\>> show_table all_switches
:::info
mac : port
---------------s1:
---------------s2:
---------------s3:
:::
\>> h1 ping h2
\>> show_table all_hosts
(for h1 : `h2ip : h2mac`, for h2 : `h1ip : h1mac`, no entry in h3 and h4's arp_table)
:::info
ip : mac
---------------h1:
h2ip : h2mac
---------------h2:
h1ip : h1mac
---------------h3:
---------------h4:
:::
\>> show_table all_switches
:::info
mac : port
---------------s1:
h1mac : 0
h2mac : 1
---------------s2:
h1mac : 0
---------------s3:
h1mac : 2
:::
\>> clear h1
\>> show_table all_hosts
:::info
ip : mac
---------------h1:
---------------h2:
h1ip : h1mac
---------------h3:
---------------h4:
:::

\>> show_table h2
:::info
ip : mac
---------------h2:
h1ip : h1mac
:::
## Sample code
- For each switch or host, when it want to send out a packet
    - 1. Decide which port to send the packet from. 
    - 2. Then use "node" to represent the node connected to that port.
    - 3. Then execute the "handle_packet" function of the "node".
![](https://i.imgur.com/KErMM21.png)

## Submission format
{student_id}_hw2.zip
└── {student_id}.py
 
## Demo
-    Download the code.
-    Import the file 'setting.py', which contains the same topology but with different names.
-    Run some test commands.
-    Show your code and explain in detail how it works.
    - e.g.
        1. What is the difference between broadcasting and flooding in networking?
        2. Explain the steps involved in the process of `h1 ping h7` when there are no entries in the switch's MAC table and the host's ARP table.
        3. What will happen when `clear h5` is executed and then `h7 ping h1` in the two scenarios below:
            3-1. Every switch **drops** the packet if the destination port is the same as the incoming port in the switch's MAC table.
            3-2. Every switch **sends** the packet if the destination port is the same as the incoming port in the switch's MAC table.

        - p.s. 
            To explain the process in detail, you need to show how:

            -    h1 determines if it will send an ARP or ICMP request 
                    (e.g. using an if-else statement in your code)
            -    s1 distinguishes between an ARP and ICMP packet 
                    (e.g. by checking for the value 'ffff')
            -    s1 decides which port to send the packet from
            -    The path the packet will take (e.g. to h2, s2, etc.)
            -    The actions each host and switch takes upon receiving the packet.
- Answer questions (no need to show your code): 
    - e.g.
        1. What problem could arise from connecting s2 and s5 together and creating a switching loop?
        2. How is this issue addressed? (mention the specific algorithm or protocol used)
        
    - Note: 
        - The questions may have similarities to the examples, but their exact wording may vary.
        - You need to have a deeper understanding of the problem and its solutions, instead of just knowing the basic terms.


## Grading Policy
### Demo - 100%
- Corretness of output: 30%
- Explanation: 50%
    - Five scenarios, each scenario: 10% 
        - Correctly orally describe the operations: 5% 
        - Correctly implement these operations: 5%
- Answer questions: 20%
    - Two questions, each question: 10%


### Penalty
- Incorrect upload format (wrong directory structures, wrong file names etc.): -10%
- Late submission: final score = original score * (3/4) ^ #_late_days
- Cannot compile or run on the workstations: -20%

# Homework 3 Specification
ppt : https://docs.google.com/presentation/d/1jiqIpg4VL-U0arDTY4NBonaPC7NfliHN/edit?usp=sharing&ouid=112064783971576677983&rtpof=true&sd=true
Deadline: April 4, 11:59 PM.


## Overview
Design and implement a simulation program to study the channel efficiency of the Aloha, Slotted Aloha, CSMA, and CSMA/CD protocols under different operation conditions.
## Methods
### Aloha
* All hosts can send packets at any time.
* If a host does not receive an acknowledgement, it considers that a collision has occurred.
* If a collision occurs, the host waits for a random time to retransmit.
* ![](https://i.imgur.com/wYoGX4C.png)
### Slotted Aloha
* All host can send packets at and only at the beginning of each time slot.
* If a host does not receive an acknowledgement, it considers that a collision has occurred.
* If a collision occurs, the host decides whether to retransmit with probability p at the beginning of each following slot.
* ![](https://i.imgur.com/8Du59WH.png)
### CSMA
* All hosts detect if someone else is sending before starting to send.
    * non-persistent: If someone is sending, the host waits for a random time and detects again. (We adopt this method.)
    * 1-persistent: If someone is sending, the host keeps detecting until it finds that no one is sending.
* If a host does not receive an acknowledgement, it considers that a collision has occurred.
* If a collision occurs, the host waits for a random time to retransmit.
### CSMA/CD
* All hosts detect if someone else is sending before starting to send.
    * non-persistent: If someone is sending, the host waits for a random time and detects again. (We adopt this method.)
    * 1-persistent: If someone is sending, the host keeps detecting until it finds that no one is sending.
* If a host does not receive an acknowledgement, it considers that a collision has occurred..
* If a collision occurs, the host waits for a random time to retransmit.
* The host detects collisions during transmission and aborts the transmission if a collision is detected.
### CSMA and CSMA/CD with Link Delay
![](https://i.imgur.com/YNW3jZJ.png)
## Performance Metrics
* $$\color{#70AD47}{Success\ Rate}= \frac{Total\ time\ of\ packets\  sent\ successfully}{Total\ simulation\ time}$$
* $$\color{#4472C4}{Idle\ Rate}= \frac{Total\ time\ when\ all\ hosts\ were\ idle}{Total\ simulation\ time}$$
* $$\color{#FF0000}{Collision\ Rate}= \frac{Total\ time\ of\ packets\ not\ sent\ successfully}{Total\ simulation\ time}$$
* $$\color{#70AD47}{Success\ Rate}+\color{#4472C4}{Idle\ Rate}+\color{#FF0000}{Collision\ Rate}=1$$
* ![](https://i.imgur.com/fKETPy6.png)


## Requirements
### Submission Format
{student_id}_hw3.zip
├──── report.pdf
├──── main.py or main.ipynb
└──── protocols.py
### Scores
1. Code Test (40%) 
2. Questions (60%)
### Penalty
* Incorrect upload format (wrong directory structures, wrong file names, etc.): -10%
* Late submission: final score = original score * (3/4) ^ #_late_days
### Settings
* The setting is defined as follows
```python
import random
class Setting():
    def __init__(self, host_num=3, total_time=10000, packet_num=500, packet_size=5, max_colision_wait_time=20, p_resend=0.3, link_delay=1, seed=None) -> None:
        self.host_num = host_num # host 數量
        self.total_time = total_time # 模擬時間總長，時間以1為最小時間單位
        self.packet_num = packet_num # 每個 host 生成的封包數量
        # packet time是完成一個封包所需的時間，包含了送packet的link delay和ack的link delay
        # 假設等待ack的時間等同於link delay
        self.packet_time = packet_size + 2*link_delay # 每個封包完成所需要的時間，等同於slotted aloha的slot size
        self.max_colision_wait_time = max_colision_wait_time # ALOHA, CSMA, CSMA/cD 重新發送封包的最大等待時間
        self.p_resend = p_resend # slotted aloha 每個slot開始時，重送封包的機率
        self.link_delay = link_delay # link delay
        if seed is None:
            self.seed = random.randint(1, 10000)
        else:
            self.seed = seed # seed 用於 random，同樣的 seed 會有相同的結果

    # hosts產生封包的時間
    # e.g.
    #   [[10, 20, 30], # host 0
    #    [20, 30, 50], # host 1
    #    [30, 50, 60]] # host 2
    def gen_packets(self):
        random.seed(self.seed)
        packets = [[] for i in range(self.host_num)]
        for i in range(self.host_num):
            packets[i] = random.sample(range(1, self.total_time-self.packet_size), self.packet_num)
            packets[i].sort()
        return packets
```
### Simulation

* Each simulation should use the setting as input and return three performance indicators as results. Also, you need to print the history.
* The file protocols.py should include four functions:
    * aloha(setting, show_history=False)
    * slotted_aloha(setting, show_history=False)
    * csma(setting, show_history=False)
    * csma_cd(setting, show_history=False)
* Example: 
``` python
def aloha(setting, show_history=False):
    for t in range(setting.total_time):
        # All hosts decide the action (send/idle/stop sending)

        # Hosts that decide to send send packets.

        # Check collision if two or above hosts are sending.

        # If the host finishes a packet, it stops sending.
    
    if show_history:
        # Show the history of each host
    
    return success_rate, idle_rate, collision_rate
```
### Code Test (40%)
* ALOHA (report: 6%, TA test: 4%)
* Slotted ALOHA (report: 6%, TA test: 4%)
* CSMA (report: 6%, TA test: 4%)
* CSMA/CD (report: 6%, TA test: 4%)
* Use this setting `Setting(host_num=3, total_time=100, packet_num=4, max_colision_wait_time=20, p_resend=0.3, packet_size=3, link_delay=1, seed=<studen_id>)` to simulate in all methods and **put the screenshot of results (including three performance indicators and the history) into your report.** 
    * <student_id>=Your student ID
* Example (".": idle, ""<": start to send a packet, "-": sending, ">": stop sending (no collision), "|": stop sending (collision happened), "V": a packet generated by the host) (This example uses seed=4)
```
aloha
                  V                V       V                                                     V      
h0: ..............<---|.......<---|...........<---|.....<---|........<---|........<---|.....<---|.......
                V       V                              V          V                                     
h1: ............<---|.<---|................<---|........<---|......<---|....................<---|.......
       V     V                                          V                  V                            
h2: ...<--->.<---|.........<---|.................<---|...<---|<---><---|........<---|......<---|........
success_rate: 0.1
idle_rate: 0.31
collision_rate: 0.59
slotted_aloha
                  V                V       V                                                     V      
h0: ...............<---|...............<---><---><--->.............................................<--->
                V       V                              V          V                                     
h1: ...............<---|.....<---><--->....................<---|<---|<---><--->.........................
       V     V                                          V                  V                            
h2: .....<---><--->........................................<---|<---|....................<---><--->.....
success_rate: 0.6
idle_rate: 0.25
collision_rate: 0.15
csma
                  V                V       V                                                     V      
h0: ................<--->..................<---><--->...................................................
                V       V                              V          V                                     
h1: ......................<---><--->...................<---|................<---><--->..................
       V     V                                          V                  V                            
h2: ...<--->.<--->......................................<---|.............................<---><--->....
success_rate: 0.55
idle_rate: 0.39
collision_rate: 0.06
csma_cd
                  V                V       V                                                     V      
h0: ................<--->..................<---><--->...................................................
                V       V                              V          V                                     
h1: ......................<---><--->...................<--|.............................<---><--->......
       V     V                                          V                  V                            
h2: ...<--->.<--->......................................<|................<---><--->....................
success_rate: 0.55
idle_rate: 0.41
collision_rate: 0.04
```
### Questions (60%)
  1. Apply the following settings in all methods and **plot the results**. (2%)
        * host_num_list = [2,3,4,6]
        * packet_num_list = [1200,800,600,400] # To ensure that the total number of packets remains constant.
        * Setting(host_num=h, packet_num=p, max_colision_wait_time=20, p_resend=0.3) for h,p in zip(host_num_list, packet_num_list)
  2. Define two expressions, one for calculating "max_colision_wait_time" and another for calculating "p_resend", which should both include a coefficient parameter c ≥ 1 and other parameters. **Write down the expressions in your report** and modify the "Setting" class accordingly. **(The subsequent questions 3~8 will be based on this new setting.)** (2%)	
        * max_colision_wait_time = ? * c (Hint: Two parameters)
        * p_resend = ? / c (Hint: One parameter)
        ```python
        def __init__(self, host_num=3, total_time=10000, packet_num=500, packet_size=5, max_colision_wait_time=None, p_resend=None, coefficient=8, link_delay=1, seed=None):
            if max_colision_wait_time is None:
                    self.max_colision_wait_time = # your answer
                else:
                    self.max_colision_wait_time = max_colision_wait_time 
                if p_resend is None:
                    self.p_resend = # your answer
                else:
                    self.p_resend = p_resend 
        ```
  3.  Redo the simulations from question 1 using the updated settings for all methods. **Plot the results and describe the influence of using these expressions.** (8%)
        * host_num_list = [2,3,4,6]
        * packet_num_list = [1200,800,600,400]
        * Setting(host_num=h, packet_num=p, coefficient=1) for h,p in zip(host_num_list, packet_num_list)
  4.  What's the influence of "coefficient" in all methods. Apply the following settings, **plot the results, and describe them**. (8%)
        * Setting(coefficient=c) for c in range(start=1, stop=31, step=1)
  5. What's the influence of "packet_num" in all methods. Apply the following settings, **plot the results, and describe them**. (10%)
        * Setting(packet_num=p) for p in range(start=100, stop=1050, step=50)
  6. What's the influence of "host_num" in all methods. Apply the following settings, **plot the results, and describe them**. (10%)
        * Setting(host_num=h) for h in range(start=1, stop=11, step=1)
  7. What's the influence of "packet_size" in all methods. Apply the following settings, **plot the results, and describe them**. (10%)
        * Setting(packet_size=p) for p in range(start=1, stop=20, step=1)
  8. What’s the influence of “link_delay” in CSMA and CSMA/CD? Apply the following settings, **plot the results, and describe them**. (10%)
        * link_delay_list= [0,1,2,3]
        * packet_size_list= [7,5,3,1] # To ensure that the packet_time remains constant.
        * Setting(link_delay=l, packet_siz=p) for l,p in zip(link_delay_list, packet_size_list)
# Homework 4 Specification

ppt: https://docs.google.com/presentation/d/13Gd4gjCjYVC3xamrG8SloPSuiUxWxZtB/edit?usp=sharing&ouid=101230107780361281728&rtpof=true&sd=true

**這次作業只要求過程正確，結果有些微偏誤不會算錯誤**

## Problem

Given a topology graph and the costs of every links, your program should compute the shortest path results by using RIP and OSPF, respectively. You need to provide source code and slides to explain how you implement these protocols.

## Test

### Requirements

Your program needs to implement the `run_ospf()` and `run_rip()` functions.

```python=
# main.py
def run_ospf(link_cost: list) -> tuple[list, list]:
    pass

def run_rip(link_cost: list) -> tuple[list, list]:
    pass
```

You should return the final results that show each router's shortest paths to all other routers and the message communication logs of each router.

## Example

Given a topology graph like this:
![](https://i.imgur.com/FfkIMm1.png =300x)


it should be represented by the following link-cost matrix:

```jsonld=
[
    [  0,   2,   5,   1, 999, 999],
    [  2,   0,   3,   2, 999, 999],
    [  5,   3,   0,   3,   1,   5],
    [  1,   2,   3,   0,   1, 999],
    [999, 999,   1,   1,   0,   2],
    [999, 999,   5, 999,   2,   0]
]
```

where the first row represents the link costs of node 0 to all other nodes, the second row represents the link costs of node 1 to all other nodes, and so on. If a link cost is 999, it means that that link does not exist.

### OSPF

For OSPF, each node (router) needs to flood its link state to all other nodes in the network, and this should be implemented by the flooding algorithm. For a node, it is not allowd to send its link state directly to each of other nodes.

The correct results should look like below:
```python=
(
    [[0, 2, 3, 1, 2, 4],
     [2, 0, 3, 2, 3, 5],
     [3, 3, 0, 2, 1, 3],
     [1, 2, 2, 0, 1, 3],
     [2, 3, 1, 1, 0, 2],
     [4, 5, 3, 3, 2, 0]],
    
    [(0, 0, 1), (0, 0, 2), (0, 0, 3),
     (1, 1, 0), (1, 1, 2), (1, 1, 3),
     (2, 2, 0), (2, 2, 1), (2, 2, 3),
     (2, 2, 4), (2, 2, 5), (3, 3, 0),
     (3, 3, 1), (3, 3, 2), (3, 3, 4),
     (4, 4, 2), (4, 4, 3), (4, 4, 5),
     (5, 5, 2), (5, 5, 4), (2, 0, 4),
     (2, 0, 5), (2, 1, 4), (2, 1, 5),
     (2, 3, 5), (2, 4, 0), (2, 4, 1),
     (2, 5, 0), (2, 5, 1), (2, 5, 3)]
)
```

The return type is tuple, and the first element of the tuple is the path cost (each list is for a router). The second element contains the logs showing how a router sends a link state to another router. Each element is a tuple. For example, `(1, 2, 3)` means that router 1 sends the link state of router 2 to router 3. The logs should be sorted in the order of (source node, original node of the link state, destination node) in each round, and then joined together.
If two messages to the same router are valid, please record the smallest one. For example, if (4, 2, 3) and (1, 2, 3) are both valid in the same round, please record (1, 2, 3) as the smallest message.

### RIP

For RIP, each node (router) will send its distance vector to all of its neighbors.

The correct results should look like below:

```python=
(
    [[0, 2, 3, 1, 2, 4],
     [2, 0, 3, 2, 3, 5],
     [3, 3, 0, 2, 1, 3],
     [1, 2, 2, 0, 1, 3],
     [2, 3, 1, 1, 0, 2],
     [4, 5, 3, 3, 2, 0]],
    
    [(0, 1), (0, 2), (0, 3), (1, 0),
     (1, 2), (1, 3), (2, 0), (2, 1),
     (2, 3), (2, 4), (2, 5), (3, 0),
     (3, 1), (3, 2), (3, 4), (4, 2),
     (4, 3), (4, 5), (5, 2), (5, 4),
     (0, 1), (0, 2), (0, 3), (1, 0),
     (1, 2), (1, 3), (2, 0), (2, 1),
     (2, 3), (2, 4), (2, 5), (3, 0),
     (3, 1), (3, 2), (3, 4), (4, 2),
     (4, 3), (4, 5), (5, 2), (5, 4),
     (0, 1), (0, 2), (0, 3), (1, 0),
     (1, 2), (1, 3), (2, 0), (2, 1),
     (2, 3), (2, 4), (2, 5), (5, 2),
     (5, 4)]
)
```

The return type is tuple, and the first element of the tuple is the path cost (each list is for a router). The second element contains the logs showing how a router sends messages to another router. Each element is a tuple. For example, `(0, 1)` means that router 0 sends its distance vector to router 1.

## Questions and Scores

* OSPF (35% for questions and 15% for code test)
* RIP (35% for questions and 15% for code test)

### Questions

For OSPF

1. Show how you implement the flooding algorithm. (Do not just use direct transmission from all nodes to all other nodes) (10%)
2. What factor will affect the convergence time of OSPF? (10%)

For RIP

1. Show how you implement the distance vector exchange mechanism. (10%)
2. What factor will affect the convergence time of RIP? (10%)


Code Test

* TA will run your code and your result should be the same as the result of TA's program.
    * OSPF (30%)
    * RIP (30%)

## Test data

Below are some test data and their answers, you should check the correctness of your program before submitting it.

```python=
testdata = [ 
    [[0, 4, 1, 999], 
     [4, 0, 2, 999], 
     [1, 2, 0, 3], 
     [999, 999, 3, 0]]
]
```

```python=
ans_ospf = [
    ([[0, 3, 1, 4], 
      [3, 0, 2, 5], 
      [1, 2, 0, 3], 
      [4, 5, 3, 0]], 

     [(0, 0, 1), (0, 0, 2), (1, 1, 0), (1, 1, 2), (2, 2, 0), 
      (2, 2, 1), (2, 2, 3), (3, 3, 2), (2, 0, 3), (2, 1, 3), 
      (2, 3, 0), (2, 3, 1)])
]
```

```python=
ans_rip = [
    ([[0, 3, 1, 4], 
      [3, 0, 2, 5], 
      [1, 2, 0, 3], 
      [4, 5, 3, 0]], 
     
     [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 3), 
      (3, 2), (0, 1), (0, 2), (1, 0), (1, 2), (3, 2)])
]
```

## Submission

* `{student_id}_hw4.zip`
    * `main.py`
    * `report.pdf`


# Homework 5 Specification

ppt: https://docs.google.com/presentation/d/1lhlASYQ1ibxrORnp0YLA0TJ8hDgosA-T/edit?usp=sharing&ouid=101230107780361281728&rtpof=true&sd=true

## Objective

Using QUIC's headers and frame structure to implement the following functions with a UDP socket.

- Error control
- Flow control
- Congestion control

## Functions you have to implement

### Error Control

* Since UDP is an unreliable transport protocol, you must perform your own error control.
* Set a timer for each packet; if the recipient doesn't respond with an ACK in time, the packet should be retransmitted.
* Re-order the packets before passing them to the application layer, as the received packets may be out of order.

### Flow Control

* Make sure that the faster sender does not overwhelm the slower receiver.
* At the connection setup stage, both sides should negotiate the maximum size of each side's receiving window, then use the maximum remote receiving window size as its maximum sending window size.

### Congestion Control

* You can use the TCP new Reno algorithm to implement the congestion control.
* use `tc` to test if your QUIC program can adapt its sending rate to the available bandwidth when you use `tc` to change the available bandwidth.

## Test

Build a pair of client and server programs to send data to each other. Use slides and screenshots to demonstrate that you have implemented the above functions by using the QUIC headers and frame structures. Also, TAs will test the functions you implemented.

You should implement the following methods:

Server side:
```python!
class QUICServer:
    def listen(socket_addr: tuple[str, int]):
        """this method is to open the socket"""
        pass
    
    def accept():
        """this method is to indicate that the client
        can connect to the server now"""
        pass
    
    def send(stream_id: int, data: bytes):
        """call this method to send data, with non-reputation stream_id"""
        pass
    
    def recv() -> tuple[int, bytes]: # stream_id, data
        """receive a stream, with stream_id"""
        pass
    
    def close():
        """close the connection and the socket"""
        pass
```

Client side:
```python!
class QUICClient:
    def connect(socket_addr: tuple[str, int]):
        """connect to the specific server"""
        pass
    
    def send(stream_id: int, data: bytes):
        """call this method to send data, with non-reputation stream_id"""
        pass
    
    def recv() -> tuple[int, bytes]: # stream_id, data
        """receive a stream, with stream_id"""
        pass
    
    def close():
        """close the connection and the socket"""
        pass
```

TA will use your server and client programs to send data to each other. The test code will be as the code below:

```python=
# server side
if __name__ == "__main__":
    server = QUICServer()
    server.listen(("", 30000))
    server.accept()
    server.send(1, b"SOME DATA, MAY EXCEED 1500 bytes")
    recv_id, recv_data = server.recv()
    print(recv_data.decode("utf-8")) # Hello Server!
    server.close() 
```

```python=
# client side
if __name__ == "__main__":
    client = QUICClient()
    client.connect(("127.0.0.1", 30000))
    recv_id, recv_data = client.recv()
    print(recv_data.decode("utf-8")) # SOME DATA, MAY EXCEED 1500 bytes
    client.send(2, b"Hello Server!")
    client.close()
```

**Notice that the maximum number of streams will not exceed 10, and the data size of each stream will be between 0 bytes and 1 megabyte.**

**Also, please note that you should not set the total size of stream buffer larger than 10MB. Otherwise, you will not be able to test the function of flow control.**



To test your function, you can try the following tc command:
```shell
sudo tc qdisc show dev lo
sudo tc qdisc add dev lo root netem loss 5%
sudo tc qdisc change dev lo root netem rate 10Mbit
sudo tc qdisc del dev lo root netem rate 10Mbit
```


## TIPs

* There are many variable-length fields in QUIC. You can set them to fixed-length fields to simplify your programs.
* You can simplify the handshake process. The main point of this lab is to implement error control, flow control, and congestion control.
* `tc` can be used to test the error control and congestion control functions of your programs.
* `struct.pack, struct.unpack` can convert a specified data type to `bytes`
* You can also use `ctypes.BigEndianStructure` to replace `struct`
* `int.to_bytes, int.from_bytes` can convert `int` type to `bytes` of a certain length and vise versa.
* Make good use of `threading` and `heapq`

## Grading Policy
### Requirements

* Program
    * Error control: 25%
    * Flow control: 25%
    * Congestion control: 25%
* Report
    * Explain how you implement error control: 5%
    * Explain how you implement flow control: 5%
    * Explain how you implement congestion control: 5%
    * If you use two streams to send data simultaneously from the client to the server or in the other direction, what will happen if one packet of a stream gets lost? Is the behavior of QUIC different from that of TCP? Why? 10%

### Penalty
- Incorrect upload format (wrong directory structures, wrong file names, etc.): -10%
- Late submission: final score = original score * (3/4) ^ #_late_days
- Cannot compile or run on the workstations: -20%

## Submission

* `{student_id}_hw5.zip`
    * `quic_server.py`
    * `quic_client.py`
    * `report.pdf`


## Reference

* RFC 9000: QUIC: A UDP-Based Multiplexed and Secure Transport
    https://www.rfc-editor.org/rfc/rfc9000.html
* socket --- 底层网络接口 — Python 3.10.10 說明文件
    https://docs.python.org/zh-tw/3.10/library/socket.html


# Homework 6 Specification

ppt : https://docs.google.com/presentation/d/1IGK9BmadXgoT-GXwvyW30lebXPn9cKpy/edit?usp=sharing&ouid=112064783971576677983&rtpof=true&sd=true
## Overview
Design and implement a pair of web client program and web server program that support the HTTP 1.0, HTTP 1.1, HTTP 2.0 protocols and HTTP 3.0 protocols, respectively.
## HTTP
### HTTP/1.0
* Request and response are in plain text.
* Each request needs to create a new connection.
### HTTP/1.1
* Request and response are in plain text.
* The connection between the client the and server will be kept for a while and multiple requests/responses can be transferred over the same connection.
### HTTP/1.0 vs HTTP/1.1
![](https://i.imgur.com/pAIBJkr.png)
### HTTP/1.X Request Format
```
<Request>::= <method> <resource> <HTTP-version>\r\n<headers>\r\n<body>
    <method>::= "GET" | "POST"
    <resource>::= <path>[<query>]
    <HTTP-version>::= “HTTP/1.0” | “HTTP/1.1”
    <headers>::= <header>*
        <header>::= <key>": "<value>"\r\n"
            <key>::= case insensitive string
            <value>::= string
    <body>: string
```
### HTTP/1.X Response Format
```
<response>::= <HTTP-version> <status>\r\n<headers>\r\n<body>
    <HTTP-version>::= “HTTP/1.0” | “HTTP/1.1”
    <status>::= “200 OK” | “404 Not Found” | “400 Bad Request”
    <headers>::= <header>*
        <header>::= <key>": "<value>"\r\n"
            <key>::= case insensitive string
            <value>::= string
    <body>::= string
```
### HTTP/1.X End of Request or Response
* When sending a request or response, the request or response should contain the header `Content-Length: <body_size>` to inform the receiver where the end of request or response is located.
* In HTTP/1.0, the server can indicate the end of a response to the client by closing the connection.
### HTTP/2
* Each connection will be kept alive for a while.
* A connection can have multiple streams to handle multiple requests and responses simultaneously. Each stream is used to transfer a pair of request and response.
* Request and response are splitted into headers frame and data frames.
* The stream id of requests should be odd.
    * E.g., stream id = 1,3,5,7,9....
### HTTP/1.1 vs HTTP/2
![](https://i.imgur.com/1y7MNIa.png)
### HTTP/2 Frame Format
![](https://i.imgur.com/OMLr68Z.png)
### HTTP/2 Frame Header
* Length is the payload size in bytes.
* Type:
    * 0: data frame
    * 1: headers frame
* Flags:
    * 0: default
    * 1: end of stream
* R is not used. Just set it to 0.
### HTTP/2 Frame Payload
* HTTP headers and body are strings. In the payload, they are encoded in utf-8.
* Headers:
    * `<headers>::= <header>*`
    * `<header>::= <key>": "<value>"\r\n"`
    * `<key>::= case insensitive string`
    * `<value>::= string`
    * The key of header is case insensitive.
* Body may be divided into multiple data frames. At the receiver, you need a buffer to append the payload you received from the data frames of a stream.
### Request and Response Pseudo Header
* Request pesudo header
```
:method: GET
:path: /
:scheme: http
:authority: 127.0.0.1:8080
```
* Response pesudo header
```
:status: 200
```
### HTTP/3
* HTTP/3 uses QUIC as the transport-layer protocol instead of TCP.
* Unlike TCP, when a packet is lost in a stream of QUIC, it does not affect the reception of data in other streams.
### HTTP/2 vs HTTP/3
![](https://i.imgur.com/lhzfQ1V.png)
### HTTP/3 Frame Format
* Type(8), Length(32)
![](https://i.imgur.com/QJueQCr.png)
### HTTP/3 Frame Header
* Length is the payload size in bytes.
* Type:
    * 0x00: data frame
    * 0x01: headers frame
### HTTP/3 Frame Payload
* Headers and body are strings. In the payload, they are encoded in utf-8.
* Headers:
    * `<headers>::= <header>*`
    * `<header>::= <key>": "<value>"\r\n"`
    * `<key>::= case insensitive string`
    * `<value>::= string`
    * The key of header is case insensitive.
* Body may be divided into multiple data frames. At the receiver, you need a buffer to append the payload you received from the data frames of a stream.
### Request and Response Pesudo Header
* Request pesudo header
```
:method: GET
:path: /
:authority: 127.0.0.1:8080
:scheme: http
```
* Response pesudo header
```
:status: 200
```
## Requirements
### Submission Format
{student_id}_hw6.zip
├────report.pdf
├────http_1_0_client.py
├────http_1_0_server.py
├────http_1_1_client.py
├────http_1_1_server.py
├────http_2_0_client.py
├────http_2_0_server.py
├────http_3_0_client.py
└────http_3_0_server.py
### Scores
* HTTP/1.0 Server (10%)
* HTTP/1.0 Client (10%)
* HTTP/1.1 Server (10%)
* HTTP/1.1 Client (10%)
* HTTP/2 Server (20%)
* HTTP/2 Client (20%)
* HTTP/2 under dropped packets (5%)
* HTTP/3 under dropped packets (15%)
### Environment
* VM: https://drive.google.com/file/d/1hb7D2ITMoT-eyltGSQ_360sET0oYCE2a/view?usp=sharing
* User: p4, Password: p4
* Python: 3.8.10 (has been installed in VM)
### Penalty
* Incorrect upload format (wrong directory structures, wrong file names, etc.): -10%
* Late submission: final score = original score * (3/4) ^ #_late_days
* **<span style="color: red;"> If you use a  third-party library: final score = 0</span>**
* **<span style="color: red;"> Cannot run on the vm: final score = 0</span>**
### Class HTTPServer
* Each file named http_x_x_server.py should contain this class.
``` python
class HTTPServer()
    def __init__(self, host="127.0.0.1", port=8080) -> None:
    def run(self):
        # Create the server socket and start accepting connections.
    def set_static(self, path):
        # Set the static directory so that when the client sends a GET request to the resource "/static/<file_name>", the file located in the static directory is sent back in the response.
    def close(self):
        # Close the server socket.
```
### Class HTTPClient for HTTP/1.X
* The files "http_1_0_client.py" and "http_1_1_client.py" should contain this class.
* The web client should support receiving the data of response by streaming. If the data is received by streaming, the response object should be returned immediately after the full headers of the response have been received. Then, you can iteratively retrieve the content of the body.
* To prevent getting stuck in a failed socket.recv(), please use socket.settimeout(5).
``` python
class HTTPClient() # For HTTP/1.X
    def __init__(self) -> None:
    def get(self, url, headers=None, stream=False):
        # Send the request and return the response (Object)
        # url = "http://127.0.0.1:8080/static/xxx.txt"
        # If stream=True, the response should be returned immediately after the full headers have been received.
        return response
class Response():
    def __init__(self, socket, stream) -> None:
        self.socket = socket
        self.stream = stream

        # fieleds
        self.version = "" # e.g., "HTTP/1.0"
        self.status = ""  # e.g., "200 OK"
        self.headers = {} # e.g., {content-type: application/json}
        self.body = b""  # e.g. "{'id': '123', 'key':'456'}"
        self.body_length = 0
        self.complete = False
        self.__reamin_bytes = b""
    def get_full_body(self): # used for handling short body
        if self.stream or not self.complete:
            return None
        return self.body # the full content of HTTP response body
    def get_stream_content(self): # used for handling long body
        if not self.stream or self.complete:
            return None
        if self.body != b"":
            content = self.body
            self.body = b""
            return content
        content = self.get_remain_body() # recv remaining body data from socket
        return content # the part content of the HTTP response body
```  
### Class HTTPClient for HTTP/2
* The file “http_2_0_client.py” should contains this class.
* In HTTP/2, the response object should be returned immediately without needing to receive any data from the response.
``` python
class HTTPClient() # For HTTP/2
    def __init__(self) -> None:
    def get(self, url, headers=None):
        # Send the request and return the response (Object)
        # url = "http://127.0.0.1:8080/static/xxx.txt"
        return response
class Response():
    def __init__(self, stream_id, headers = {}, status = "Not yet") -> None:
        self.stream_id = stream_id
        self.headers = headers
        
        self.status = status
        self.body = b""

        self.contents = deque()
        self.complete = False
        
    def get_headers(self):
        begin_time = time.time()
        while self.status == "Not yet":
            if time.time() - begin_time > 5:
                return None
        return self.headers
    
    def get_full_body(self): # used for handling short body
        begin_time = time.time()
        while not self.complete:
            if time.time() - begin_time > 5:
                return None
        if len(self.body) > 0:
            return self.body
        while len(self.contents) > 0:
            self.body += self.contents.popleft()
        return self.body # the full content of HTTP response body
    def get_stream_content(self): # used for handling long body
        begin_time = time.time()
        while len(self.contents) == 0: # contents is a buffer, busy waiting for new content
          if self.complete or time.time()-begin_time > 5: # if response is complete or timeout
              return None
        content = self.contents.popleft() # pop content from deque
        return content # the part content of the HTTP response body
```
### Test Method
* For HTTP/1.0, HTTP/1.1, HTTP/2 in question 1-6:
    * The TA's client should be able to connect to the student's server.
    * The student’s client should be able to connect to the TA’s server
* For question 7-8:
    * Submit your answers in the report.
    * The report should include the screenshots of outputs and the answers to questions.
### HTTP/1.0
* Communication flow:
    1. Run the server on `127.0.0.1:8080` and set the static directory.
    2. The client then calls `client.get(url=f"127.0.0.1:8080/")`.
    3. The server then sends a response. (The file names are randomly selected.)
    ```
    (The new line in the body may be represented as '\r\n' or '\n')
    b"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nContent-Length:254\r\n\r\n<html>
        <header>
        </header>
        <body>
            <a href="/static/file_06.txt">file_06.txt</a>
            <br/>
            <a href="/static/file_01.txt">file_01.txt</a>
            <br/>
            <a href="/static/file_04.txt">file_04.txt</a>
        </body>
    </html>"
    ```
    4. For each file_name in file_names, do step 5-7.
    5. The client call `get("http://127.0.0.1/static/<file_name>", stream=True)`.
    6. The server sends a response `b"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nContent-Length: <file_size>\r\n\r\n<file_data>"`.The file data is read about 4096 bytes at a time until the end of the file is reached.
    7. The client iteratively writes the content obtained by calling `response.get_stream_content()` into the file ``"./target/<file_name>"``.
### HTTP/1.1
* Communication flow:
    1. Run the server on `127.0.0.1:8080` and set the static directory.
    2. The client then calls `client.get(url=f"127.0.0.1:8080/")`.
    3. The server sends a response. (The file names are randomly selected.)
    ```
    (The new line in the body may be represented as '\r\n' or '\n')
    b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length:254\r\n\r\n<html>
        <header>
        </header>
        <body>
            <a href="/static/file_06.txt">file_06.txt</a>
            <br/>
            <a href="/static/file_01.txt">file_01.txt</a>
            <br/>
            <a href="/static/file_04.txt">file_04.txt</a>
        </body>"
    </html>
    ```
    4. For each file_name in file_names, do step 5-7. (The connection should be kept for these four requests, which include the request in step 2 and three requests for files.)
    5. The client calls `get("http://127.0.0.1/static/<file_name>", stream=True)`.
    6. The server sends response `b"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nContent-Length: <file_size>\r\n\r\n<file_data>"`. The file data is read about 4096 bytes at a time until the end of the file is reached.
    7. The client iteratively writes the content obtained by calling `response.get_stream_content()` into the file ``"./target/<file_name>"``.
### HTTP/2
* Communication flow:
    1. Run the server on `127.0.0.1:8080` and set the static directory.
    2. The client calls `client.get(url=f"127.0.0.1:8080/")`.
    3. The server sends a response. (The file names are randomly selected.)
    ```
    headers: 
        :status: 200 OK\r\nContent-Type: text/html\r\nContent-Length:254\r\n
    body: 
        <html>
            <header>
            </header>
            <body>
                <a href="/static/file_06.txt">file_06.txt</a>
                <br/>
                <a href="/static/file_01.txt">file_01.txt</a>
                <br/>
                <a href="/static/file_04.txt">file_04.txt</a>
            </body>
        </html>"
    ```
    4. For each file_name in file_names, the client should continuously call `get("http://127.0.0.1/static/<file_name>", stream=True)` to send out the file request without the need to receive the response of the previous file request.
    5. The server then sends a response (file data) for each file request. The file data is read about 4096 bytes at a time and then sent in data frames until the end of the file is reached.
    ```
    headers: 
        :status: 200 OK\r\nContent-Type: text/plain\r\nContent-Length: <file_size>\r\n
    body:
        <file_data>
    ```
    6. The client iteratively writes the content obtained by calling `response.get_stream_content()` into the file ``"./target/<file_name>"`` for each response. Multiple streams should be handled  simultaneously.
### HTTP/2 Under the Packet-dropping Condition
* Environment setting:
    * Open the VM provided by TA and enter the user ID "p4". (password: p4).
    * Open the terminal and execute `cd "/home/p4/tutorials/exercises/http_drop"`.
    * Copy your HTTP/2 server and client programs to here.
    * Execute `make run` and wait for the environment to be configured, you will see `mininet>`. 
    * Execute `xterm h1 h2` to open two terminals. (You can use **ctrl + right click** to change the font size.)
* Experiment:
    1. Run the server on h1 (10.0.1.1) and set the static directory. *Hints: `python3 http_2_0_server_demo.py`*
    2. The environment will purposely drop the headers frame in stream 5. (If this is not working, please send each of the headers frames with a little delay between them.)
    3. Your client should send requests in the order of stream ID 1, 3, 5, 7. The first get(“http://10.0.1.1:8080/”) request should use stream ID = 1. Then, the three file requests should use stream ID = 3, 5, 7, respectively.
* Questions:
    * Describe why there was only one request received by the server. Write your answers in the report. *Hints: The socket used is a TCP socket.*
### HTTP/3 Under the Packet-dropping Condition
* Requirement:
    1. Use the QUIC API provided by the TA to implement an HTTP/3 server and client, and follow the communication flow used in HTTP/2.
    2. To drop headers frame in stream 5, call the function client_socket.drop(5) on the client socket after creating it.
    3. Your client should send requests in the order of stream ID 1, 3, 5, 7. The first get(“http://10.0.1.1:8080/”) request should use stream ID = 1. Then, the three file requests should use stream ID = 3, 5, 7, respectively.
* Questions:
    * Describe the differences between HTTP/3 and HTTP/2 according to experimental results. Write your answer in the report.
# Homework 7 Specification
TBA

# Mid-term
TBA

# Final project
TBA
