class BlockNode():

    def __init__(self, block_type, children):
        self.block_type = block_type
        self.children = children

    def __eq__(self, block_node):
        if not self.block_type == block_node.block_type:
            return False
        if not self.children == block_node.children:
            return False
        return True

    def __repr__(self):
        children_str = ""
        repr_str = f"BlockNode(block_type={self.block_type}, self.children="
        for child in self.children:
            repr_str += child.__repr__()
        repr_str += ")"

        return repr_str
        
