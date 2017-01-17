from collections import OrderedDict
import json
import sys


SOURCE_JSON = 'source.json'


class BaseTag(object):

    def __init__(self, parent=None):
        if parent:
            parent.add(self)
        self.tag_name = None
        self.children = []

    def render(self):
        raise NotImplementedError


class Tag(BaseTag):

    FORMAT_STR = '<{0}>{1}</{0}>'

    def __init__(self, tag_name=None, parent=None):
        super(Tag, self).__init__(parent)
        self.tag_name = tag_name

    def add(self, *tags):
        self.children.extend(tags)

    def render(self):
        children = ''.join([child.render() for child in self.children])
        if self.tag_name:
            return self.FORMAT_STR.format(self.tag_name, children)
        return children

    @classmethod
    def parse(cls, data):
        root = cls()
        if isinstance(data, list):
            root.parse_list(data)
        else:
            root.parse_dict(data)
        return root

    def parse_dict(self, data):
        for key, value in data.items():
            tag = Tag(key, self)
            if isinstance(value, list):
                tag.parse_list(value)
            else:
                TextTag(value, tag)

    def parse_list(self, data):
        ul = Tag('ul', self)
        for item in data:
            li = Tag('li', ul)
            li.parse_dict(item)


class TextTag(BaseTag):

    def __init__(self, text='', parent=None):
        super(TextTag, self).__init__(parent)
        self.text = text

    def render(self):
        return self.text


def main():
    with open(SOURCE_JSON) as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    root = Tag.parse(data)
    sys.stdout.write(root.render())


if __name__ == "__main__":
    main()
