import os
import sys
import subprocess
import shlex
from machine import *

class pdfCreator():

    def __init__(self,dn,fn,inv):
        self.invention = inv
        self.file = self.create_TeX_file(dn,fn)
        self.title = self.create_title()
        self.abstract = self.create_abstract()
        self.illustrations = self.create_illustrations()
        self.description = self.create_description()
        self.claims = self.create_claims()
        self.file_contents = self.create_LaTeX()

    def create_TeX_file(self,dname,fname):

        if not os.path.exists(dname):
            os.makedirs(dname)

        return open(dname + "/" + fname + ".tex","a+")

    def create_LaTeX(self):
        # write article class
        text = "\\documentclass[english]{uspatent}"
        # begin document
        text += "\n\\begin{document}"
        # make title
        text += self.title
            
        # make abstract section
        text += self.abstract

        # make drawings section
        text += self.illustrations

        # make embodiments section
        text += self.description

        # make claims section
        text += self.claims

        # end document
        text += "\n\\end{document}"

        return text

    def create_title(self):
        # title
        title = "\n\\title{" + self.invention.title + "}"
        # date
        title += "\n\\date{\\today}"
        # inventor
        title += "\n\\inventor{First Named Inventor}"
        # write the title
        title += "\n\\maketitle"

        return title

    def create_abstract(self):
        abs = "\n\\patentSection{Abstract}"
        abs += "\n\\patentParagraph " + self.invention.abstract

        return abs

    def create_illustrations(self):
        ill = "\n\\patentSection{Brief Description of the Drawings}"
        for i in self.invention.illustrations:
            ill += "\n\\patentParagraph " + i

        return ill

    def create_description(self):
        desc = "\n\\patentSection{Detailed Description of the Preferred Embodiments}"
        desc += "\n\\patentParagraph " + self.invention.description

        return desc

    def create_claims(self):
        cla = "\n\\patentClaimsStart"
        
        for i,claim in enumerate(self.invention.claims):
            cla += "\n\\beginClaim{Claim" + str(i) + "}" + claim[2:]

        cla += "\n\\patentClaimsEnd"

        return cla

    def write_LaTeX_to_file(self):
        self.file.write(self.file_contents.replace("\n\n","\n\\patentParagraph "))

    
            
    #def compile_LaTeX(self):
        #process = subprocess.call("pdflatex test/test.tex", shell=True)


if __name__ == '__main__':

    import sys

    text = open(sys.argv[1],"r").read().decode('ascii', errors='replace')
    dir_name = sys.argv[2]
    file_name = sys.argv[3]

    invention = Invention(text)

    pdf = pdfCreator(dir_name,file_name,invention)
    pdf.write_LaTeX_to_file()
    #pdf.compile_LaTeX()



