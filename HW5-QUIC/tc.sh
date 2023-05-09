#!/usr/bin/env bash

tc qdisc show dev lo
tc qdisc add dev lo root netem loss 5%
tc qdisc change dev lo root netem rate 10Mbit
# tc qdisc del dev lo root netem rate 10Mbit
