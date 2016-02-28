import sys
import re


def main():
    _, dirty_file = sys.argv
    text = ''

    with open(dirty_file) as f:
        text = f.read()

    # remove the multitude of useless spans
    text = replace_regex(r'<\/?span[^>]*>', '', text)

    #remove &nbsp;
    text = replace_regex(r'&nbsp;', ' ', text)

    # put headings on one line
    text = replace_regex(r'<h([1-5])>\n([^<]*)<\/h\1>',
                         r'\n<h\1>\2</h\1>', text)

    # remove class divs
    text = replace_regex(r'<\/?div[^>]*>', '', text)

    # remove div encapsulated brs
    text = replace_regex(r'<div>\s*<br \/>\s*<\/div>', '</ br>', text)

    #remove brs within heading tags
    text = replace_regex(r'<h([1-5])>\s*(<br \/>)([^<]*)<\/h\1>',
                        r'<h\1>\3</h\1>', text)

    # remove empty tags eg <pre></pre>
    text = replace_regex(r'<([^>]*)>\s*<\/\1>', '', text)

    with open(dirty_file + '_cleaned', 'w+') as f:
        f.write(fix_formatting(text))


def fix_formatting(text):
    """Fixes aesthetic formatting of text"""

    # make sure <br \> tags have one line above and below
    text = replace_regex(r'(\s*<br \/>\s*)', r'\n\1\n', text)

    # remove multiple \n
    text = replace_regex(r'\n{2,}', r'\n', text)

    return text


def replace_regex(regex, repl, text):
    """Replaces all occurances of a regex pattern regex, in text"""
    replacer = re.compile(regex, re.DOTALL)
    replaced = replacer.sub(repl, text)

    return replaced

if __name__ == '__main__':
    main()
