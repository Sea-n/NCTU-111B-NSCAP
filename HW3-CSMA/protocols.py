from random import randint, random


def common_end(setting, show_history, pkts, graph):
    if show_history:
        for k in range(setting.host_num):
            print('   ', ''.join(['V' if i in pkts[k] else ' '
                                  for i in range(setting.total_time)]))
            print(f'h{k}:', ''.join(graph[k]))

    succ_cnt = sum([graph[k].count('>') for k in range(setting.host_num)
                    ]) * (setting.packet_size + 2)
    idle_cnt = sum([1 if sum([1 if graph[k][t] != '.' else 0
                              for k in range(setting.host_num)]) == 0 else 0
                    for t in range(setting.total_time)])

    return ((succ_cnt / setting.total_time),
            (idle_cnt / setting.total_time),
            (1 - (succ_cnt + idle_cnt) / setting.total_time))


def aloha(setting, show_history=False):
    pkts = setting.gen_packets()
    graph = [[] for _ in range(setting.host_num)]
    queue = [0 for _ in range(setting.host_num)]
    sending = [1e9 for _ in range(setting.host_num)]
    for t in range(setting.total_time):
        # Decide packet time
        for k in range(setting.host_num):
            if t in pkts[k]:
                if sending[k] == 1e9 and queue[k] == 0:
                    sending[k] = t
                else:
                    queue[k] += 1

        # Detect collision
        coll = []
        for k in range(setting.host_num):
            if sending[k] + setting.packet_size + 1 == t:
                for i in range(setting.host_num):  # Check collision
                    if i != k and graph[i][-(t - sending[k]):] \
                                  .count('.') != t - sending[k]:
                        coll.append(k)

        # Draw graph
        for k in range(setting.host_num):
            if sending[k] > t:
                graph[k].append('.')
            elif sending[k] == t:
                graph[k].append('<')
            elif k in coll:
                graph[k].append('|')
                sending[k] = t + 1 + randint(0, setting.max_colision_wait_time)
            elif sending[k] + setting.packet_size + 1 == t:
                graph[k].append('>')
                sending[k] = 1e9
                if queue[k]:
                    sending[k] = t + 1
                    queue[k] -= 1
            else:
                graph[k].append('-')

    return common_end(setting, show_history, pkts, graph)


def slotted_aloha(setting, show_history=False):
    pkts = setting.gen_packets()
    graph = [[] for _ in range(setting.host_num)]
    queue = [0 for _ in range(setting.host_num)]
    sending = [1e9 for _ in range(setting.host_num)]
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
        coll = []
        for k in range(setting.host_num):
            if sending[k] + setting.packet_size + 1 == t:
                for i in range(setting.host_num):  # Check collision
                    if i != k and graph[i][-(t - sending[k]):] \
                                  .count('.') != t - sending[k]:
                        coll.append(k)

        # Draw graph
        for k in range(setting.host_num):
            if sending[k] > t:
                graph[k].append('.')
            elif sending[k] == t:
                graph[k].append('<')
            elif k in coll:
                graph[k].append('|')
                sending[k] = 1e9
                queue[k] += 1
            elif sending[k] + setting.packet_size + 1 == t:
                graph[k].append('>')
                sending[k] = 1e9
                if queue[k]:
                    sending[k] = (t // slot + 1) * slot
                    queue[k] -= 1
            else:
                graph[k].append('-')

    return common_end(setting, show_history, pkts, graph)


def csma(setting, show_history=False):
    pkts = setting.gen_packets()
    graph = [[] for _ in range(setting.host_num)]
    queue = [0 for _ in range(setting.host_num)]
    sending = [1e9 for _ in range(setting.host_num)]
    for t in range(setting.total_time):
        # Decide packet time
        for k in range(setting.host_num):
            if t in pkts[k]:
                if sending[k] == 1e9 and queue[k] == 0:
                    sending[k] = t
                else:
                    queue[k] += 1

        # CSMA
        for k in range(setting.host_num):
            for i in range(setting.host_num):
                if sending[k] == t and i != k and graph[i][-1] in ['-', '>']:
                    sending[k] = t + 1 \
                        + randint(0, setting.max_colision_wait_time)

        # Detect collision
        coll = []
        for k in range(setting.host_num):
            if sending[k] + setting.packet_size + 1 == t:
                for i in range(setting.host_num):  # Check collision
                    if i != k and graph[i][-(t - sending[k]):] \
                                  .count('.') != t - sending[k]:
                        coll.append(k)

        # Draw graph
        for k in range(setting.host_num):
            if sending[k] > t:
                graph[k].append('.')
            elif sending[k] == t:
                graph[k].append('<')
            elif k in coll:
                graph[k].append('|')
                sending[k] = t + 1 + randint(0, setting.max_colision_wait_time)
            elif sending[k] + setting.packet_size + 1 == t:
                graph[k].append('>')
                sending[k] = 1e9
                if queue[k]:
                    sending[k] = t + 1
                    queue[k] -= 1
            else:
                graph[k].append('-')

    return common_end(setting, show_history, pkts, graph)


def csma_cd(setting, show_history=False):
    pkts = setting.gen_packets()
    graph = [[] for _ in range(setting.host_num)]
    queue = [0 for _ in range(setting.host_num)]
    sending = [1e9 for _ in range(setting.host_num)]
    for t in range(setting.total_time):
        # Decide packet time
        for k in range(setting.host_num):
            if t in pkts[k]:
                if sending[k] == 1e9 and queue[k] == 0:
                    sending[k] = t
                else:
                    queue[k] += 1

        # CSMA
        for k in range(setting.host_num):
            for i in range(setting.host_num):
                if sending[k] == t and i != k and graph[i][-1] in ['-', '>']:
                    sending[k] = t + 1 \
                        + randint(0, setting.max_colision_wait_time)

        # Detect collision
        coll = []
        for k in range(setting.host_num):
            if sending[k] <= t:
                for i in range(setting.host_num):  # Check collision
                    if i != k and graph[i][:-setting.link_delay][
                            -(t - sending[k]):].count('.') != t - sending[k]:
                        coll.append(k)

        # Draw graph
        for k in range(setting.host_num):
            if sending[k] > t:
                graph[k].append('.')
            elif sending[k] == t:
                graph[k].append('<')
            elif k in coll:
                graph[k].append('|')
                sending[k] = t + 1 + randint(0, setting.max_colision_wait_time)
            elif sending[k] + setting.packet_size + 1 == t:
                graph[k].append('>')
                sending[k] = 1e9
                if queue[k]:
                    sending[k] = t + 1
                    queue[k] -= 1
            else:
                graph[k].append('-')

    return common_end(setting, show_history, pkts, graph)
