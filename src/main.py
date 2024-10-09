from textnode import * 
from htmlnode import *

def main():
    text_node = TextNode("This is a text node", "bold", "localhost:8080")
    print(text_node)
    html_node = HTMLNode("p", "this is the value", [HTMLNode(), HTMLNode()], {"href": "https://google.com/", "target": "_blank"})
    print(html_node)


if __name__ == "__main__":
    main()
