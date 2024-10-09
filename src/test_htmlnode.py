import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        cmp_val = " href=\"https://google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), cmp_val)

        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")



if __name__ == "__main__":
    unittest.main()
