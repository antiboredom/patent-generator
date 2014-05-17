import os
import sys
import subprocess
import shlex
from machine import *

class pdfCreator():

    # declare and define all variables in the constructor
    def __init__(self,dn,fn,inv):
        self.invention = inv
        self.file = self.create_TeX_file(dn,fn)
        self.title = self.create_title()
        self.abstract = self.create_abstract()
        self.illustrations = self.create_illustrations()
        self.description = self.create_description()
        self.claims = self.create_claims()
        self.file_contents = self.create_LaTeX()

    # used to open a new folder and open appropriate file
    def create_TeX_file(self,dname,fname):

        if not os.path.exists(dname):
            os.makedirs(dname)

        return open(dname + "/" + fname + ".tex","a+")

    # assemble the full LaTeX text
    def create_LaTeX(self):
        text = "\\documentclass[english]{uspatent}\n\\begin{document}"
        
        text += self.title
        
        text += self.abstract

        text += self.illustrations

        text += self.description

        text += self.claims

        text += "\n\\end{document}"

        return text

    # assemble the title featuers
    def create_title(self):
        title = "\n\\title{" + self.invention.title + "}"
        title += "\n\\date{\\today}"
        title += "\n\\inventor{First Named Inventor}"
        title += "\n\\maketitle"

        return title

    # put the abstract together
    def create_abstract(self):
        abs = "\n\\patentSection{Abstract}"
        abs += "\n\\patentParagraph " + self.invention.abstract

        return abs

    # collect image descriptions
    def create_illustrations(self):
        ill = "\n\\patentSection{Brief Description of the Drawings}"
        for i in self.invention.illustrations:
                    # seperate paragraph for each, maybe not necessary
            ill += "\n\\patentParagraph " + i

        return ill

    # put description together
    def create_description(self):
        desc = "\n\\patentSection{Detailed Description of the Preferred Embodiments}"
        desc += "\n\\patentParagraph " + self.invention.description

        return desc

    # assemble the claims together
    def create_claims(self):
        cla = "\n\\patentClaimsStart"
        
        for i,claim in enumerate(self.invention.claims):
            cla += "\n\\beginClaim{Claim" + str(i) + "}" + claim[2:]

        cla += "\n\\patentClaimsEnd"

        return cla

    # write the entire text to the file
    def write_LaTeX_to_file(self):
                                            # to fix paragraph formatting
        self.file.write(self.file_contents.replace("\n\n","\n\\patentParagraph "))

    # function to compile the LaTeX formatting, not working yet
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



