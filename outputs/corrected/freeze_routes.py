"""Source audit and deterministic route construction. No gallery values are read.
Run: python3 freeze_routes.py PATH_TO_TMC
"""
import csv, hashlib, json, re, sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
SRC=Path(sys.argv[1])
REV='6fb6dfb4a7efbe24d0fd1dda5097af6131faacde'
def preprocess(text, region, assembly=False):
    macros={'EU','EU_JP'} if region=='PAL' else set()
    active=True; stack=[]; lines=[]
    for no,line in enumerate(text.splitlines(),1):
        m=re.match(r'\s*(?:#|\.)(ifdef|ifndef|if)\s+(.+)',line)
        if m:
            kind,exp=m.groups()
            if kind in ('ifdef','ifndef'): condition=(exp.strip() in macros)==(kind=='ifdef')
            else:
                exp=re.sub(r'defined\s*\(?\s*(\w+)\s*\)?',lambda m:str(m[1] in macros),exp)
                exp=exp.replace('&&',' and ').replace('||',' or ').replace('!',' not ')
                condition=bool(eval(exp,{'__builtins__':{}},{}))
            stack.append((active,condition));active=active and condition
        elif re.match(r'\s*(?:#|\.)(else)\b',line):
            parent,condition=stack[-1];active=parent and not condition
        elif re.match(r'\s*(?:#|\.)(endif)\b',line): active=stack.pop()[0]
        elif active: lines.append((no,line))
    return lines
def figurines(region):
    text='\n'.join(x for _,x in preprocess((SRC/'src/fileselect.c').read_text(),region))
    text=text.split('const struct_080FC3E4 gUnk_080FC3E4[] = {')[1].split('\n};')[0]
    rows=[dict(zip(('bank','flag','gate','category'),(x.strip() for x in m))) for m in re.findall(r'\{\s*([^,]+),([^,]+),([^,]+),([^}]+)\}',text)]
    assert len(rows)==140
    return rows[1:137]
def eligible(row, stage, flags, fused, region):
    gate=row['gate'];flag=row['flag']
    if gate.isdigit(): return stage>=int(gate)
    if gate in ('UNK_6_8','UNK_6_40'): return stage >= (8 if gate=='UNK_6_8' else 64) or flag in flags
    if gate=='UNK_6_10': return flag in fused
    if gate=='UNK_6_20':
        k=int(flag,0)
        groups={0:['20','10','19'],2:['54','56','3D'],3:['3B','4A','D'],4:['49','55','3C']}
        if k==1:return stage>=5 and 'KINSTONE_28' in fused
        if k==5:return stage>=2 and 'MACHI_MACHIHOKORI' in flags
        return any('KINSTONE_'+x in fused for x in groups[k])
    raise ValueError(row)
def audit(region):
    rows=[];label=''
    for no,line in preprocess((SRC/'data/map/entity_headers.s').read_text(),region,True):
        m=re.match(r'(\w+)::',line)
        if m:label=m[1]
        p={k:int(v,16) for k,v in re.findall(r'(\w+)=(0x[0-9a-f]+)',line)}
        if 'tile_entity type=0x2,' in line and p.get('paramB',0)&255==63:
            rows.append(dict(source_id=f'{label}:{p.get("paramA")}',label=label,quantity=p['paramB']>>8,line=no,kind='chest',evidence='EU/US-preprocessed room text',source='data/map/entity_headers.s'))
        if 'object_raw subtype=0x5,' in line and p.get('paramA')==63:
            rows.append(dict(source_id=f'{label}:ground:{p.get("paramC",0)>>16}',label=label,quantity=max(1,p.get('paramB',0)>>8),line=no,kind='ground',evidence='Room text; flagged ground object',source='data/map/entity_headers.s'))
    rows=[r for r in rows if not ('Unused' in r['label'] or r['label'].startswith('TileEntities_37_') or (r['label']=='TileEntities_HyliaDigCaves_North' and r['source_id'].endswith(':56')))]
    for label,source in [('Gregal reward','data/scripts/cloudTops/script_GregalSick.inc'),('Percy reward','src/npc/percy.c')]:
        rows.append(dict(source_id=label,label=label,quantity=100,line=0,kind='reward',evidence='Reward source code',source=source))
    for code,label in [('H','Mt. Crenel fusion'),('P','South Field fusion'),('T','North Field fusion'),('Y','Wind Ruins fusion')]:
        rows.append(dict(source_id='KAKERA_TAKARA_'+code,label=label,quantity=200,line=0,kind='fusion reward',evidence='Flag comment; active regional binary table unavailable',source='include/flags.h'))
    text=(SRC/'src/object/cuccoMinigame.c').read_text().split('prizeData[10] =')[1].split(';')[0]
    for i,q in enumerate(re.findall(r'ITEM_SHELLS,\s*(\d+)',text)):
        rows.append(dict(source_id=f'Anju round {i+1}',label=f'Anju round {i+1}',quantity=int(q),line=86,kind='reward',evidence='prizeData; levels advance, reward skipped after gallery completion',source='src/object/cuccoMinigame.c'))
    assert len({r['source_id'] for r in rows})==len(rows)
    return rows
