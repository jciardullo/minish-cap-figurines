import unittest,math
from search import policy,CASES
from complexity_audit import audit as features
from frontier import knee,frontier,selections

def row(id,C,R,mean=None,compact=True):return dict(id=id,complexity=C,features=[0,0,0,0,C,0,0,0],worst_regret=R,mean_regret=R if mean is None else mean,compact=compact,cases=[])
class Tests(unittest.TestCase):
 def test_imports_are_read_only(self):
  import subprocess,sys,tempfile
  from pathlib import Path
  code="""from pathlib import Path
import sys
sys.path.insert(0, sys.argv[1])
def reject_write(*args, **kwargs):
 raise AssertionError('Import attempted to write a file')
Path.write_text = reject_write
import search, frontier, complexity_audit
assert len(search.CASES) == 26
"""
  with tempfile.TemporaryDirectory() as scratch:
   subprocess.run([sys.executable,'-c',code,str(Path(__file__).resolve().parent)],cwd=scratch,check=True,capture_output=True,text=True)
 def test_cases(self):
  self.assertEqual(len(CASES),26);self.assertEqual(sum(c['scenario_class']=='route' for c in CASES),16);self.assertEqual(sum(c['region']=='PAL' for c in CASES),14);self.assertEqual(sum(c['region']=='NTSC-U' for c in CASES),12)
 def test_geometry(self):
  data=[row(1,1,.9),row(2,2,.2),row(3,4,.1)];picked,coords,interior=knee(data);self.assertEqual(picked['id'],2);self.assertTrue(interior);self.assertGreater(coords[1]['signed_distance'],0);self.assertAlmostEqual(coords[0]['signed_distance'],0);self.assertAlmostEqual(coords[-1]['signed_distance'],0)
 def test_no_knee(self):
  p,_,yes=knee([row(1,1,.9),row(2,2,.6),row(3,3,.1)]);self.assertEqual(p['id'],1);self.assertFalse(yes)
 def test_named_rules(self):
  data=[row(1,1,.8),row(2,1,.7),row(3,4,.05),row(4,4,.04),row(5,6,.03)];s=selections(data);self.assertEqual(s['minimal'],2);self.assertEqual(s['compact'],5);self.assertEqual(s['simplest_5_percent'],4)
 def test_no_5(self):self.assertIsNone(selections([row(1,1,.1)])['simplest_5_percent'])
 def test_dominance(self):self.assertEqual([r['id'] for r in frontier([row(1,1,.9),row(2,2,.95),row(3,3,.5)])],[1,3])
 def test_distinct_counting(self):
  v=policy(early=(900,600,20,100),post=((20,100),)*3);vec,C,tier,compact,valid=features(v);self.assertEqual(vec[2],1);self.assertEqual(vec[5],1);self.assertEqual(vec[6],0);self.assertEqual(C,sum(a*b for a,b in zip(vec,[4,2,1,2,1,2,0,1])));self.assertTrue(compact)
 def test_selected_feature_vectors(self):
  import json
  from pathlib import Path
  d=json.loads((Path(__file__).parent/'candidates.json').read_text())
  self.assertEqual(features(d[6457]['parameters'])[0],[1,0,2,0,5,1,0,1])
  self.assertEqual(features(d[6098]['parameters'])[0],[1,0,2,0,4,1,0,2])
  for p in d:self.assertTrue(features(p['parameters'])[-1])
 def test_degenerate_knee(self):
  p,_,yes=knee([row(1,1,.1)]);self.assertEqual(p['id'],1);self.assertFalse(yes)
 def test_score_extremes(self):self.assertEqual(features(policy())[0][3],0)
 def test_timing_policy_unchanged(self):
  import json
  from pathlib import Path
  for region,id in [('PAL',6457),('NTSC-U',6098)]:
   d=json.loads((Path(__file__).parent/'exact'/f'{region}_{id}.json').read_text());ref=d['cases'][0]['resources']
   for c in d['cases']:
    if ':timing:' in c['scenario']:self.assertEqual(c['resources'],ref)
 def test_compact_need_not_have_largest_complexity(self):
  d=[row(1,1,.8,compact=False),row(2,3,.1),row(3,6,.2)];self.assertEqual(selections(d)['compact'],2)
 def test_protected_does_not_require_point_frontier(self):
  from search import retain
  candidates=[dict(id=0,complexity=10,tier=1),dict(id=1,complexity=11,tier=1)];r={('PAL',0):dict(point=.1,lower=.05,upper=.15),('PAL',1):dict(point=.12,lower=.08,upper=.16)};self.assertIn(1,retain(candidates,r,'PAL'))
if __name__=='__main__':unittest.main()
