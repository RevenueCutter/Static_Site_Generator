import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links

class testExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        matches2 = extract_markdown_images(
            "This is text with an ![]()"
        )
        matches3 = extract_markdown_images(
            "Text1 ![image1](link1)![image2](link2)"
        )
        matches4 = extract_markdown_images(
            "Text [anchor](url)![image](?id=123)"
        )
        matches5 = extract_markdown_images(
            "[only brackets]"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        self.assertListEqual([("", "")], matches2)
        self.assertListEqual([("image1", "link1"), ("image2", "link2")], matches3)
        self.assertListEqual([("image", "?id=123")], matches4)
        self.assertListEqual([], matches5)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links("Text [anchor](url)")
        matches2 = extract_markdown_links("Text ![image](link)")
        matches3 = extract_markdown_links("Text [anchor1](url1)[anchor2](url2)")
        matches4 = extract_markdown_links("Text []()")
        matches5 = extract_markdown_links("Text [anchor1] (url1)[anchor-2](url?2)")
        matches6 = extract_markdown_links("[start](url1) and[end](url2)")
        self.assertListEqual([("anchor", "url")], matches)
        self.assertListEqual([], matches2)
        self.assertListEqual([("anchor1", "url1"), ("anchor2", "url2")], matches3)
        self.assertListEqual([("", "")], matches4)
        self.assertListEqual([("anchor-2", "url?2")], matches5)
        self.assertListEqual([("start", "url1"), ("end", "url2")], matches6)
