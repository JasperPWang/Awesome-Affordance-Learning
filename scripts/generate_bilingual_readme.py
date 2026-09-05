#!/usr/bin/env python3
"""Generate README_zh-CN.md from the upstream-compatible README.md."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "README.md"
TARGET = ROOT / "README_zh-CN.md"

REPLACEMENTS = {
    "## From Passive Perception to Active Interaction: A Survey of <br> Affordance Learning for Embodied AI":
        "## From Passive Perception to Active Interaction: A Survey of <br> Affordance Learning for Embodied AI<br><sub>从被动感知到主动交互：面向具身智能的可供性学习综述</sub>",
    "> 🧭 Exploring Embodied AI and Embodied perception? We hope this collection proves useful in your journey. If you'd like to support the project, feel free to ⭐️ the repo and share it with your peers. Contributions are warmly welcome!":
        "> 🧭 Exploring Embodied AI and embodied perception? We hope this collection proves useful in your journey. If you'd like to support the project, feel free to ⭐️ the repo and share it with your peers. Contributions are warmly welcome!  \n> 正在探索具身智能与具身感知？希望这份资料集能为你的研究之旅提供帮助。如果你愿意支持本项目，欢迎为仓库点亮 ⭐️、分享给同行，也欢迎参与贡献！",
    "## 📖 Contents": "## 📖 Contents / 目录",
    "## 🔥 News": "## 🔥 News / 动态",
    "## 🌟 Introduction": "## 🌟 Introduction / 介绍",
    "## 🧭 Taxonomy": "## 🧭 Taxonomy / 分类体系",
    "## 📄 Paper List": "## 📄 Paper List / 论文列表",
    "### 👁️ Affordance Perception": "### 👁️ Affordance Perception / 可供性感知",
    "### 🧠 Affordance Reasoning": "### 🧠 Affordance Reasoning / 可供性推理",
    "### 🤖 Affordance-Guided Action": "### 🤖 Affordance-Guided Action / 可供性引导的动作",
    "### 📊 Affordance Datasets / Benchmarks": "### 📊 Affordance Datasets / Benchmarks / 可供性数据集与基准",
    "### 📚 Related Surveys": "### 📚 Related Surveys / 相关综述",
    "## 🎉 Contributing": "## 🎉 Contributing / 参与贡献",
    "## 🌟 Acknowledgment": "## 🌟 Acknowledgment / 致谢",
    "## 📄 License": "## 📄 License / 许可证",
    "> 📢 This list is **actively maintained**, and community contributions are always appreciated!  ":
        "> 📢 This list is **actively maintained**, and community contributions are always appreciated!  \n> 本列表正在**持续维护**，诚挚欢迎社区贡献！  ",
    "> Feel free to [open a pull request](https://github.com/hq-King/Awesome-Affordance-Learning/pulls) if you find any relevant papers.":
        "> Feel free to [open a pull request](https://github.com/hq-King/Awesome-Affordance-Learning/pulls) if you find any relevant papers.  \n> 如果发现相关论文，欢迎[提交 Pull Request](https://github.com/hq-King/Awesome-Affordance-Learning/pulls)。",
    "- **[2025-05]** 🎉 This repository was launched to curate a comprehensive list of affordance-learning research.":
        "- **[2025-05]** 🎉 This repository was launched to curate a comprehensive list of affordance-learning research.  \n  本仓库正式发布，用于汇总可供性学习研究。",
    "This repository accompanies the survey **From Passive Perception to Active Interaction: A Survey of Affordance Learning for Embodied AI** and maintains a curated collection of papers, datasets, and benchmarks.":
        "This repository accompanies the survey **From Passive Perception to Active Interaction: A Survey of Affordance Learning for Embodied AI** and maintains a curated collection of papers, datasets, and benchmarks.\n\n本仓库与综述论文 **From Passive Perception to Active Interaction: A Survey of Affordance Learning for Embodied AI** 配套，持续整理论文、数据集与评测基准。",
    "As robots and embodied agents move into real-world applications, they must understand not only what objects are, but also where, why, and how they can interact with them. Following the survey, the list is organized around three complementary questions:":
        "As robots and embodied agents move into real-world applications, they must understand not only what objects are, but also where, why, and how they can interact with them. Following the survey, the list is organized around three complementary questions:\n\n当机器人与具身智能体走向真实世界应用时，它们不仅需要识别物体，还需要理解在何处、为何以及如何与物体交互。依据该综述，本列表围绕三个相互补充的问题组织：",
    "- **Affordance Perception:** Where or which region affords an interaction?": "- **Affordance Perception:** Where or which region affords an interaction?<br>**可供性感知：** 哪里或哪个区域支持某种交互？",
    "- **Affordance Reasoning:** Which affordance is relevant under the current task, environment, and constraints?": "- **Affordance Reasoning:** Which affordance is relevant under the current task, environment, and constraints?<br>**可供性推理：** 在当前任务、环境和约束下，哪种可供性有关？",
    "- **Affordance-Guided Action:** How can an affordance be converted into an executable action?": "- **Affordance-Guided Action:** How can an affordance be converted into an executable action?<br>**可供性引导的动作：** 如何将可供性转化为可执行动作？",
    "A paper may be cross-referenced when the survey discusses it in more than one role (for example, both perception and reasoning). A separate section collects datasets and benchmarks. Venue labels use the formally published version whenever one is available; otherwise the first public preprint is marked `arXiv`.":
        "A paper may be cross-referenced when the survey discusses it in more than one role (for example, both perception and reasoning). A separate section collects datasets and benchmarks. Venue labels use the formally published version whenever one is available; otherwise the first public preprint is marked `arXiv`.\n\n如果综述从多种角色讨论同一篇论文（例如同时涉及感知与推理），该论文可能在多个分类中交叉收录。数据集和基准单独列出。如果存在正式发表版本，会议/期刊标签优先使用正式版本；否则以首次公开的预印本标记为 `arXiv`。",
    "The taxonomy follows the survey's functional pipeline rather than only model architecture. It expands each primary category into second- and third-level categories. Cross-listing is intentional when a method contributes to multiple stages or perspectives.":
        "The taxonomy follows the survey's functional pipeline rather than only model architecture. It expands each primary category into second- and third-level categories. Cross-listing is intentional when a method contributes to multiple stages or perspectives.\n\n本分类体系遵循综述中的功能流程，而非仅依据模型架构。每个一级类别进一步展开为二级和三级类别。当一种方法贡献于多个阶段或视角时，会有意进行交叉分类。",
    "The **Venue/Date** column prioritizes the formal venue and publication year. Papers without a confirmed venue are labeled `arXiv`. The **Name** column records the method or system name explicitly introduced by the authors, including names stated only in the abstract or main text rather than in the title; `-` means that no explicit method name has been verified and no acronym is inferred from the title.":
        "The **Venue/Date** column prioritizes the formal venue and publication year. Papers without a confirmed venue are labeled `arXiv`. The **Name** column records the method or system name explicitly introduced by the authors, including names stated only in the abstract or main text rather than in the title; `-` means that no explicit method name has been verified and no acronym is inferred from the title.\n\n**会议/日期**列优先记录正式发表场所与年份；未确认正式发表场所的论文标记为 `arXiv`。**名称**列记录作者明确提出的方法或系统名称，包括仅出现于摘要或正文中而未出现于标题的名称；`-` 表示尚未核验到明确的方法名，也不根据标题自行推导缩写。\n\n> 说明：论文标题保留作者发布的正式英文原题，便于精确检索与引用。各表按年份从新到旧排列；同年记录保持上游顺序。",
    "**Survey groups:** object-centric · scene-level · interaction-driven · language- and reasoning-oriented · action-oriented.":
        "**Survey groups:** object-centric · scene-level · interaction-driven · language- and reasoning-oriented · action-oriented.<br>**综述分组：** 以物体为中心 · 场景级 · 交互驱动 · 语言与推理导向 · 动作导向。",
    "Thanks for the wonderful researchers focusing on affordance learning and embodied AI ":
        "Thanks to all the wonderful researchers focusing on affordance learning and embodied AI.  \n感谢所有致力于可供性学习和具身智能研究的优秀学者。",
    "This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).":
        "This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).  \n本项目采用 [MIT License](https://opensource.org/licenses/MIT)。",
}

CELL = {
    "Venue/Date": "Venue/Date<br>会议/日期", "Name": "Name<br>名称",
    "Title": "Title<br>论文标题", "Paper": "Paper<br>论文",
    "Scope": "Scope<br>范围", "Perception Subcategory": "Perception Subcategory<br>感知子类",
    "Reasoning Subcategory": "Reasoning Subcategory<br>推理子类",
    "Model Type": "Model Type<br>模型类型", "Affordance Form": "Affordance Form<br>可供性形式",
    "Action Subcategory": "Action Subcategory<br>动作子类",
    "Data Modality": "Data Modality<br>数据模态", "Focus": "Focus<br>关注点",
    "Primary Category": "Primary Category<br>一级类别",
    "Secondary Category": "Secondary Category<br>二级类别",
    "Third-Level Categories": "Third-Level Categories<br>三级类别",
    "Main Distinction": "Main Distinction<br>主要区别",
}

TERMS = {
    "Affordance Perception": "Affordance Perception / 可供性感知",
    "Affordance Reasoning": "Affordance Reasoning / 可供性推理",
    "Affordance-Guided Action": "Affordance-Guided Action / 可供性引导的动作",
    "Object": "Object / 物体", "Scene": "Scene / 场景", "Object/Scene": "Object/Scene / 物体/场景",
    "Object-pair": "Object-pair / 物体对", "Visual": "Visual / 视觉", "Spatial": "Spatial / 空间",
    "Interaction-driven": "Interaction-driven / 交互驱动", "Generalizable": "Generalizable / 可泛化",
    "E2E": "E2E / 端到端", "Hierarchical model": "Hierarchical model / 层次模型",
    "explicit": "explicit / 显式", "implicit": "implicit / 隐式", "explicit/implicit": "explicit/implicit / 显式/隐式",
    "Visual affordance perception": "Visual affordance perception / 视觉可供性感知",
    "Spatial affordance perception": "Spatial affordance perception / 空间可供性感知",
    "Interaction-driven affordance perception": "Interaction-driven affordance perception / 交互驱动的可供性感知",
    "Generalizable affordance perception": "Generalizable affordance perception / 可泛化的可供性感知",
    "Relation-based reasoning": "Relation-based reasoning / 基于关系的推理",
    "Language-centric reasoning": "Language-centric reasoning / 以语言为中心的推理",
    "Agentic reasoning": "Agentic reasoning / 智能体式推理",
    "Hierarchical affordance-to-action": "Hierarchical affordance-to-action / 层次化可供性到动作",
    "Affordance-integrated policy learning": "Affordance-integrated policy learning / 可供性集成策略学习",
    "Relation-Based Affordance Reasoning": "Relation-Based Affordance Reasoning / 基于关系的可供性推理",
    "Language-Centric Affordance Reasoning": "Language-Centric Affordance Reasoning / 以语言为中心的可供性推理",
    "Agentic Affordance Reasoning": "Agentic Affordance Reasoning / 智能体式可供性推理",
    "Integrated policy": "Integrated policy / 集成策略", "Optimization signal": "Optimization signal / 优化信号",
    "Implicit representation": "Implicit representation / 隐式表征", "Explicit representation": "Explicit representation / 显式表征",
    "Object-centric grounding; scene-level grounding; weakly supervised perception": "Object-centric grounding; scene-level grounding; weakly supervised perception / 以物体为中心的定位；场景级定位；弱监督感知",
    "3D object grounding; 3D scene grounding": "3D object grounding; 3D scene grounding / 三维物体定位；三维场景定位",
    "Demonstration/HOI video; HOI image; interaction-conditioned 3D; interaction-grounded scene perception": "Demonstration/HOI video; HOI image; interaction-conditioned 3D; interaction-grounded scene perception / 示范或 HOI 视频；HOI 图像；交互条件三维感知；交互定位的场景感知",
    "Example-based transfer; open-set grounding": "Example-based transfer; open-set grounding / 基于示例的迁移；开放集定位",
    "Probabilistic/semantic relations; object-pair and scene context; manipulation graphs": "Probabilistic/semantic relations; object-pair and scene context; manipulation graphs / 概率或语义关系；物体对与场景上下文；操作图",
    "Grounded skill selection; integrated LLM/MLLM prediction; modular semantic-to-spatial grounding; sequential reasoning": "Grounded skill selection; integrated LLM/MLLM prediction; modular semantic-to-spatial grounding; sequential reasoning / 基于环境定位的技能选择；集成式 LLM/MLLM 预测；模块化语义到空间定位；序列推理",
    "Predefined workflows; adaptive workflows": "Predefined workflows; adaptive workflows / 预定义工作流；自适应工作流",
    "Primitive-based execution; retrieval-based transfer; planner-based execution": "Primitive-based execution; retrieval-based transfer; planner-based execution / 基于原语的执行；基于检索的迁移；基于规划器的执行",
    "Affordance as explicit input; implicit representation; optimization signal": "Affordance as explicit input; implicit representation; optimization signal / 将可供性作为显式输入；隐式表征；优化信号",
    "Grounds masks, heatmaps, or keypoints on the 2D image plane.": "Grounds masks, heatmaps, or keypoints on the 2D image plane. / 在二维图像平面上定位掩码、热力图或关键点。",
    "Grounds functional regions or geometric structures directly in metric 3D space.": "Grounds functional regions or geometric structures directly in metric 3D space. / 直接在度量三维空间中定位功能区域或几何结构。",
    "Derives supervision or context from observed human-object interactions.": "Derives supervision or context from observed human-object interactions. / 从观测到的人–物交互中获取监督信号或上下文。",
    "Transfers to novel objects, labels, queries, or interaction contexts.": "Transfers to novel objects, labels, queries, or interaction contexts. / 迁移到新物体、新标签、新查询或新的交互情境。",
    "Infers affordances through explicit relations among objects, actions, agents, and scene context.": "Infers affordances through explicit relations among objects, actions, agents, and scene context. / 通过物体、动作、智能体和场景上下文之间的显式关系推断可供性。",
    "Uses language to interpret intent and select or ground task-relevant affordances.": "Uses language to interpret intent and select or ground task-relevant affordances. / 使用语言理解意图，并选择或定位与任务相关的可供性。",
    "Uses planning, memory, verification, or iterative tool/model calls over multiple steps.": "Uses planning, memory, verification, or iterative tool/model calls over multiple steps. / 在多步过程中使用规划、记忆、验证或迭代式工具与模型调用。",
    "Predicts affordances first and then converts them into actions through a separate execution module.": "Predicts affordances first and then converts them into actions through a separate execution module. / 先预测可供性，再通过独立的执行模块将其转换为动作。",
    "Integrates affordance information directly into policy representation, input, or optimization.": "Integrates affordance information directly into policy representation, input, or optimization. / 将可供性信息直接融入策略表征、输入或优化过程。",
}
TERMS = {key: value.replace(" / ", "<br>", 1) for key, value in TERMS.items()}


def translate_table_cells(line: str) -> str:
    if not line.startswith("|"):
        return line
    cells = line.split("|")
    for i in range(1, len(cells) - 1):
        raw = cells[i].strip()
        if raw in CELL:
            cells[i] = f" {CELL[raw]} "
        elif raw in TERMS:
            cells[i] = f" {TERMS[raw]} "
        else:
            for term in sorted(TERMS, key=len, reverse=True):
                if " · " in raw and term in raw:
                    raw = raw.replace(term, TERMS[term])
            cells[i] = f" {raw} "
    return "|".join(cells)


def year_key(row: str, position: int) -> tuple[int, int, int]:
    first = row.split("|", 2)[1]
    m = re.search(r"((?:19|20)\d{2})(?:[.\-/](\d{1,2}))?\b", first)
    return (int(m.group(1)) if m else -1, int(m.group(2) or 0) if m else 0, -position)


def sort_markdown_tables(lines: list[str]) -> list[str]:
    out, i = [], 0
    while i < len(lines):
        if i + 1 < len(lines) and lines[i].startswith("|") and re.match(r"^\|\s*:?-+", lines[i + 1]):
            header, separator = lines[i], lines[i + 1]
            rows, j = [], i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(lines[j]); j += 1
            if "Venue/Date" in header:
                rows = [r for _, r in sorted(enumerate(rows), key=lambda x: year_key(x[1], x[0]), reverse=True)]
            out.extend([translate_table_cells(header), separator])
            out.extend(translate_table_cells(r) for r in rows)
            i = j
        else:
            out.append(lines[i]); i += 1
    return out


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    toc = {
        "[🔥 News](#-news)": "[🔥 News / 动态](#news)",
        "[🌟 Introduction](#-introduction)": "[🌟 Introduction / 介绍](#introduction)",
        "[🧭 Taxonomy](#-taxonomy)": "[🧭 Taxonomy / 分类体系](#taxonomy)",
        "[📄 Paper List](#-paper-list)": "[📄 Paper List / 论文列表](#paper-list)",
        "[👁️ Affordance Perception](#perception)": "[👁️ Affordance Perception / 可供性感知](#perception)",
        "[🧠 Affordance Reasoning](#reasoning)": "[🧠 Affordance Reasoning / 可供性推理](#reasoning)",
        "[🤖 Affordance-Guided Action](#action)": "[🤖 Affordance-Guided Action / 可供性引导的动作](#action)",
        "[📊 Affordance Datasets / Benchmarks](#affordance-datasets-benchmarks)": "[📊 Affordance Datasets / Benchmarks<br>数据集与基准](#affordance-datasets-benchmarks)",
        "[📚 Related Surveys](#related-surveys)": "[📚 Related Surveys / 相关综述](#related-surveys)",
        "[🎉 Contributing](#-contributing)": "[🎉 Contributing / 参与贡献](#contributing)",
        "[🌟 Acknowledgment](#-acknowledgment)": "[🌟 Acknowledgment / 致谢](#acknowledgment)",
        "[📄 License](#-license)": "[📄 License / 许可证](#license)",
    }
    for old, new in toc.items():
        text = text.replace(old, new)
    # Use line breaks, rather than slashes, as the visual separator between
    # English and Chinese. Semantic slashes inside names remain untouched.
    def heading_break(match: re.Match[str]) -> str:
        line = match.group(0)
        english, chinese = line.rsplit(" / ", 1)
        return f"{english}<br><sub>{chinese}</sub>"

    text = re.sub(r"^#{2,3} [^\n]+ / [^\n]+$", heading_break, text, flags=re.MULTILINE)

    def toc_break(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        if "<br>" in label:
            return match.group(0)
        english, chinese = label.rsplit(" / ", 1)
        return f"[{english}<br>{chinese}]({target})"

    text = re.sub(r"\[([^\]]+ / [^\]]+)\]\((#[^)]+)\)", toc_break, text)
    anchors = {
        "## 🔥 News<br><sub>动态</sub>": "news", "## 🌟 Introduction<br><sub>介绍</sub>": "introduction",
        "## 🧭 Taxonomy<br><sub>分类体系</sub>": "taxonomy", "## 📄 Paper List<br><sub>论文列表</sub>": "paper-list",
        "## 🎉 Contributing<br><sub>参与贡献</sub>": "contributing", "## 🌟 Acknowledgment<br><sub>致谢</sub>": "acknowledgment",
        "## 📄 License<br><sub>许可证</sub>": "license",
    }
    for heading, anchor in anchors.items():
        text = text.replace(heading, f'<a id="{anchor}"></a>\n{heading}')
    text = text.replace(
        "## 📖 Contents / 目录\n",
        "## 📖 Contents / 目录\n\n> This bilingual edition is generated from `README.md`. Do not edit generated paper rows directly.  \n> 本中英对照版由 `README.md` 生成，请勿直接修改生成的论文条目。\n",
    )
    text = text.replace("## 🎉 Contributing / 参与贡献\n", "## 🎉 Contributing / 参与贡献\n\n欢迎补充或更新论文。请选择最合适的分类、保持现有格式，并优先使用 arXiv `/abs/` 摘要链接。\n")
    text = "\n".join(sort_markdown_tables(text.splitlines())) + "\n"
    text = "[English](README.md)<br>**简体中文 · English–Chinese**\n\n" + text
    TARGET.write_text(text, encoding="utf-8")
    print(f"generated {TARGET.name}: {len(text.splitlines())} lines")


if __name__ == "__main__":
    main()
