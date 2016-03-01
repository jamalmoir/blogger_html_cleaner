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

    #remove unclosed HTML tags
    text = remove_unclosed(text)

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

def remove_unclosed(text):
    """removed all unclosed HTML tags"""
    unclosed = find_next_unclosed(text)

    if unclosed:
        start, end = unclosed
        text = ''.join([text[:start], text[end:]])

        return remove_unclosed(text)

    return text


def find_next_unclosed(text):
    """Finds the next unclosed HTML tag"""
    tag_stack = []

    tag_regex= re.compile(r'<[^>]*>', re.DOTALL)
    tags = tag_regex.finditer(text)

    for tag in tags:
        #If it is a closing tag check if it matches the last opening tag
        if re.match(r'<\/[^>]*>', tag.group()):

            if tag_match(tag_stack[-1].group(), tag.group()):
                tag_stack.pop()
            else:
                unclosed = tag_stack.pop()
                return (unclosed.start(), unclosed.end())
        else:
            tag_stack.append(tag)


def tag_match(tag1, tag2):
    if get_pure_tag(tag1)[1:] == get_pure_tag(tag2)[2:]:
        return True

def get_pure_tag(tag):
    pure_tag = re.sub(r'<(\/?\S*)[^>]*>', r'<\1>', tag)

    return pure_tag

if __name__ == '__main__':
    main()
