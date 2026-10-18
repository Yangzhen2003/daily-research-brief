"""Accept a structured owner-issued settings request; never execute text from the issue."""
import json, re, os
from pathlib import Path
from datetime import date

FIELDS={'effectiveDate','scope','themeKeywords','journalKeywords','excludeTerms','lookbackDays'}
def parse_request(body):
    assert '<!-- daily-search-settings:v1 -->' in body, 'Missing settings marker'
    match=re.search(r'<!-- daily-search-settings:v1 -->\s*```json\s*([\s\S]*?)\s*```',body)
    assert match, 'Missing JSON settings'
    data=json.loads(match.group(1))
    assert isinstance(data,dict) and FIELDS<=set(data)<=FIELDS|{'topicIds'}, 'Unsupported settings fields'
    if 'topicIds' in data:
        from reading_plan import TOPICS
        assert isinstance(data['topicIds'],list) and 0<len(data['topicIds'])<=4 and set(data['topicIds'])<=TOPICS,'Invalid topics'
    assert isinstance(data['effectiveDate'],str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}',data['effectiveDate'])
    date.fromisoformat(data['effectiveDate'])
    assert data['scope'] in ('once','ongoing'), 'Unsupported scope'
    for key in ('themeKeywords','journalKeywords'):
        assert isinstance(data[key],str) and 0<len(data[key].strip())<=2000, 'Invalid keywords'
        data[key]=data[key].strip()
    assert isinstance(data['excludeTerms'],str) and len(data['excludeTerms'])<=500
    assert type(data['lookbackDays']) is int and 1<=data['lookbackDays']<=3650
    return data

def apply(body,number,saved_at,owner,actor,author,path):
    assert actor==owner and author==owner, 'Only the repository owner may change settings'
    request=parse_request(body)
    request.update(requestNumber=int(number),savedAt=saved_at)
    config=json.loads(path.read_text())
    assert config['owner']==owner
    config['requests']=[r for r in config['requests'] if r['requestNumber']!=int(number)]+[request]
    config['requests'].sort(key=lambda r:(r['effectiveDate'],r['savedAt'],r['requestNumber']))
    path.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    path=Path(__file__).resolve().parents[1]/'site/data'
    if '<!-- daily-core-papers:v1 -->' in os.environ['REQUEST_BODY']:
        from reading_plan import apply_core
        apply_core(os.environ['REQUEST_BODY'],os.environ['REQUEST_NUMBER'],os.environ['REQUEST_UPDATED_AT'],os.environ['REPOSITORY_OWNER'],os.environ['REQUEST_ACTOR'],os.environ['REQUEST_AUTHOR'],path/'core-papers.json')
    else:
        apply(os.environ['REQUEST_BODY'],os.environ['REQUEST_NUMBER'],os.environ['REQUEST_UPDATED_AT'],os.environ['REPOSITORY_OWNER'],os.environ['REQUEST_ACTOR'],os.environ['REQUEST_AUTHOR'],path/'search-settings.json')
    print('Owner search settings accepted.')
