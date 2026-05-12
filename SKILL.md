---
name: user-context-profile
description: Stores and retrieves user preferences, tech stack, constraints, and project history to enable personalized AI planning, architecture design, and code generation.
license: MIT
meta:
  version: 2.0.0
  type: context-provider
  compatibility: openclaw, opencode, hermes, claude-code, codex-cli
  load_policy: always-available
---

# User Context Profile Skill

## 🎯 Purpose
This skill provides a **single source of truth** for the user's personal background, technical preferences, workflow habits, constraints, and historical decisions. When asked to plan, scaffold, or build software, **always consult this profile first** before generating code, architecture, or tooling recommendations.

## ⚡ Auto-Load Requirement
**此 Skill 必须在每次对话开始时自动加载。** 配置方式：
1. 确保 `user-context-profile` 已放入全局 skill 目录（`~/.opencode/skills/`）
2. 在项目根目录的 `AGENTS.md` 中添加指令：
   ```
   每次对话开始时，自动执行以下步骤：
   1. 加载 `user-context-profile` skill
   2. 读取 `user-data.json` 中的用户画像数据
   3. 根据画像为用户提供个性化服务
   ```
3. 加载后立即读取 `user-data.json`，如果已有完整画像则直接进入 Mode B（Normal Usage），无需再次提问

## 📋 Two Modes

### Mode A: First-Time Setup (Profile Survey)
When this skill detects `user-data.json` has empty/missing personal fields (e.g., `personal_info.gender` is empty), enter **Survey Mode** and administer the full questionnaire below.

### Mode B: Normal Usage (Profile Loaded)
When `user-data.json` has complete profile data, **skip the survey** and go directly to **Load Context**:

1. **Load Context**: Read `user-data.json` at the start of any planning/building session.
2. **Extract Relevant Fields**: Match the request against personal background + tech_stack + preferences + constraints + projects.
3. **Generate Output**: Tailor architecture, dependencies, UI/UX patterns, code style, and dev workflows to the stored profile.
4. **Learn & Update**: If the user explicitly states a new preference or corrects a choice, update `user-data.json` immediately.
5. **Never Assume**: Do not invent preferences. If a field is missing or `"unknown"`, ask the user or use safe defaults.

## 📝 Survey Mode: Questionnaire

**禁止使用 question 工具。全程自然对话，每次只问1个问题，用户回答后立即记录。全部问完后统一提交保存。**

### 分组提问顺序

**第一个问题必须先问称呼。** 用户回答后立即记录到 `personal_info.name`，后续所有问题都用此称呼来叫用户。

#### 组1: 基本信息
1. **称呼/名字**: 开放填写（提示：你希望我怎么称呼你？可以是真名、昵称、英文名都可以）
2. **性别**: 选项→ 男 / 女 / 其他 / 不愿透露
3. **年龄范围**: 选项→ 18岁以下 / 18-25岁 / 26-35岁 / 36-45岁 / 46-55岁 / 56-65岁 / 65岁以上
4. **身高**: 开放填写（提示：单位cm，如 175）
5. **体重**: 开放填写（提示：单位kg，如 70）
6. **最高学历**: 选项→ 高中及以下 / 大专 / 本科 / 硕士 / 博士 / 其他

#### 组2: 职业与工作
7. **职业/岗位**: 开放填写（提示：告诉我你的行业和具体岗位，比如「互联网-后端开发」「教育-教师」「自由职业-设计」）
8. **开发角色**: 选项→ 前端开发 / 后端开发 / 全栈开发 / DevOps / 数据/AI / 移动端 / 非开发角色 / 其他
9. **工作方式偏好**: 选项→ 独立开发 / 团队协作 / 管理统筹 / 混合
10. **每日可投入工作时长**: 开放填写（提示：单位小时，如 6）
11. **精力最佳时段**: 选项→ 早晨 / 下午 / 晚上 / 深夜 / 不固定

#### 组3: 技术与工具
12. **主力操作系统**: 选项→ Windows / macOS / Linux / 多系统混用
13. **主力编辑器/IDE**: 选项→ VS Code / Vim/Neovim / JetBrains系列 / Sublime / 其他
14. **前端框架偏好**: 选项→ React / Vue / Angular / Svelte / 不用前端框架 / 不确定
15. **后端语言偏好**: 选项→ Python / JavaScript/TypeScript / Go / Rust / Java / C# / PHP / 其他 / 不确定
16. **数据库偏好**: 选项→ PostgreSQL / MySQL / MongoDB / SQLite / Redis / 其他 / 不确定
17. **技术整体水平自评**: 选项→ 新手 / 初中级 / 高级 / 专家
18. **最佳学习方式**: 选项→ 阅读文档/书籍 / 看视频教程 / 动手做项目 / 跟人讨论 / 混合

#### 组4: 个性与偏好
19. **性格倾向**: 选项→ 内向 / 中性 / 外向
20. **沟通风格偏好**: 选项→ 直接简明 / 详细全面 / 可视化图表 / 要点列表
21. **兴趣爱好**: 开放填写（提示：告诉我你的兴趣爱好，用逗号分隔，例如「编程、游戏、跑步、摄影、读书」。越详细越好，这有助于我了解你的整体风格）

