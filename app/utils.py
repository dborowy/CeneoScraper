def extract_feature(opinion, selector, attribute = None) :
    try:
        if not attribute:
            return opinion.select(selector).pop(0).get_text().strip()
        else:
            return opinion.select(selector).pop(0)[attribute]
    except IndexError:
        return None

def remove_whitespace(text):
    try:
        for char in ["\n", "\r"]:
            text = text.replace(char, ". ")
        return text
    except AttributeError:
        pass