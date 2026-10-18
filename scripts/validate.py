"""Check daily selection, source coverage, journal indexing and historical identities."""
import json,re
from pathlib import Path
from urllib.parse import urlparse
from paper_identity import identifiers,papers_in,normalize_title
from apply_search_request import parse_request
from reading_plan import rotation,TOPICS
root=Path(__file__).resolve().parents[1]/'site/data'
index=json.loads((root/'index.json').read_text());dates=set();seen={}
ledger_path=root/'recommended.json'
ledger=json.loads(ledger_path.read_text()) if ledger_path.exists() else {'version':1,'records':[]}
assert ledger['version']==1 and isinstance(ledger['records'],list)
required=('title','titleZh','authors','venue','source','category','evidence','takeaway','theory','data','method','results','relevance','limitations','url')
journals={normalize_title(j['name']):j for j in json.loads((root/'journals.json').read_text())['journals']}
for issue in sorted(index,key=lambda x:x['date']):
    date=issue['date'];assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',date) and date not in dates;dates.add(date)
    data=json.loads((root/f'{date}.json').read_text());assert data['date']==date and data['title'] and data['summary']
    assert data['schemaVersion'] in (5,6) and data['historyPolicy']=='exclude-recommended'
    modern=data['schemaVersion']==6
    assert data['journalPolicy']=='ssci-communication-q1-q2-and-social-science'
    assert data['searchPlatforms']==['Google Scholar','NBER','SSRN','arXiv']
    groups=data['groups'];assert [g['id'] for g in groups]==(['crossdisciplinary','journals','communication-issue','general-science'] if modern else ['crossdisciplinary','journals'])
    assert all(g['label'] and g['target']==target and 0<=len(g['papers'])<=target for g,target in zip(groups,[5 if modern else 10,5]))
    assert [g['sortBy'] for g in groups]==(['split','citationCount','issue','publicationDate'] if modern else ['split','citationCount'])
    other=groups[0]['papers'];latest=[p for p in other if p.get('selectionBucket')=='latest'];popular=[p for p in other if p.get('selectionBucket')=='cited']
    assert len(latest)<=(3 if modern else 5) and len(popular)<=(2 if modern else 5) and latest+popular==other, 'Invalid latest/cited split'
    assert [b['id'] for b in groups[0]['selectionBuckets']]==['latest','cited']
    assert data['themeSearches'] and data['searchNote']
    for row in data['themeSearches']+data.get('verificationLog',[]):
        assert all(isinstance(row.get(k),str) and row[k].strip() for k in ('platform','query','timeRange','purpose','status'))
    papers=papers_in(data);assert issue['count']==len(papers), 'Index count mismatch'
    if (modern and (len(other)<5 or len(groups[1]['papers'])<5 or len(groups[3]['papers'])<1)) or (not modern and len(papers)<15):assert data.get('shortfallReason'), 'Explain missing papers'
    for p in papers:
        for field in required:assert isinstance(p.get(field),str) and p[field].strip(), (date,field)
        assert urlparse(p['url']).scheme=='https' and isinstance(p['year'],int)
        assert p['evidence'] in ('全文核验','摘要核验','理论综述')
        if modern:
            assert isinstance(p.get('topicIds'),list) and set(p['topicIds'])<=TOPICS
            assert p.get('readingUse') and p.get('researchConnection') and p.get('priorityReason')
            assert p.get('readingPriority') in ('high','normal','reference')
        assert p['abstractZh'] and urlparse(p['abstractSource']).scheme=='https'
        assert p['abstractMode'] in ('full','unavailable')
        if p['abstractMode']=='full':assert p['originalAbstract'] and p.get('abstractLicense')
        else:assert not p.get('originalAbstract') and p.get('abstractUnavailableReason')
        for identity in identifiers(p):
            assert identity not in seen, 'Repeated paper: '+p['title']
            assert not any(identity in entry['identifiers'] and entry['date']<date for entry in ledger['records']), 'Previously recommended paper: '+p['title']
            seen[identity]=date
    for group in groups[:1]:
        assert all(p.get('sourceDatabase') in ('NBER','SSRN','arXiv') for p in group['papers'])
        coverage={c['database']:c for c in group['sourceCoverage']}
        assert set(coverage)=={'NBER','SSRN','arXiv'}, 'Missing source coverage'
        for db,c in coverage.items():
            included=any(p['sourceDatabase']==db for p in group['papers'])
            assert c['status']==('included' if included else 'unavailable'), 'Incorrect source coverage'
            if not included:assert c.get('reason'), 'Explain missing database'
    recent=latest
    assert all(re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?',p.get('publicationDate','')) and p.get('publicationDateSource') for p in recent)
    assert [p['publicationDate'] for p in recent]==sorted((p['publicationDate'] for p in recent),reverse=True), 'Publication dates out of order'
    if modern:
        plan=json.loads((root/'reading-plan.json').read_text())
        latest_dbs=[p['sourceDatabase'] for p in latest]
        if set(latest_dbs)!={'NBER','SSRN','arXiv'} or len(latest_dbs)!=len(set(latest_dbs)):
            assert groups[0].get('latestSourceExceptions') and data.get('shortfallReason'),'Explain latest source exceptions'
        assert groups[0]['selectionBuckets'][0]['target']==3 and groups[0]['selectionBuckets'][1]['target']==2
        assert groups[1].get('journalPriorityNote'),'Explain communication-first selection'
        comm,general=groups[2:]
        assert general['target']==1 and len(general['papers'])<=1
        assert general['rotationJournalId']==rotation(plan,date,'general')['id'],'Wrong general journal rotation'
        assert comm.get('unit')=='issue'
        collection=comm.get('collection')
        if collection:
            assert collection['journalId']==rotation(plan,date,'communication')['id'],'Wrong communication rotation'
            assert collection['kind'] in ('online-first','issue') and type(collection['complete']) is bool
            assert collection['url'].startswith('https://') and collection['checkedAt'] and collection['title']
            assert isinstance(collection['toc'],list)
            if not collection['complete']:assert data.get('shortfallReason'),'Explain incomplete collection'
            new=[]
            for entry in collection['toc']:
                assert entry['title'] and entry['url'].startswith('https://') and entry['articleType']
                assert entry['status'] in ('new','previously-recommended','non-research')
                if entry['status']=='new':new.append(normalize_title(entry['title']))
                if entry['status']=='previously-recommended':
                    assert entry.get('recommendedDate') and entry.get('reviewUrl')
                    assert any(normalize_title(entry['title'])==normalize_title(r['title']) and r['date']==entry['recommendedDate'] for r in ledger['records']),'Unverified prior recommendation'
            assert sorted(new)==sorted(normalize_title(p['title']) for p in comm['papers']),'Collection directory mismatch'
            assert comm['target']==len(new)
        else:
            assert not comm['papers'] and data.get('shortfallReason'),'Missing collection'
        for p in general['papers']:
            assert re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?',p.get('publicationDate','')) and p.get('publicationDateSource')
            assert p.get('socialScienceReason'),'Explain social science eligibility'
        assert data.get('periodicalChecks'),'Document publisher browsing'
        for row in data['periodicalChecks']:
            assert all(row.get(k) for k in ('platform','query','timeRange','purpose','status'))
    for cited in [popular,groups[1]['papers']]:
        assert all(type(p.get('citationCount')) is int and p['citationCount']>=0 and p.get('citationSource')=='Google Scholar' and p.get('citationCheckedAt') and urlparse(p.get('citationSourceUrl','')).scheme=='https' for p in cited), 'Use actual Google Scholar citations'
        assert [p['citationCount'] for p in cited]==sorted((p['citationCount'] for p in cited),reverse=True), 'Citations out of order'
    for p in groups[1]['papers']:
        assert p['publicationType']=='journal' and p.get('discoverySource')=='Google Scholar'
        assert p.get('journalEdition')=='SSCI' and p.get('indexSource'), 'ESCI or unverified journal indexing'
        assert p.get('discipline') in ('communication','social-science')
        if p['discipline']=='communication':
            j=journals.get(normalize_title(p.get('journalName','')))
            assert j and j['edition']=='SSCI' and j['quartile'] in ('Q1','Q2'), 'Journal outside uploaded Q1/Q2 list'
            assert p['jifQuartile']==j['quartile'] and p['quartileSource']
config=json.loads((root/'search-settings.json').read_text())
assert config['version']==1 and config['owner']=='Yangzhen2003'
for r in config['requests']:
    data={k:r[k] for k in ('effectiveDate','scope','themeKeywords','journalKeywords','excludeTerms','lookbackDays')}
    if 'topicIds' in r:data['topicIds']=r['topicIds']
    parse_request('<!-- daily-search-settings:v1 -->\n```json\n'+json.dumps(data)+'\n```')
    assert type(r['requestNumber']) is int and r['savedAt']
print(f'Validated {len(index)} issue(s), history, source coverage, journal scope and sorting.')
