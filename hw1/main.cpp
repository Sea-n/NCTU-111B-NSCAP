#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <netinet/ip.h>
#include <getopt.h>
#include <cstring>
#include <cstdlib>
#include <cstdio>
#include <pcap.h>

#define BUFSIZE 1002003
#define SIZE_ETHERNET 14

using namespace std;

void parse_pcap(u_char *args, const struct pcap_pkthdr *header, const u_char *packet);

int main(int argc, char** argv) {
	char *dev_name = nullptr;
	char filter_all[] = "tcp or udp or icmp";
	char *filter = nullptr;
	char ebuf[BUFSIZE];
	int opt, cnt=-1;
	pcap_t *handle;
	bpf_program fp;

	static struct option long_options[] = {
		{"interface", required_argument, 0, 'i'},
		{"filter",    required_argument, 0, 'f'},
		{"count",     required_argument, 0, 'c'},
	};

	while ((opt = getopt_long(argc, argv, "i:f:c:", long_options, NULL)) != -1) {
		switch (opt) {
			case 'i':
				dev_name = optarg;
				handle = pcap_open_live(dev_name, BUFSIZE, 1, 1000, ebuf);
				break;
			case 'f':
				if (strcmp(optarg, "all") != 0)
					filter = optarg;
				break;
			case 'c':
				cnt = atoi(optarg);
				break;
		}
	}

	if (dev_name == nullptr) {
		fputs("wrong command", stderr);
		return 1;
	}

	if (handle == NULL) {
		fprintf(stderr, "Couldn't open device %s: %s\n", dev_name, ebuf);
		return 1;
	}

	if (filter == nullptr) filter = filter_all;
	if (pcap_compile(handle, &fp, filter, 0, 0) == -1) {
		fprintf(stderr, "Couldn't parse filter %s: %s\n", filter, pcap_geterr(handle));
		return 2;
	}
	pcap_setfilter(handle, &fp);

	pcap_loop(handle, cnt, parse_pcap, NULL);
	pcap_close(handle);

	return 0;
}

void parse_pcap(u_char *args, const struct pcap_pkthdr *header, const u_char *packet) {
	ip *ip_hdr = (ip*) (packet + SIZE_ETHERNET);
	const unsigned char *payload;
	char addr[256];
	int len;

	if (ip_hdr->ip_p == 1) {
		puts("Transport type: ICMP");
	} else if (ip_hdr->ip_p == 6) {
		puts("Transport type: TCP");
	} else if (ip_hdr->ip_p == 17) {
		puts("Transport type: UDP");
	} else {
		printf("Transport code: %d (unknown)\n\n", ip_hdr->ip_p);
		return;
	}

	inet_ntop(AF_INET, &(ip_hdr->ip_src), addr, INET_ADDRSTRLEN);
	printf("Source IP: %s\n", addr);
	inet_ntop(AF_INET, &(ip_hdr->ip_dst), addr, INET_ADDRSTRLEN);
	printf("Destination IP: %s\n", addr);

	if (ip_hdr->ip_p == 1) {  /* ICMP */
		printf("ICMP type value: %d\n", packet[SIZE_ETHERNET + ip_hdr->ip_hl*4]);
		puts("");
		return;
	}

	/* Print port for both TCP and UDP */
	tcphdr *tcp_hdr = (tcphdr*) (packet + SIZE_ETHERNET + ip_hdr->ip_hl*4);
	udphdr *udp_hdr = (udphdr*) (packet + SIZE_ETHERNET + ip_hdr->ip_hl*4);
	printf("Source port: %d\n", ntohs(tcp_hdr->th_sport));
	printf("Destination port: %d\n", ntohs(tcp_hdr->th_dport));

	if (ip_hdr->ip_p == 6) {  /* TCP */
		payload = packet + SIZE_ETHERNET + ip_hdr->ip_hl*4 + tcp_hdr->th_off*4;
		len = ntohs(ip_hdr->ip_len) - ip_hdr->ip_hl*4 - tcp_hdr->th_off*4;
	}

	if (ip_hdr->ip_p == 17) {  /* UDP */
		payload = packet + SIZE_ETHERNET + ip_hdr->ip_hl*4 + sizeof(udp_hdr);
		len = ntohs(ip_hdr->ip_len) - ip_hdr->ip_hl*4 - sizeof(udp_hdr);
	}

	printf("Payload:");
	for (int i=0; i<(len > 16 ? 16 : len); i++)
		printf(" %02x", payload[i]);
	puts("\n");
	return;

	puts("");
}
