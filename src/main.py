import os
import shutil
import sys
from pathlib import Path
from textnode import TextType, TextNode
from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode

def copy_files_recursive(source_dir_path, dest_dir_path):
    if os.path.exists(source_dir_path):
        source_list = os.listdir(source_dir_path)
        for item in source_list:
            item_path = os.path.join(source_dir_path, item)
            if os.path.isfile(item_path):
                shutil.copy(item_path, dest_dir_path)
                print(f"Copying {item} from {item_path} to {dest_dir_path}")
            else:
                new_dest_dir_path = os.path.join(dest_dir_path, item)
                os.mkdir(new_dest_dir_path)
                print(f"Creating new {new_dest_dir_path} sub directory at destination")
                copy_files_recursive(item_path, new_dest_dir_path)



def initialize_public_files(dest_dir_path):
    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
    os.mkdir(dest_dir_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(from_path, 'r') as f:
        content = f.read()
        f_html = markdown_to_html_node(content).to_html()
        title = extract_title(content)
    with open(template_path, 'r') as g:
        template = g.read()
        full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", f_html)
        full_html = full_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    with open(dest_path, 'w') as h:
        h.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.exists(dir_path_content):
        content_list = os.listdir(dir_path_content)
        for item in content_list:
            item_path = os.path.join(dir_path_content, item)
            if os.path.isfile(item_path):
                new_dest_dir_path = os.path.join(dest_dir_path, item)
                new_dest_html_path = Path(new_dest_dir_path).with_suffix(".html")
                generate_page(item_path, template_path, new_dest_html_path, basepath)
            else:
                new_dest_dir_path = os.path.join(dest_dir_path, item)
                os.makedirs(new_dest_dir_path, exist_ok=True)
                print(f"Creating new {new_dest_dir_path} subdirectory at destination")
                generate_pages_recursive(item_path, template_path, new_dest_dir_path, basepath)


def extract_title(markdown):
    if markdown:
        for line in markdown.split("\n"):
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[1:].lstrip()
        else:
            raise Exception("No heading in Markdown format found")

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    initialize_public_files("docs")
    copy_files_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()

