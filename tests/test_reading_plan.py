import json, sys, tempfile, unittest
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'scripts'))
from reading_plan import rotation, core_request, apply_core
from apply_search_request import parse_request


class ReadingPlan(unittest.TestCase):
    def test_rotation_is_independent_and_repeats(self):
        plan = json.loads((root / 'site/data/reading-plan.json').read_text())
        self.assertEqual(rotation(plan, '2026-10-18', 'communication')['id'], 'joc')
        self.assertEqual(rotation(plan, '2026-10-24', 'communication')['id'], 'sms')
        self.assertEqual(rotation(plan, '2026-10-25', 'communication')['id'], 'joc')
        self.assertEqual(rotation(plan, '2026-10-24', 'general')['id'], 'pnas')
        self.assertEqual(rotation(plan, '2026-10-23', 'general')['id'], 'nature-communications')
        with self.assertRaises(AssertionError):
            rotation(plan, '2026-10-17', 'general')

    def test_core_request_owner_and_idempotence(self):
        payload = {'papers': [dict(title='Example', url='https://doi.org/10.1/example',
                                   doi='10.1/example', topicIds=['sti'], note='')]}
        body = '<!-- daily-core-papers:v1 -->\n```json\n' + json.dumps(payload) + '\n```'
        self.assertEqual(core_request(body), payload)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'core.json'
            path.write_text(json.dumps(dict(version=1, owner='owner', requests=[])))
            with self.assertRaises(AssertionError):
                apply_core(body, 4, 'now', 'owner', 'other', 'owner', path)
            for _ in range(2):
                apply_core(body, 4, 'now', 'owner', 'owner', 'owner', path)
            self.assertEqual(len(json.loads(path.read_text())['requests']), 1)
        payload['papers'][0]['url'] = 'javascript:alert(1)'
        with self.assertRaises(AssertionError):
            core_request('<!-- daily-core-papers:v1 -->\n```json\n' + json.dumps(payload) + '\n```')
        payload['papers'][0]['topicIds'] = ['unknown']
        with self.assertRaises(AssertionError):
            core_request('<!-- daily-core-papers:v1 -->\n```json\n' + json.dumps(payload) + '\n```')

    def test_topic_request_preserves_legacy(self):
        data = dict(effectiveDate='2026-10-18', scope='once', themeKeywords='x',
                    journalKeywords='y', excludeTerms='', lookbackDays=30)
        def parse():
            return parse_request('<!-- daily-search-settings:v1 -->\n```json\n' + json.dumps(data) + '\n```')
        self.assertNotIn('topicIds', parse())
        data['topicIds'] = ['agency']
        self.assertEqual(parse()['topicIds'], ['agency'])
        data['topicIds'] = ['leader']
        with self.assertRaises(AssertionError):
            parse()


if __name__ == '__main__':
    unittest.main()
