from pathlib import Path
import re,hashlib,random,json,collections
D=Path(__file__).resolve().parent
p=Path('/mnt/data/ZL3b-n(7).txt')
h=hashlib.sha256(p.read_bytes()).hexdigest()
assert h=='bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc'
rx=re.compile(r'^<(f\\d+[rv]\\d*)\\.(\\d+),(@Ri|@Ro)>\\s*(.*)$')
g=collections.defaultdict(list)
for line in p.read_text(encoding='utf-8-sig').splitlines():
 m=rx.match(line)
 if not m:continue
 fol,num,kind,body=m.groups()
 body=re.sub(r'^(?:<%>|<![^>]*>|\\s+)*','',body)
 if not re.match('[a-z]',body):raise ValueError((fol,num,body))
 physical=re.sub(r'(?<=[rv])\\d+$','',fol)
 g[physical].append((int(num),fol,body[0]))
seqs={f:[r[2] for r in sorted(rows)] for f,rows in g.items() if len(rows)>=2}
obs=sum(sum(a==b for a,b in zip(s,s[1:])) for s in seqs.values())
pairs=sum(len(s)-1 for s in seqs.values())
rng=random.Random(20261113); vals=[]
for i in range(20000):
 v=0
 for s in seqs.values():
  t=s.copy();rng.shuffle(t)
  v+=sum(a==b for a,b in zip(t,t[1:]))
 vals.append(v)
ge=sum(v>=obs for v in vals)
out={'classification':'EXPLORATORY','verdict':'POSITIVO' if (ge+1)/20001<.05 else 'NULLO','input_sha256':h,'protocol_sha256':hashlib.sha256((D/'PROTOCOL.txt').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'folios':len(seqs),'radial_loci':sum(len(s) for s in seqs.values()),'pairs':pairs,'observed_equal_pairs':obs,'baseline_mean':sum(vals)/len(vals),'baseline_95_interval':[sorted(vals)[499],sorted(vals)[19499]],'null_ge':ge,'p_upper':(ge+1)/20001,'seed':20261113,'permutations':20000}
(D/'RESULT.json').write_text(json.dumps(out,indent=2)+'\\n');print(json.dumps(out,indent=2))
