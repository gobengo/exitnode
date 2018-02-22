#!/bin/bash

# print each line
# set -x

# exit on error
set -e

./build/bin/set-public-ip "$EXITNODE_PUBLIC_IP"

service sudomesh-gateway start
service tunneldigger start
service babeld start

exec "$@"
