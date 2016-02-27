import pytest
import cleaner

class TestTagRemoval():
    def test_span_removal(self):
        text = ('<span style="font-family: &quot;helvetica neue&quot; ,'
        '&quot;arial&quot; , &quot;helvetica&quot; , sans-serif;">This is some'
        ' dummy text lalalala</span> This is some more dummy text '
        '<span>test</span>')

        expected = ('This is some dummy text lalalala This is some more dummy '
        'text test')

        cleaned = cleaner.remove_superflous_markup(text)

        assert cleaned == expected
