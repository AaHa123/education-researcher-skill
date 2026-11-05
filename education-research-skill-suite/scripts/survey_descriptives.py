#!/usr/bin/env python3
"""研究问卷CSV描述统计及完整案例Cronbach α；不做构念效度或因果检验。"""
import argparse,csv,json,statistics,math
from pathlib import Path

def fmt(x):return '无法计算' if x is None else f'{x:.3f}'
def variance(xs):return statistics.variance(xs) if len(xs)>1 else None
def alpha(rows):
    if len(rows)<3 or len(rows[0])<2:return None
    cols=list(zip(*rows))
    vtotal=variance([sum(r) for r in rows]);vitems=[variance(list(col)) for col in cols]
    if not vtotal or any(x is None for x in vitems):return None
    k=len(cols)
    return k/(k-1)*(1-sum(vitems)/vtotal)
def get_num(raw,low,high,missing):
    if str(raw).strip() in missing:return None,'missing'
    try:v=float(raw)
    except (TypeError,ValueError):return None,'invalid'
    if not math.isfinite(v) or not low<=v<=high:return None,'invalid'
    return v,None

def analyze(data,codebook):
    scales=codebook.get('scales',[])
    missing=set(str(x) for x in codebook.get('missing_values',['','NA']))
    rows=list(data); headers=set(rows[0]) if rows else set()
    output=['# 问卷描述性统计报告','','> 输入若为示例数据，仅供演示脚本；本报告不自动证明量表效度、因果关系或研究假设。','',f'- 记录行数：{len(rows)}','']
    for sc in scales:
        name=sc['name'];items=sc['items'];rev=set(sc.get('reverse_items',[]));low=sc['min'];high=sc['max']
        if len(items)<2:raise ValueError(f'{name}: 至少2题才能形成量表')
        if not rev.issubset(set(items)):raise ValueError(f'{name}: 反向题不在量表题项中')
        absent=[item for item in items if item not in headers]
        if absent:raise ValueError(f'{name}: 数据缺失列 {absent}')
        output += [f'## {name}',f"题项：{', '.join(items)}；量尺范围：{low}—{high}；反向计分题：{', '.join(sorted(rev)) or '无'}",'', '| 题项 | 有效n | 缺失n | 非法n | 均值 | 样本标准差 |','|---|---:|---:|---:|---:|---:|']
        values=[]
        peritem={item:[] for item in items};missing_n={item:0 for item in items};invalid_n={item:0 for item in items}
        for row in rows:
            observed=[]
            for item in items:
                val,err=get_num(row.get(item,''),low,high,missing)
                if err=='missing':missing_n[item]+=1
                if err=='invalid':invalid_n[item]+=1
                if val is not None:
                    if item in rev:val=low+high-val
                    peritem[item].append(val)
                observed.append(val)
            if all(v is not None for v in observed):values.append(observed)
        for item in items:
            xs=peritem[item]
            output.append(f"| {item} | {len(xs)} | {missing_n[item]} | {invalid_n[item]} | {fmt(statistics.mean(xs) if xs else None)} | {fmt(statistics.stdev(xs) if len(xs)>1 else None)} |")
        scores=[statistics.mean(r) for r in values]
        output+=['',f'- 完整案例n：**{len(values)}** / {len(rows)}',f'- 完整案例量表均分：**{fmt(statistics.mean(scores) if scores else None)}**',f'- 完整案例量表均分标准差：**{fmt(statistics.stdev(scores) if len(scores)>1 else None)}**',f'- 完整案例Cronbach α：**{fmt(alpha(values))}**','- α仅为内部一致性信息，不证明因子结构或构念效度；小样本解释尤其谨慎。','']
        if len(values)<30:output.append('- 提示：完整案例少于30人，信度与描述统计估计不稳定。\n')
        if sc.get('source_note'):output.append(f"- 溯源提醒：{sc['source_note']}\n")
    return '\n'.join(output)+'\n'
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--data',type=Path,required=True);p.add_argument('--codebook',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    with a.data.open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
    codebook=json.loads(a.codebook.read_text(encoding='utf-8-sig'))
    report=analyze(rows,codebook)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(report,encoding='utf-8');print('完成:',a.out)
if __name__=='__main__':main()
