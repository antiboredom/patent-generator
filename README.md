Patent Generator
================

Transforms literary/philosophical texts into patent applications.

Read the blog post here: http://lav.io/2014/05/transform-any-text-into-a-patent-application/


### Repository Contents
* "machine.py" generates patents
* "search.py" searches texts for parts of speech and hypernym combinations (among other things)
* "get_illustrations.py" scrapes Bing for patent illustrations
* "scraper.py" downloads the full text of patent applications based on keywords
* "latex_pdf.py" generates a pdf file using pdflatex and the uspatent package

### Dependencies
The script requires [pattern](https://github.com/clips/pattern). If you have pip installed, just run:
```
pip install pattern
```


### Using it
To run the patent generator:
```
python machine.py < text.txt
```

To generate a patent:
```
python latex_pdf.py text.txt directory-to-store-file pdfname
```
