"""Pure date rotation and structured owner requests; no network or credential access."""
import json,re
from datetime import date
TOPICS={'sti','social','agency','methods'}
def rotation(plan,day,kind):
    offset=(date.fromisoformat(day)-date.fromisoformat(plan['rotations']['startDate'])).days
    assert offset>=0, 'Rotation has not started'
    rows=plan['rotations'][kind]
    return rows[offset%len(rows)]
def core_request(body):
    match=re.search(r'<!-- daily-core-papers:v1 -->\s*```json\s*([\s\S]*?)\s*```',body)
    assert match,'Missing core paper marker'
    data=json.loads(match.group(1))
    assert set(data)=={'papers'} and isinstance(data['papers'],list) and 0<len(data['papers'])<=100
    for p in data['papers']:
        assert set(p)=={'title','url','doi','topicIds','note'}
        assert isinstance(p['title'],str) and 0<len(p['title'])<=1000
        assert isinstance(p['url'],str) and p['url'].startswith('https://') and len(p['url'])<=2000
        assert isinstance(p['doi'],str) and len(p['doi'])<=500
        assert isinstance(p['note'],str) and len(p['note'])<=5000
        assert isinstance(p['topicIds'],list) and set(p['topicIds'])<=TOPICS
    return data
def apply_core(body,number,saved_at,owner,actor,author,path):
    assert actor==author==owner,'Only the repository owner may change core papers'
    request=core_request(body);config=json.loads(path.read_text());assert config['owner']==owner
    config['requests']=[r for r in config['requests'] if r['requestNumber']!=int(number)]+[dict(request,requestNumber=int(number),savedAt=saved_at)]
    path.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
