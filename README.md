# NineHells v0.4.1 — Grafix & Purgatory

A working cursed forum where nine components have mandatory semantic jobs and no component gets the whole truth.

## The nine Hells

1. HTML — structural forum database
2. CSS — one authorization oracle
3. JavaScript — event broker
4. PHP — sessions/login/read state
5. Python — inter-component exception protocol + HTTP coordinator
6. TypeScript — referential-integrity oracle and one vote on reality
7. C++ — moderation policy compiler
8. Unix — FIFOs, locks, processes, plus filesystem mode bits as a second authorization oracle
9. Directories — source/storage/linker; the main runtime is reconstructed from directory names

## v0.4.1: memfd bootstrap fix

Bugfix release only. Fixed the Linux bootstrap so the directory-reconstructed Python runtime memfd is explicitly inherited across `exec`. This prevents `/proc/self/fd/N` from disappearing before the child Python interpreter can open it. No forum features or architecture changed.

`version control/` now also contains the exact v0.4 release ZIP.

## v0.4: Grafix & Purgatory

The feature-complete usability pass. NineHells now has a responsive dark forum UI, visible login state, logout, first-user admin ownership, thread likes backed by Unix hardlinks, admin thread deletion, clearer action feedback, and a dedicated REALITY DISAGREEMENT page that exposes CSS/Unix/TypeScript votes when consensus fails. Startup and component-death behavior remain strict.

The architecture is intentionally not made saner: the compiler-error Ouroboros, directory-held runtime, CSS/Unix/TypeScript consensus, C++ moderation, PHP sessions, JavaScript events, Python exception IPC, HTML structure and Unix kernel objects remain required.

`version control/` now carries exact v0.1, v0.2 and v0.3 release ZIPs.

## v0.3: No Source of Truth

Important forum decisions no longer trust one subsystem. CSS, Unix filesystem permissions and TypeScript integrity independently vote on whether an operation is valid. The request proceeds only when all required views of reality agree. A disagreement is rejected and recorded in `runtime/reality-disagreements.log`.

For create/reply permissions, CSS selectors provide one answer while Unix mode bits under `policy/unix/` provide another. TypeScript separately proves that the current user/thread/reply relationship graph is internally valid. The existing compiler-error Ouroboros remains intact.

The smoke test deliberately creates a split-brain state where CSS allows a reply and Unix denies it, and verifies that NineHells rejects the operation.

`version control/` contains exact ZIP snapshots of previous releases so only the newest tree needs to be pushed.

## Version history

### v0.4.1 — memfd bootstrap fix

Fixed memfd descriptor inheritance across `exec`; no feature changes.

### v0.1 — First Circle

First working NineHells prototype. Register/login/thread/reply/read, CSS permissions, TypeScript integrity, C++ moderation, JavaScript events, PHP sessions, Python exception IPC, Unix FIFOs/locks, HTML structure, and directory-encoded main runtime. Every Hell had a component-death test.

### v0.2 — Ouroboros

Added cross-language diagnostic storage: TypeScript compiler failures carry JavaScript, C++ compiler failures carry TypeScript, and a JavaScript parser failure carries C++. Successful compilation/parsing where failure is expected means corruption.

### v0.3 — No Source of Truth

Added multi-system reality consensus. CSS authorization, Unix mode-bit authorization and TypeScript integrity must agree before important operations proceed. Added deliberate split-brain testing and disagreement logging while retaining the v0.2 Ouroboros.

### v0.4 — Grafix & Purgatory

Feature-complete polish release. Added responsive browser UI, login/logout feedback, first-user admin, hardlink-backed likes, admin deletion, visible consensus status and human-readable reality-disagreement handling. Retains all previous architectural abuse and tests.

## Requirements

Linux, Python 3, PHP CLI, Node.js, TypeScript (`tsc`), and `g++`. Debian/Ubuntu quick install: `sudo apt install -y python3 php-cli nodejs npm g++ && sudo npm install -g typescript`.

## Run

    ./smoke-test.sh
    ./run.sh 127.0.0.1 9099

Open `http://127.0.0.1:9099`.
