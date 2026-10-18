import json, sys, tempfile, unittest, subprocess, shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'scripts'))
from apply_search_request import apply, parse_request
from reading_plan import TOPICS


def base_issue(date='2026-10-18'):
    return {
        'schemaVersion': 6,
        'historyPolicy': 'exclude-recommended',
        'journalPolicy': 'ssci-communication-q1-q2-and-social-science',
        'searchPlatforms': ['Google Scholar', 'NBER', 'SSRN', 'arXiv'],
        'date': date,
        'title': 'fixture',
        'summary': 'fixture',
        'notice': '',
        'searchNote': 'fixture',
        'themeSearches': [dict(platform='arXiv', query='fixture', channel='API', timeRange='today', purpose='discovery', status='ok')],
        'periodicalChecks': [dict(platform='Journal of Communication', query='https://example.org/toc', channel='publisher', timeRange='today', purpose='issue', status='blocked')],
        'shortfallReason': 'fixture: no eligible candidates',
        'groups': [
            dict(id='crossdisciplinary', label='其他研究', target=5, sortBy='split',
                 sortDescription='fixture',
                 selectionBuckets=[dict(id='latest', label='最新研究', target=3, sortBy='publicationDate', sortDescription='fixture'),
                                   dict(id='cited', label='高被引研究', target=2, sortBy='citationCount', sortDescription='fixture')],
                 sourceCoverage=[dict(database=db, status='unavailable', reason='fixture') for db in ('NBER', 'SSRN', 'arXiv')],
                 latestSourceExceptions='fixture: no eligible candidates',
                 papers=[]),
            dict(id='journals', label='传播学与社会科学', target=5, sortBy='citationCount',
                 journalPriorityNote='fixture', sortDescription='fixture', papers=[]),
            dict(id='communication-issue', label='传播学顶刊推荐', unit='issue', target=0, sortBy='issue', papers=[]),
            dict(id='general-science', label='综合顶刊推荐', target=1, sortBy='publicationDate',
                 rotationJournalId='pnas', papers=[]),
        ],
    }


def make_paper(title='Fixture paper', doi='10.1000/x', db='arXiv', bucket='latest'):
    p = {k: 'fixture' for k in ('titleZh', 'authors', 'venue', 'source', 'category', 'takeaway',
                                'theory', 'data', 'method', 'results', 'relevance', 'limitations',
                                'readingUse', 'researchConnection', 'priorityReason')}
    p.update(title=title, url='https://example.org/' + title.replace(' ', '-') + '/' + doi,
             year=2026, evidence='摘要核验', doi='https://doi.org/' + doi,
             abstractZh='fixture', abstractSource='https://example.org/abstract',
             abstractMode='unavailable', originalAbstract='', abstractUnavailableReason='fixture',
             topicIds=['sti'], readingPriority='normal',
             publicationDate='2026-10-17', publicationDatePrecision='day',
             publicationDateSource='https://example.org/date',
             sourceDatabase=db, selectionBucket=bucket)
    return p


class Pipeline(unittest.TestCase):
    def test_owner_only_and_topic_validation(self):
        payload = dict(effectiveDate='2026-10-18', scope='once', themeKeywords='sti', journalKeywords='sti',
                       excludeTerms='', lookbackDays=30)
        body = '<!-- daily-search-settings:v1 -->\n```json\n' + json.dumps(payload) + '\n```'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'settings.json'
            path.write_text(json.dumps(dict(owner='Yangzhen2003', requests=[])))
            with self.assertRaises(AssertionError):
                apply(body, 1, '2026-10-17T00:00:00Z', 'Yangzhen2003', 'stranger', 'Yangzhen2003', path)
            apply(body, 1, '2026-10-17T00:00:00Z', 'Yangzhen2003', 'Yangzhen2003', 'Yangzhen2003', path)
            self.assertEqual(json.loads(path.read_text())['requests'][0]['themeKeywords'], 'sti')
            payload['scope'] = 'unknown'
            with self.assertRaises(AssertionError):
                parse_request('<!-- daily-search-settings:v1 -->\n```json\n' + json.dumps(payload) + '\n```')

    def test_four_topics_accepted_and_unknown_rejected(self):
        data = dict(effectiveDate='2026-10-18', scope='once', themeKeywords='x', journalKeywords='y',
                    excludeTerms='', lookbackDays=30, topicIds=['sti', 'social', 'agency', 'methods'])
        body = '<!-- daily-search-settings:v1 -->\n```json\n' + json.dumps(data) + '\n```'
        self.assertEqual(parse_request(body)['topicIds'], ['sti', 'social', 'agency', 'methods'])
        data['topicIds'] = ['sti', 'social', 'agency', 'methods', 'leader']
        with self.assertRaises(AssertionError):
            parse_request('<!-- daily-search-settings:v1 -->\n```json\n' + json.dumps(data) + '\n```')
        self.assertEqual(TOPICS, {'sti', 'social', 'agency', 'methods'})

    def _fixture(self, tmp):
        target = Path(tmp)
        shutil.copytree(root / 'scripts', target / 'scripts')
        data = target / 'site' / 'data'
        data.mkdir(parents=True)
        for name in ('reading-plan.json', 'journals.json', 'search-settings.json'):
            shutil.copy(root / 'site' / 'data' / name, data / name)
        return target, data

    def _run(self, target, issue, index_count, ledger=None):
        data = target / 'site' / 'data'
        (data / '2026-10-18.json').write_text(json.dumps(issue, ensure_ascii=False))
        (data / 'index.json').write_text(json.dumps([dict(date='2026-10-18', title=issue['title'], count=index_count)]))
        (data / 'recommended.json').write_text(json.dumps(dict(version=1, records=ledger or [])))
        return subprocess.run([sys.executable, str(target / 'scripts/validate.py')], capture_output=True, text=True)

    def test_empty_issue_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            target, _ = self._fixture(tmp)
            result = self._run(target, base_issue(), 0)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_duplicate_and_history_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target, _ = self._fixture(tmp)
            issue = base_issue()
            issue['groups'][0]['papers'] = [make_paper()]
            issue['groups'][0]['sourceCoverage'] = [
                dict(database='NBER', status='unavailable', reason='fixture'),
                dict(database='SSRN', status='unavailable', reason='fixture'),
                dict(database='arXiv', status='included', reason='fixture'),
            ]
            issue['groups'][0]['latestSourceExceptions'] = 'fixture: only arXiv reachable'
            result = self._run(target, issue, 1)
            self.assertEqual(result.returncode, 0, result.stderr)

            dup = json.loads(json.dumps(issue))
            dup['groups'][1]['papers'] = [make_paper()]
            result = self._run(target, dup, 2)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Repeated paper', result.stderr)

            old = dict(date='2026-10-01', title='old', identifiers=['doi:10.1000/x'])
            result = self._run(target, issue, 1, [old])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Previously recommended', result.stderr)

    def test_rotation_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target, _ = self._fixture(tmp)
            issue = base_issue()
            issue['groups'][3]['rotationJournalId'] = 'science'
            result = self._run(target, issue, 0)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Wrong general journal', result.stderr)


if __name__ == '__main__':
    unittest.main()
