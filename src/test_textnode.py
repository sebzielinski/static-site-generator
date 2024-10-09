import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("bla", "italic")
        node2 = TextNode("blub", "italic")
        self.assertNotEqual(node, node2)

        node = TextNode("bla", "italic")
        node2 = TextNode("bla", "bold")
        self.assertNotEqual(node, node2)

        node = TextNode("bla", "italic", "https://boot.dev")
        node2 = TextNode("bla", "italic")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
