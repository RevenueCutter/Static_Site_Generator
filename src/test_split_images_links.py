import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_image, split_nodes_link

class TestSplitNodes(unittest.TestCase):

    def test_split_nodes_image(self):
        node = TextNode("text![alt text](url)", TextType.TEXT)
        node2 = TextNode("![alt text1](url1)text!![alt text2](url2)more text?", TextType.TEXT)
        split_node = split_nodes_image([node])
        split_node2 = split_nodes_image([node, node2])
        self.assertListEqual([TextNode("text", TextType.TEXT),
                              TextNode("alt text", TextType.IMAGE, "url"),
                              ]
                             , split_node
                             )
        self.assertListEqual([TextNode("text", TextType.TEXT),
                              TextNode("alt text", TextType.IMAGE, "url"),
                              TextNode("alt text1", TextType.IMAGE, "url1"),
                              TextNode("text!", TextType.TEXT),
                              TextNode("alt text2", TextType.IMAGE, "url2"),
                              TextNode("more text?", TextType.TEXT)
                              ]
                             , split_node2
                             )

    def test_split_nodes_link(self):
        node = TextNode("text[anchor](url)", TextType.TEXT)
        node2 = TextNode("text2", TextType.TEXT)
        node3 = TextNode("_BOLD_", TextType.CODE)
        node4 = TextNode("", TextType.IMAGE, "")
        node5 = TextNode("[anchor2](url2) ![alt](url3)", TextType.TEXT)
        node6 = TextNode("(url5)[anchor6](url6)", TextType.TEXT)
        split_node = split_nodes_link([node, node2, node3, node4])
        split_node2 = split_nodes_link([node5, node6])
        self.assertListEqual([TextNode("text", TextType.TEXT),
                              TextNode("anchor", TextType.LINK, "url"),
                              TextNode("text2", TextType.TEXT),
                              TextNode("_BOLD_", TextType.CODE),
                              TextNode("", TextType.IMAGE, "")
                              ]
                             , split_node
                             )
        self.assertListEqual([TextNode("anchor2", TextType.LINK, "url2"),
                              TextNode(" ![alt](url3)", TextType.TEXT),
                              TextNode("(url5)", TextType.TEXT),
                              TextNode("anchor6", TextType.LINK, "url6")
                              ]
                             , split_node2
                             )

