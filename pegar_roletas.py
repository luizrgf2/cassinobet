from sqlite3.dbapi2 import Cursor
from selenium import webdriver
import pickle
import os
from selenium.webdriver.common.keys import Keys
import json
import undetected_chromedriver
from time import sleep as tm
import sqlite3
import _thread

class Roll():
    
    def __init__(self,user:str,visible:bool):
        
        import platform

        self.conec = sqlite3.connect('roletas.db')
        self.cursor = self.conec.cursor()
        
        path = ''
        sistema = platform.system()
        undetected_chromedriver.install()
        self.path = os.getcwd()+self.barra()+user
        self.user = user
        
        if sistema == 'Linux':
            path = os.getcwd()+self.barra()+'chromedriver'
        else:
            path = os.getcwd()+self.barra()+'chromedriver.exe'
        
        options = webdriver.ChromeOptions()
        if visible == False:
            
            options.add_argument("--headless")
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        
        self.driver = webdriver.Chrome(executable_path=path,chrome_options=options)
        
        self.driver.get('https://casino.bet365.com/home')
        
        cookies = pickle.load(open(os.getcwd()+self.barra()+user+self.barra()+'cookie.pkl','rb'))
        
        for cookie in cookies:
            
            self.driver.add_cookie(cookie)
        self.driver.get('https://casino.bet365.com/Play/LiveRoulette')

        self.cursor.execute(f'UPDATE roletas SET alternada=Null')
        self.cursor.execute(f'UPDATE roletas SET dalternada=Null')
        self.cursor.execute(f'UPDATE roletas SET talternada=Null')
        self.cursor.execute(f'UPDATE roletas SET bunico=Null')
        self.cursor.execute(f'UPDATE roletas SET balternada=Null')
        self.cursor.execute(f'UPDATE roletas SET bduplo=Null')
        self.conec.commit()
        tm(1)
        
        
    def barra(self):
        
        import platform
        
        sistema = platform.system()
        
        if sistema == 'Linux':
            return '/'
        else:
            return '\\'
    def entry_roletes(self):
        tm(10)
        
        link = ''
        
        while True:
            try:
                self.driver.switch_to_frame(self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/main/div[1]/iframe'))
                link = self.driver.find_element_by_id('gamecontent').get_attribute('src')
                break
            except Exception as e:
                print(e)
        
        self.driver.get(link)
        
        tm(3)
        
        
        element = None
        
            
        while True:
            
            try:
                element = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/ul/li[1]')
                break
            except:
                print()   
        tm(3)
        element.click()
        tm(1)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div[4]/div/div/div[1]/div/div/ul[1]/li[1]/span').click()
        tm(10)
    def get_names(self):

        text = str(self.driver.page_source)
        
        
        corte_principal_name = text.split('class="lobby-table__name-container"')
        corte_principal_name.pop(0)
        names = []
        
        
        for i in range(len(corte_principal_name)):
            
            names.append(corte_principal_name[i].split('">')[1].split('</div><div')[0])



        
        
        return names
    def check_updates_in_roletes(self):
        
        conec = sqlite3.connect('roletas.db') #abrindo banco de dados para ler in inserir novas informaçoes
        cursor = conec.cursor()
        while True:
            text = str(self.driver.page_source) #pegando html da roleta
            
            corte_principal = text.split('lobby-table-rol-round-result__container"><div') #separando onde estao os ultimos numeros
            corte_principal.pop(0)
           
            
                
            names = self.get_names()
              
            for i in range(len(corte_principal)):

                
                name = names[i]

                num_atual = str(corte_principal[i].split('item-number">')[1].split('</')[0])+' '+str(corte_principal[i].split('lobby-table-rol-round-result__item_')[1].split('">')[0])
                

                cursor.execute(f'SELECT alternada, dalternada, talternada, bunico, balternada, bduplo FROM roletas WHERE name="{name}"')
                
                dados = cursor.fetchone()
                
                alternada = dados[0]
                
                dalternada = dados[1]
                
                talternada = dados[2]
                
                bunico = dados[3]
                
                balternada = dados[4]
                
                bduplo = dados[5]
                

                


                if alternada == None:

                    
                    cursor.execute(f'UPDATE roletas SET alternada="{num_atual}" WHERE name="{name}"')
                    conec.commit()

                else:

                    numero = alternada.split(',')[-1]
                    if numero != num_atual:
                        insert = alternada+','+num_atual
                        cursor.execute(f'UPDATE roletas SET alternada="{insert}" WHERE name="{name}"')
                        conec.commit()

                if dalternada == None:

                    cursor.execute(f'UPDATE roletas SET dalternada="{num_atual}" WHERE name="{name}"')
                    conec.commit()
                else:

                    numero = dalternada.split(',')[-1]
                    if numero != num_atual:
                        insert = dalternada+','+num_atual
                        cursor.execute(f'UPDATE roletas SET dalternada="{insert}" WHERE name="{name}"')
                        conec.commit()

                
                if talternada == None:
                    cursor.execute(f'UPDATE roletas SET talternada="{num_atual}" WHERE name="{name}"')
                    conec.commit()
                else:

                    numero = talternada.split(',')[-1]
                    if numero != num_atual:
                        insert = talternada+','+num_atual
                        cursor.execute(f'UPDATE roletas SET talternada="{insert}" WHERE name="{name}"')
                        conec.commit()

                
                if bunico == None:

                    cursor.execute(f'UPDATE roletas SET bunico="{num_atual}" WHERE name="{name}"')
                    conec.commit()
                else:

                    numero = bunico.split(',')[-1]
                    if numero != num_atual:
                        
                        insert = bunico+','+num_atual
                        cursor.execute(f'UPDATE roletas SET bunico="{insert}" WHERE name="{name}"')
                        conec.commit()

                
                if balternada == None:

                    cursor.execute(f'UPDATE roletas SET balternada="{num_atual}" WHERE name="{name}"')
                    conec.commit()
                else:

                    numero = balternada.split(',')[-1]
                    if numero != num_atual:
                        
                        insert = balternada+','+num_atual
                        cursor.execute(f'UPDATE roletas SET balternada="{insert}" WHERE name="{name}"')
                        conec.commit()

                
                
                if bduplo == None:

                    cursor.execute(f'UPDATE roletas SET bduplo="{num_atual}" WHERE name="{name}"')
                    conec.commit()
                else:

                    numero = bduplo.split(',')[-1]
                    
                    if numero != num_atual:
                        
                        insert = bduplo+','+num_atual
                        cursor.execute(f'UPDATE roletas SET bduplo="{insert}" WHERE name="{name}"')
                        conec.commit() 
                tm(1)     
    def detele_values(self):

        names = self.get_names()
        conec = sqlite3.connect('roletas.db')
        cursor = conec.cursor()
        while True:
            for name in names:
                cursor.execute(f'SELECT roleta FROM roletas WHERE name="{name}"')
                roleta = str(cursor.fetchall())
                roleta = roleta[2:len(roleta)-3]

                if roleta.find('None') == -1:


                    tamanho = len(roleta.split(','))-1

                    if tamanho >=20:

                
                        cursor.execute(f'UPDATE roletas SET roleta=Null WHERE name="{name}"')
                        conec.commit()
    def alternada(self,giro):
        tm(4)
        conec = sqlite3.connect('roletas.db')
        cursor = conec.cursor()
        names = self.get_names()
        


        while True:
            for name in names:

                cursor.execute(f'SELECT alternada FROM roletas WHERE name="{name}"')
                roleta = cursor.fetchone()[0]
                alternada_encontrado = True
                print('Alternada('+name+')',roleta)
                if roleta != None:

                    roll = roleta.split(',')

                    if len(roll) >=giro -1:

                        for i in range(giro-1):
                            print(roll[i])
                            if i%2 == 0:

                                if roll[i].find('black') == -1:

                                    alternada_encontrado = False

                            if i%2 !=0:

                                if roll[i].find('red') == -1:

                                    alternada_encontrado = False


                        cursor.execute(f'UPDATE roletas SET alternada=Null WHERE name="{name}"')
                        conec.commit()
                        if alternada_encontrado == True:
                            open('alternada.txt','w',encoding='utf8').write(name)
    def init(self):

        self.entry_roletes()
        _thread.start_new_thread(self.check_updates_in_roletes,())
        _thread.start_new_thread(self.alternada,())

        while True:
            print()
    

        
    




tete = Roll('luizrgfg',True)
tete.init()
