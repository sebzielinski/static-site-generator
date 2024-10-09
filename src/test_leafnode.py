import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(tag="a", value="this is some text.", props={"href": "https://google.com", "target": "_blank"})
        grnd_trth = "<a href=\"https://google.com\" target=\"_blank\">this is some text.</a>"
        self.assertEqual(node.to_html(), grnd_trth)

        node = LeafNode(tag="p", value="this is some text.")
        grnd_trth = "<p>this is some text.</p>"
        self.assertEqual(node.to_html(), grnd_trth)

        


if __name__ == "__main__":
    unittest.main()
