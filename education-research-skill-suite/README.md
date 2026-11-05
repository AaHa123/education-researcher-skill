# 教育学与教育技术学研究 Skill 工具包

版本：1.0.0 · 中文 · 2026-11-05

## 组成

- `FULL_WORKFLOW.md`：单独可阅读的全流程说明。
- `skills/00-orchestrator/SKILL.md`：总控（阶段路由与G1/G2质量关口）。
- `skills/01-*`—`skills/11-*`：11 个专业子 Skill，均严格采用“角色定义／核心能力／工作流程／规则约束／输出格式／示例展示”六节模板。
- `scripts/`：仅使用Python标准库的工具；自动化资料校验、整理、描述分析和作品评分，不负责作出学术或伦理裁决。
- `templates/`：可编辑的CSV/JSON/Markdown工作模板。
- `examples/`：演示项目数据；全部为**虚构示例，严禁当作真实实证数据**。
- `references/`：学术报告规范与教育AI权威链接清单。
- `tests/`：基本自动化测试。

## 建议安装／使用方式

1. 将 `skills/00-orchestrator/SKILL.md` 加载为主Skill，按需加载其他目录中的 `SKILL.md`。不假定所有Agent平台自动识别本套目录；如平台要求单Skill文件夹，请分别导入对应子目录。
2. 阅读 `FULL_WORKFLOW.md` 与 `skills/00-orchestrator/SKILL.md`，从选题或当前研究阶段开始。
3. 启动项目：

```bash
python scripts/init_project.py --name "网络热梗PPT研究" --out ./my_research
```

4. 在 `my_research/` 中逐步完善工作文件。**G1、G2均须研究者签署并提供证据路径**。
5. 示例命令：

```bash
python scripts/quality_gate.py --gate G1 --file templates/gate_g1.json
python scripts/quality_gate.py --gate G2 --file templates/gate_g2.json
python scripts/literature_matrix.py --input templates/literature_matrix.csv --out ./literature_report.md
python scripts/source_audit.py --input templates/literature_matrix.csv
python scripts/survey_descriptives.py --data examples/demo_survey.csv --codebook templates/survey_codebook.json --out ./survey_demo.md
python scripts/ppt_rubric.py --data examples/demo_ppt_scores.csv --rubric templates/ppt_rubric.json --out ./ppt_demo.md
python scripts/industry_evidence_audit.py --input templates/industry_evidence.csv
python scripts/paper_outline.py --project templates/project.json --out ./paper_outline.md
python -m unittest discover -s tests -v
```

上面质量关口的默认模板处于**未完成**状态，检查命令应报告未通过，这是刻意的安全机制。

## 研究关口规则

- **G1（文献综述后）**：选题、研究空白、理论框架和问题成立性。通过后方可视为立项论证完成。
- **G2（正式采集前）**：研究设计、测量工具、数据分析预案、伦理和实施可行性。通过后方可视为正式采集准备完成。
- 脚本只做**证据文件是否已列、字段是否完整、人工审核是否已签**的检查；不能判断文献或研究方案是否真的优质。

## 教育技术学专项能力

AI行业支持Skill涵盖：基础模型与多模态技术、生成式AI、检索增强生成、学习分析、智能导师／智能体、教育产品评价、实证证据、隐私与版权、无障碍、成本及版本更新。任何具体产品的功能、价格、隐私政策与效果主张必须以**当期可核实来源**为准，不能从通用Skill内容直接推断。

## 学术与数据边界

- 不提供伪造的数据、文献或显著性结果。
- 不通过脚本自动认定“创新性”或批准伦理。
- 不把调查中的使用意愿推断为实际采用行为，也不把感知参与直接认定为学习效果。
- 问卷基础分析是描述性辅助工具：只提供样本量、缺失、均值、标准差和完整案例的Cronbach α，不替代测量效度分析。
- 作品评分工具输出评分者差异提醒，不假称已计算ICC或κ。

## 定制

直接编辑各个 `SKILL.md`、模板和 `manifest.json`。可增加自有学科数据库检索、统计或文献管理接口，但必须注明其授权与数据来源，并保留人工复核点。
