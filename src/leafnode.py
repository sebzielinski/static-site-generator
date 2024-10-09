import htmlnode


class LeafNode(htmlnode.HTMLNode):

    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self):
        if self.value == None:
            raise ValueError("No value specified")
        if self.tag == None:
            return self.value
    
        html_repr = ""
        html_repr += f"<{self.tag}"
        html_repr += self.props_to_html()
        html_repr += ">"
        html_repr += f"{self.value}"
        html_repr += f"</{self.tag}>"
        return html_repr



