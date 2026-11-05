#!/usr/bin/env python3
"""汇总本地文献矩阵的数量／研究类型／年份及缺失信息，不创造文献结论。"""
import argparse,csv,collections
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    with a.input.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    rows=[r for r in rows if r.get('ref_id','').strip()]
    bytype=collections.Counter(r.get('study_type','').strip() or '未分类' for r in rows)
    byyear=collections.Counter(r.get('year','').strip() or '未标注' for r in rows)
    missing=collections.Counter(k for r in rows for k in ['title','authors','year','doi','source_url','method','findings','limitations','verification_status'] if not r.get(k,'').strip())
    out=['# 文献矩阵自动汇总','','> 仅汇总输入CSV；本脚本不会检索、核实全文或判定研究质量。','',f'- 收录记录数：**{len(rows)}**','','## 研究类型']
    out += [f'- {k}: {v}' for k,v in bytype.most_common()]
    out+=['','## 年份分布']+[f'- {k}: {v}' for k,v in sorted(byyear.items())]
    out+=['','## 缺失元数据']+[f'- {k}: {v}' for k,v in missing.most_common()]
    out+=['','## 待人工核对清单']
    if not rows:out.append('- 暂无文献记录')
    for r in rows:
        flags=[]
        if not r.get('source_url','').strip() and not r.get('doi','').strip():flags.append('无URL/DOI')
        if r.get('verification_status','').strip().lower() not in ('primary_verified','verified_primary'):flags.append('未标记原文核实')
        if flags:out.append(f"- {r.get('ref_id')}: {r.get('title','')[:40]} — {'、'.join(flags)}")
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text('\n'.join(out)+'\n',encoding='utf-8')
    print(f'汇总{len(rows)}条记录 -> {a.out}')
if __name__=='__main__':main()
