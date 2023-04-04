from random import randint, random


def aloha(setting, show_history=False):
    pkts = setting.gen_packets()
    graph = [[] for _ in range(setting.host_num)]
    queue = [0 for _ in range(setting.host_num)]
    sending = [1e9 for _ in range(setting.host_num)]
    flying = []
    succ_cnt = 0
    idle_cnt = 0
    for t in range(setting.total_time):
        # Decide packet time
        for k in range(setting.host_num):
            if t in pkts[k]:
                if sending[k] == 1e9 and queue[k] == 0:
                    sending[k] = t
                else:
                    queue[k] += 1

        # Detect collision
        flying.append(0)
        for k in range(setting.host_num):
            if sending[k] < t + 1:
                flying[-1] += 1
        if flying[-1] == 0:
            idle_cnt += 1

        # Draw graph
        for k in range(setting.host_num):
            if sending[k] > t:
                graph[k].append('.')
            elif sending[k] == t:
                graph[k].append('<')
            elif sending[k] + setting.packet_size + 1 == t:
                for i in range(sending[k], t+1):  # Check collision
                    if flying[i] >= 2:
                        graph[k].append('|')
                        sending[k] = t + 1 + \
                            randint(0, setting.max_colision_wait_time)
                        break
                else:  # Success
                    graph[k].append('>')
                    succ_cnt += setting.packet_size + 2
                    if queue[k]:
                        sending[k] = t + 1
                        queue[k] -= 1
                    else:
                        sending[k] = 1e9
            else:
                graph[k].append('-')

    if show_history:
        # Show the history of each host
        for k in range(setting.host_num):
            print('   ', ''.join(['V' if i in pkts[k] else ' '
                                  for i in range(setting.total_time)]))
            print(f'h{k}:', ''.join(graph[k]))

    return (succ_cnt / setting.total_time), \
        (idle_cnt / setting.total_time), \
        (1 - (succ_cnt + idle_cnt) / setting.total_time)


def slotted_aloha(setting, show_history=False):
    pkts = setting.gen_packets()
    graph = [[] for _ in range(setting.host_num)]
    queue = [0 for _ in range(setting.host_num)]
    sending = [1e9 for _ in range(setting.host_num)]
    flying = []
    succ_cnt = 0
    idle_cnt = 0
    slot = setting.packet_size + 2
    for t in range(setting.total_time):
        # Decide packet time
        for k in range(setting.host_num):
            if t in pkts[k]:
                if sending[k] == 1e9 and queue[k] == 0:
                    sending[k] = ((t-1) // slot + 1) * slot
                else:
                    queue[k] += 1
            if sending[k] == 1e9 and queue[k]:
                if t % slot == 0 and random() < 0.3:
                    sending[k] = t
                    queue[k] -= 1

        # Detect collision
        flying.append(0)
        for k in range(setting.host_num):
            if sending[k] < t + 1:
                flying[-1] += 1
        if flying[-1] == 0:
            idle_cnt += 1

        # Draw graph
        for k in range(setting.host_num):
            if sending[k] > t:
                graph[k].append('.')
            elif sending[k] == t:
                graph[k].append('<')
            elif sending[k] + setting.packet_size + 1 == t:
                for i in range(sending[k], t+1):  # Check collision
                    if flying[i] >= 2:
                        graph[k].append('|')
                        sending[k] = 1e9
                        queue[k] += 1
                        break
                else:  # Success
                    graph[k].append('>')
                    succ_cnt += setting.packet_size + 2
                    if queue[k]:
                        sending[k] = (t // slot + 1) * slot
                        queue[k] -= 1
                    else:
                        sending[k] = 1e9
            else:
                graph[k].append('-')

    if show_history:
        # Show the history of each host
        for k in range(setting.host_num):
            print('   ', ''.join(['V' if i in pkts[k] else ' '
                                  for i in range(setting.total_time)]))
            print(f'h{k}:', ''.join(graph[k]))

    return (succ_cnt / setting.total_time), \
        (idle_cnt / setting.total_time), \
        (1 - (succ_cnt + idle_cnt) / setting.total_time)
