"""Observable, spoiler-light policy lookup. No future pickups or hidden RNG input.
Raw selected representatives are supplied in policy_lookup/*.policy.gz.
"""
import argparse,gzip,json,random,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PHASE={'earth':0,'fire':1,'boots':2,'mitts':3,'water':4,'crypt':5,'wind':6,'full':8}
WEIGHTS={'reference':.0466465141507168,'earlier':.217688307470214,'halfcap_reference':.7356651783790692}
def action(region,milestone,owned,shells,rupees,chance,profile='reference',wind_mode='early'):
 if not(0<=owned<=136 and 0<=shells<=999 and 0<=rupees<=999 and 0<=chance<=100):raise ValueError('Inputs outside game caps')
 if owned==136:return dict(action='complete')
 if chance==0:return dict(action='wait',reason='Current eligible pool is exhausted.')
 if milestone=='full' and chance!=max(1,100*(136-owned)//136):return dict(action='wait',reason='The displayed base chance does not match the full pool. Finish remaining eligibility unlocks, or check the inputs.')
 j=PHASE[milestone]
 if milestone=='wind':j=6 if wind_mode=='early' else 7
 source='earlier' if profile=='earlier' else 'reference';query_shells=shells
 if j==6 and chance==max(1,100*(130-owned)//130) and chance!=max(1,100*(123-owned)//123):source='fusion_early'
 if profile=='halfcap_reference' and j==7:source='missed_postgame';query_shells=max(0,shells-150)
 qr=rupees if rupees%5 in [0,4] else rupees-rupees%5
 index=(owned*400000+query_shells*400+2*(qr//5)+(qr%5==4))*2
 file=ROOT/'policy_lookup'/f'{region}_{source}_optimal_phase{j}.policy.gz'
 with gzip.open(file,'rb') as f:f.seek(index);raw=f.read(2)
 a=struct.unpack('<H',raw)[0] if len(raw)==2 else 0
 result=dict(profile=profile,wind_mode=wind_mode,certified_cash_grid=qr==rupees)
 if a==0:result.update(action='wait',reason='End this gallery visit and continue playing normally.')
 elif a<=100:result.update(action='pull',wager=min(a,101-chance,shells),nominal_success_percent=max(15 if owned<50 else 12 if owned<80 else 9 if owned<110 else 6,chance+min(a,101-chance,shells)-1))
 else:
  bundles=4 if region=='NTSC-U' else 3;q=(a-101)%bundles+1;n=(a-101)//bundles;price=200 if region=='NTSC-U' else 300;wallet=300 if j<2 else 999
  if min(wallet,rupees+20*n)<q*price or shells+30*q>999:raise ValueError('State outside lookup coverage: recommended transaction is not legal.')
  result.update(action='restock',bundles=q,shells_purchased=30*q,farming_pickups=n,purchase_rupees=q*price,trip_seconds=(45 if n else 20)+15*q+4*n,ending_rupees=min(wallet,rupees+20*n)-price*q)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--region',choices=['PAL','NTSC-U'],default='PAL');p.add_argument('--milestone',choices=PHASE,required=True);p.add_argument('--owned',type=int,required=True);p.add_argument('--shells',type=int,required=True);p.add_argument('--rupees',type=int,default=0);p.add_argument('--chance',type=int,required=True);p.add_argument('--begin-visit',action='store_true');p.add_argument('--balanced',action='store_true');p.add_argument('--reset',action='store_true');p.add_argument('--session',type=Path,default=ROOT/'gallery_session.json');args=p.parse_args()
 session=json.loads(args.session.read_text()) if args.session.exists() and not args.reset else dict(profile=random.choices(list(WEIGHTS),weights=list(WEIGHTS.values()))[0] if args.balanced else 'reference')
 if args.begin_visit or 'wind_mode' not in session:session['wind_mode']='early' if args.owned<80 else 'late'
 args.session.write_text(json.dumps(session,indent=2));print(json.dumps(action(args.region,args.milestone,args.owned,args.shells,args.rupees,args.chance,session['profile'],session['wind_mode']),indent=2))
