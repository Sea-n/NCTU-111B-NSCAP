#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")" || exit 1

main() {
	if [[ "${1:-x}" = "docker" ]]; then
		listen
	else
		forward
	fi

	echo "Switch 1 exit."
}

listen() {
	socat tcp-listen:4242,bind=10.113.20.4,fork,reuseaddr exec:/sw1.sh
}

forward() {
	port=$((RANDOM % 8 + 1))
	target="10.113.2$port.5"
	echo "Connected to $target"

	exec socat - tcp-connect:$target:4242
	nc "$target" 4242
	echo done
}

main "$@"
