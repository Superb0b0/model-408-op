#!/usr/bin/env python3
"""Bounded, reproducible Voynich experiment runner. No frozen inputs are changed."""
import hashlib, json, os, pathlib, random, re, sys
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=pathlib.Path(os.environ.get("VOYNICH_OUTPUT","/tmp/voynich-run"))
OUT.mkdir(parents=True,exist_ok=True)
SEED=20261113
def sha(b): return hashlib.sha256(b).hexdigest()
candidates=sorted(p for p in ROOT.rglob("ZL3b-n.txt") if ".git" not in p.parts)
report={"experiment":"INFRA-01","status":"INCONCLUSIVE","seed":SEED,"utc":datetime.now(timezone.utc).isoformat(),"input":None,"reason":None}
if len(candidates)!=1:
    report["reason"]=f"Expected exactly one ZL3b-n.txt; found {len(candidates)}. No test executed."
else:
    p=candidates[0]; raw=p.read_bytes()
    report["input"]={"path":str(p.relative_to(ROOT)),"sha256":sha(raw),"bytes":len(raw)}
    # Intentionally no scientific claims: corpus parser must be validated before any analysis.
    report["reason"]="Corpus located; scientific test gated pending validated parser and preregistered protocol."
(OUT/"report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(report,ensure_ascii=False))
