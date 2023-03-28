from random import randint


def aloha(setting, show_history=False):
    pkts = setting.gen_packets()
    graph = [[] for _ in range(setting.host_num)]
    queue = [0 for _ in range(setting.host_num)]
    sending = [1e9 for _ in range(setting.host_num)]
    collision = [-1 for _ in range(setting.host_num)]
    print(pkts)
    for t in range(setting.total_time):
        # Decide packet time
        for k in range(setting.host_num):
            if t in pkts[k]:
                if sending[k] == 1e9 and queue[k] == 0:
                    sending[k] = t
                else:
                    queue[k] += 1
            if queue[k] and sending[k] == 1e9:
                queue[k] -= 1
                sending[k] = t + randint(1, setting.max_colision_wait_time)

        # Send packets
        for k in range(setting.host_num):
            if sending[k] > t:
                graph[k].append('.')
            elif sending[k] == t:
                collision = 0
                for i in range(setting.host_num):
                    if i != k and sending[i] < t + 2:
                        collision += 1
                graph[k].append('<')
            elif sending[k] + setting.packet_size + 1 == t:
                if collision:
                    graph[k].append('|')
                else:
                    graph[k].append('>')
            else:
                for i in range(setting.host_num):
                    if i != k and sending[i] < t + 2:
                        collision += 1
                graph[k].append('-')

        # After packet sent
        for k in range(setting.host_num):
            if sending[k] + setting.packet_size + 1 == t:
                sending[k] = 1e9
                if collision:
                    queue[k] += 1

    if show_history:
        print(f'{queue=}, {sending=}')
        for k in range(setting.host_num):
            print('    ', end='')
            for i in range(setting.total_time):
                print('V' if i in pkts[k] else ' ', end='')
            print()
            print(f'h{k}:', ''.join(graph[k]))
        # Show the history of each host

    success_rate = 0
    idle_rate = 0
    collision_rate = 0

    return success_rate, idle_rate, collision_rate
