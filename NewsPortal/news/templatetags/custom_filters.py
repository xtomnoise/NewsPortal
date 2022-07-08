from django import template
import re

register = template.Library()

CENS_WORDS = [
    'сука',
    'козёл',
    'тварь',
    'скотина'
]


@register.filter()
def censor(text):
    if not type(text) == str:
        raise ValueError('Filter censor gets strings only.')

    censed_text = ''
    words = re.findall(r'[0-9]+|[A-z]+|[А-яё]+|\S| |', text)
    for word in words:
        if word in CENS_WORDS:
            word = word[0] + '*' * (len(word) - 1)
        censed_text += word
    return censed_text

