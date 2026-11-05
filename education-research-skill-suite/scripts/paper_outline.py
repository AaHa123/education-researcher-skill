#!/usr/bin/env python3
"""根据研究项目元数据生成占位符论文结构，不杜撰研究结果。"""
import argparse,json
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();project=json.loads(a.project.read_text(encoding='utf-8-sig'))
    title=project.get('title','【待定论文标题】');rqs=project.get('primary_rq',[])
    s=[f'# {title}','','> 研究写作骨架：所有【待填】处必须有真实资料。不得将示例或AI生成文本当成研究结果。','','## 摘要','【待填：问题、研究设计、真实样本、主要结果、边界】','','## 关键词','【待填3—6个关键词】','','## 一、引言','- 背景与教育问题【待填证据】','- 国内外研究与缺口【待填核实文献】','- 研究目的与贡献【待填】','','## 二、理论基础与研究问题']
    s += [f'- {rq}' for rq in rqs] if rqs else ['【待填RQ】']
    s+=['- 概念定义及理论模型【待填】','','## 三、研究方法','- 研究范式与设计【待填】','- 对象、抽样及样本流失【待填】','- 工具、量表溯源及评价量规【待填】','- 伦理、实施流程和预分析计划【待填】','','## 四、研究结果','【待填：真实统计或质性结果，报告效应量、置信区间及非显著结果】','','## 五、讨论','- 与关键研究比较【待填】','- 理论贡献与可能解释【待填】','- 方法局限及推断范围【待填】','','## 六、结论与教育启示','【待填：只写证据支持的结论与条件性建议】','','## 参考文献','【待填：逐条核实原始出处和DOI】','','## 伦理、数据与AI使用声明','【按学校及目标期刊规定填写】','']
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text('\n'.join(s),encoding='utf-8');print('完成:',a.out)
if __name__=='__main__':main()
