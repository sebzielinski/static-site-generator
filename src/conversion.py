from textnode import TextNode
from leafnode import LeafNode
import re

text_types = ["text", "bold", "italic", "code", "link", "image"] 

def text_node_to_html_node(text_node):

    match text_node.text_type:
        case "text":
            return LeafNode(value=text_node.text)
        case "bold":
            return LeafNode(tag="b", value=text_node.text)
        case "italic":
            return LeafNode(tag="i", value=text_node.text)
        case "code":
            return LeafNode(tag="code", value=text_node.text)
        case "link":
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case "image":
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    
    raise ValueError

    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if len(old_nodes) == 0:
        raise ValueError("The node list should not be empty.")

    new_nodes = []
    for node in old_nodes:
        split_node = node.text.split(delimiter)
        if len(split_node) == 1:
            new_nodes.append(node)
            continue
        elif len(split_node) % 2 == 0:
            raise SyntaxError("Invalid markdown syntax.")

        for i, _ in enumerate(split_node):
            if i % 2 == 0:
                if split_node[i] == '':
                    continue
                new_nodes.append(TextNode(split_node[i], node.text_type))
            elif i % 2 == 1:
                new_nodes.append(TextNode(split_node[i], text_type))

    return new_nodes

def split_nodes_image(old_nodes):
    if len(old_nodes) == 0:
        raise ValueError("The node list should not be empty.")

    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if not images:
            new_nodes.append(node)
            continue
        
        texts = node.text
        for i, image in enumerate(images):
            texts = texts.split(f"![{image[0]}]({image[1]})", maxsplit=1)
            if not texts[0] == '':
                new_nodes.append(TextNode(texts[0], "text"))
            new_nodes.append(TextNode(image[0], "image", image[1]))
            if len(images) == i+1 and not texts[1] == '':  # we are at the last image. there might be some text after the last image, that we have to add manually.
                new_nodes.append(TextNode(texts[1], "text"))
            texts = texts[1]

    return new_nodes

def split_nodes_link(old_nodes):
    if len(old_nodes) == 0:
        raise ValueError("The node list should not be empty.")

    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue
        
        texts = node.text
        for i, link in enumerate(links):
            texts = texts.split(f"[{link[0]}]({link[1]})", maxsplit=1)
            if not texts[0] == '':
                new_nodes.append(TextNode(texts[0], "text"))
            new_nodes.append(TextNode(link[0], "link", link[1]))
            if len(links) == i+1 and not texts[1] == '':  # we are at the last link. there might be some text after the last link, that we have to add manually.
                new_nodes.append(TextNode(texts[1], "text"))
            texts = texts[1]

    return new_nodes


def extract_markdown_images(text):
    # matches = re.findall(r"!\[([^\[]*)\]\(([^\(]*)\)", text)
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def text_to_textnodes(text):
    new_nodes = split_nodes_delimiter([TextNode(text, "text")], "**", "bold")
    new_nodes = split_nodes_delimiter(new_nodes, "*", "italic")
    new_nodes = split_nodes_delimiter(new_nodes, "`", "code")
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(md_doc):
    split_result = md_doc.split("\n\n")
    stripped_blocks = [block.strip() for block in split_result if not block.strip() == '']
    return stripped_blocks

