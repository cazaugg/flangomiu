#!/bin/sh
set -eu

DATA_DIR="${DATA_DIR:-/data/flagomiu}"
export DATA_DIR

mkdir -p "$DATA_DIR/uploads" 2>/dev/null || true

if [ ! -w "$DATA_DIR" ]; then
    cat >&2 <<EOF
entrypoint: $DATA_DIR is not writable by uid $(id -u).
On the host run:
  sudo mkdir -p $DATA_DIR
  sudo chown -R 10001:10001 $DATA_DIR
EOF
    exit 1
fi

if [ -n "${ADMIN_PASSWORD:-}" ] || [ -n "${GUEST_PASSWORD:-}" ]; then
    python -m app.bootstrap
fi

exec "$@"
