---
name: gkd-rule-generator
description: 根据 gkd（https://github.com/gkd-kit/gkd）的手机屏幕快照生成自动点击弹窗关闭按钮的规则。当用户提供一个快照压缩包（.zip 文件）或解压后的快照文件夹/JSON，并要求生成 gkd 规则、点击规则、关闭弹窗按钮规则、跳过广告规则时使用。快照文件通常包含一个 .json（节点树）和一个 .webp（截图）。适用场景：gkd 规则、GKD 订阅规则、自动点击、无障碍点击规则、跳过弹窗。
agent_created: true
---

# GKD 规则生成器

根据 gkd 的手机屏幕快照，自动分析节点树并生成「点击关闭按钮」的规则。

## 概述

gkd 是一款基于无障碍的自定义屏幕点击安卓应用。用户会用 gkd 录制屏幕快照，快照是一个压缩包（.zip），内含一个节点树 JSON（描述当前屏幕所有控件）和一张 .webp 截图。本 skill 负责：解析快照 → 定位目标按钮 → 生成可直接导入 gkd 的规则。

## 何时使用

- 用户提供一个 `.zip` 快照文件，要求生成规则
- 用户提供解压后的快照文件夹或快照 `.json`，要求生成规则
- 用户提到「生成 gkd 规则」「自动点击关闭弹窗」「跳过广告规则」等

## 工作流程

### 第 1 步：解析快照

先运行解析脚本，自动解压并分析快照：

```bash
python "<skill目录>/scripts/parse_snapshot.py" <快照.zip|文件夹|json>
```

脚本会输出：
- `appId`、`activityId`、应用名与版本
- 完整节点树（含 `vid`、`id`、`name`、`text`、`desc`、`clickable`、bounds）
- `[CLOSE CANDIDATES]` 段落：自动高亮疑似「关闭/跳过/取消」按钮的节点

如需查看每个节点的完整属性（含 bounds、text/desc 细节），加 `--full` 参数：

```bash
python "<skill目录>/scripts/parse_snapshot.py" <快照> --full
```

> 脚本路径可用 `Glob` 或直接定位到 skill 目录下的 `scripts/parse_snapshot.py`。

### 第 2 步：确定目标按钮

从脚本输出中识别要点击的按钮节点，判断依据（按优先级）：

1. 命中 `[CLOSE CANDIDATES]` 且 `clickable=true` 的节点（最可能是目标）
2. `vid` 或 `id` 含 `close` / `skip` / `cancel` / `x` 等关键词
3. `text` 或 `desc` 为「关闭」「跳过」「知道了」「取消」等
4. 若都未命中，根据节点树结构人工判断（如弹窗卡片容器下的关闭图标 ImageView）

### 第 3 步：编写选择器

选择器语法详见 `references/gkd-format.md`。核心原则：

- **优先用 `vid`**（短、稳定）：`ImageView[vid="close_button"]`
- **vid 可能不唯一时用完整 id**：`[id="com.xxx:id/close_button"]`
- **想更精准、防误触时加父容器约束**：`[vid="pop_card_parent"] > [vid="close_button"]`
- **按文字定位**：`TextView[text="跳过"]`
- 选择器末尾的 `@` 标注真正要点击的目标节点（默认取最后一个属性选择器，通常可省略）

### 第 4 步：生成规则 JSON

按以下结构生成规则（字段说明见 `references/gkd-format.md`）：

```json
{
  "id": "<appId>",
  "name": "<应用名>",
  "groups": [
    {
      "key": 0,
      "name": "<规则组名，如：关闭弹窗卡片>",
      "activityIds": ["<activityId>"],
      "rules": [
        { "matches": "<选择器>", "action": "click" }
      ]
    }
  ]
}
```

要点：
- `id`、`activityIds`、`name` 一律取自快照 JSON 的真实值，不要臆造
- `activityIds` 用快照里的 `activityId` 限定，避免在其他页面误触发
- 若页面有多个关闭/跳过按钮，在同一 group 内写多条 rule，或拆多个 group
- 默认动作 `action` 为 `click`

### 第 5 步：输出与验证提示

向用户展示：

1. **选择器**（可直接粘贴到审查工具搜索框测试）
2. **完整 JSON 规则**（可导入 gkd 本地规则或订阅）

并提示用户可用 https://i.gkd.li 审查工具上传快照、在搜索框输入选择器确认命中高亮。

## 输出格式建议

最终回复应包含：
- 命中的目标节点信息（vid / id / 类名）
- 选择器字符串
- 完整 JSON 规则
- 简要说明为什么这样写（用 vid 还是完整 id、是否加父容器约束、是否限定 activityIds）

## 资源

- `scripts/parse_snapshot.py`：快照解析脚本，解压 zip 并分析节点树
- `references/gkd-format.md`：选择器语法、规则 JSON 结构、生成决策要点的详细参考
