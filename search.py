from pattern.search import Pattern
from pattern.en import parsetree, wordnet

#p = Pattern.fromstring('NP * than * NP')
#p = Pattern.fromstring('RB VB|VBZ|VBP|VBD|VBN|VBG NP')

def re_search(text, search_string):
    tree = parsetree(text, lemmata=True)
    pat = Pattern.fromstring(search_string)
    results = pat.search(tree)
    return results

def search(text, search_string):
    results = re_search(text, search_string)
    output = []
    for match in results:
        sent = []
        for word in match:
            sent.append(word.string)
        output.append(" ".join(sent))
    return output

def hypernym_search(text, search_word):
    output = []
    synset = wordnet.synsets(search_word)[0]
    pos = synset.pos
    possible_words = re_search(text, pos)
    for match in possible_words:
        word = match[0].string
        #print word
        synsets = wordnet.synsets(word)
        if len(synsets) > 0:
            hypernyms = synsets[0].hypernyms(recursive=True)
            if any(search_word == h.senses[0] for h in hypernyms):
                output.append(word)
    return set(output)

def list_hypernyms(search_word):
    output = []
    for synset in wordnet.synsets(search_word):
        hypernyms = synset.hypernyms(recursive=True)
        #output = output + [h.senses[0] for h in hypernyms]
        output.append([h.senses[0] for h in hypernyms])
    return output

#s.hypernyms(recursive=True)


if __name__ == '__main__':

    import sys

    #results = list_hypernyms(sys.argv[1])
    text = sys.stdin.read()
    #results = search(text, sys.argv[1])
    results = hypernym_search(text, sys.argv[1])
    for result in results:
        print result
