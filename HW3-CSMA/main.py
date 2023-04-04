from protocols import aloha, slotted_aloha, csma, csma_cd
import matplotlib.pyplot as plt
from setting import Setting


def main():
    # Code Test
    funcs = [aloha, slotted_aloha, csma, csma_cd]
    setting = Setting(host_num=3, total_time=100, packet_num=4,
                      max_colision_wait_time=20, p_resend=0.3,
                      packet_size=3, link_delay=1, seed='0816146')

    for func in funcs:
        print(func.__name__)
        succ_rate, idle_rate, coll_rate = func(setting, show_history=True)
        print('success_rate: %.2f' % succ_rate)
        print('idle_rate: %.2f' % idle_rate)
        print('collision_rate: %.2f' % coll_rate)
        print()

    plot('Q1', 'host_num', {func.__name__: {n: func(Setting(host_num=n,
         packet_num=2400//n, max_colision_wait_time=20, p_resend=0.3))
         for n in [2, 3, 4, 6]} for func in funcs})

    plot('Q3', 'host_num', {func.__name__: {n: func(Setting(
         host_num=n, packet_num=2400//n, coefficient=1))
         for n in [2, 3, 4, 6]} for func in funcs})

    plot('Q4', 'coefficient', {func.__name__: {n: func(Setting(coefficient=n))
         for n in range(1, 32)} for func in funcs})

    plot('Q5', 'packet_num', {func.__name__: {n: func(Setting(packet_num=n))
         for n in range(100, 1100, 50)} for func in funcs})

    plot('Q6', 'host_num', {func.__name__: {n: func(Setting(host_num=n))
         for n in range(1, 12)} for func in funcs})

    plot('Q7', 'packet_size', {func.__name__: {n: func(Setting(packet_size=n))
         for n in range(1, 21)} for func in funcs})

    plot('Q8', 'link_delay', {func.__name__: {n: func(Setting(link_delay=n,
         packet_size=7-n-n)) for n in range(4)} for func in [csma, csma_cd]})


def plot(no, param, rates):
    print(f'Plot {no}. {param}')
    for frame in [(0, 'Success'), (1, 'Idle'), (2, 'Collision')]:
        plt.clf()
        plt.title(f'{no}. Influence of {param}')
        plt.xlabel(param)
        xticks = list(rates['csma'].keys())
        if len(xticks) < 8:
            plt.xticks(xticks)
        plt.ylabel(frame[1] + ' Rates')
        plt.ylim([0, 1])
        for func, color in {'aloha': 'kx-', 'slotted_aloha': 'rs-',
                            'csma': 'g^-', 'csma_cd': 'bo-'}.items():
            if func in rates:
                plt.plot(xticks, [r[frame[0]] for n, r in rates[func].items()],
                         color, label=func)
        plt.legend()
        plt.savefig(f'{no}-{frame[1]}.png')


if __name__ == '__main__':
    main()
