import re


def clean_word(word: str, allowed_chars: str = '') -> str:
    # allowed_chars = allowed_chars.replace('.', '\.') # TODO: Fix for dots
    regexp = '[^\w{}]'.format(allowed_chars)
    result = re.sub(regexp, '', word).lower()
    for char in allowed_chars:
        result = re.sub('{0}{0}'.format(char), char, result)
    return result
