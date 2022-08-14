from transliterate import translit


def transliterate_text(text, lang='ru', reversed=True):
    return translit(text, lang, reversed=reversed)
