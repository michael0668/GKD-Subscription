# GKD-Subscription

基于 [GKD](https://github.com/gkd-kit/gkd)（基于无障碍的自定义屏幕点击安卓应用）的个人订阅规则仓库。

## 订阅地址

```
https://raw.githubusercontent.com/michael0668/GKD-Subscription/refs/heads/main/sub.json5
```

在 GKD 中：**首页 → 订阅 → 添加订阅**，粘贴上述地址即可。

## 规则说明

本订阅包含三部分规则：

### 1. 自定义应用规则（apps）

根据手机已安装的用户级应用，从 [Lin-arm/GKD_subscription](https://github.com/Lin-arm/GKD_subscription) 提取匹配的应用规则，并加入本人的自定义规则，共 **44 个应用**。主要覆盖：

| 应用 | 规则组数 |
|------|---------|
| 微信 | 46 |
| 哔哩哔哩 | 34 |
| 抖音 | 31 |
| 拼多多 | 26 |
| 支付宝 | 26 |
| QQ | 22 |
| 小红书 | 19 |
| 淘宝 | 16 |
| 京东 | 14 |
| WPS Office / 闲鱼 | 11 |
| …（其余 33 个应用） | 1~9 |

> 其中微信、主题商店额外包含本人的自定义规则（小程序视频广告跳过、关闭弹窗卡片），与提取规则互补、无冲突。

### 2. 全局规则（globalGroups / categories）

整合自 [Lin-arm/GKD_subscription](https://github.com/Lin-arm/GKD_subscription)，用于拦截通用开屏广告、更新提示、青少年模式弹窗等：

| 全局规则 | 说明 |
|----------|------|
| 开屏广告-全局 | 关闭打开应用时的开屏广告 |
| 更新提示-全局 | 关闭应用的更新弹窗 |
| 青少年模式-全局 | 关闭应用的青少年模式弹窗 |

分类（categories）：开屏广告、青少年模式、更新提示、评价提示、通知提示、权限提示、局部广告、全屏广告、分段广告、功能类、其他。

## 更新日志

- **v4** (2026-11-12)：微信规则精简——仅保留 8 个广告跳过规则组，其余 38 个功能类/提示类规则组默认关闭。
- **v3** (2026-11-12)：根据手机已安装应用，从 Lin-arm 订阅提取 44 个应用的规则并整合（微信 46、B站 34、抖音 31、拼多多 26、支付宝 26 等）。
- **v2** (2026-11-12)：整合 Lin-arm 全局规则（categories + 3 条 globalGroups），全局规则全部启用。
- **v1** (2026-11-12)：初始版本。包含主题商店、微信两条自定义规则。

## 致谢

- [gkd-kit/gkd](https://github.com/gkd-kit/gkd) — 强大的自定义屏幕点击工具
- [Lin-arm/GKD_subscription](https://github.com/Lin-arm/GKD_subscription) — 全局规则来源

## 免责声明

本规则仅供学习交流使用，请勿用于商业或非法用途。
