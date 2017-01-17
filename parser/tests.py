import unittest
from parse_json import Tag, TextTag


class TestTags(unittest.TestCase):

    def setUp(self):
        self.test_tag1 = 'h1'
        self.test_value1 = 'test1'
        self.test_result1 = '<h1>test1</h1>'

        self.test_tag2 = 'p'
        self.test_value2 = 'test2'
        self.test_result2 = '<p>test2</p>'

    def test_text_tag(self):
        """
        Test `TextTag` functionality
        """
        content = 'Hello world!'
        self.assertEqual(TextTag(content).render(), content)

        content = 'Good day!'
        self.assertEqual(TextTag(content).render(), content)

    def test_render_tag(self):
        """
        Test `Tag` functionality
        """
        tag1 = Tag(self.test_tag1)
        tag1.add(TextTag(self.test_value1))
        self.assertEqual(tag1.render(), self.test_result1)

        tag2 = Tag(self.test_tag2)
        tag2.add(TextTag(self.test_value2))
        self.assertEqual(tag2.render(), self.test_result2)

    def test_children(self):
        """
        Test `children` functionality
        """
        tag1 = Tag(self.test_tag1)
        tag1.add(TextTag(self.test_value1))

        tag2 = Tag(self.test_tag2, tag1)
        tag2.add(TextTag(self.test_value2))

        html = '<h1>test1<p>test2</p></h1>'
        self.assertEqual(tag1.render(), html)

    def test_parse_dict(self):
        """
        Test dictionary parsing
        """
        data = {'p': 'Hello!'}

        root = Tag.parse(data)
        tag = Tag('p')
        TextTag(data['p'], tag)
        self.assertEqual(root.render(), tag.render())

    def test_parse_list(self):
        """
        Test list parsing
        """
        data = [{'p': 'Hello!'}, {'div': 'Example 1'}]

        root = Tag.parse(data)

        tag = Tag('ul')
        li = Tag('li', tag)
        tag1 = Tag('p', li)
        TextTag('Hello!', tag1)

        li = Tag('li', tag)
        tag2 = Tag('div', li)
        TextTag('Example 1', tag2)
        self.assertEqual(root.render(), tag.render())


if __name__ == '__main__':
    unittest.main()
