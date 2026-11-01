import json
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock, patch

import bot


class InternationalTests(unittest.TestCase):
    def test_old_and_named_feeds_keep_language_and_balance(self):
        stamp = datetime.now(timezone.utc).timetuple()
        def entry(title, url):
            return {'title': title, 'summary': 'Inflation economy business update',
                    'link': url, 'published_parsed': stamp}
        feeds = [SimpleNamespace(feed={'language': 'id'}, entries=[
            entry('Inflasi Indonesia', 'https://local.example/1'),
            entry('Berita ekonomi kedua', 'https://local.example/2')]),
            SimpleNamespace(feed={'language': 'en-GB'}, entries=[
                entry('Inflation falls in Britain', 'https://foreign.example/1')])]
        config = {'feeds': ['https://local.example/rss',
                  {'url': 'https://foreign.example/rss', 'name': 'Foreign Publisher', 'language': 'en'}],
                  'keywords': ['inflation'], 'max_candidates': 2}
        with patch.object(bot.requests, 'get', return_value=Mock(content=b'rss')), \
             patch.object(bot.feedparser, 'parse', side_effect=feeds):
            items = bot.fetch_sources(config)
        self.assertEqual([s['language'] for s in items], ['id', 'en'])
        self.assertEqual(items[1]['publisher'], 'Foreign Publisher')
        self.assertEqual(items[1]['url'], 'https://foreign.example/1')

    def test_cross_language_meaning_matches_without_shared_words(self):
        sources = [
            {'title': 'British central bank cuts borrowing costs', 'summary': 'Decision on Thursday', 'language': 'en'},
            {'title': 'Bank Inggris meluncurkan uang kertas baru', 'summary': 'Desain uang', 'language': 'en'},
        ]
        with patch.object(bot, 'ai', return_value={'indices': [0]}) as ai:
            result = bot.relevant_sources('Bank Inggris memangkas suku bunga', sources)
        self.assertEqual(result, [sources[0]])
        # Even word overlap must not accept an unrelated English event automatically.
        self.assertEqual(len(ai.call_args.args[1]['sources']), 2)

    def test_invalid_semantic_indices_fail_closed(self):
        for indices in ([True], [-1], [99], '0', None):
            with self.subTest(indices=indices), patch.object(bot, 'ai', return_value={'indices': indices}):
                with self.assertRaises(ValueError):
                    bot.relevant_sources('Pemangkasan suku bunga', [{'title': 'Rate cuts', 'language': 'en'}])

    def test_indonesian_sources_keep_local_filter_without_ai(self):
        sources = [{'title': 'Penurunan suku bunga bank sentral', 'language': 'id'},
                   {'title': 'Peluncuran desain uang kertas', 'language': 'id'}]
        with patch.object(bot, 'ai') as ai:
            self.assertEqual(bot.relevant_sources('Penurunan suku bunga', sources), sources[:1])
        ai.assert_not_called()

    def test_selection_and_recheck_keep_foreign_sources(self):
        sources = [{'title': 'Central bank cuts borrowing costs', 'summary': 'A rate decision',
                    'url': 'https://a.example/story', 'language': 'en'},
                   {'title': 'British interest rate reduced', 'summary': 'The same rate decision',
                    'url': 'https://b.example/story', 'language': 'en'}]
        config = {'min_domains': 2, 'category_slugs': ['ekonomi']}
        with patch.object(bot, 'ai', side_effect=[
            {'topic': 'Bank Inggris memangkas suku bunga', 'indices': [0, 1], 'category_slug': 'ekonomi'},
            {'indices': [0, 1]}]):
            topic, selected = bot.choose(sources, ['Topik lama'], config)
        self.assertTrue(topic)
        self.assertEqual(selected, sources)

    def test_minimum_domains_rechecked_after_relevance_filter(self):
        with patch.object(bot, "relevant_sources", return_value=[{"url": "https://a.example/1"}]), \
             patch.object(bot, "write_article") as write:
            with self.assertRaises(RuntimeError):
                bot.prepare_article("Suku bunga", [], {}, {"min_domains": 2})
        write.assert_not_called()

    def test_config_includes_multiple_foreign_publishers(self):
        config = json.loads((bot.ROOT / 'config.json').read_text())
        foreign = [s for s in config['feeds'] if isinstance(s, dict) and s.get('language') == 'en']
        self.assertGreaterEqual(len(foreign), 4)
        self.assertGreaterEqual(config['min_domains'], 2)


if __name__ == '__main__':
    unittest.main()
