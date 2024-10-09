import unittest
from textnode import TextNode
from leafnode import LeafNode
import conversion

class ConversionTest(unittest.TestCase):
    
    def test_text_to_html_conversion(self):
        node = TextNode("this is a text", "text")
        leaf_node = LeafNode(tag=None, value="this is a text")
        self.assertEqual(conversion.text_node_to_html_node(node).to_html(), leaf_node.to_html())

        node = TextNode("this is a text", "bold")
        leaf_node = LeafNode(tag="b", value="this is a text")
        self.assertEqual(conversion.text_node_to_html_node(node).to_html(), leaf_node.to_html())

        node = TextNode("this is a text", "italic")
        leaf_node = LeafNode(tag="i", value="this is a text")
        self.assertEqual(conversion.text_node_to_html_node(node).to_html(), leaf_node.to_html())

        node = TextNode("this is a text", "code")
        leaf_node = LeafNode(tag="code", value="this is a text")
        self.assertEqual(conversion.text_node_to_html_node(node).to_html(), leaf_node.to_html())

        node = TextNode("this is a text", "link", "https://google.com/")
        leaf_node = LeafNode(tag="a", value="this is a text", props={"href": "https://google.com/"})
        self.assertEqual(conversion.text_node_to_html_node(node).to_html(), leaf_node.to_html())

        node = TextNode("this is a text", "image", "https://google.com/")
        leaf_node = LeafNode(tag="img", value="", props={"src": "https://google.com/", "alt": "this is a text"})
        self.assertEqual(conversion.text_node_to_html_node(node).to_html(), leaf_node.to_html())

        try:
            node = TextNode("this is a text", "bla")
            conversion.text_node_to_html_node(node)
            assert False, "A ValueError should have been thrown, but wasn't."
        except ValueError:
            pass

if __name__ == "__main__":
    unittest.main()

