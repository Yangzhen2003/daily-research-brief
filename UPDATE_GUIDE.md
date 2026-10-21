# 每日研究简报更新指南

2026-10-18起执行以下规则，日期按Asia/Shanghai计算，启动时间以现有Agent日程为准，完成后发布。历史简报不改写；新简报schemaVersion:6。

一次性例外：2026-10-21按所有者明确指令清除10月18日至20日简报、重做21日、重置index/recommended/rotation-state；保留用户设置、期刊名单、核心文献配置和Git历史。此次重置后恢复正常追加规则，未授权后续任务继续清空。

## 读取与设置

必须读取main最新UPDATE_GUIDE.md、site/data/reading-plan.json、rotation-state.json、core-papers.json、search-settings.json、journals.json、index.json、recommended.json。保留未来设置、收藏与永久历史。search-settings的once只当天生效，ongoing从生效日起持续；适用项按effectiveDate、savedAt、requestNumber降序选择，否则defaults。

四个研究主题：measurement（文本测量与理论构念：词典开发与验证、embedding文化测量、DDR和文本测量效度；自2026-10-21起替换平台/算法想象）、social（微博等中国社交媒体的表达、谣言、集体行动与审查）、agency（主体性与共融性语言，agency/communion的测量与效应）、methods（因果识别、文本作为数据、计算社会科学）。默认四个主题都启用；有效设置含topicIds时只启用该列表。有效用户请求的themeKeywords、journalKeywords用于全部主题或单主题覆盖；没有有效用户请求时，使用保存的defaults。四个主题同时启用时，其余主题采用reading-plan中的query。表单单主题设置时两个关键词字段覆盖该主题。分别记录实际执行式与topicIds，不把计划检索冒称已执行。每日篇数是栏目合计，不是每个主题各一份；质量和相关性优先，不为主题配额凑数。

measurement主题优先使用reading-plan中的queries逐条执行，supplementalQueries只作补充；两个默认关键词字段中的换行表示独立检索式，不将全部行合并为AND查询。有效用户覆盖仍优先。跨平台按原生语法分别适配并记录真实执行式；网页域名限定检索不能冒称原生检索。2026-10-21抽样未验证Scholar原生访问、引用数或30天新文献供给，不据此放宽现有来源、期刊资格、日期与引用数规则。测量研究关注理论构念、操作化、分析层级、效度证据和中文微博迁移条件。legacyTopics中的sti只供历史简报与已有收藏标签解析，不再默认检索；不得将旧sti论文重标为measurement。

## 四个栏目

groups依次crossdisciplinary、journals、communication-issue、general-science。前两栏使用关键词；后两栏不使用关键词，直接查看出版方最新在线内容。

### 其他研究：5篇

target:5，sortBy:split。selectionBuckets为latest（target:3、sortBy:publicationDate）和cited（target:2、sortBy:citationCount），papers先latest后cited。

最新3篇分别来自NBER、SSRN、arXiv各1篇，按首次公开日期降序。保存publicationDate、publicationDatePrecision、publicationDateSource；不把修订日当首发，不虚构日期。sourceCoverage含每库included/unavailable和原因。某库受阻或没有合格未推荐论文，才由其他两库补足，并用latestSourceExceptions说明原因。最新优先lookbackDays，不足可扩展但须说明。

高被引2篇从三库剩余合格候选选取，以Google Scholar实际网页引用次数降序；保存citationCount、citationSource:Google Scholar、citationSourceUrl、citationCheckedAt。不能用下载、浏览、OpenAlex或平台排名替代，未知不记0。不声称穷尽全库最高引用。

### 传播学与社会科学：5篇

target:5，sortBy:citationCount。Google Scholar先主题检索再筛期刊，优先传播学。先穷尽本轮已核验的相关传播学候选，不足5才补其他SSCI社会科学；journalPriorityNote解释补充与候选范围，最终按实际引用数降序。排除ESCI与未确认当前收录项。传播学匹配上传表77种SSCI Q1/Q2，保存discipline:communication、journalName、journalEdition:SSCI、indexSource、jifQuartile、quartileSource；其他社会科学另核验SSCI。JIF不是中科院分区，未知指标年份不猜测。

### 传播学顶刊推荐：完整一期

unit:issue，sortBy:issue，不使用主题关键词，不因与个人课题无关而漏掉研究论文。按reading-plan的七刊顺序每天轮换一本，从2026-10-18的Journal of Communication开始，以当地日历日差取模，使用scripts/reading_plan.rotation；失败也不偷换当天轮到的期刊。

Online First / Advance Articles单独视为一期：抓取当次可访问在线列表的完整目录和核验日期，优先推荐该刊所有新在线、未推荐研究论文与综述。首次访问应覆盖整个在线集合，不能只拿第一页冒充整期；分页或访问不全时collection.complete:false并明确缺失，不提前推进完成游标。无新在线论文时，从最新尚未完整推荐的正式卷期向前推荐一期。每刊分别保存正式卷期完成进度，在线集合用日期快照，不能固定数量截断。

