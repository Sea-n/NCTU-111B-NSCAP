from setting import Setting
from protocols import aloha


def main():
    setting = Setting(host_num=3, total_time=100, packet_num=4,
                      max_colision_wait_time=20, p_resend=0.3,
                      packet_size=3, link_delay=1, seed=4)

    print('aloha')
    aloha(setting, show_history=True)


if __name__ == '__main__':
    main()
