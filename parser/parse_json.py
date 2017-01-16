from collections import OrderedDict
import json
import sys


SOURCE_JSON = 'source.json'


def render_tag(tag, content):
    """
    Wrap content by html tags.
    """
    return '<{0}>{1}</{0}>'.format(tag, content)


def main():
    with open(SOURCE_JSON) as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    result = []
    for el in data:
        for key, value in el.items():
            result.append(render_tag(key, value))
    sys.stdout.write("".join(result))


if __name__ == "__main__":
    main()
