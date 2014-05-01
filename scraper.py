from pattern.web import URL, DOM, abs, plaintext
import urllib, sys, time, re

def get_patent_urls(keyword, limit=10):
    keyword = urllib.quote_plus(keyword);
    base_url = "http://www.lens.org"
    url = URL(base_url + "/lens/search?ft=true&l=en&st=true&n=" + str(limit) + "&q=" + keyword)
    dom = DOM(url.download())
    links = [base_url + a.attributes.get('href') for a in dom('a.link')]
    return links

def get_patent(url):
    url = URL(url + "/fulltext")
    html = url.download()
    dom = DOM(html)
    title = plaintext(dom('h3 a')[0].content)
    body = plaintext(dom('#contents')[0].content)
    return [title, body]

def download_patents(keyword, limit=10):
    urls = get_patent_urls(keyword, limit)
    time.sleep(.5)
    for url in urls:
        try:
            title, body = get_patent(url)
            body = title + "\n\n" + body
            file_title = re.sub(r'\W', "_", title)
            with open('patents/' + file_title.lower() + '.txt', 'w') as f:
                f.write(body.encode('utf8'))
            time.sleep(.5)
        except(IndexError):
            continue

for line in sys.stdin:
    download_patents(line.strip())
