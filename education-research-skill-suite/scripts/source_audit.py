#!/usr/bin/env python3
"""本地文献元数据语法核查。不会联网验证文献真实存在。"""
import argparse,csv,re,collections,sys
from pathlib import Path
from urllib.parse import urlparse
DOI=re.compile(r'^10\.\d{4,9}/\S+$',re.I)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    a=p.parse_args()
    with a.input.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    issues=[];seen=collections.defaultdict(list)
    for i,r in enumerate(rows,2):
        rid=r.get('ref_id','')
        if not rid:issues.append(f'L{i}: 缺ref_id')
        doi=(r.get('doi') or '').strip().lower()
        if doi:
            doi=re.sub('^https?://(dx\.)?doi\.org/','',doi)
            if not DOI.match(doi):issues.append(f'L{i}: DOI形式异常')
            seen[doi].append(i)
        url=(r.get('source_url') or '').strip()
        if url and (urlparse(url).scheme not in ('https','http') or not urlparse(url).netloc):issues.append(f'L{i}: source_url不是有效HTTP(S)地址')
        if r.get('year') and (not str(r['year']).isdigit() or not 1800 <= int(r['year']) <= 2100):issues.append(f'L{i}: 年份格式异常')
        if not (r.get('title') or '').strip():issues.append(f'L{i}: 无标题')
        if (r.get('verification_status') or '').strip().lower() in ('primary_verified','verified_primary') and not (doi or url):issues.append(f'L{i}: 已标记原文核实但无DOI/URL')
    for doi,lines in seen.items():
        if len(lines)>1:issues.append(f'重复DOI {doi} 见行{lines}')
    print(f'检测{len(rows)}条；问题{len(issues)}项。注意：仅元数据核查，非在线真实性验证。')
    for issue in issues: print('-',issue)
    return 2 if issues else 0
if __name__=='__main__':sys.exit(main())
