"""Stable identifiers shared by validation and the append-only recommendation ledger."""
import re, unicodedata

def normalize_title(value):
    return ''.join(c for c in unicodedata.normalize('NFKC',value).lower() if c.isalnum())

def identifiers(p):
    out=['title:'+normalize_title(p['title'])]
    doi=re.sub(r'^https?://(?:dx\.)?doi\.org/|^doi:\s*','',p.get('doi',''),flags=re.I).strip().lower()
    if doi: out.append('doi:'+doi)
    arxiv=re.search(r'arxiv\.org/(?:abs|html|pdf)/([\d.]+)',p.get('url',''),re.I)
    if arxiv: out.append('arxiv:'+arxiv.group(1))
    out.extend(p.get('identityAliases',[]))
    return sorted(set(out))

def papers_in(data):
    return [p for g in data.get('groups',[]) for p in g['papers']] if 'groups' in data else data['papers']
