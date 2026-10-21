# 文本测量主题：小规模检索与替换依据

日期：2026-10-21（Asia/Shanghai）。目的：用简要检索挑选可用搜索词，替换默认“平台/算法想象”主题，其余主题、来源、选文资格及轮换规则保留。

## 方法与限制

实际使用网页搜索工具检索下列12个式子，查看返回题名与摘录，并对部分关键论文尝试打开原始页面。这里只判断候选发现能力与噪声；没有相关文献全集，不能计算严格召回率。返回顺序也不等于Google Scholar原生排名。比较不设时间限制；不能据此声称最近30天的新文献供给充足。

为便于复核，下文数量均按工具返回顺序的前6条网页记录人工去重；同一论文的DOI页、全文、摘要、预印本与镜像尽量合并。不将软件库或会议总目录计为独立论文。这里只评估相关性，没有完成逐篇全文、SSCI资格、Scholar引用数与永久推荐历史核验，故不代表已经满足每日简报入选条件。

## 保留的四条主检索式

| 独立执行的检索式 | 前6条记录的抽样表现 | 决定 |
|---|---|---|
| `"dictionary" "text" "development" "validation" psychology` | 5项不同研究：怀旧、STEM领域词典、alcohol talk、个人价值观、罗马尼亚LIWC；怀旧出现两个版本。STEM属于领域词典方法参考，其余更接近构念或行为表达测量。 | 保留，作为词典发现入口 |
| `"word embeddings" measurement sociology` | 3项不同研究：Meaning in Hyperspace、Theoretical Foundations and Limits of Word Embeddings、Mobilizing Conceptual Spaces；其余为重复版本。 | 保留，关注测量对象与理论含义 |
| `"distributed dictionary representation" measurement` | 1篇DDR基础论文、1项传播学应用研究的补充材料、1个dictvectoR软件项目；基础论文出现多个版本。 | 保留，方法专名精确，但不能把多版本当作丰富的新论文供给 |
| `("text measurement" OR "text-based measures" OR "text as data") "construct validity"` | 3项不同研究：Textual Analysis in Accounting、The Search for Solid Ground in Text as Data、ValiTex；后两项含预印本或重复页面。 | 保留，提供效度与操作化筛选依据 |

代表性原始来源：

- [Identifying nostalgia in text](https://doi.org/10.1002/jcpy.1359)：原始论文被检索命中，尝试打开出版方页面失败；未声称全文核验。
- [Personal Values Dictionary](https://doi.org/10.1002/per.2294)：已有构念种子，可沿应用和验证研究继续追踪。
- [Meaning in Hyperspace](https://www.annualreviews.org/content/journals/10.1146/annurev-soc-090324-024027)：embedding文化测量的对象与概念问题。
- [DDR](https://link.springer.com/article/10.3758/s13428-017-0875-9)：词典与embedding相结合的方法。
- [The Search for Solid Ground in Text as Data](https://doi.org/10.1080/19312458.2023.2285765)：检索命中，当前直接打开返回403；未声称全文核验。

## 补充式与未采用式

| 实际检索式 | 观察与处理 |
|---|---|
| `"word embeddings" "cultural dimensions"` | 前6条主要集中于The Geometry of Culture的多个版本及一份学位论文；适合基础文献与文化维度补充，放入supplementalQueries，不依靠它提供每日新研究。 |
| `"semantic projection" "word embeddings"` | 前6条主要集中于一项投影基础研究的多个版本，另有数学方法研究；保留为投影方法补充，需筛掉与社会科学构念无关的结果。 |
| `("dictionary-based" OR "lexicon-based") "text analysis" (measurement OR validation OR construct)` | 有4篇不同学术研究，但前6条混入2个方法百科聚合页；词典开发发现优先使用上面的短式，不作为默认独立式。 |
| `("word embeddings" OR "sentence embeddings") ("cultural dimensions" OR "semantic projection" OR "construct measurement")` | 前6条中3条是同一篇文化学习研究的不同页面，另外3条为ACL会议总目录；不采用这一长式。 |
| `"sentence embeddings" "construct" "measurement"` | 同时命中构念发现工具、embedding效度研究，也明显转向问卷题项语义和临床量表预验证；不列为默认独立式，需要此类方法时再定向检索。 |

补充基础来源：[The Geometry of Culture](https://doi.org/10.1177/0003122419877135)、[Semantic projection](https://www.nature.com/articles/s41562-022-01316-8)。

## 简报来源的可发现性探查

以下为普通网页搜索的域名限定查询，不是四库原生搜索，也没有读取Scholar引用次数。

| 实际检索式 | 观察 |
|---|---|
| `site:arxiv.org ("distributed dictionary" OR "text measurement") (moral OR construct OR rhetoric)` | 命中vec-tionary、MoralStrength、Twitter道德叙事等相关研究，同时有Distributed Dictionary Learning等技术噪声。vec-tionary原始摘要页已成功打开。 |
| `site:ssrn.com ("dictionary" OR "embeddings") ("measurement" OR "values")` | 命中文化契合、语义框架与用户参与、政党传播测量等候选，也有医学影像噪声；文化契合详情页直接访问403。 |
| `site:nber.org ("text analysis" OR "word embeddings") measurement` | 有文化文本分析、技能语义与经济概念测量候选，但大量命中PDF正文与参考文献；需按实际测量对象筛选，不能保证每天都有合格新论文。 |

可复核例子：[Constructing Vec-tionaries to Extract Message Features from Texts](https://arxiv.org/abs/2312.05990)、[Beyond Word Counts: Measuring Cultural Fit with Generative AI](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6981283)、[Large Language Models: An Applied Econometric Framework](https://www.nber.org/papers/w33344)。

## 落地范围

新的活动主题为measurement，标签“文本测量与理论构念”。四条主式分别执行；两条窄式保留作补充。两个默认关键词字段同步替换。social、agency、methods的标签与原查询保留。

旧sti只保留为历史标签标识，避免旧简报或已有收藏被错误显示为新主题。2026-10-21已发布简报及此前历史不改写。云端任务已要求每次读取最新仓库规则，因此本次只更新仓库设置，不重新创建日程，也不触发一期新简报。
