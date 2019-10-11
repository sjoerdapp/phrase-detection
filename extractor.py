#%%
# natural language processing module (Extractor)
import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

# search engine
from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh.index import open_dir
from whoosh.query import Every

# library for list manipulation
import itertools

nlp = spacy.load('en_core_web_sm')

def extractor(document, *pattern):
    '''
    @param str file: text file for tuple extraction
    @param list pattern: extraction pattern
    A phrase extractor based on spacy
    '''
    phrases = []
    matcher = Matcher(nlp.vocab)
    matcher.add("pattern extraction", None, *pattern)
    doc = nlp(document)
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        phrases.append(span.text)
    return phrases



#%%
def patternSearch(T_0, file):
    phrase_patterns = set()
    seed_pattern = [nlp(x) for x in T_0]
    phrase_matcher = PhraseMatcher(nlp.vocab)
    phrase_matcher.add('pattern search', None, *seed_pattern)
    # find occurrences of seed phrases
    with open(file, "r") as f:
        document = nlp(f.read().lower())
        matches = phrase_matcher(document)
        for match_id, start, end in matches:
            p = tuple((start, end))
            if p not in phrase_patterns:
                phrase_patterns.add(p)
    # find patterns around seed phrases
    extraction_pattern = []
    new_phrases = set()
    matcher = Matcher(nlp.vocab)
    with open(file, "r") as f:
        text = nlp(f.read().lower())
        for phrase_pattern in phrase_patterns:
            start = phrase_pattern[0]
            end = phrase_pattern[1]
            # # add content pattern 
            # tmp = []
            # span = text[start:end]
            # for token in span:
            #     tmp.append({"POS": token.pos_})
            # extraction_pattern.append(tmp)
            # add context pattern
            tmp = []
            for i in range(2, 0, -1):
                tmp.append({"TEXT": text[start - i].text})
            tmp.append({"TEXT": {"REGEX": "[a-zA-Z0-9_]"}, "OP":"+"})
            for i in range(3):
                tmp.append({"TEXT": text[end + i].text})
            extraction_pattern.append(tmp)
            for ep in extraction_pattern:
                print(ep)
                matcher.add("find new", None, ep)
                matches = matcher(text)
                for match_id, start, end in matches:
                    new_phrase = text[start+2:end-2].text
                    if new_phrase not in new_phrases:
                        new_phrases.add(new_phrase)
                matcher.remove("find new")

    # get new phrases
    return extraction_pattern, new_phrases

seed = ['machine learning', 'database system', 'natural language processing']
ep, n = patternSearch(seed, 'test.txt')
#%%
