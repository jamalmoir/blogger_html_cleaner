import pytest
import cleaner

class TestTagTools():
    def test_get_pure_tag(self):
        tag1 = '<div>'
        tag2 = '</div>'
        tag3 = '<pre class="prettyprint">'

        assert cleaner.get_pure_tag(tag1) == '<div>'
        assert cleaner.get_pure_tag(tag2) == '</div>'
        assert cleaner.get_pure_tag(tag3) == '<pre>'
