from protocols import aloha, slotted_aloha, csma, csma_cd
import matplotlib.pyplot as plt
from setting import Setting


def main():
    # Code Test
    setting = Setting(host_num=3, total_time=100, packet_num=4,
                      max_colision_wait_time=20, p_resend=0.3,
                      packet_size=3, link_delay=1, seed='0816146')

    for func in [aloha, slotted_aloha, csma, csma_cd]:
        print(func.__name__)
        succ_rate, idle_rate, coll_rate = func(setting, show_history=True)
        print('success_rate: %.2f' % succ_rate)
        print('idle_rate: %.2f' % idle_rate)
        print('collision_rate: %.2f' % coll_rate)
        print()

    # Question 1 & 3: host_num
    nums = [2, 3, 4, 6]
    for func in [aloha, slotted_aloha, csma, csma_cd]:
        rates = {n: func(Setting(host_num=n, packet_num=2400//n,
                 max_colision_wait_time=20, p_resend=0.3)) for n in nums}
        plot('Q1', 'host_num', func.__name__, nums, rates)

        rates = {n: func(Setting(host_num=n, packet_num=2400//n,
                                 coefficient=1)) for n in nums}
        plot('Q3', 'host_num', func.__name__, nums, rates)

    # Question 4: coefficient
    nums = list(range(1, 32))
    for func in [aloha, slotted_aloha, csma, csma_cd]:
        rates = {n: func(Setting(coefficient=n)) for n in nums}
        plot('Q4', 'coefficient', func.__name__, nums, rates)

    # Question 5: packet_num
    nums = list(range(100, 1100, 50))
    for func in [aloha, slotted_aloha, csma, csma_cd]:
        rates = {n: func(Setting(packet_num=n)) for n in nums}
        plot('Q5', 'packet_num', func.__name__, nums, rates)

    # Question 6: host_num
    nums = list(range(1, 12))
    for func in [aloha, slotted_aloha, csma, csma_cd]:
        rates = {n: func(Setting(host_num=n)) for n in nums}
        plot('Q6', 'host_num', func.__name__, nums, rates)

    # Question 7: packet_size
    nums = list(range(1, 21))
    for func in [aloha, slotted_aloha, csma, csma_cd]:
        rates = {n: func(Setting(packet_size=n)) for n in nums}
        plot('Q7', 'packet_size', func.__name__, nums, rates)

    # Question 8: link_delay
    nums = list(range(4))
    for func in [csma, csma_cd]:
        rates = {n: func(Setting(link_delay=n, packet_size=7-n-n))
                 for n in nums}
        plot('Q8', 'link_delay', func.__name__, nums, rates)


def plot(no, param, func, xticks, rates):
    plt.clf()
    plt.title(f'{no}. {param}: {func}')
    plt.xlabel(param)
    if len(xticks) < 8:
        plt.xticks(xticks)
    plt.ylabel('Rates')
    plt.ylim([0, 1])
    plt.plot(xticks, [rates[i][0] for i in xticks], 'go-', label='success')
    plt.plot(xticks, [rates[i][1] for i in xticks], 'bo-', label='idle')
    plt.plot(xticks, [rates[i][2] for i in xticks], 'ro-', label='collision')
    plt.legend()
    plt.savefig(f'{no}-{func}.png')

    print(f'Plot {no}. {param}: {func}')


if __name__ == '__main__':
    main()
