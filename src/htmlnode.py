class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""
        html_props_string = ""
        for prop in self.props:
            html_props_string += f" {prop}=\"{self.props[prop]}\""
        return html_props_string


    def __repr__(self):
        string = "HTMLNode(\n"
        string += f"    Tag: {self.tag}\n"
        string += f"    Value: {self.value}\n"
        string += f"    Children: {self.children}\n"
        string += f"    Props: {self.props}\n"
        string += ")"
        return string
