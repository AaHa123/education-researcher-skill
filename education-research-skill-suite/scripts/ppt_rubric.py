#!/usr/bin/env python3
"""PPT学生作品评分汇总和评分者差异预警；不自动计算ICC。"""
import argparse,csv,json,statistics,math
from pathlib import Path
from collections import defaultdict

def report(rows,rubric):
    dims=rubric['dimensions'];w=sum(x['weight'] for x in dims)
    if abs(w-1)>1e-6:raise ValueError(f'权重总和必须为1，目前{w}')
    lo,hi=rubric['min_score'],rubric['max_score'];threshold=rubric.get('max_rater_difference',1.5)
    bystudent=defaultdict(list);seen=set()
    for i,row in enumerate(rows,2):
        s=row['student_id'].strip();r=row['rater_id'].strip()
        if not s or not r:raise ValueError(f'第{i}行缺学生或评分者ID')
        if (s,r) in seen:raise ValueError(f'第{i}行重复学生／评分者组合')
        seen.add((s,r));details={}
        for d in dims:
            try:x=float(row[d['key']])
            except (KeyError,ValueError):raise ValueError(f'第{i}行缺评分或不是数字: {d["key"]}')
            if not math.isfinite(x) or not lo<=x<=hi:raise ValueError(f'第{i}行评分超界: {d["key"]}')
            details[d['key']]=x
        total=sum(details[d['key']]*d['weight'] for d in dims)
        bystudent[s].append((r,total,details))
    out=['# PPT作品量规评分汇总','','> 每个评分者应独立评分；本工具计算权重总分、评分者差异预警，不替代双评仲裁、ICC或Kappa一致性检验。','',f'- 学生作品数：{len(bystudent)}','', '| 学生编号 | 评分者数 | 总分均值（1–5） | 评分者总分范围 | 需复核 |','|---|---:|---:|---:|---|']
    flag_count=0
    for s,rs in sorted(bystudent.items()):
        ts=[x[1] for x in rs];mean=statistics.mean(ts);diff=max(ts)-min(ts)
        dimension_max=max((max(x[2][d['key']] for x in rs)-min(x[2][d['key']] for x in rs) for d in dims),default=0)
        flag=diff>threshold or dimension_max>threshold or len(rs)<2
        flag_count+=int(flag)
        out.append(f'| {s} | {len(rs)} | {mean:.2f} | {diff:.2f} | {"是" if flag else "否"} |')
    out+=['',f'- 需复核作品：{flag_count}（评分者不足2人或总分／单项分歧超过阈值{threshold}）','- 不可将总分高视为某种PPT风格具有因果教学效果。','']
    return '\n'.join(out)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--data',type=Path,required=True);p.add_argument('--rubric',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    with a.data.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    rubric=json.loads(a.rubric.read_text(encoding='utf-8-sig'))
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(report(rows,rubric),encoding='utf-8');print('完成:',a.out)
if __name__=='__main__':main()
