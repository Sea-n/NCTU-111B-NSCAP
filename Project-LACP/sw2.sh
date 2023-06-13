#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")" || exit 1

main() {
	tc qdisc add dev eth0 root netem rate 100kbit loss 1%
	tc qdisc add dev eth1 root netem rate 100kbit loss 1%
	tc qdisc add dev eth2 root netem rate 100kbit loss 1%
	tc qdisc add dev eth3 root netem rate 100kbit loss 1%
	tc qdisc add dev eth4 root netem rate 100kbit loss 1%
	tc qdisc add dev eth5 root netem rate 100kbit loss 1%
	tc qdisc add dev eth6 root netem rate 100kbit loss 1%
	tc qdisc add dev eth7 root netem rate 100kbit loss 1%

	socat tcp-listen:4242,bind=10.113.21.5,fork,reuseaddr tcp-connect:10.113.29.6:4242 &
	socat tcp-listen:4242,bind=10.113.22.5,fork,reuseaddr tcp-connect:10.113.29.6:4242 &
	socat tcp-listen:4242,bind=10.113.23.5,fork,reuseaddr tcp-connect:10.113.29.6:4242 &
	socat tcp-listen:4242,bind=10.113.24.5,fork,reuseaddr tcp-connect:10.113.29.6:4242 &
	socat tcp-listen:4242,bind=10.113.25.5,fork,reuseaddr tcp-connect:10.113.29.6:4242 &
	socat tcp-listen:4242,bind=10.113.26.5,fork,reuseaddr tcp-connect:10.113.29.6:4242 &
	socat tcp-listen:4242,bind=10.113.27.5,fork,reuseaddr tcp-connect:10.113.29.6:4242 &
	socat tcp-listen:4242,bind=10.113.28.5,fork,reuseaddr tcp-connect:10.113.29.6:4242 &

	sleep 86400
}

main "$@"
