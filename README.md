# 教育学研究 Skill 套件：使用说明与兼容性检查

本仓库包含完整的原始技能套件和使用说明。套件目录为 [`education-research-skill-suite/`](education-research-skill-suite/)，其中保留原有文件与研究流程。本次上传未修改技能正文、脚本或模板。

## 快速开始

1. 下载本仓库 ZIP 并解压，或使用 Git 克隆：

   ```powershell
   git clone https://github.com/AaHa123/education-researcher-skill.git
   cd education-researcher-skill/education-research-skill-suite
   ```

2. 在支持读取本地文件的 AI 代理中，指定该目录，并使用以下提示：

   > 请读取当前套件目录中的 `skills/00-orchestrator/SKILL.md`，根据我的研究目标和已有材料识别阶段，再按需读取对应专业模块。脚本和模板路径均以套件根目录为基准。先说明本轮任务和交付物，再推进工作。

3. 如需新建研究项目，准备 Python 3 后，在套件根目录运行：

   ```powershell
   python scripts/init_project.py --name "我的教育研究" --out ./my_research
   python -B -m unittest discover -s tests -v
   ```

当前版本可按文件路径手动加载。Codex 自动发现所需的元数据和共享资源路径仍待适配，详见本文第 6 节。

### 文档入口

- [原套件使用说明与命令](education-research-skill-suite/README.md)
- [完整研究工作流程](education-research-skill-suite/FULL_WORKFLOW.md)
- [总控技能入口](education-research-skill-suite/skills/00-orchestrator/SKILL.md)
- [模块与关口清单](education-research-skill-suite/manifest.json)
- [工作模板](education-research-skill-suite/templates/)
- [虚构演示数据及说明](education-research-skill-suite/examples/)

以下为原始套件的兼容性检查报告；其中目录结构与运行命令均以 `education-research-skill-suite/` 为基准。

检查日期：2026-11-06

被检查版本：`manifest.json` 标注的 1.0.0

适用对象：希望使用本套件辅助教育学、教育技术学研究的研究者，以及负责将其接入 Codex 的维护者。

## 1. 检查结论

本套件可以作为研究工作流指导材料手动加载，自带 Python 脚本在本次本地测试中可运行。要作为 Codex 自动发现和调用的技能使用，仍需补齐技能元数据，并整理共享资源路径。

本说明记录的是原始套件的检查结果与使用建议，不代表已经完成适配、安装或真实研究任务的端到端验收。

| 检查项 | 本次结果 | 含义 |
| --- | --- | --- |
| 自带自动化测试 | 8 项全部通过 | 覆盖部分脚本的示例运行和基础行为 |
| 技能入口格式 | 13 个入口全部未通过本地格式校验 | 根目录和 12 个子技能的 `SKILL.md` 均缺少 YAML 元数据头 |
| 资源组织 | 脚本、模板及参考材料集中在套件根目录 | 分别安装子技能时，需要处理共享资源依赖 |
| 自动发现与调用 | 尚未实测 | 不能仅凭脚本测试通过认定技能已成功接入 |

## 2. 套件能做什么

套件采用一个总控模块和 11 个专业模块，覆盖从选题到论文归档的研究流程。

| 模块 | 用途 |
| --- | --- |
| `00-orchestrator` | 识别研究阶段、路由任务、维护 G1/G2 关口状态 |
| `01-topic-selection` | 形成选题与可行性方案 |
| `02-introduction` | 组织引言的问题与证据 |
| `03-literature-review` | 规划综述检索、文献矩阵和研究缺口论证 |
| `04-theory-and-questions` | 界定概念、理论框架及研究问题 |
| `05-research-design` | 设计抽样、研究实施与分析预案 |
| `06-measurement-and-ethics` | 准备测量工具、预测试与伦理材料 |
| `07-data-collection` | 组织数据采集、清理与治理 |
| `08-data-analysis` | 将研究问题映射到统计或质性分析 |
| `09-ai-industry-support` | 核查 AI 技术、教育产品及行业证据 |
| `10-paper-writing` | 基于真实研究材料组织论文 |
| `11-review-and-archive` | 模拟评审、返修及研究归档 |

这些模块提供流程与判断指引。文献检索、复杂统计、图表制作及文档导出是否能够执行，仍取决于所用代理平台的工具和运行环境。

## 3. 目录说明

```text
education_research_skill_suite/
├── SKILL.md              # 根目录总控说明
├── README.md             # 原套件介绍与命令
├── FULL_WORKFLOW.md      # 全流程说明
├── manifest.json         # 版本、入口和模块清单
├── skills/               # 总控及 11 个专业模块
├── scripts/              # Python 工具与 Bash 验证入口
├── templates/            # CSV、JSON、Markdown 工作模板
├── examples/             # 虚构演示数据
├── references/           # 参考框架与来源入口
└── tests/                # 自带自动化测试
```

建议手动使用时保留整个目录，避免只复制一个子技能后遗漏脚本或模板。

## 4. 当前版本的使用方式

### 4.1 手动加载工作流

向支持读取本地文件的代理提供套件目录，并明确要求读取入口和与任务相关的子模块。例如：

> 请读取此套件的 `skills/00-orchestrator/SKILL.md`，根据我已有的材料判断研究阶段，再读取需要的专业模块。项目已经完成问卷采集，请先核对研究问题、工具来源与数据条件。

