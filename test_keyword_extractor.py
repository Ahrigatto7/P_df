import unittest
from keyword_extractor import extract_keywords

class TestKeywordExtractor(unittest.TestCase):
    def test_korean_keywords(self):
        text = "오늘은 날씨가 좋고 내일은 흐릴 것입니다. 날씨와 기온이 중요합니다."
        keywords = extract_keywords(text, top_n=5)
        self.assertTrue("날씨" in keywords)
        self.assertTrue(isinstance(keywords, list))
        self.assertGreater(len(keywords), 0)

if __name__ == '__main__':
    unittest.main()
