#!/usr/bin/env python3
"""检查研究问题与证据映射，核心项目缺失时阻止把预案视为完成。"""
import argparse,csv,sys
from pathlib import Path

def load(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--questions',type=Path,required=True);p.add_argument('--mapping',type=Path,required=True)
    a=p.parse_args(); qs=load(a.questions); ms=load(a.mapping)
    errors=[];rqids={r.get('rq_id','').strip() for r in qs if r.get('rq_id','').strip()}
    if not rqids:errors.append('没有RQ')
    for rq in rqids:
        matches=[m for m in ms if m.get('rq_id','').strip()==rq]
        if not matches:errors.append(f'{rq}: 未映射任何证据')
        for m in matches:
            for k in ('variable_or_theme','data_source','measurement_or_coding','analysis_method','limitation'):
                if not m.get(k,'').strip():errors.append(f'{rq}: 缺{k}')
    for m in ms:
        if m.get('rq_id','').strip() not in rqids:errors.append(f"无对应RQ的映射: {m.get('rq_id')}")
    print(f'RQ数:{len(rqids)}; 映射数:{len(ms)}; 问题数:{len(errors)}')
    for x in errors:print('-',x)
    return 2 if errors else 0
if __name__=='__main__':sys.exit(main())
