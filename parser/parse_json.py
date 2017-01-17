from collections import OrderedDict
import html
import json
import sys
import re


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

    TAG_STR = '<{0}{2}>{1}</{0}>'

    def __init__(self, tag_name=None, parent=None):
        super(Tag, self).__init__(parent)
        self.parse_key(tag_name)

    def add(self, *tags):
        self.children.extend(tags)

    def render(self):
        children = ''.join([child.render() for child in self.children])
        if self.tag_name:
            attrs = []
            if self.class_list or self.tag_id:
                attrs = ['']
                if self.class_list:
                    attrs.append('class="{}"'.format(' '.join(self.class_list)))
                if self.tag_id:
                    attrs.append('id="{}"'.format(self.tag_id))
            return self.TAG_STR.format(self.tag_name, children, ' '.join(attrs))
        return children

    @classmethod
    def parse(cls, data):
        root = cls()
        if isinstance(data, list):
            root.parse_list(data)
        else:
            root.parse_dict(data)
        return root

    def parse_key(self, key):
        self.tag_id = None
        self.class_list = []
        if key is None:
            self.tag_name = key
            return
        # initial tag attributes
        self.tag_name = re.match('^(\w+)', key).group()
        if re.findall('#(\w+)', key):
            self.tag_id = re.findall('#(\w+)', key)[0]
        self.class_list = re.findall('\.(\w+)', key)

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
        self.text = html.escape(text)

    def render(self):
        return self.text


def main():
    with open(SOURCE_JSON) as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    root = Tag.parse(data)
    sys.stdout.write(root.render())


if __name__ == "__main__":
    main()
