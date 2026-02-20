import unittest
from htmlnode import HTMLNode, LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        node3 = LeafNode(None, "Hello, world!")
        node4 = LeafNode("p", None)
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Hello, world!</a>')
        self.assertEqual(node3.to_html(), "Hello, world!")
        with self.assertRaises(ValueError):
            node4.to_html()
