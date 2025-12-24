from django import template

register = template.Library()

CENSOR_WORDS = {
    'дурак',
    'насилие',
    'алкоголь',
    'наркотики',
    'курение',
    'убийство',
}

PUNCTUATION_RIGHT = ".,!?:;…"

@register.filter(name="censor")
def censor(value):
    if not isinstance(value, str):
        raise TypeError("Фильтр censor можно применять только к строкам (str).")

    tokens = value.split()
    censored_tokens = []
    for token in tokens:
        clean = token.rstrip(PUNCTUATION_RIGHT)
        suffix = token[len(clean):]

        if clean.lower() in CENSOR_WORDS and len(clean) > 0:
            masked = clean[0] + "*" * (len(clean) - 1)
            censored_tokens.append(masked + suffix)
        else:
            censored_tokens.append(token)
    return " ".join(censored_tokens)