NAMES=['Earth Element acquired','Fire Element acquired','Pegasus Boots and second sword acquired','Wind dungeon completed; Mole Mitts acquired','Water Element acquired','Royal Crypt completed','Wind Element acquired; Roc\u2019s Cape acquired','Main-game completionist sidequests finished','Vaati defeated; remaining completionist cleanup']
STAGES=[0,1,2,3,4,5,7,7,9]
def assign(r):
    x=r['label']
    if 'Deepwood' in x:return 0
    if x.startswith('Anju'):return (int(x.rsplit(' ',1)[1])-1)//2*2
    if x=='Mt. Crenel fusion':return 1
    if 'HillsKeese' in x or 'Rafters' in x or x in ('Gregal reward','South Field fusion','North Field fusion'):return 2
    if 'Fortress' in x or 'CastorWilds' in x or x in ('Wind Ruins fusion','TileEntities_Ruins_Armos','TileEntities_MinishCaves_Ruins'):return 3
    if 'Droplets' in x or 'Frozen' in x or 'CastleGarden' in x or x in ('Percy reward','TileEntities_HyruleField_WesternWoodsNorth','TileEntities_Caves_HyruleTownWaterfall'):return 4
    if 'RoyalValley' in x or x=='gUnk_080D9328':return 5
    if 'CloudTops' in x:return 6
    return 7
def build(region, variant, rows):
    buckets=[[] for _ in NAMES]
    for r in rows:
        phase=assign(r)
        # Fixed variants concern optional reward sweeps, never encountered-chest delay.
        optional=r['kind']=='fusion reward' or 'Beanstalk' in r['label'] or 'Boomerang' in r['label']
        if optional and variant=='later':phase=min(7,phase+1)
        if optional and variant=='earlier' and phase==7 and 'Boomerang' in r['label']:phase=6
        if variant=='missed_early' and ('DeepwoodShrine_StairsToB1' in r['label'] or r['label']=='Mt. Crenel fusion'):phase=4
        if variant=='missed_late' and r['label']=='TileEntities_Caves_HyruleTownWaterfall':phase=7
        if variant=='missed_postgame' and r['label'] in ('TileEntities_Caves_HyruleTownWaterfall','TileEntities_RoyalValleyGraves_Gina'):phase=8
        buckets[phase].append(r)
    flags=set();fused=set();previous=set();events=[];phases=[]
    table=figurines(region)
    for j,(name,stage,bucket) in enumerate(zip(NAMES,STAGES,buckets)):
        if j==0:flags.update(['0x12','MACHI_MACHIHOKORI'])
        if j>=1:flags.add('YAMADOUKUTU_0E_SENNIN')
        if j>=3:fused.add('KINSTONE_2C')
        if j>=4:flags.add('LV4_10_BOSSDIE')
        if j>=6:flags.add('GORON_DOUKUTU_APPEAR')
        if j>=(6 if variant=='fusion_early' else 8 if variant=='fusion_late' else 7):fused.update('KINSTONE_'+x for x in ['30','33','28','20','54','3B','49'])
        available={i+1 for i,r in enumerate(table) if eligible(r,stage,flags,fused,region)}
        assert previous<=available;previous=available
        wallet=300 if j<2 else 999
        # Wallet 500 and 999 upgrades are both acquired during the boots/ranch cycle.
        for r in bucket:
            events.append(dict(event=len(events),phase=j,milestone=name,type='pickup',source_id=r['source_id'],shells_received=r['quantity'],prerequisites=r['label'],evidence=r['evidence'],source=f'https://github.com/zeldaret/tmc/blob/{REV}/{r["source"]}',collection='immediate on encounter',gallery_access=False))
        events.append(dict(event=len(events),phase=j,milestone=name,type='ordinary town visit',shells_received=0,story_stage=stage,available_ids=sorted(available),unlocked=len(available),wallet_cap=wallet,gallery_access=True,flags=sorted(flags),fusions=sorted(fused)))
        phases.append(dict(phase=j,milestone=name,unlocked=len(available),wallet_cap=wallet,pickups=[r['quantity'] for r in bucket],sources=[r['source_id'] for r in bucket],start_at_farm=False))
    assert phases[-1]['unlocked']==136
    route=dict(schema=1,region=region,variant=variant,source_revision=REV,status='Frozen conditional reference: optional fusion timing assumptions require game/ROM confirmation',construction='Walkthrough story spine; regional reward sweeps chosen before any gallery calculation',events=events,phases=phases,natural_shells=sum(r['quantity'] for r in rows))
    payload=json.dumps(route,sort_keys=True,indent=2)+'\n';path=OUT/f'{region}_{variant}.json';path.write_text(payload)
    digest=hashlib.sha256(payload.encode()).hexdigest();path.with_suffix('.sha256').write_text(digest+'\n')
    with path.with_suffix('.csv').open('w') as f:
        keys=['event','phase','milestone','type','source_id','shells_received','unlocked','wallet_cap','gallery_access','evidence']
        w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(events)
    return route,digest
if __name__=='__main__':
    manifest=[]
    for region in ['PAL','NTSC-U']:
        rows=audit(region)
        (OUT/f'{region}_source_audit.json').write_text(json.dumps(rows,indent=2))
        (OUT/f'{region}_figurine_eligibility.json').write_text(json.dumps(figurines(region),indent=2))
        for variant in ['reference','earlier','later','missed_early','missed_late','fusion_early','fusion_late','missed_postgame']:
            route,digest=build(region,variant,rows);manifest.append(dict(region=region,route=variant,sha256=digest,natural_shells=route['natural_shells'],pools=[p['unlocked'] for p in route['phases']]))
    (OUT/'route_manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2))
