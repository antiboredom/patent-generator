from pattern.en import tag
import sys

text = sys.stdin.read()

try:
    pos = sys.argv[1]
except(IndexError):
    pos = 'NN'

try:
    min_length = int(sys.argv[2])
except(IndexError):
    min_length = 5 

words = [] 

for word, p in tag(text):
    if p == pos and len(word) >= min_length:
        words.append(word)

for word in set(words):
    print word

