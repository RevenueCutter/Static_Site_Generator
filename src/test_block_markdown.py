import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        
        md = """
**BOLD**

_italic_
`code`


- list
- [anchor](url1)
- ![alt](url2)
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
                blocks,
                [
                    "**BOLD**",
                    "_italic_\n`code`",
                    "- list\n- [anchor](url1)\n- ![alt](url2)"
                ]
                )
        md2 = ""
        blocks2 = markdown_to_blocks(md2)
        self.assertEqual(blocks2, [])

    def test_block_typing_heading(self):
        block = "# H"
        block2 = "###### H"
        block3 = "####### H"
        block4 = "###H"
        block5 = "### "
        blocktype = block_to_block_type(block)
        blocktype2 = block_to_block_type(block2)
        blocktype3 = block_to_block_type(block3)
        blocktype4 = block_to_block_type(block4)
        blocktype5 = block_to_block_type(block5)
        self.assertEqual(blocktype, BlockType.HEADING)
        self.assertEqual(blocktype2, BlockType.HEADING)
        self.assertEqual(blocktype3, BlockType.PARAGRAPH)
        self.assertEqual(blocktype4, BlockType.PARAGRAPH)
        self.assertEqual(blocktype5, BlockType.HEADING)

    def test_block_typing_code(self):
        block = "```\ncode\n```"
        block2 = "```\n```"
        block3 = "``\ncode\n```"
        block4 = "```\ncode"
        blocktype = block_to_block_type(block)
        blocktype2 = block_to_block_type(block2)
        blocktype3 = block_to_block_type(block3)
        blocktype4 = block_to_block_type(block4)
        self.assertEqual(blocktype, BlockType.CODE)
        self.assertEqual(blocktype2, BlockType.CODE)
        self.assertEqual(blocktype3, BlockType.PARAGRAPH)
        self.assertEqual(blocktype4, BlockType.PARAGRAPH)

    def test_block_typing_quote(self):
        block = ">a\n>b"
        block2 = ">a\nb"
        block3 = "> "
        blocktype = block_to_block_type(block)
        blocktype2 = block_to_block_type(block2)
        blocktype3 = block_to_block_type(block3)
        self.assertEqual(blocktype, BlockType.QUOTE)
        self.assertEqual(blocktype2, BlockType.PARAGRAPH)
        self.assertEqual(blocktype3, BlockType.QUOTE)

    def test_block_typing_ul(self):
        block = "- a\n- b"
        block2 = "- a\n-b"
        block3 = "- "
        blocktype = block_to_block_type(block)
        blocktype2 = block_to_block_type(block2)
        blocktype3 = block_to_block_type(block3)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)
        self.assertEqual(blocktype2, BlockType.PARAGRAPH)
        self.assertEqual(blocktype3, BlockType.UNORDERED_LIST)

    def test_block_typing_ol(self):
        blocktype = block_to_block_type("1. a\n2. b\n3. c")
        blocktype2 = block_to_block_type("1. a\n3. b")
        blocktype3 = block_to_block_type("2. a")
        blocktype4 = block_to_block_type("1.a")
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)
        self.assertEqual(blocktype2, BlockType.PARAGRAPH)
        self.assertEqual(blocktype3, BlockType.PARAGRAPH)
        self.assertEqual(blocktype4, BlockType.PARAGRAPH)

