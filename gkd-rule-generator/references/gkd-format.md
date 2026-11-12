# gkd 选择器与规则格式参考

本文件记录 gkd（https://github.com/gkd-kit/gkd）选择器语法与规则 JSON 结构的关键要点，供生成规则时查阅。

## 1. 快照 JSON 结构

gkd 快照是单文件 JSON，关键字段：

```json
{
  "id": 1794462245270,
  "appId": "com.heytap.themestore",
  "activityId": "com.nearme.themespace.activities.ThemeMainActivity",
  "screenWidth": 1216,
  "screenHeight": 2640,
  "appInfo": { "id": "...", "name": "主题商店", "versionName": "17.22.1", "versionCode": 1722010 },
  "nodes": [ ... ]
}
```

每个 node 的 `attr` 字段包含：`id`、`vid`、`name`（节点类名）、`text`、`desc`、`clickable`、`left/top/right/bottom`（bounds）、`childCount`、`index`、`depth` 等。

- `id`：完整资源 id，形如 `com.heytap.themestore:id/close_button`
- `vid`：gkd 自动提取的短 id（去掉包名前缀），形如 `close_button`
- `name`：java 类名，如 `android.widget.ImageView`、`android.widget.TextView`

## 2. 选择器语法要点

选择器类似 CSS，由「属性选择器 + 关系选择器」交叉组成，从右往左匹配。

### 属性选择器

- 用 `[]` 包裹布尔表达式，如 `[vid="close_button"]`、`[text="知道了"]`
- 类名简写：`TextView` 等价于 `[name="TextView" || name$=".TextView"]`
- 常见属性：`id`、`vid`、`text`、`desc`、`name`、`clickable`、`childCount`、`index`、`depth`、`bounds`
- 操作符：`=` `!=` `^=`（开头）`$=`（结尾）`*=`（包含）`~=`（正则）等
- 多个 `[]` 并列表示 AND：`[vid="x"][clickable=true]`
- 逻辑：`||`（或）、`&&`（且）、`!(...)`（取反）

### 关系选择器

- `A > B`：A 是 B 的祖先节点（父）
- `A < B`：A 是 B 的直接子节点
- `A + B`：A 是 B 的前置兄弟
- `A - B`：A 是 B 的后置兄弟
- `A << B`：A 是 B 的子孙节点

### @ 符号

选择器末尾用 `@` 标注真正要点击的目标节点。默认取最后一个属性选择器。

### 示例

- 点击关闭按钮（vid 唯一）：`ImageView[vid="close_button"]`
- 限定父容器，防止误触：`[vid="pop_card_parent"] > [vid="close_button"]`
- 按文字点跳过：`TextView[text="跳过"]`
- 完整 id 写法：`[id="com.xxx:id/close_button"]`

## 3. 规则 JSON 结构

一条可导入 gkd 的规则（订阅或本地规则的 groups 片段）：

```json
{
  "id": "com.heytap.themestore",
  "name": "主题商店",
  "groups": [
    {
      "key": 0,
      "name": "关闭弹窗卡片",
      "activityIds": ["com.nearme.themespace.activities.ThemeMainActivity"],
      "rules": [
        { "matches": "ImageView[vid=\"close_button\"]", "action": "click" }
      ]
    }
  ]
}
```

字段说明：

| 字段 | 说明 |
|------|------|
| `id` | 目标应用包名（appId） |
| `name` | 应用显示名 |
| `groups[].key` | 分组序号（从 0 递增） |
| `groups[].name` | 规则组名，描述用途 |
| `groups[].activityIds` | 限定在哪些 Activity 生效（可省略表示全局） |
| `groups[].rules[].matches` | 选择器字符串 |
| `groups[].rules[].action` | 动作，常见 `click`（点击）、`longClick`、`back` 等 |

## 4. 生成规则的决策要点

1. **优先用 `vid`**：短、稳定。若 vid 不唯一则用完整 `id`。
2. **加父容器约束**：当目标 id 可能在别处复用、或想更精准时，用 `父容器 > 目标` 形式。
3. **限定 activityIds**：快照里有 `activityId`，加上它可避免在其他页面误触发。
4. **多候选按钮**：若页面有多个关闭/跳过按钮，分别建多条 rule，或在一个 group 里写多个 rule。
5. **用审查工具验证**：打开 https://i.gkd.li ，上传快照，在搜索框输入选择器确认命中高亮。

## 5. 常见动作

- `click`：点击目标节点
- `longClick`：长按
- `back`：返回键
- `doubleClick`：双击
