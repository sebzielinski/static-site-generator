import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
                    tag="p",
                    children=[
                        LeafNode(tag="b", value="bold text"),
                        LeafNode(tag=None, value="normal text"),
                        LeafNode(tag="i", value="italic text"),
                        LeafNode(tag=None, value="normal text"),
                    ]
                )
        grnd_trth = "<p><b>bold text</b>normal text<i>italic text</i>normal text</p>"
        self.assertEqual(node.to_html(), grnd_trth)

        try:
            node = ParentNode(
                        tag="h1",
                        children=None
                    )
            html = node.to_html()
        except ValueError:
            pass 

        node = ParentNode(
                    tag="div",
                    children=[
                        ParentNode(
                           tag="h2",
                           children=[
                                LeafNode(tag=None, value="This is some "),
                                LeafNode(tag="b", value="bold "),
                                LeafNode(tag=None, value="text.")
                            ]
                        ),
                        LeafNode(tag="i", value="some italic text of some class", props={"class": "italic"})
                    ]
                )

        grnd_trth = "<div><h2>This is some <b>bold </b>text.</h2><i class=\"italic\">some italic text of some class</i></div>"
        self.assertEqual(node.to_html(), grnd_trth)


if __name__ == "__main__":
    unittest.main()
