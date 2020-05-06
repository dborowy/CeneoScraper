def extract_feature(opinion, selector,attribute = None) :
    try:
        if not attribute:
            return opinion.select(selector).pop().get_text().strip()
        else:
            return opinion.select(selector).pop()[attribute]
    except IndexError:
        return None

def remove_whitespace(text):
    if text!=None:
        return re.sub("\n|\r", ". ", str(text))