#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")" || exit 1

main() {
	if [[ "$#" -eq 0 ]]; then
		menu
	else
		worker "$@"
	fi
}

menu() {
	while true; do
		seq=$((RANDOM % 1000))
		echo "## File seq $seq:"
		echo -n 'file size (unit: MB) > '
		read -r size
		echo -n 'chunk count > '
		read -r chunk
		send $seq $size $chunk
	done
}

send() {
	seq="$1"
	size="$2"
	chunk="$3"
	file="/tmp/file-$seq"

	dd bs=$((1000 * size / chunk))K count=1 if=/dev/random of=$file

	echo "Sending $file"
	ls -lh "$file"
	seq $chunk | time xargs -n1 -P$chunk /send.sh $seq
}

worker() {
	seq="$1"
	id=$2

	# echo "Thread $id: sending file seq $seq"
	cat "/tmp/file-$seq" | nc 10.113.20.4 4242
	echo "Thread $id done"
}

main "$@"
