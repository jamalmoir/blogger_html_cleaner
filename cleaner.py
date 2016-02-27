import sys
import re

def main():
    _, dirty_file = sys.argv
    text = ''

    with open(dirty_file) as f:
        text = f.read()

    markup_removed = purge_regex(r'<\/?span[^>]*>', text)
    empty_removed = purge_regex(r'<([^>]*)><\/\1>', markup_removed)

    with open(dirty_file + '_cleaned', 'w+') as f:
        f.write(empty_removed)

def purge_regex(regex, text):
    #removed all occurances of regex pattern in text
    purger = re.compile(regex, re.DOTALL)
    purged = purger.sub('', text)

    return purged

if __name__ == '__main__':
    main()
