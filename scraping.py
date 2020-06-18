# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 08:50:00 2020

@author: Dalvan
"""


from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError

import unicodedata
import re

from simple_colors import blue

class getSinonimos:
    def __init__ (self):
        self.link= "https://www.sinonimos.com.br"
        
    def getPagina(self, palavra):
        try:
            url=self.link +"/"+ self.removerAcentosECaracteresEspeciais(palavra)+"/"
            html = urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            print("Link: "+ blue(url))
            return soup
        except URLError:
            print("Link: "+ blue(url))
            return None

    def getSinonimo(self, pagina):
        if(pagina != None):
            tags = pagina.find_all("a", class_="sinonimo")
            vetorSinonimos = []
            for tag in tags:
                vetorSinonimos.append(tag.getText())
            return vetorSinonimos
        else:
            return "404"
        
    def removerAcentosECaracteresEspeciais(self, palavra):
        palavra = palavra.replace(" ", "")
        nfkd = unicodedata.normalize('NFKD', palavra)
        palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
        return re.sub('[^a-zA-Z0-9- \\\]', '', palavraSemAcento)