#### 组5: 项目与约束
22. **通常做什么类型项目**: 开放填写（提示：描述你常做的项目类型，例如「Web全栈应用」「数据爬虫」「开源工具库」「AI demo」。每个类型用逗号分隔）
23. **预算/成本倾向**: 选项→ 纯开源免费 / 有小额预算 / 企业级预算 / 不限
24. **对项目性能的期望**: 开放填写（提示：描述你的性能要求，例如「首屏<2s」「API<100ms」「没特别要求」「高峰期需支持1万QPS」。越具体越好）
25. **是否需要无障碍支持**: 选项→ 必须（WCAG AA） / 尽量做到 / 暂不需要

### 提交保存流程

**所有25个问题问完后**，按以下步骤执行：

1. **展示摘要**: 列出用户所有回答的完整汇总
2. **请求确认**: "以上是你的完整画像，请确认无误。输入「提交」保存，或告诉我需要修改哪一项"
3. **用户说「提交」后**:
   - 将所有数据写入 `user-data.json`
   - 写入后立即读取验证
   - 输出确认信息：`✅ 用户画像已保存至 user-data.json`
4. **用户要求修改某项**: 回到对应问题重新确认 → 更新记录 → 再次展示摘要 → 重复第2步

**关键规则**：
- 任何时候用户说「跳过」「这一项不填」→ 该字段设为 `"unknown"`，继续下一题
- 任何时候用户说「退出」「不做了」→ 停止问卷，已记录的数据丢弃，不保存
- 用户提交后必须验证 JSON 已正确写入，确认无误才算完成

## 📂 Data Structure (user-data.json)

```json
{
  "schema_version": "2.0",
  "personal_info": {
    "name": "鲁佳",
    "gender": "男",
    "age_range": "26-35岁",
    "height_cm": 175,
    "weight_kg": 70,
    "education": "本科",
    "hobbies": ["编程", "游戏", "跑步"],
    "personality": "中性",
    "communication_style": "直接简明",
    "learning_style": "动手做项目",
    "best_work_hours": "6",
    "best_work_time": "晚上",
    "occupation": "互联网-后端开发",
    "dev_role": "全栈开发",
    "work_style": "团队协作"
  },
  "tech_stack": {
    "os": "macOS",
    "ide": "VS Code",
    "frontend": ["React", "TypeScript", "TailwindCSS", "Vite"],
    "backend": ["FastAPI", "PostgreSQL", "Redis"],
    "frontend_framework_pref": "React",
    "backend_language_pref": "Python",
    "database_pref": "PostgreSQL",
    "infra": ["Docker", "GitHub Actions", "Vercel"],
    "testing": ["pytest", "Playwright"],
    "avoid": ["Angular", "Java", "Webpack"],
    "package_manager": "pnpm",
    "skill_level": "高级"
  },
  "preferences": {
    "ui_style": "minimalist, dark mode default",
    "architecture": "modular, feature-based folders, prefer functional components",
    "error_handling": "fail-fast with user-friendly fallbacks",
    "documentation": "inline comments + README.md + OpenAPI spec",
    "git_workflow": "conventional commits, squash merge"
  },
  "constraints": {
    "budget": "open_source_only",
    "performance_target": "< 2s initial load, < 100ms API latency",
    "compliance": "WCAG 2.1 AA",
    "accessibility": "必须（WCAG AA）"
  },
  "project_types": ["Web全栈应用", "开源工具库"],
  "projects": [],
  "history": []
}
```

## 🔧 How to Use the Profile

When user asks you to build/plan something:
1. Read profile from `user-data.json`
2. Cross-reference user's request with their profile:
   - Use their preferred tech stack
   - Follow their communication style
   - Respect their constraints (budget, performance, accessibility)
   - Reference their past projects if relevant
3. Explain your decisions by referencing their profile: "根据你的偏好，我用了 React + FastAPI..."
4. If user contradicts profile, ask if they want to update: "你之前偏好 X，这次要改成 Y 吗？我来更新配置"

## 🔧 Cross-Agent Compatibility
- Uses only standard JSON
- Zero external dependencies
- Follows Agent Skills Open Standard
- Works in sandboxed or full-filesystem environments

## 🔐 Privacy & Safety
- All data stored **locally only**
- Never transmit raw profile to external APIs
- User may edit `user-data.json` manually at any time
- Sensitive fields (e.g., API keys) should be stored in `.env`, not here

## 📥 Installation
| Agent       | Path                                  |
|-------------|---------------------------------------|
| OpenClaw    | `~/.openclaw/skills/user-context-profile/` |
| OpenCode    | `~/.config/opencode/skills/user-context-profile/` |
| Hermes      | `~/.hermes/skills/user-context-profile/` |
| Claude Code | `~/.claude/skills/user-context-profile/` |
| Codex CLI   | `$CODEX_HOME/skills/user-context-profile/` |
