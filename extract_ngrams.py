#import sys
#from pattern.search import Pattern
#from pattern.en import parsetree

#text = sys.stdin.read()
#t = parsetree(text, lemmata=True)
##print text
#p = Pattern.fromstring('NP *+ than NP *+')
#search = p.search(t)

#for match in search:
    #sent = []
    #for word in match:
        #sent.append(word.string)
    #print " ".join(sent)
    #for word in sent:
        #print word
#match = pattern.match(text)

#print match.group(1)

import sys
from pattern.vector import Document, count, words
from pattern.en import ngrams

text = sys.stdin.read()

total = int(sys.argv[1])
grams = ngrams(text, n=total)
ngramcount = {}
for gram in grams:
    if gram in ngramcount:
        ngramcount[gram] += 1
    else:
        ngramcount[gram] = 1

for gram in sorted(ngramcount, key=ngramcount.get, reverse=True):
    count = ngramcount[gram]
    if count > 10 and all(len(x) > 0 for x in gram):
        print str(count) + ': ' + ' '.join(gram)


#doc = Document(text, threshold=2)
#for w in doc.keywords(top=50):
    #print w[1]
