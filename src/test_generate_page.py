import unittest
from main import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        markdown = " # 'eading "
        self.assertEqual(extract_title(markdown), "'eading")
