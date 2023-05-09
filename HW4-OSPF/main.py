def run_ospf(link_cost):
    log = []
    for i in range(len(link_cost)):
        for j in range(len(link_cost)):
            if i != j and 0 < link_cost[i][j] < 999:
                log.append((i, i, j))

    next_cost = [i[:] for i in link_cost]
    for _ in range(len(link_cost)):
        for k in range(len(link_cost)):
            for i in range(len(link_cost)):
                for j in range(len(link_cost)):
                    if i != j and link_cost[i][k] + link_cost[k][j] < 999:
                        if next_cost[i][j] == 999:
                            log.append((k, i, j))
                        if next_cost[i][j] > link_cost[i][k] + link_cost[k][j]:
                            next_cost[i][j] = link_cost[i][k] + link_cost[k][j]
        link_cost = next_cost

    return (link_cost, log)


def run_rip(link_cost):
    log = []
    for i in range(len(link_cost)):
        for j in range(len(link_cost)):
            if i != j and 0 < link_cost[i][j] < 999:
                log.append((i, j))

    now_cost = [i[:] for i in link_cost]
    next_cost = [i[:] for i in link_cost]
    for _ in range(len(link_cost)):
        for k in range(len(link_cost)):
            for i in range(len(link_cost)):
                for j in range(len(link_cost)):
                    if i != j and now_cost[i][k] + now_cost[k][j] < 999:
                        if next_cost[i][j] > now_cost[i][k] + now_cost[k][j]:
                            next_cost[i][j] = now_cost[i][k] + now_cost[k][j]
        for k in range(len(link_cost)):
            if sum(now_cost[k]) > sum(next_cost[k]):
                for i in range(len(link_cost)):
                    if 0 < link_cost[k][i] < 999:
                        log.append((k, i))
        now_cost = [i[:] for i in next_cost]

    return (now_cost, log)


def main():
    link_cost = [
            [0,     2,   5,   1, 999, 999],
            [2,     0,   3,   2, 999, 999],
            [5,     3,   0,   3,   1,   5],
            [1,     2,   3,   0,   1, 999],
            [999, 999,   1,   1,   0,   2],
            [999, 999,   5, 999,   2,   0]
    ]

    testdata = [
        [[0, 4, 1, 999],
         [4, 0, 2, 999],
         [1, 2, 0, 3],
         [999, 999, 3, 0]]
    ]

    link_cost = testdata[0]

    print('OSPF:')
    ans_ospf = run_ospf([i[:] for i in link_cost])
    print(ans_ospf)

    print('RIP:')
    ans_rip = run_rip([i[:] for i in link_cost])
    print(ans_rip)


if __name__ == '__main__':
    main()
