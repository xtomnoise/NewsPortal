CENS_WORDS = [
    'сука',
    'козёл',
    'тварь',
    'скотина'
]


# @register.filter()
def censor(text):
    censed_text = []
    words = text.split()
    for word in words:
        if word in CENS_WORDS:
            word = word[0] + '*' * (len(word) - 1)
        censed_text.append(word)
    return ' '.join(censed_text)

a = 'Fdsa'
print(a[:-1])


