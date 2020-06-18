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
        self.link = "https://gartic.com.br"
        options = webdriver.ChromeOptions()
        options.add_argument('lang=pt-br')
        options.add_argument('no-sandbox')
        options.add_argument('start-maximized')
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe', chrome_options=options)
        
    def getPagina(self):
        self.driver.get(self.link)         
        print("Página " + self.link + " carregada!")

    def jogar(self):
        while True:
            palavra = input("Informe a palavra: ")
            self.interarJogo(palavra)
            try:
                vet = self.scraping(palavra)
                self.imprimirSinonimos(vet, palavra)
            except WebDriverException as erro:
                print("Erro - : ", erro)
            if(vet != "404"):
                try:
                    for sinonimo in vet:
                        self.interarJogo(sinonimo)
                        time.sleep(0.5)
                except KeyboardInterrupt: 
                    pass
            else:
                print("Erro - 404")
                
    def interarJogo(self, palavra):
        try:
            campo_resposta = self.driver.find_element_by_xpath('//*[@id="respostas"]/form/label/input')
            campo_resposta.click()
            campo_resposta.clear()
            campo_resposta.send_keys(palavra)
            campo_resposta.send_keys(Keys.ENTER)
        except WebDriverException:
            print("Acertou ou intervalo")
        
        
    def scraping(self, palavra):
        scraper = getSinonimos()
        return scraper.getSinonimo(scraper.getPagina(palavra))
    
    def imprimirSinonimos(self, vet, palavra):
        if(vet != "404"):
            print("Sinonimos de: "+ red(palavra,['bold']))
            for sinonimo in vet:
                print (sinonimo)
        else:
            print("Erro - 404")
        


bot = garticBOT()
bot.getPagina()
bot.jogar()