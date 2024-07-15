import spacy

nlp = spacy.load("en_core_web_sm")


def named_entity_recognition(text: str) -> [str]:
    """
    Extract person names from checkspod episode summary
    :param text: Text summary of checkspod episode
    :return: List of person names
    """
    ans = []
    ner = nlp(text)
    for word in ner.ents:
        if word.label_ == 'PERSON':
            ans.append(word.text)
    return ans
