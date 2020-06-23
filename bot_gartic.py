# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 08:27:18 2020

@author: Dalvan
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scraping import getSinonimos
from selenium.common.exceptions import WebDriverException
import time

from simple_colors import red

class garticBOT:
    def __init__(self):
        self.dicas = {}
        self.sinonimos=[]
        self.link = "https://gartic.com.br"
        
        
    def getPagina(self):
        options = webdriver.ChromeOptions()
        options.add_argument('lang=pt-br')
        options.add_argument('no-sandbox')
        options.add_argument('start-maximized')
        #options.add_argument("user-data-dir=C:/Users/Dalvan/AppData/Local/Google/Chrome/User Data") #diretório com dados do usuário
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe', options=options)
        self.driver.get(self.link)         
        print("Página " + self.link + " carregada!")

    def jogar(self):
        while True:
            palavra = input("Informe a palavra: ")
            try:                
                self.interarJogo(palavra)
                self.dicas={}
                self.sinonimos=[]
                self.getDicas()
                self.sinonimos = self.scraping(palavra)
                self.aplicarDicas()
                print(red("Sinônimos possíveis"))                
                self.imprimirSinonimos(palavra)
            except WebDriverException as erro:
                print("Erro - : ", erro)
                pass
            if(self.sinonimos != "404"):
                try:
                    for sinonimo in self.sinonimos:
                        if(self.interarJogo(sinonimo) =="fim da rodada"):
                            break
                except KeyboardInterrupt: 
                    pass
           
                
    def interarJogo(self, palavra):
        try:
            campo_resposta = self.driver.find_element_by_xpath('//*[@id="respostas"]/form/label/input')
            campo_resposta.click()
            campo_resposta.clear()
            campo_resposta.send_keys(palavra)
            campo_resposta.send_keys(Keys.ENTER)
            time.sleep(0.6)
        except WebDriverException:
            print("Acertou ou intervalo")
            return "fim da rodada"
    
    def getDicas(self):
        #verifica se tem dica
        numDicas = self.driver.find_element_by_xpath('//*[@id="dica"]/div[1]/h2').text
        if(len(numDicas) > 4):
            self.dicas["num"]=int((numDicas[6]+numDicas[7]).replace(" ",""))
            elementos = self.driver.find_elements_by_xpath('.//span[@class = "traco ativo"] | .//span[@class = "espaco"]')
            for index, letra in enumerate(elementos):
                if(letra.text != " "):
                    print(letra.text, " - ", index+1)
                    self.dicas[index+1]= letra.text.lower()
            print("Número de letras: ",self.dicas["num"])
            print("Dicas: ",self.dicas)
            
    def aplicarDicas(self):   
        if "num" in self.dicas: #avalia se tem dicas
            sinonimos = self.sinonimos
            num= int(self.dicas["num"]) #armazena o número de letras da palavra
            del self.dicas["num"] 
            #laço para remover todos sinônimos com número de letras diferente da dica
            filtrada = [] 
            for item in sinonimos:
                if len(item) == num :
                    filtrada.append(item)            
            #laço para marcar os sinônimos que não encaixam nas dicas
            #não remover diretamente, loop volta a tentar acessar posição excluída
            for index, item in enumerate(filtrada):
                for dica in self.dicas:
                    if item[dica-1] != self.dicas[dica]:
                        filtrada[index] = "!" # mark for filter          
            #filter dos sinônimos que não encaixam nas dicas
            filtrada2 = list(filter(lambda x: x!="!", filtrada))        
            self.sinonimos= filtrada2
        
    def scraping(self, palavra):
        scraper = getSinonimos()
        return scraper.getSinonimo(scraper.getPagina(palavra))
    
    def imprimirSinonimos(self, palavra):
        if(self.sinonimos != "404"):
            print("Sinônimos de: "+ red(palavra,['bold']))
            for sinonimo in self.sinonimos:
                print (sinonimo)
        else:
            print("Erro - 404")
        
    def encerrar(self):
        self.driver.quit()

bot = garticBOT()
bot.getPagina()
bot.jogar()

