from django import template


register = template.Library()


CENSOR_WORDS = [
    'ночь', #для проверки
]


@register.filter()
def censor(value):
    """
    выводит 'Х****' вместо цензурированных слов

    value: цензурированные слова
    """
    if type(value) is str:
        for word in CENSOR_WORDS:
            value = value.replace(word, "*" * len(word))
            value = value.replace(word.capitalize(), "*" * len(word))
    else:
        raise ValueError('Требуется строка')

    return f'{value}'