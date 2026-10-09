"""Deterministic compression of exact selected policies; no rounding or interpolation."""
import gzip,hashlib,json,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parent;W=ROOT.parent/'work/funded';dest=ROOT/'policy_lookup';rows=[]
for region in ['PAL','NTSC-U']:
 for profile in ['reference','earlier','missed_postgame','fusion_early']:
  for phase in range(9):
   if profile=='fusion_early' and phase!=6:continue
   source=W/f'{region}_{profile}_optimal_phase{phase}.policy'
   raw=source.read_bytes();out=dest/(source.name+'.gz');out.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));assert gzip.decompress(out.read_bytes())==raw
   rows.append(dict(region=region,profile=profile,phase=phase,file=out.name,raw_bytes=len(raw),compressed_bytes=out.stat().st_size,raw_sha256=hashlib.sha256(raw).hexdigest()))
(dest/'manifest.json').write_text(json.dumps(rows,indent=2));print(len(rows),'policy tables packaged')

ties={}
for region in ['PAL','NTSC-U']:
 for profile in ['reference','earlier','missed_postgame','fusion_early']:
  for row in csv.DictReader((W/f'{region}_{profile}_optimal_values.csv').open()):
   if profile=='fusion_early' and row['phase']!='6':continue
   actions=[int(a) for a in row['tied_actions'].split(';') if a]
   if len(actions)>1:ties['|'.join([region,profile,row['phase'],row['owned'],row['shells'],row['rupees']])]=actions
(dest/'sampled_tied_actions.json').write_text(json.dumps(ties,separators=(',',':')))
print(len(ties),'sampled tied sets packaged')
