import pytest
from .context import blogger_html_cleaner


class TestTextManipulation():

    def test_replace_regex(self):
        string1 = "This is a<div class='remove'> test<remove>"
        string2 = "This is a banana"
        string3 = """What will happen to this mango, that is on
        multiple lines. Will this mango work?"""

        expected1 = "This is a test"
        expected2 = "This is a test"
        expected3 = """What will happen to this test, that is on
        multiple lines. Will this test work?"""

        replaced1 = blogger_html_cleaner.cleaner.replace_regex(r'<[^>]*>', ''
                                                              ,string1)
        replaced2 = blogger_html_cleaner.cleaner.replace_regex(r'banana'
                                                              ,'test', string2)
        replaced3 = blogger_html_cleaner.cleaner.replace_regex(r'mango', 'test'
                                                              , string3)

        assert replaced1 == expected1
        assert replaced2 == expected2
        assert replaced3 == expected3

class TestTagTools():

    def test_get_pure_tag(self):
        tag1 = '<div>'
        tag2 = '</div>'
        tag3 = '<pre class="prettyprint">'

        assert blogger_html_cleaner.cleaner.get_pure_tag(tag1) == '<div>'
        assert blogger_html_cleaner.cleaner.get_pure_tag(tag2) == '</div>'
        assert blogger_html_cleaner.cleaner.get_pure_tag(tag3) == '<pre>'

    def test_tag_match(self):
        tag1 = '<div>'
        tag2 = '</div>'
        tag3 = '<pre>'
        tag4 = '</pre>'

        assert blogger_html_cleaner.cleaner.tag_match(tag1, tag2) == True
        assert blogger_html_cleaner.cleaner.tag_match(tag1, tag1) == False
        assert blogger_html_cleaner.cleaner.tag_match(tag3, tag2) == False
        assert blogger_html_cleaner.cleaner.tag_match(tag3, tag3) == False
        assert blogger_html_cleaner.cleaner.tag_match(tag3, tag4) == True

class TestUnclosedTagRemover():

    def test_find_next_unclosed(self):
        text = ''

        with open('unclosed') as f:
            text = f.read()

        unclosed = blogger_html_cleaner.cleaner.find_next_unclosed(text)

        assert unclosed == (231, 254)

    def test_remove_unclosed(self):
        text = ''
        expected = ''

        with open('unclosed') as f:
            text = f.read()

        with open('unclosed_expected') as f:
            expected = f.read()

        removed = blogger_html_cleaner.cleaner.remove_unclosed(text)

        assert removed == expected

    def test_find_next_unopened(self):
        text = ''

        with open('unopened') as f:
            text = f.read()

        unopened = blogger_html_cleaner.cleaner.find_next_unopened(text)

        assert unopened == (232, 256)

    def test_remove_unopened(self):
        text = ''
        expected = ''

        with open('unopened') as f:
            text = f.read()

        with open('unopened_expected') as f:
            expected = f.read()

        removed = blogger_html_cleaner.cleaner.remove_unopened(text)

        assert removed == expected
