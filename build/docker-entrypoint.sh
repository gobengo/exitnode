#!/bin/bash

usage () {
cat <<HELP_USAGE
$0

Docker entrypoint. Configures services for PUBLIC_IP env var, starts services.
HELP_USAGE
}

# print each line
# set -x

# exit on error
set -e

./build/bin/set-public-ip "$PUBLIC_IP"

service sudomesh-gateway start
service tunneldigger start
service babeld start

exec "$@"
