import unittest
from parse_json import render_tag


class TestTags(unittest.TestCase):

    def setUp(self):
        self.test_tag1 = 'title'
        self.test_value1 = 'test1'
        self.test_result1 = '<h1>test1</h1>'

        self.test_tag2 = 'body'
        self.test_value2 = 'test2'
        self.test_result2 = '<p>test2</p>'

    def test_render_tag(self):
        """
        Test `render_tag` functionality
        """
        self.assertEqual(render_tag(self.test_tag1, self.test_value1),
                         self.test_result1)
        self.assertEqual(render_tag(self.test_tag2, self.test_value2),
                         self.test_result2)


if __name__ == '__main__':
    unittest.main()
