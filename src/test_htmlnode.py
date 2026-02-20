import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("div", "Hello, world!", None, {"class": "greeting", "id": "main"})
        node2 = HTMLNode("div", "Hello, world!", None, {"class": "greeting", "id": "main", "param": "nope"})
        node3 = HTMLNode(None, "Hello, world!", None, {"class": "greeting", "id": "main"})
        node4 = HTMLNode("div", "Herro, worudo!", None, {"class": "greeting", "id": "main"})
        node5 = HTMLNode("div", "Hello, world", None, None)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)
        # What do you expect node.props_to_html() to return?
        # self.assertEqual(...)
