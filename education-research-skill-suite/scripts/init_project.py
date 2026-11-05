#!/usr/bin/env python3
"""新建研究项目工作目录及工作模板，不复制合成演示数据。"""
from pathlib import Path
import argparse,shutil,json,re
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--name',required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();out=a.out.resolve()
    if out.exists() and any(out.iterdir()):p.error('输出目录必须为空，避免覆盖已有研究资料')
    out.mkdir(parents=True,exist_ok=True)
    for folder in ['01-topic','02-literature','03-design','04-instruments','05-raw-data','06-clean-data','07-analysis','08-manuscript','09-review','10-archive']:
        (out/folder).mkdir(exist_ok=True)
    shutil.copytree(ROOT/'templates',out/'templates',dirs_exist_ok=True)
    project=json.loads((out/'templates'/'project.json').read_text(encoding='utf-8'))
    project['title']=a.name
    project['project_id']='EDU-NEW-PROJECT'
    project['primary_rq']=[]
    project['research_type']='待确认'
    (out/'project.json').write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'README.md').write_text(f'# {a.name}\n\n项目结构由教育研究Skill工具包创建。所有模板仅为起始稿；G1/G2仍待人工评审。\n',encoding='utf-8')
    print(out)
if __name__=='__main__':main()
