#!/usr/bin/env python3
"""人工质量关口证据完整性检查。不会自动评价创新性、效度或伦理合规。"""
import argparse,json,sys
from pathlib import Path
from datetime import date
REQUIRED={
'G1':{'research_object','search_log','literature_review','research_gap','research_questions','theory_link','feasibility'},
'G2':{'rq_data_map','sampling','design_control','instrument_trace','pilot_quality','analysis_plan','ethics','data_security','implementation'},
}
def evaluate(gate,record,strict_files=False,source=None):
    errors=[];warnings=[]
    if record.get('gate') != gate: errors.append('文件中的gate与指定关口不一致')
    reviewer=(record.get('reviewer_name') or '').strip()
    if not reviewer: errors.append('缺少人工审核人reviewer_name')
    try:
        d=date.fromisoformat(record.get('review_date',''))
        if d>date.today(): warnings.append('审核日期晚于当前日期')
    except ValueError: errors.append('review_date缺少或不是YYYY-MM-DD')
    if record.get('summary_decision')!='pass':errors.append('summary_decision必须由人工填写pass')
    items=record.get('items')
    if not isinstance(items,list):return {'passed':False,'errors':errors+['items须为列表'],'warnings':warnings}
    entries={}
    for i,row in enumerate(items):
        if not isinstance(row,dict):errors.append(f'items[{i}]无效');continue
        id_=row.get('id')
        if id_ in entries:errors.append(f'重复项目{id_}')
        entries[id_]=row
    for id_ in REQUIRED[gate]:
        if id_ not in entries:errors.append(f'缺失必查项目{id_}');continue
        row=entries[id_]
        if row.get('status')!='pass':errors.append(f'{id_}尚未通过人工评审')
        if not str(row.get('reviewer_note','')).strip():errors.append(f'{id_}缺少审核意见')
        ref=str(row.get('evidence_ref','')).strip()
        if not ref:errors.append(f'{id_}缺少证据路径／标识')
        elif strict_files and source and not (source.parent/ref).exists():errors.append(f'{id_}证据文件不存在: {ref}')
    for row in items:
        if not isinstance(row,dict):continue
        if row.get('status') not in ('pass','revise','na','pending'):errors.append(f"{row.get('id')}状态值不合法")
    return {'gate':gate,'project_id':record.get('project_id',''),'passed':not errors,'errors':sorted(errors),'warnings':warnings,'checked_items':len(REQUIRED[gate]),'disclaimer':'本工具只验证证据记录的完整性，人工签核真实性和学术判断需另行确认。'}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--gate',choices=['G1','G2'],required=True)
    p.add_argument('--file',type=Path,required=True)
    p.add_argument('--out',type=Path)
    p.add_argument('--strict-files',action='store_true',help='核查每个相对证据路径是否存在')
    a=p.parse_args()
    try:r=json.loads(a.file.read_text(encoding='utf-8-sig'))
    except (OSError,ValueError) as e: print(f'无法读取评审文件: {e}',file=sys.stderr);return 1
    result=evaluate(a.gate,r,a.strict_files,a.file)
    result_str=json.dumps(result,ensure_ascii=False,indent=2)
    print(result_str)
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(result_str+'\n',encoding='utf-8')
    return 0 if result['passed'] else 2
if __name__=='__main__':sys.exit(main())
