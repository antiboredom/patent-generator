import sys, random
import machine
from pattern.en import tag
from pattern.web import Bing, SEARCH, IMAGE, URL, extension

def save_image(url, figure):
    url = URL(url)
    f = open('illustrations/' + figure + extension(url.page), 'wb')
    f.write(url.download())
    f.close()


text = sys.stdin.read()
invention = machine.Invention(text)
engine = Bing(license=None)

#the following searches for patent illustrations on bing, using a generated noun from each description of the illustration
#search_base = "patent illustration "
#for i, illustration in enumerate(invention.unformatted_illustrations):
    #nouns = [word for word, pos in tag(illustration) if pos == 'NN']
    #if len(nouns) > 0:
        #search_string = search_base + random.choice(nouns)#' '.join(nouns) 
        #print "searching for: " + search_string
        #for j, result in enumerate(engine.search(search_string, type=IMAGE, count=5)):
            #print "saving: " + result.url
            #try:
                #save_image(result.url, "fig_" + str(i+1) + "_" + str(j+1))
            #except:
                #next

# the following searches for "fig N patent illustration"
search_base = " patent illustration"
for i, illustration in enumerate(invention.unformatted_illustrations):
    search_string = 'fig ' + str(i+1) + search_base
    print "searching for: " + search_string
    for j, result in enumerate(engine.search(search_string, type=IMAGE, count=5)):
        print "saving: " + result.url
        try:
            save_image(result.url, "fig_" + str(i+1) + "_" + str(j+1))
        except:
            next