手动指定文件可用于当前任务，但不等于平台已注册该技能，也不保证后续聊天会自动发现它。

### 4.2 新建研究项目

以下命令均在套件根目录运行。需要本机具备可用的 Python 3 环境；本次测试使用现有 Python 环境，未验证最低支持版本。套件业务脚本只使用 Python 标准库。

```powershell
python scripts/init_project.py --name "教育技术研究示例" --out ./my_research
```

初始化脚本创建研究目录并复制模板，不复制虚构示例数据。输出目录应不存在或为空。

### 4.3 运行基本检查

```powershell
python -B -m unittest discover -s tests -v
python scripts/rq_coverage.py --questions templates/research_questions.csv --mapping templates/rq_evidence_map.csv
```

Windows PowerShell 可直接运行这些 Python 命令。`scripts/run_validation.sh` 是 Bash 脚本，需要 Bash 环境。

### 4.4 运行演示分析

```powershell
python scripts/literature_matrix.py --input templates/literature_matrix.csv --out ./output/literature_report.md
python scripts/survey_descriptives.py --data examples/demo_survey.csv --codebook templates/survey_codebook.json --out ./output/survey_demo.md
python scripts/ppt_rubric.py --data examples/demo_ppt_scores.csv --rubric templates/ppt_rubric.json --out ./output/ppt_demo.md
python scripts/paper_outline.py --project templates/project.json --out ./output/paper_outline.md
```

`examples/` 中的数据全部为虚构演示数据，生成的报告只能用于了解脚本输出。真实研究需使用自己的数据、代码本和评分规则。

## 5. G1/G2 质量关口

- **G1**：综述与理论问题论证后的选题、研究空白、研究问题和可行性检查。
- **G2**：正式数据收集前的抽样、研究设计、测量工具、分析预案及伦理准备检查。

```powershell
python scripts/quality_gate.py --gate G1 --file templates/gate_g1.json
python scripts/quality_gate.py --gate G2 --file templates/gate_g2.json
```

预置模板处于待完成状态，以上命令预期返回未通过，退出码为 `2`。

脚本检查记录字段、审核人字段、意见和证据标识是否齐全。默认不会核验证据文件是否存在；需要此项检查时添加 `--strict-files`。该选项以关口 JSON 所在目录为基准解析相对证据路径，因此应按实际项目结构填写路径。

脚本无法认证签核人身份或判断研究是否具有创新性，也不能替代学术评审和正式伦理审批。

## 6. 接入 Codex 前需要完成的适配

### 6.1 补齐每个入口的 YAML 元数据

本次发现根目录和 12 个子技能的 `SKILL.md` 都以 Markdown 标题直接开头，缺少 `name` 与 `description`。本地技能校验器对这 13 个入口均返回 `No YAML frontmatter found`。

可参考以下格式，为各模块分别编写准确的名称和触发描述：

```yaml
---
name: education-research-orchestrator
description: 协调教育学与教育技术学研究的阶段判断、任务路由和 G1/G2 质量关口；适用于规划或继续推进教育研究项目。
---
```

名称与描述承担技能发现和任务匹配功能。参见 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills)。上述内容仅为适配示例，原始文件尚未修改。

### 6.2 明确共享资源的路径基准

例如，总控子技能位于 `skills/00-orchestrator/`，正文提及的 `scripts/quality_gate.py` 实际位于套件根目录。测量模块引用的 `templates/survey_codebook.json` 也有同样问题。

维护者应选择一种明确的打包方式：

- 将整套工具组织为一个主技能，在技能根目录保留脚本、模板和参考材料，由主入口按需读取专业模块。
- 将各模块作为独立技能安装，并为每个模块提供可访问的资源及明确的共享资源定位规则。

第一种方式通常更便于本套件当前的共享资源组织。无论选择哪种方式，都应在移动或安装后复核路径，避免把原工作目录作为隐含前提。

### 6.3 进行实际调用验收

完成格式与路径适配后，还应验证：

1. 平台能发现入口，并显示正确名称与描述。
2. 明确点名技能时，代理能读取入口和相关模块。
3. 自然描述教育研究任务时，能选择合适模块。
4. 只要求修改一个段落时，不强制重新执行完整项目流程。
5. 在研究项目目录中运行时，仍能正确定位套件脚本和模板。

## 7. 本次测试范围与能力边界

本次自带测试共 8 项，全部通过，覆盖默认关口阻断、填入审核字段后的结构检查、研究问题映射、问卷报告、作品评分报告、文献报告、论文大纲和项目初始化。

测试通过说明这些预设场景可运行，不代表所有输入、统计正确性、外部来源或完整研究流程均已验证。

问卷脚本提供样本量、缺失及非法值计数、均值、标准差和完整案例的 Cronbach α。复杂模型、因子分析、因果推断及正式推断统计需另行实现与验证。作品评分脚本提供汇总及评分差异提醒，不能将其输出当作 ICC 或 κ 的计算结果。

文献与行业证据脚本主要检查本地记录。使用时仍需打开原始来源，核实文献、产品版本、价格、隐私政策和具体主张。

## 8. 建议的采用顺序

先保留完整套件并手动加载，以真实任务验证流程是否适合自己的研究；随后补齐元数据、统一路径与入口组织，再做自动发现和实际调用验收。已有论文或数据的项目，应从当前材料出发补齐证据与步骤。
