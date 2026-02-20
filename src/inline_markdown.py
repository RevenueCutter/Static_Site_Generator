from textnode import TextNode, TextType
from htmlnode import HTMLNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise ValueError("Invalid Markdown syntax: no matching delimiter found")
            for i in range(len(split_text)):
                if split_text[i] != "" and i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                elif split_text[i] != "" and i % 2 == 1:
                    new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            images_extracted = extract_markdown_images(node.text)
            if images_extracted == []:
                new_nodes.append(node)
            else:
                current_text = node.text
                for image in images_extracted:
                    md_string = f"![{image[0]}]({image[1]})"
                    sections = current_text.split(md_string, 1)
                    if sections[0]:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    current_text = sections[1]
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            links_extracted = extract_markdown_links(node.text)
            if links_extracted == []:
                new_nodes.append(node)
            else:
                current_text = node.text
                for link in links_extracted:
                    md_string = f"[{link[0]}]({link[1]})"
                    sections = current_text.split(md_string, 1)
                    if sections[0]:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    current_text = sections[1]
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    if text is not None and text != "":
        old_nodes = [TextNode(text, TextType.TEXT)]
        img_link_text_nodes = split_nodes_link(split_nodes_image(old_nodes))
        img_link_bold_text_nodes = split_nodes_delimiter(img_link_text_nodes, "**", TextType.BOLD)
        img_link_bold_italic_text_nodes = split_nodes_delimiter(img_link_bold_text_nodes, "_", TextType.ITALIC)
        return split_nodes_delimiter(img_link_bold_italic_text_nodes, "`", TextType.CODE)
    else:
        return []
