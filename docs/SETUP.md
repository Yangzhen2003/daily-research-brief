> 本文件说明这套站点的搭建与运维方式。

# 搭建与运维

## 分工

| 组件 | 职责 |
| --- | --- |
| Agent（本机，`scripts/daily.sh`） | 检索、核验、写简报 JSON、跑校验、提交 |
| GitHub Actions `pages.yml` | 校验 + 测试 + 部署 GitHub Pages |
| GitHub Actions `search-settings.yml` | 把所有者提交的 Issue 写成 `search-settings.json` / `core-papers.json` |
| 浏览器 | 收藏、阅读状态、笔记（localStorage，不上传） |

Actions 不调用大模型，也不抓取网页。每天的内容必须由 Agent 产生；这是原项目最容易误解的一点。

## 目录

```
site/                 静态站点（部署根目录）
  data/*.json         每天一期简报 + 配置 + 永久推荐账本
scripts/              validate / rebuild_registry / reading_plan / 每日执行
tests/                Python 与 Node 测试（Actions 会跑）
prompts/daily.md      Agent 的每日任务说明
UPDATE_GUIDE.md       规则细节（选题、去重、核验、栏目）
```

## 本地跑一次

```bash
git clone https://github.com/Yangzhen2003/daily-research-brief.git
cd daily-research-brief
python3 scripts/validate.py
python3 -m unittest discover -s tests
node --test tests/core.test.js
./scripts/daily.sh
```

`daily.sh` 会先确认工作区干净，再 `git pull --rebase`，然后：

```bash
dsh --profile headless "$(cat prompts/daily.md)"
```

日志写到 `.logs/daily-YYYY-MM-DD.log`。

## 每天 10:00 自动跑

macOS（launchd）：

```bash
./scripts/install-schedule.sh          # 安装
launchctl print gui/$(id -u)/com.local.daily-research-brief | head
./scripts/install-schedule.sh remove   # 卸载
```

Linux（crontab）：

```cron
0 10 * * * cd /path/to/daily-research-brief && TZ=Asia/Shanghai ./scripts/daily.sh >> .logs/cron.log 2>&1
```

注意：cron/launchd 里的 PATH 很短，`dsh` 需要绝对路径或在该脚本里 `export PATH`。若 Agent 需要交互式授权，headless profile 要在 `~/.dsh` 里预先放行。

## 首次部署（已执行）

```bash
gh repo create Yangzhen2003/daily-research-brief --public --source=. --remote=origin --push
gh api -X POST repos/Yangzhen2003/daily-research-brief/pages -f build_type=workflow
```

仓库必须是 public 才能免费用 Pages。部署来源选 “GitHub Actions”，由 `pages.yml` 推送产物。

## 改主题或期刊

- 主题与检索式：`site/data/reading-plan.json` 的 `topics`，以及 `activeTopicIds`。
- 轮换期刊：`reading-plan.json` 的 `rotations.communication` / `rotations.general`。
- 主题白名单：`scripts/reading_plan.py` 的 `TOPICS`、`site/app.js` 的 `sanitizeFavorite`、`site/index.html` 的下拉框。三处要同步改。
- 期刊 Q1/Q2 名单：`site/data/journals.json`（当前 77 种传播学 SSCI）。
- 起始日期：`rotations.startDate`。改日期会改变当天轮到哪本刊。

## 已知限制

- Google Scholar 可能弹验证码；拿不到真实被引数时，简报留空并写 `shortfallReason`，不记 0。
- SSRN、OUP、SAGE、PNAS 对本机 curl 返回 403；Agent 用浏览器/网页工具访问时仍可能被 Cloudflare 拦，失败要如实记录。
- 浏览器收藏只在本机；换设备用导出/导入。
- 核心文献追踪要先在网页勾选并提交 GitHub Issue，工作流保存后才会进入每日任务。
