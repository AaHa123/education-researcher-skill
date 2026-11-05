#!/usr/bin/env python3
"""AI教育产品证据记录校验：检查来源、版本、查询时间及厂商宣传依赖。"""
import argparse,csv,sys
from pathlib import Path
from datetime import date
from urllib.parse import urlparse

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True);p.add_argument('--max-age-days',type=int,default=180)
    a=p.parse_args()
    with a.input.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    flags=[]
    for n,r in enumerate(rows,2):
        i=r.get('evidence_id') or f'第{n}行'
        for field in ('product','claim','source_type','source_url','accessed_on','region'):
            if not (r.get(field) or '').strip():flags.append(f'{i}: 缺{field}')
        url=(r.get('source_url') or '').strip()
        if url and (urlparse(url).scheme not in ('http','https') or not urlparse(url).netloc):flags.append(f'{i}: URL形式异常')
        try:
            d=date.fromisoformat((r.get('accessed_on') or '').strip())
            age=(date.today()-d).days
            if age>a.max_age_days:flags.append(f'{i}: 证据已超过{a.max_age_days}天，动态产品主张需重新核实')
            if age<0:flags.append(f'{i}: 查询日期晚于当前日期')
        except ValueError:flags.append(f'{i}: accessed_on非YYYY-MM-DD')
        if (r.get('source_type') or '')=='vendor_marketing' and (r.get('independent_validation') or '').lower()!='yes':flags.append(f'{i}: 仅厂商宣传，不能证明教育效果')
        if not (r.get('product_version') or '').strip():flags.append(f'{i}: 缺产品／模型版本')
    print(f'检查记录数:{len(rows)}; 警示／缺失:{len(flags)}。本工具未联网核实URL或事实。')
    for x in flags:print('-',x)
    return 2 if flags else 0
if __name__=='__main__':sys.exit(main())
