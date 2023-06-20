#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")" || exit 1

main() {
	if [[ "${1:-x}" = "docker" ]]; then
		listen
	else
		accept
	fi

	# echo "Receiver exit."
}

listen() {
	socat tcp-listen:4242,bind=10.113.29.6,fork,reuseaddr exec:/recv.sh
}

accept() {
	# echo "Here is a shink server."
	socat stdio /dev/null,ignoreeof
	# echo done
}

main "$@"
