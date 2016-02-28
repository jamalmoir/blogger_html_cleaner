import sys
import re


def main():
    _, dirty_file = sys.argv
    text = ''

    with open(dirty_file) as f:
        text = f.read()

    # remove the multitude of useless spans
    span_removed = purge_regex(r'<\/?span[^>]*>', text)
    # remove empty tags eg <pre></pre>
    empty_removed = purge_regex(r'<([^>]*)><\/\1>', span_removed)
    # put headings on one line
    heading_fixed = replace_regex(r'<h([1-5])>\n([^<]*)<\/h\1>',
                                  r'\n<h\1>\2<h\1>', empty_removed)

    with open(dirty_file + '_cleaned', 'w+') as f:
        f.write(heading_fixed)


def purge_regex(regex, text):
    """Removes all occurances of a regex pattern regex, in text"""
    purger = re.compile(regex, re.DOTALL)
    purged = purger.sub('', text)

    return purged


def replace_regex(regex, repl, text):
    """Replaces all occurances of a regex pattern regex, in text"""
    replacer = re.compile(regex, re.DOTALL)
    replaced = replacer.sub(repl, text)

    return replaced

if __name__ == '__main__':
    main()
