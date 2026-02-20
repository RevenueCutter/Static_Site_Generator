import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, text_to_textnodes

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_preserve_images(self):
        node = TextNode("Plain text", TextType.TEXT)
        image_node = TextNode("Alt text", TextType.IMAGE, "https://example.com/img.png")
        new_nodes = split_nodes_delimiter([node, image_node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Plain text", TextType.TEXT),
                TextNode("Alt text", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )
    def test_unmatched_delimiter(self):
        node = TextNode("This is **unmatched bold", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_text_to_textnodes(self):
        text = "**ROFLMAO** this [site](https://www.dank.net) is `def` _sick_, yo. ![alt](https://www.grug.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
                [
                    TextNode("ROFLMAO", TextType.BOLD),
                    TextNode(" this ", TextType.TEXT),
                    TextNode("site", TextType.LINK, "https://www.dank.net"),
                    TextNode(" is ", TextType.TEXT),
                    TextNode("def", TextType.CODE),
                    TextNode(" ", TextType.TEXT),
                    TextNode("sick", TextType.ITALIC),
                    TextNode(", yo. ", TextType.TEXT),
                    TextNode("alt", TextType.IMAGE, "https://www.grug.dev")
                ],
                new_nodes
                )
        text2 = ""
        new_nodes2 = text_to_textnodes(text2)
        self.assertListEqual([], new_nodes2)
        text3 = "no markdown"
        new_nodes3 = text_to_textnodes(text3)
        self.assertListEqual([TextNode("no markdown", TextType.TEXT)], new_nodes3)
        text4 = "**_italicbold_**"
        new_nodes4 = text_to_textnodes(text4)
        self.assertListEqual([TextNode("_italicbold_", TextType.BOLD)], new_nodes4)
        text5 = "`CODE"
        with self.assertRaises(Exception):
            text_to_textnodes(text5)




if __name__ == "__main__":
    unittest.main()
