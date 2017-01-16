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

    def bind_obvious_tags(self, **kwargs):
        for key, value in kwargs.items():
            tag = Tag(key)
            tag.add(TextTag(value))
            self.add(tag)


class TextTag(BaseTag):

    def __init__(self, text='', parent=None):
        super(TextTag, self).__init__(parent)
        self.text = text

    def render(self):
        return self.text


def main():
    with open(SOURCE_JSON) as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    if not isinstance(data, list):
        root = Tag()
        root.bind_obvious_tags(**data)
    else:
        root = Tag('ul')
        for el in data:
            li = Tag('li', root)
            li.bind_obvious_tags(**el)

    sys.stdout.write(root.render())


if __name__ == "__main__":
    main()
