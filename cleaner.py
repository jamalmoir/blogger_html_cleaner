import sys
import re


def main():
    _, dirty_file = sys.argv
    text = ''

    with open(dirty_file) as f:
        text = f.read()

    # remove the multitude of useless spans
    span_removed = replace_regex(r'<\/?span[^>]*>', '', text)
    # put headings on one line
    heading_fixed = replace_regex(r'<h([1-5])>\n([^<]*)<\/h\1>',
                                  r'\n<h\1>\2</h\1>', span_removed)
    # remove class blob-wrapper divs
    blob_removed = replace_regex(r'(<div class="blob-wrapper[^>]*>)'
                                '(.*?(?=<\/div>))(<\/div>)', r'\2',
                                heading_fixed)
    #remove div encapsulated brs
    divbr_removed = replace_regex(r'<div>\s*<br \/>\s*<\/div>', '</ br>',
                                 blob_removed)
    # remove empty tags eg <pre></pre>
    empty_removed = replace_regex(r'<([^>]*)>\s*<\/\1>', '', divbr_removed)

    with open(dirty_file + '_cleaned', 'w+') as f:
        f.write(fix_formatting(empty_removed))

def fix_formatting(text):
    # make sure <br \> tags have one line above and below
    br_fixed = replace_regex(r'(\s*<br \/>\s*)', r'\n\1\n', text)
    #remove multiple \n
    multin_removed = replace_regex(r'\n{2,}', r'\n', br_fixed)

    return multin_removed

def replace_regex(regex, repl, text):
    """Replaces all occurances of a regex pattern regex, in text"""
    replacer = re.compile(regex, re.DOTALL)
    replaced = replacer.sub(repl, text)

    return replaced

if __name__ == '__main__':
    main()
