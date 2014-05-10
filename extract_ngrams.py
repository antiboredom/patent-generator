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

