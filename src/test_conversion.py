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

    def test_split_nodes(self):
        node = TextNode("This is a **bold** text.", "text")
        new_nodes = conversion.split_nodes_delimiter([node], "**", "bold")
        grnd_trth = [TextNode("This is a ", "text"), TextNode("bold", "bold"), TextNode(" text.", "text")]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode("**bold** text.", "text")
        new_nodes = conversion.split_nodes_delimiter([node], "**", "bold")
        grnd_trth = [TextNode("bold", "bold"), TextNode(" text.", "text")]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode("**bold**", "text")
        new_nodes = conversion.split_nodes_delimiter([node], "**", "bold")
        grnd_trth = [TextNode("bold", "bold")]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode("This is a *italic* text.", "text")
        new_nodes = conversion.split_nodes_delimiter([node], "*", "italic")
        grnd_trth = [TextNode("This is a ", "text"), TextNode("italic", "italic"), TextNode(" text.", "text")]
        self.assertEqual(new_nodes, grnd_trth)
        
        node = TextNode("This is a `code block` text.", "text")
        new_nodes = conversion.split_nodes_delimiter([node], "`", "code")
        grnd_trth = [TextNode("This is a ", "text"), TextNode("code block", "code"), TextNode(" text.", "text")]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode("This is a normal text.", "text")
        new_nodes = conversion.split_nodes_delimiter([node], "*", "italic")
 
        old_nodes = [
                    TextNode("This is ", "text"),
                    TextNode("italic", "italic"),
                    TextNode(" and this is **bold** text.", "text"),
                ]
        new_nodes = conversion.split_nodes_delimiter(old_nodes, "**", "bold")
        grnd_trth = [
                    TextNode("This is ", "text"),
                    TextNode("italic", "italic"),
                    TextNode(" and this is ", "text"),
                    TextNode("bold", "bold"),
                    TextNode(" text.", "text"),
                ]
        self.assertEqual(new_nodes, grnd_trth)

        try:
            node = TextNode("This is a normal **broken text.", "text")
            new_nodes = conversion.split_nodes_delimiter([node], "**", "bold")
            assert False, "A Syntax Error should have been thrown, but wasn't."
        except SyntaxError:
            pass

        try:
            node = TextNode("This is a **really** **broken text.", "text")
            new_nodes = conversion.split_nodes_delimiter([node], "**", "bold")
            assert False, "A Syntax Error should have been thrown, but wasn't."
        except SyntaxError:
            pass
        
        try:
            new_nodes = conversion.split_nodes_delimiter([], "**", "code")
            assert False, "A Value Error should have been thrown, but wasn't."
        except ValueError:
            pass

    def test_split_images(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) some more text",
            "text",
        )
        new_nodes = conversion.split_nodes_image([node])
        grnd_trth = [
                    TextNode("This is text with a ", "text"),
                    TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(" and ", "text"),
                    TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" some more text", "text"),
                ]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            "text",
        )
        new_nodes = conversion.split_nodes_image([node])
        grnd_trth = [
                    TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
                ]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) some more text",
            "text",
        )
        new_nodes = conversion.split_nodes_image([node])
        grnd_trth = [
                    TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" some more text", "text"),
                ]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode(
            "",
            "text",
        )
        new_nodes = conversion.split_nodes_image([node])
        grnd_trth = [
                    TextNode("", "text"),
                ]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode(
            "some text",
            "text",
        )
        new_nodes = conversion.split_nodes_image([node])
        grnd_trth = [
                    TextNode("some text", "text"),
                ]
        self.assertEqual(new_nodes, grnd_trth)


    def test_split_links(self):
        node = TextNode(
            "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg) some more text",
            "text",
        )
        new_nodes = conversion.split_nodes_link([node])
        grnd_trth = [
                    TextNode("This is text with a ", "text"),
                    TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(" and ", "text"),
                    TextNode("obi wan", "link", "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" some more text", "text"),
                ]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode(
            "[rick roll](https://i.imgur.com/aKaOqIh.gif)[obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            "text",
        )
        new_nodes = conversion.split_nodes_link([node])
        grnd_trth = [
                    TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode("obi wan", "link", "https://i.imgur.com/fJRm4Vk.jpeg"),
                ]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode(
            "[rick roll](https://i.imgur.com/aKaOqIh.gif)[obi wan](https://i.imgur.com/fJRm4Vk.jpeg) some more text",
            "text",
        )
        new_nodes = conversion.split_nodes_link([node])
        grnd_trth = [
                    TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode("obi wan", "link", "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" some more text", "text"),
                ]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode(
            "",
            "text",
        )
        new_nodes = conversion.split_nodes_link([node])
        grnd_trth = [
                    TextNode("", "text"),
                ]
        self.assertEqual(new_nodes, grnd_trth)

        node = TextNode(
            "some text",
            "text",
        )
        new_nodes = conversion.split_nodes_link([node])
        grnd_trth = [
                    TextNode("some text", "text"),
                ]
        self.assertEqual(new_nodes, grnd_trth)



    def test_img_regex(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = conversion.extract_markdown_images(text)
        grnd_trth = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(matches, grnd_trth)

        text = "This is text with a ![](https://i.imgur.com/aKaOqIh.gif) and ![](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = conversion.extract_markdown_images(text)
        grnd_trth = [('', 'https://i.imgur.com/aKaOqIh.gif'), ('', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(matches, grnd_trth)

    def test_link_regex(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = conversion.extract_markdown_links(text)
        grnd_trth = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(matches, grnd_trth)

        text = "This is text with a link [](https://www.boot.dev) and [](https://www.youtube.com/@bootdotdev)"
        matches = conversion.extract_markdown_links(text)
        grnd_trth = [('', 'https://www.boot.dev'), ('', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(matches, grnd_trth)


    def test_text_to_textnodes(self):
        text = "This is a text with some **bold** and *italic* words, as well as some `code segment`. Have some ![images](https://google.com/image.jpg) and [links](https://google.com/maps) too!"
        new_nodes = conversion.text_to_textnodes(text)
        grnd_trth = [
                    TextNode("This is a text with some ", "text"),
                    TextNode("bold", "bold"),
                    TextNode(" and ", "text"),
                    TextNode("italic", "italic"),
                    TextNode(" words, as well as some ", "text"),
                    TextNode("code segment", "code"),
                    TextNode(". Have some ", "text"),
                    TextNode("images", "image", "https://google.com/image.jpg"),
                    TextNode(" and ", "text"),
                    TextNode("links", "link", "https://google.com/maps"),
                    TextNode(" too!", "text"),
                ]
        self.assertEqual(new_nodes, grnd_trth)

    def test_md_to_blocks(self):
        md_doc = '''

# This is a heading

This is a normal text with **bold elements** and 'code blocks'.

* Here we have a block
* of bold text
* as you can see

'''
        blocks = conversion.markdown_to_blocks(md_doc)
        grnd_trth = [
                    "# This is a heading",
                    "This is a normal text with **bold elements** and 'code blocks'.",
'''* Here we have a block
* of bold text
* as you can see''',
                ]
        self.assertEqual(blocks, grnd_trth)

        md_doc = ""
        blocks = conversion.markdown_to_blocks(md_doc)
        grnd_trth = []
        self.assertEqual(blocks, grnd_trth)
                        

    def test_block_to_block_type(self):
        block = "# This is a heading"
        grnd_trth = "heading"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = "#This is a NOT a heading"
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = "###### This is a level 6 heading"
        grnd_trth = "heading"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = "####### This is not a heading"
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = '''###### This is a level 6 heading
# This is a normal heading
This is not a heading
# normal heading'''
        # block = "###### This is a level 6 heading\n# This is a normal heading\nThis is not a heading\nJust a paragraph"
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)


        ### code ### 

        block = "```This is a code block```"
        grnd_trth = "code"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = "```This is a \nmultiline \ncode block```"
        grnd_trth = "code"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = "```This is a broken \nmultiline \ncode block```\n```"
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = "bla"
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)


        ### quote ###
        
        block = '''>Test quote
>without any defects
>bla'''
        grnd_trth = "quote"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = '''>Test quote
>with some
defects
>bla'''
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = '''asda>Test quote
>with some defects
>bla'''
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = '''>Test quote
>with some defects
>bla
asdas'''
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)


        ### unordered list ###
        
        block = '''* Test quote
* without any defects
* bla'''
        grnd_trth = "unordered_list"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = '''* Test quote
* with defects
bla'''
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = ''' - Test quote
- with defects
- bla'''
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = '''- Test quote
-with defects
- bla'''
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)


        ### ordered list ###
        block = '''1. Test ol
2. without any defects
3. bla'''
        grnd_trth = "ordered_list"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = '''1. Test ol
2. without any defects
4. bla'''
        grnd_trth = "paragraph"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = '''1. Test ol
2. without any defects
3. bla
4. sad
5.  q4
6. 23
7. asdhjas
8. ahdjags
9. asdjk
10. ajdsk
11. asdhjas'''
        grnd_trth = "ordered_list"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)

        block = "1. Test ol\n"
        for i in range(2, 10020):
            block += f"{i}. list item\n"
        grnd_trth = "ordered_list"
        block_type = conversion.block_to_block_type(block)
        self.assertEqual(block_type, grnd_trth)





if __name__ == "__main__":
    unittest.main()

