import htmlnode


class ParentNode(htmlnode.HTMLNode):

    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, props=props, children=children)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag specified.")
        if self.children == None:
            raise ValueError("No children specified.")
    
        html_repr = ""
        html_repr += f"<{self.tag}"
        if not self.props == None:
            html_repr += self.props.to_html()
        html_repr += ">"
        for child in self.children:
            html_repr += child.to_html()
        html_repr += f"</{self.tag}>"
        return html_repr



