#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export NINEHELLS_ROOT="$PWD"
mkdir -p runtime data/users data/threads
: > runtime/forum.lock
[[ -p runtime/events.fifo ]] || mkfifo runtime/events.fifo
exec python3 boot.py "${1:-127.0.0.1}" "${2:-9099}"
