# 每日研究简报

网站：https://yangzhen2003.github.io/daily-research-brief/

每天上午10点（UTC+8）由 Agent 启动 Google Scholar、NBER、SSRN、arXiv 主题检索，整理后提交，GitHub Actions 发布到 GitHub Pages。

四个研究主题：文本测量与理论构念（词典、embedding、DDR与效度）、社交媒体平台（微博专项）、主体性与共融性语言（agency/communion）、计算社会科学方法。2026-10-21起替换原平台/算法想象主题；其抽样检索依据见 [检索记录](docs/search-probe-2026-10-21.md)。

四个栏目：其他研究5篇（最新3篇分别来自NBER、SSRN、arXiv，高被引2篇）；传播学与社会科学5篇，优先传播学SSCI Q1/Q2；传播学七刊每天轮换完整一期，Online First 单独算一期；综合六刊每天轮换1篇最新在线社会科学研究。后两个栏目不使用主题关键词。访问受限或合格候选不足时明确说明，不凑数。

新论文附研究用途、相关性与阅读优先级。配置见 site/data/reading-plan.json，轮换进度见 rotation-state.json；历史简报保持原版。

下一次检索设置通过所有者提交 GitHub Issue 保存。收藏保存在浏览器，支持待读、已读、准备引用、不相关、备注、核心文献标记以及导入导出。核心文献须通过网页生成的 GitHub Issue 提交并经工作流保存，之后每日追踪前后引用；私人笔记不会自动上传。每周五的每日任务同时编写周评；每周整理页提供最近7天目录与已发布精读建议。

## 每天怎么跑

检索与写作由 Agent 完成（不是在 Actions 里跑模型）。本机用 `scripts/daily.sh` 调 `dsh --profile headless` 执行 `prompts/daily.md` 的流程：

```bash
./scripts/daily.sh          # 检索、写 JSON、校验、提交
```

定时可用 cron 或 launchd，见 docs/SETUP.md。Actions（`.github/workflows/pages.yml`）只负责校验和部署。

## 发布前校验

```bash
python3 scripts/rebuild_registry.py   # 追加历史
python3 scripts/validate.py
python3 -m unittest discover -s tests
node --test tests/core.test.js
```

main 推送后 Actions 部署 GitHub Pages。具体规则见 UPDATE_GUIDE.md。
