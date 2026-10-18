# 每日简报执行任务

你是这个仓库的每日文献简报 Agent。工作目录就是仓库根目录。

## 目标

产出当天（Asia/Shanghai）的一期简报：`site/data/YYYY-MM-DD.json`，并同步更新 `site/data/index.json`、`recommended.json`、`rotation-state.json`，提交到 `main`，推送后确认 GitHub Pages 部署成功。

## 步骤

1. `git pull --rebase origin main`，确认工作区干净。
2. 读 `UPDATE_GUIDE.md`（规则以此为准）、`site/data/reading-plan.json`、`search-settings.json`、`recommended.json`、`rotation-state.json`、`index.json`、`journals.json`、`core-papers.json`。
3. 计算当天日期（`TZ=Asia/Shanghai date +%F`），用 `scripts/reading_plan.py` 的 `rotation()` 确定当天轮到的传播学刊与综合刊。
4. 按 `search-settings.json` 取当天生效设置（once 仅当天、ongoing 持续、按 effectiveDate/savedAt/requestNumber 降序，否则 defaults）。
5. 执行检索。前两栏只用 Google Scholar、NBER、SSRN、arXiv；后两栏直接访问出版方目录。记录**真实**执行的检索式、渠道、时间范围、状态。
6. 按 DOI / arXiv ID / 规范化题名，对 `recommended.json` 和本期所有栏目去重。
7. 逐篇核验题录、摘要、日期、引用数。分不清“摘要核验”和“全文核验”时，按较低者记录。
8. 生成中文解读：理论、数据、方法、结果、局限；附 `topicIds`、`readingUse`、`researchConnection`、`readingPriority`、`priorityReason`。
9. 写简报 JSON，更新 index（新条目置顶）、`recommended.json`（运行 `scripts/rebuild_registry.py`）、`rotation-state.json`。
10. 运行：

```bash
python3 scripts/rebuild_registry.py
python3 scripts/validate.py
python3 -m unittest discover -s tests
node --test tests/core.test.js
```

11. 校验通过后 `git add -A && git commit -m "Daily briefing YYYY-MM-DD" && git push origin main`。
12. `gh run list --limit 1` 查看 Pages 部署；成功后访问网站确认当天期次可见。

## 硬性约束

- **不编造**：引用次数、发布日期、期刊分区、DOI、作者、样本量，任何一项无法核验就留空并写明原因。
- 引用数只能来自 Google Scholar 网页实际显示；拿不到就 `citationCount` 缺失并计入 shortfall，不记 0，不用 OpenAlex 冒充。
- 摘要无法逐字核验或许可不允许转载时，`abstractMode: "unavailable"`，`originalAbstract` 留空，写 `abstractUnavailableReason` 和来源链接。
- 合格候选不足时宁缺毋滥：栏目留空或减少，写 `shortfallReason`，不用无关论文凑数。
- 访问被 Cloudflare/验证码拦截：如实记录 `status`，不绕验证、不索取密码、不换刊冒充。
- 历史简报不改写；`recommended.json` 只追加。
- 不发送邮件或外部消息，不写凭证。
