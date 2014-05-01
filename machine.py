import search
import sys, random
from pattern.en import tag

#text = sys.stdin.read()

# a [adjective] [specific noun] [(optional device/invention/machine)] that [something a character does something in the story]

#try lolita
#melville

class Invention(object):
    def __init__(self, text):
        self.source_text = text
        self.title = self.create_gerund_title()
        self.create_first_line()
        self.find_lines()

    def prefix(self):
        prefixes = ["system", "method", "apparatus", "device"]
        title = random.choice(prefixes)
        prefixes.remove(title)
        title += " and " + random.choice(prefixes) + " for "
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
                'VBG * NN', 'VBG * JJ *? NP NP?']

        gerund_phrases = search.search(text, search_patterns[-1])
        self.possible_titles = []
        for title in gerund_phrases:
            self.possible_titles.append(title)
            #print self.prefix() + title
        partial_title = random.choice(self.possible_titles)
        title = self.prefix() + partial_title
        self.set_keywords(partial_title)
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
        if random.random() < .1:
            template = 'The present invention relates generally to the field of {0} and, more specifically, to methods and apparatus to {1} {2}.'

    def find_lines(self):
        lines = search.search(self.source_text, '|'.join(self.nouns + self.verbs + self.adjectives))
        print lines

    def make_name_one(self):
        title_combos = search.hypernym_combo(text, 'instrumentality', 'JJ NN')
        title = random.choice(title_combos)
        #print title
        words = title.split()
        for i in range(len(words)):
            word = words[i]
            #if tag(word)[0][1] in ['NN', 'NNP']:
            new_word = search.random_hyponym(word)
            if len(new_word) > 0:
                words[i] = new_word
        return ' '.join(words)

        #for title in title_combos:
            #words = title.split()
            #for i in range(len(words)):
                #word = words[i]
                #if tag(word)[0][1] in ['NN', 'NNP']:
                    #words[i] = search.random_hyponym(word)




text = sys.stdin.read()

invention = Invention(text)
print invention.title
print invention.first_line
#print invention.make_name_one()
