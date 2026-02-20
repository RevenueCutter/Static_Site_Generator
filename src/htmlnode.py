

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ''

        html_str = ''
        for key, value in self.props.items():
            html_str += f' {key}="{value}"'

        return html_str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is not None:
            if self.tag is not None:
                return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
            else:
                return self.value
        else:
            raise ValueError

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is not None:
            if self.children is not None:
                string = f'<{self.tag}>'
                for child in self.children:
                    string += child.to_html()
                return string + f'</{self.tag}>'
            else:
                raise ValueError('Parent Node must have children')
        else:
            raise ValueError('Parent Node must have tags')
        

