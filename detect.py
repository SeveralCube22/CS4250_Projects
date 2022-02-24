from langdetect import detect
from langdetect import detect_langs

# Checks against the most likely language detected
def is_lang(lang, str):
	return detect(str) == lang

# Checks if the string matches the target language by at least the given probability    
def is_lang_prob(targetLang, prb, str):
    langs = detect_langs(str)
    for l in langs:
        if l.lang == targetLang and l.prob >= prb:
            return True
    return False