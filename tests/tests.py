import pytest
from .context import blogger_html_cleaner


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
