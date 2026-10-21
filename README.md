# 每日研究简报

网站：https://yangzhen2003.github.io/daily-research-brief/

每日由已配置的 Agent 日程启动 Google Scholar、NBER、SSRN、arXiv 主题检索，整理后提交，GitHub Actions 发布到 GitHub Pages。

四个研究主题：文本测量与理论构念（词典、embedding、DDR与效度）、社交媒体平台（微博专项）、主体性与共融性语言（agency/communion）、计算社会科学方法。2026-10-21起替换原平台/算法想象主题；其抽样检索依据见 [检索记录](docs/search-probe-2026-10-21.md)。

四个栏目：其他研究5篇（最新3篇分别来自NBER、SSRN、arXiv，高被引2篇）；传播学与社会科学5篇，优先传播学SSCI Q1/Q2；传播学七刊每天轮换完整一期，Online First 单独算一期；综合六刊每天轮换1篇最新在线社会科学研究。后两个栏目不使用主题关键词。访问受限或合格候选不足时明确说明，不凑数。

新论文附研究用途、相关性与阅读优先级。配置见 site/data/reading-plan.json，轮换进度见 rotation-state.json；2026-10-21按所有者指令清除旧简报及推荐账本，从当日重新开始；Git历史可恢复，之后恢复正常追加。

下一次检索设置通过所有者提交 GitHub Issue 保存。收藏保存在浏览器，支持待读、已读、准备引用、不相关、备注、核心文献标记以及导入导出。核心文献须通过网页生成的 GitHub Issue 提交并经工作流保存，之后每日追踪前后引用；私人笔记不会自动上传。每周五的每日任务同时编写周评；每周整理页提供最近7天目录与已发布精读建议。

main 推送后 Actions 部署 GitHub Pages。具体规则见 UPDATE_GUIDE.md。
