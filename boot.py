#!/usr/bin/env python3
from pathlib import Path
import base64,hashlib,os,sys,subprocess,re,shutil
R=Path(__file__).resolve().parent
G=R/'runtime/generated'; G.mkdir(parents=True,exist_ok=True)

def require_fail(cmd,label):
    p=subprocess.run(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if p.returncode==0: raise SystemExit(f'{label} unexpectedly succeeded; NineHells is corrupt')
    return p.stdout

# TypeScript compiler diagnostics -> JavaScript
s=require_fail(['tsc','--pretty','false','--noEmit',str(R/'carriers/javascript-in-typescript.ts')],'TypeScript JS carrier')
parts={int(i):h for i,h in re.findall(r"NHJS(\d{4})_([0-9A-F]+)",s)}
if not parts: raise SystemExit('TypeScript diagnostics contained no JavaScript payload')
(G/'events.js').write_bytes(bytes.fromhex(''.join(parts[i] for i in sorted(parts))))

# C++ compiler diagnostics -> TypeScript
s=require_fail(['g++','-std=c++17','-fsyntax-only',str(R/'carriers/typescript-in-cpp.cpp')],'C++ TS carrier')
parts={int(i):h for i,h in re.findall(r'NHTS(\d{4})_([0-9A-F]+)',s)}
if not parts: raise SystemExit('C++ diagnostics contained no TypeScript payload')
(G/'integrity.ts').write_bytes(bytes.fromhex(''.join(parts[i] for i in sorted(parts))))

# JavaScript parser diagnostic -> C++
s=require_fail(['node','--check',str(R/'carriers/cpp-in-javascript.js')],'JavaScript C++ carrier')
m=re.search(r'NHCPP_([0-9A-F]+)',s)
if not m: raise SystemExit('JavaScript diagnostic contained no C++ payload')
(G/'moderation.cpp').write_bytes(bytes.fromhex(m.group(1)))

if os.environ.get('NINEHELLS_RECONSTRUCT_ONLY')=='1':
    print('NINEHELLS_CROSS_LANGUAGE_RECONSTRUCT_OK')
    raise SystemExit(0)

# Main Python coordinator remains Folderum-style directory source.
parts=[]
for d in sorted((R/'hellsrc').iterdir()):
    if d.is_dir(): parts.append(d.name.split('_',1)[1])
s=''.join(parts); data=base64.b32decode(s+'='*((8-len(s)%8)%8))
if hashlib.sha256(data).hexdigest()!=(R/'RUNTIME.sha256').read_text().strip(): raise SystemExit('directory-source checksum failure')
if not hasattr(os,'memfd_create'): raise SystemExit('NineHells requires Linux memfd_create')
fd=os.memfd_create('ninehells-runtime'); os.write(fd,data); os.lseek(fd,0,0)
# memfd_create() uses close-on-exec on many Python/Linux builds. The runtime path
# therefore vanished during exec. Explicitly keep this one descriptor alive.
os.set_inheritable(fd, True)
os.execv(sys.executable,[sys.executable,f'/proc/self/fd/{fd}',*sys.argv[1:]])
