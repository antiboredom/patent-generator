import search
import sys, random, re
from pattern.en import tag, tokenize, conjugate, wordnet
from pprint import pprint

#text = sys.stdin.read()

# a [adjective] [specific noun] [(optional device/invention/machine)] that [something a character does something in the story]

#try lolita
#melville

class Invention(object):
    def __init__(self, text):
        self.source_text = text
        self.title = self.create_gerund_title()
        self.create_first_line()
        self.create_abstract()
        self.create_illustrations()
        self.create_description()
        #self.body = self.body()
        #self.find_lines()

    def prefix(self):
        prefixes = ["system", "method", "apparatus", "device"]
        self.prefixes = [random.choice(prefixes)]
        prefixes.remove(self.prefixes[0])
        self.prefixes.append(random.choice(prefixes))
        title = self.prefixes[0] + " and " + self.prefixes[1] + " for "
        if random.random() < .2:
            title = "web-based " + title
        pre = "a "
        if title[0] in 'aeiou':
            pre = "an "
        return pre + title


    def create_gerund_title(self):
        search_patterns = [
                'VBG DT NN RB', 'VBG NNP * NP', 'VBG NNP * .',
                'RB VBG NNP', 'VBG JJ NP', 'VBG * JJ * NP', 'VBG * JJ *',
                'VBG * NN', 'VBG * JJ *? NP NP?', 'VBG * JJ? NP']

        gerund_phrases = search.search_out(text, search_patterns[-1])
        self.possible_titles = []
        for title in gerund_phrases:
            self.possible_titles.append(title)
            #print self.prefix() + title
        self.partial_title = random.choice(self.possible_titles)
        title = self.prefix() + self.partial_title
        self.set_keywords(self.partial_title)
        return title.capitalize()

    def set_keywords(self, title):
        words = tag(title)
        self.nouns = [word[0] for word in words if word[1] == 'NN']
        self.verbs = [word[0] for word in words if word[1] in ['VB', 'VBZ']]
        self.adjectives = [word[0] for word in words if word[1] == 'JJ']
        #print self.nouns
        #print self.verbs
        #print words

    def create_first_line(self):
        templates = ['{0} is provided.', '{0} is disclosed.', 'The present invention relates to {0}.']
        self.first_line = random.choice(templates).format(self.title).capitalize()
        #if random.random() < .1 + ' comprising: ':
            #template = 'The present invention relates generally to the field of {0} and, more specifically, to methods and apparatus to {1} {2}.'

    def find_lines(self):
        lines = search.search_out(self.source_text, '|'.join(self.nouns + self.verbs + self.adjectives))
        print lines

    def key_sentences(self):
        words = set(search.hypernym_search(self.source_text, 'instrumentality'))
        sents = tokenize(self.source_text)
        pat = re.compile(' ' + '|'.join(words) + ' ')
        sents = [s for s in sents if pat.search(s) != None]
        #pat = '|'.join(words)
        #sents = [s for s in sents if search.contains(s, pat)]

        pprint(sents)
        pprint(words)
        #matches = re.findall('(([aA-zA].*' + '|'.join(words) + ').*\.)', self.source_text)
        #print matches

    def how_it_works(self):
        # 1. a title comprising of:
        # a. gerund nounphrase [n times]
        # b. gerund nounphrase
        # 2. 
        pass

    def sentence_walk(self):
        output = []
        sents = tokenize(self.source_text)
        words = set(search.hypernym_search(self.source_text, 'artifact'))
        pat = re.compile(' ' + '|'.join(words) + ' ')
        sents = [s for s in sents if pat.search(s) != None]
        pprint(sents)

    def create_illustrations(self):
        self.illustrations = []
        templates = ["Figure {0} illustrates {1}", 
            "Figure {0} is a schematic drawing of {1}",
            "Figure {0} is a perspective view of {1}",
            "Figure {0} is an isometric view of {1}",
            "Figure {0} schematically illustrates {1}",
            "Figure {0} is a block diagram of {1}",
            "Figure {0} is a cross section of {1}",
            "Figure {0} is a diagrammatical view of {1}"]
        illustrations = list(set(search.search_out(self.source_text, 'DT JJ NP IN * NN')))
        for i in range(len(illustrations)):
            self.illustrations.append(random.choice(templates).format(i+1, illustrations[i]))
        #sents = tokenize(self.source_text)
        #words = []
        #for s in sents:
            #tags = tag(s)
            #for i in range(len(tags)):
                #word, pos = tags[i]
                #if pos in ["VB", "VBZ", "VBP", "VBD", "VBN", "VBG"]:

    def create_abstract(self):
        artifacts = search.hypernym_combo(self.source_text, 'artifact', "JJ NN|NNS")
        #artifacts +=search.hypernym_combo(self.source_text, 'material', "JJ NN|NNS")
        artifacts = set(artifacts)
        self.artifacts = artifacts
        words = []
        #for w in artifacts:
            #pre = 'a'
            #if w[0] in 'aeiou':
                #pre = 'an'
        words = ["an " + w if w[0] in "aeiou" else "a " + w for w in artifacts]
        self.abstract = self.title + ". "
        self.abstract += "The devices comprises "
        self.abstract += ", ".join(words) 
    
    def define_word(self, word):
        synsets = wordnet.synsets(word)
        if len(synsets) > 0:
            gloss = synsets[0].gloss
            if gloss.find(';') > -1:
                gloss = gloss[:gloss.find(';')]
            word = word + " (comprising of " + gloss + ") "
        return word
       #w  + " which is "

    def create_description(self):
        pat = 'VB|VBD|VBZ|VBG * NN IN * NN'
        #pat = 'PRP * VB|VBD|VBZ|VBG * NN'
        phrases = search.search_out(self.source_text, pat)
        conjugated_phrases = []
        for phrase in phrases:
            words = []
            for word, pos in tag(phrase):
                if pos in ["VBZ", "VBD", "VB", "VBG"]:
                    words.append(conjugate(word, "3sg"))
                elif pos == "NN" and random.random() < .1:
                    words.append(self.define_word(word))
                else:
                    words.append(word)
            conjugated_phrases.append(' '.join(words))

        artifacts = list(self.artifacts)

        templates = ["The present invention", "According to a beneficial embodiment, the invention", "According to another embodiment, the device", "According to a preferred embodiment, the invention", "In accordance with an alternative specific embodiment, the present invention"] 
        i = 0
        self.description = ''
        for phrase in conjugated_phrases:
            #if i==0 or random.random() < .1:
            phrase = random.choice(templates) + " " + phrase
            self.description += phrase + ". "
            #i += 1
            #print random.choice(artifacts) + " " + phrase
        #print conjugated_phrases


    def body_old(self):
        output = []
        #self.possible_titles.remove(self.partial_title)
        useful_phrases = search.hypernym_combo(text, 'instrumentality', 'JJ? NP')
        random.shuffle(useful_phrases)
        random.shuffle(self.possible_titles)
        for i in range(len(self.possible_titles)):
            if (i < len(useful_phrases) and self.possible_titles[i] != self.partial_title):
                output.append(useful_phrases[i] + ' for ' + self.possible_titles[i])
        return output

    def format(self):
        print self.title
        print "\n\nABSTRACT\n\n"
        print self.abstract
        print '\n\nBRIEF DESCRIPTION OF THE DRAWINGS\n\n'
        for illustration in self.illustrations:
            print illustration

        print "\n\nDETAILED DESCRIPTION OF THE PREFERRED EMBODIMENTS\n\nThe detailed description set forth below in connection with the appended drawings is intended as a description of presently-preferred embodiments of the invention and is not intended to represent the only forms in which the present invention may be constructed or utilized. The description sets forth the functions and the sequence of steps for using the invention in connection with the illustrated embodiments. However, it is to be understood that the same or equivalent functions and sequences may be accomplished by different embodiments that are also intended to be encompassed within the spirit and scope of the invention."
        print "\n"

        print self.description

        #print self.first_line + ' comprising: '
        #for line in self.body:
            #print line


    def make_name_one(self):
        title_combos = search.hypernym_combo(text, 'instrumentality', 'JJ NP')
        title_combos = [t for t in title_combos if t.endswith('round') == False]
        #for t in title_combos:
            #print t
        title = random.choice(title_combos)
        return title

    def specific_title(self, title):
        words = title.split()
        for i in range(len(words)):
            word = words[i]
            new_word = search.random_hyponym(word)
            if len(new_word) > 0:
                words[i] = new_word
        return ' '.join(words)



text = sys.stdin.read()

invention = Invention(text)
#invention.sentence_walk()
invention.format()
#print invention.make_name_one()
#print invention.title
#print invention.nouns
#print invention.first_line
#print invention.make_name_one()

#'material', 'fastener'

#artifacts are non-person things'

# the person is the invention?