group.collection含journalId、journalName、kind:online-first或issue、title、url、checkedAt、complete，以及toc数组。toc每条含title、url、articleType、status:new或previously-recommended或non-research，已推荐项附recommendedDate和reviewUrl。目录列所有条目，社论、书评、勘误注明类型但无需研究解读；papers只含未推荐的研究论文和综述，其target等于当次未推荐研究论文数。曾在其他栏目推荐的论文只在目录标记并链接旧解读，不再次放入papers或重复登记。每篇新研究提供标准摘要及中文解读。无卷期连续出版期刊可将出版方最新在线集合视为一期，说明范围。

### 综合顶刊推荐：1篇

target:1，sortBy:publicationDate。不使用关键词，按PNAS、Nature、Science、Science Advances、Scientific Data、Nature Communications六刊每天轮换，2026-10-18从PNAS开始。仅选轮到期刊最新在线发表且未推荐的社会科学原始研究、研究综述或社会科学数据论文，Online First即可，不等正式卷期；不是推荐完整一期。社会科学归属依据研究问题、分析对象与主要结论判断，期刊栏目标签只作线索。归属不明确但可能相关的跨学科研究可以推荐，不因无法确定学科而排除，交由用户判断；保存socialScienceAssessment:uncertain和socialScienceReason说明可能相关之处与不确定原因，category明确显示“综合顶刊 · 学科归属待判断”，limitations同样说明。确认归属则socialScienceAssessment:confirmed并给依据。此不确定性许可不改变论文题录、内容核验和历史去重要求，也不取消主题期刊栏的SSCI/ESCI限制。明确属于纯自然科学或纯技术性能、没有人类行为或社会问题关联的论文仍不纳入。Scientific Data允许相关Data Descriptor。无合格候选时留空并解释，不擅自扩充或替换轮换名单。保存group.rotationJournalId、每篇首次在线日期与来源。

## 内容、检索与去重

前两栏仅Google Scholar、NBER、SSRN、arXiv；不使用WoS或Sider Scholar。后两栏允许直接浏览上述指定期刊出版方目录和文章，不能套用旧四库限制而跳过。themeSearches分别列各主题各平台实际式、渠道、时间、状态；periodicalChecks分别列两类期刊浏览的目录URL、范围、状态；verificationLog单列逐篇身份、摘要、全文、引用核验。域名公开网页检索不得冒称站内高级检索。访问失败如实说明，不绕验证、不索取密码。

按DOI、arXiv ID、规范化题名和已核验identityAliases对recommended.json永久历史及本期所有papers去重，跨栏目、跨平台、修订版与正式版本均不重复。toc中的已推荐目录引用不是新推荐，rebuild_registry只登记papers。历史永久追加，即使旧简报移出index也不删除。

原文完整摘要只有逐字核验且许可允许时abstractMode:full并保存originalAbstract、abstractLicense；否则unavailable、原文为空、附原因与abstractSource。abstractZh原创。理论、数据、方法、结果尽量详细，样本、时期、单位、变量、识别、效应及局限具体；未知注明，读正文关键部分才标全文核验。不为凑数牺牲相关性，任何缺额或整期不完整写shortfallReason。

所有新papers额外保存topicIds数组（无关联可为空）、readingUse（用途）、researchConnection（支持、挑战或补充哪个判断及其边界）、readingPriority:high/normal/reference及priorityReason。用途可为理论框架、假设推导、变量测量、研究设计、结果讨论、背景阅读。期刊通读栏目不强行关联个人课题。

## 核心文献与每周整理

浏览器收藏支持待读、已读、准备引用、不相关，备注和核心文献标记。浏览器本地数据不能直接用于远端检索。用户通过“提交核心文献追踪”生成GitHub Issue后，只有所有者提交且工作流写入core-papers.json才进入每日任务；未提交的私人收藏不视为已同步。

读取core-papers所有请求，按DOI/题名合并核心文献，追踪其参考文献与后续引用，记录coreTracking数组：coreTitle、direction:references/citations、checkedAt、channel、status、findings。每条finding有title、url、relation、evidenceUrl及证据；不能只凭主题相近宣称引用关系。核心文献本身历史不受改动；新发现论文如符合两主题栏资格可进入对应栏目并去重。不合格或已推荐仅以关系链接展示，不重复解读。没有核心文献就明确显示待用户提交，不虚构跟踪成功。

每个当地周五在当天简报写weeklyReview：weekStart、weekEnd、topPapers（最多3条title/url/reason）、designImplications、literatureUses、openQuestions，基于最近7天已发布文献，说明选读理由、设计影响、综述位置及矛盾。网站每日也提供最近7天回顾目录，但不能把自动汇总冒称编辑完成的周评。无需额外创建定时任务。

## 数据验证和发布

schemaVersion:6；historyPolicy:exclude-recommended；journalPolicy:ssci-communication-q1-q2-and-social-science；searchPlatforms依次四库（仅主题渠道）。新增期刊渠道保存periodicalChecks。保留全部题录与摘要字段。轮换完成后同提交更新rotation-state.json，失败与不完整不能推进完成状态。

运行rebuild_registry.py永久追加，validate.py及相关Python/Node测试。基于最新main原子提交简报、index、recommended和rotation-state，非强制更新；并发重新合并，不覆盖用户关键词、核心文献或历史。确认数量、排序、来源和Actions Pages部署成功，再报告实际网站状态。不发邮件、外部消息或写凭证。
