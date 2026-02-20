from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "normal paragraph"
    HEADING = "start with 1-6 # characters, followed by a space and the heading text"
    CODE = "start with ```\n then end with ```"
    QUOTE = "every line starts with a > 'QUOTED_TEXT'"
    UNORDERED_LIST = "every line starts with a - character, followed by a space"
    ORDERED_LIST = "starts with a number followed by a . and a space. The number must start at 1 and += 1"

def markdown_to_blocks(markdown):
    blocks = []
    stripped = markdown.strip()
    split_blocks = stripped.split("\n\n")
    for block in split_blocks:
        block = block.strip()
        if block != "":
            blocks.append(block)
    return blocks

def block_to_block_type(block):
    if block.startswith("#") and "\n" not in block:
        i = 0
        while i < len(block) and block[i] == "#":
            i += 1
        if i >= 1 and i <= 6 and i < len(block) and block[i] == " ":
            return BlockType.HEADING
    if block.startswith("```\n"):
        if block.endswith("\n```") or block.endswith("```"):
            return BlockType.CODE
    if block.startswith(">"):
        quote_lines = block.split("\n")
        if all(line.startswith(">") for line in quote_lines):
            return BlockType.QUOTE
    if block.startswith("- "):
        ul_lines = block.split("\n")
        if all(line.startswith("- ") for line in ul_lines):
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        ol_lines = block.split("\n")
        ordinal = 1
        for line in ol_lines:
            if not line.startswith(f"{ordinal}. "):
                break
            ordinal += 1
        else:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    parent_nodes = []
    split_blocks = markdown_to_blocks(markdown)
    for block in split_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            paragraph_node = get_paragraph_node(block)
            if paragraph_node:
                parent_nodes.append(paragraph_node)
        elif block_type == BlockType.HEADING:
            heading_node = get_heading_node(block)
            if heading_node:
                parent_nodes.append(heading_node)
        elif block_type == BlockType.QUOTE:
            quote_node = get_quote_node(block)
            if quote_node:
                parent_nodes.append(quote_node)
        elif block_type == BlockType.UNORDERED_LIST:
            ul_node = get_ul_node(block)
            if ul_node:
                parent_nodes.append(ul_node)
        elif block_type == BlockType.ORDERED_LIST:
            ol_node = get_ol_node(block)
            if ol_node:
                parent_nodes.append(ol_node)
        elif block_type == BlockType.CODE:
            code_node = get_code_node(block)
            if code_node:
                parent_nodes.append(code_node)
    return ParentNode("div", parent_nodes)

def text_to_children(text):
    leaf_nodes = []
    if text != "" and text != " ":
        text_nodes = text_to_textnodes(text)
        for text_node in text_nodes:
            leaf_nodes.append(text_node_to_html_node(text_node))
    return leaf_nodes

def get_paragraph_node(block):
    if block != "":
        leaf_nodes = text_to_children(block.replace("\n", " "))
        return ParentNode("p", leaf_nodes)

def get_heading_node(block):
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1
    heading_body = block[i + 1:]
    if heading_body != "":
        return ParentNode(f"h{i}", text_to_children(heading_body))

def get_quote_node(block):
    cleaned_lines = []
    lines = block.split("\n")
    for line in lines:
        cleaned_lines.append(line[1:].lstrip())
    if cleaned_lines != []:
        leaf_nodes = text_to_children(" ".join(cleaned_lines))
        return ParentNode("blockquote", leaf_nodes)

def get_ul_node(block):
    parent_nodes = []
    lines = block.split("\n")
    for line in lines:
        leaf_nodes = text_to_children(line[2:])
        parent_nodes.append(ParentNode("li", leaf_nodes))
    return ParentNode("ul", parent_nodes)

def get_ol_node(block):
    parent_nodes = []
    lines = block.split("\n")
    for line in lines:
        split_line = line.split(". ", 1)
        leaf_nodes = text_to_children(split_line[1])
        parent_nodes.append(ParentNode("li", leaf_nodes))
    return ParentNode("ol", parent_nodes)

def get_code_node(block):
    if block != "":
        text_node = TextNode(block[4: -3], TextType.CODE)
        return ParentNode("pre", [text_node_to_html_node(text_node)])






