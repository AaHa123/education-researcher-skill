import sys,unittest,tempfile,subprocess,json,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'scripts';T=ROOT/'templates';E=ROOT/'examples'

def run_script(name,*args):
    return subprocess.run([sys.executable,str(S/name),*map(str,args)],capture_output=True,text=True)
class TestScripts(unittest.TestCase):
    def test_default_gates_block(self):
        for gate in ('G1','G2'):
            res=run_script('quality_gate.py','--gate',gate,'--file',T/f'gate_{gate.lower()}.json')
            self.assertEqual(res.returncode,2,res.stdout+res.stderr)
            self.assertIn('"passed": false',res.stdout)
    def test_human_signed_gate_can_pass_schema(self):
        record=json.loads((T/'gate_g1.json').read_text(encoding='utf-8'))
        record['reviewer_name']='示例评审人（仅测试）';record['review_date']='2026-11-05';record['summary_decision']='pass'
        for item in record['items']:
            item.update(status='pass',evidence_ref='reference/mock.md',reviewer_note='此记录仅用于自动化测试，不是真实学术评审')
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'gate.json';file.write_text(json.dumps(record,ensure_ascii=False),encoding='utf-8')
            res=run_script('quality_gate.py','--gate','G1','--file',file)
            self.assertEqual(res.returncode,0,res.stdout+res.stderr)
            self.assertIn('"passed": true',res.stdout)
    def test_rq_coverage(self):
        res=run_script('rq_coverage.py','--questions',T/'research_questions.csv','--mapping',T/'rq_evidence_map.csv')
        self.assertEqual(res.returncode,0,res.stdout+res.stderr)
    def test_survey_report(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'survey.md'
            res=run_script('survey_descriptives.py','--data',E/'demo_survey.csv','--codebook',T/'survey_codebook.json','--out',out)
            self.assertEqual(res.returncode,0,res.stderr)
            s=out.read_text(encoding='utf-8')
            self.assertIn('完整案例n',s);self.assertIn('Cronbach',s)
    def test_rubric_report(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'rubric.md'
            res=run_script('ppt_rubric.py','--data',E/'demo_ppt_scores.csv','--rubric',T/'ppt_rubric.json','--out',out)
            self.assertEqual(res.returncode,0,res.stderr)
            self.assertIn('DEMO001',out.read_text(encoding='utf-8'))
    def test_literature_report(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'lit.md'
            res=run_script('literature_matrix.py','--input',T/'literature_matrix.csv','--out',out)
            self.assertEqual(res.returncode,0,res.stderr)
            self.assertTrue(out.exists())
    def test_paper_outline(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'paper.md'
            res=run_script('paper_outline.py','--project',T/'project.json','--out',out)
            self.assertEqual(res.returncode,0,res.stderr)
            self.assertIn('【待填',out.read_text(encoding='utf-8'))
    def test_init_project(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'myproject'
            res=run_script('init_project.py','--name','示例课题','--out',out)
            self.assertEqual(res.returncode,0,res.stderr)
            self.assertTrue((out/'templates'/'gate_g1.json').exists())
            self.assertFalse((out/'examples').exists())
if __name__=='__main__':unittest.main()
