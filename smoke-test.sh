#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export NINEHELLS_ROOT="$PWD"
for x in python3 php node tsc g++; do command -v "$x" >/dev/null || { echo "missing: $x"; exit 1; }; done
rm -rf data runtime
mkdir -p data/users data/threads runtime/generated
: > runtime/forum.lock
mkfifo runtime/events.fifo
NINEHELLS_RECONSTRUCT_ONLY=1 python3 boot.py
[[ -s runtime/generated/events.js && -s runtime/generated/integrity.ts && -s runtime/generated/moderation.cpp ]]
echo NINEHELLS_CROSS_LANGUAGE_RECONSTRUCT_OK
PORT="${NINEHELLS_SMOKE_PORT:-19099}"
./run.sh 127.0.0.1 "$PORT" >runtime/smoke-server.log 2>&1 &
pid=$!
cleanup(){ kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true; }
trap cleanup EXIT
python3 - "$PORT" <<'PY'
import sys,time,urllib.request
port=int(sys.argv[1]); url=f'http://127.0.0.1:{port}/'
last=None
for _ in range(12):
    try:
        with urllib.request.urlopen(url,timeout=15) as r:
            body=r.read().decode('utf-8','replace')
        assert 'NINEHELLS' in body
        print('NINEHELLS_V041_BOOT_HTTP_OK')
        break
    except Exception as e:
        last=e; time.sleep(.5)
else:
    raise SystemExit(f'NineHells did not become reachable: {last}')
PY
cleanup
trap - EXIT
grep -q 'NineHells listening' runtime/smoke-server.log
printf 'NINEHELLS_SMOKE_OK\n'
