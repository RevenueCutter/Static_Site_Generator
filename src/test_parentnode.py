import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        child_node3 = LeafNode("span", None)
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("div", [child_node, child_node2])
        parent_node3 = ParentNode("div", [child_node3])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        self.assertEqual(parent_node2.to_html(), "<div><span>child</span><span>child2</span></div>")
        with self.assertRaises(ValueError):
            parent_node3.to_html()

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
        )
