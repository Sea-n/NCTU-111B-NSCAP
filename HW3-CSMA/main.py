from setting import Setting
from protocols import aloha, slotted_aloha, csma


def main():
    setting = Setting(host_num=3, total_time=100, packet_num=4,
                      max_colision_wait_time=20, p_resend=0.3,
                      packet_size=3, link_delay=1, seed=4)

    for func in [aloha, slotted_aloha, csma]:
        print(func.__name__)
        succ_rate, idle_rate, coll_rate = func(setting, show_history=True)
        print('success_rate: %.2f' % succ_rate)
        print('idle_rate: %.2f' % idle_rate)
        print('collision_rate: %.2f' % coll_rate)
        print()


if __name__ == '__main__':
    main()
