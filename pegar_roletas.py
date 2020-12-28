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
        open('tete.txt','w').write(text)
        
        corte_principal_name = text.split('class="lobby-table__name-container"')
        corte_principal_name.pop(0)
        names = []
        
        
        for i in range(len(corte_principal_name)):
            
            names.append(corte_principal_name[i].split('">')[1].split('</div><div')[0])



        
        
        return names
    def check_updates_in_roletes(self):
        
        while True:
            text = str(self.driver.page_source)
            open('tete.txt','w').write(text)
            corte_principal = text.split('lobby-table-rol-round-result__container"><div')
            corte_principal.pop(0)
            nums = []
            
            
            
                
            names = self.get_names()        
            for i in range(len(corte_principal)):
                
                nums.append(str(corte_principal[i].split('item-number">')[1].split('</')[0])+' '+str(corte_principal[i].split('lobby-table-rol-round-result__item_')[1].split('">')[0]))

                conec = sqlite3.connect('roletas.db')
                cursor = conec.cursor()
                




                    

                cursor.execute(f'UPDATE roletas SET value="{nums[i]}" WHERE name="{names[i]}"')
                conec.commit()
                
                    
                cursor.close()
                conec.close()
                tm(0.1)
            tm(3)
    def verify_updates(self,alternada:int,dalternada:int,talternada:int,bunico:int,balternada:int,bduplo:int):

        nomes = self.get_names()
        possibilidades = ['alternada','dalternada','talternada','bunico','balternada','bduplo']

        while True:

            for name in nomes:

                
                for possibilidade in possibilidades:

                    self.cursor.execute(f'SELECT value FROM roletas WHERE name="{name}"')
                    
                    value = ''
                    
                    try:
                        value = self.cursor.fetchone()[0]
                    except:
                        value = self.cursor.fetchone()

                    
                    
                    self.cursor.execute(f'SELECT {possibilidade} FROM roletas WHERE name="{name}"')
                    try:
                        roleta = self.cursor.fetchone()[0]
                    except:
                        roleta = self.cursor.fetchone()
                    
                    if roleta == None:

                        self.cursor.execute(f'UPDATE roletas SET {possibilidade}="{value}" WHERE name="{name}"')
                        self.conec.commit()
                    elif roleta.split(',')[-1] != value :
                        
                        resut = roleta+','+value

                        self.cursor.execute(f'UPDATE roletas SET {possibilidade}="{resut}" WHERE name="{name}"')
                        self.conec.commit()
                    #grupos de if para verificar os giros
                    if possibilidade == possibilidades[0]:
                        self.cursor.execute(f'SELECT {possibilidade} FROM roletas WHERE name="{name}"')
                        
                        try:
                            roleta = self.cursor.fetchone()[0]
                        except:
                            roleta = self.cursor.fetchone()
                        tamanho = alternada

                        if len(str(roleta).split(',')) == tamanho:
                             self.cursor.execute(f'UPDATE roletas SET {possibilidade}=Null')

                    elif possibilidade == possibilidades[1]:
                        self.cursor.execute(f'SELECT {possibilidade} FROM roletas WHERE name="{name}"')
                        
                        try:
                            roleta = self.cursor.fetchone()[0]
                        except:
                            roleta = self.cursor.fetchone()
                        tamanho = dalternada

                        if len(str(roleta).split(',')) == tamanho:
                             self.cursor.execute(f'UPDATE roletas SET {possibilidade}=Null')

                    elif possibilidade == possibilidades[2]:
                        self.cursor.execute(f'SELECT {possibilidade} FROM roletas WHERE name="{name}"')
                        
                        try:
                            roleta = self.cursor.fetchone()[0]
                        except:
                            roleta = self.cursor.fetchone()
                        tamanho = talternada

                        if len(str(roleta).split(',')) == tamanho:
                             self.cursor.execute(f'UPDATE roletas SET {possibilidade}=Null')

                    elif possibilidade == possibilidades[3]:
                        self.cursor.execute(f'SELECT {possibilidade} FROM roletas WHERE name="{name}"')
                        
                        try:
                            roleta = self.cursor.fetchone()[0]
                        except:
                            roleta = self.cursor.fetchone()
                        tamanho = bunico

                        if len(str(roleta).split(',')) == tamanho:
                             self.cursor.execute(f'UPDATE roletas SET {possibilidade}=Null')

                    elif possibilidade == possibilidades[4]:
                        self.cursor.execute(f'SELECT {possibilidade} FROM roletas WHERE name="{name}"')
                        
                        try:
                            roleta = self.cursor.fetchone()[0]
                        except:
                            roleta = self.cursor.fetchone()
                        tamanho = bduplo

                        if len(str(roleta).split(',')) == tamanho:
                             self.cursor.execute(f'UPDATE roletas SET {possibilidade}=Null')

                    elif possibilidade == possibilidades[5]:
                        self.cursor.execute(f'SELECT {possibilidade} FROM roletas WHERE name="{name}"')
                        
                        try:
                            roleta = self.cursor.fetchone()[0]
                        except:
                            roleta = self.cursor.fetchone()
                        tamanho = balternada

                        if len(str(roleta).split(',')) == tamanho:
                             self.cursor.execute(f'UPDATE roletas SET {possibilidade}=Null')
                

                    print(name,self.cursor.execute(f'SELECT {possibilidade} FROM roletas WHERE name="{name}"').fetchone())   
        tm(1.5)         
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
    def alternado(self,giros:int,name:str):
        
        
        controller = False
        conec = sqlite3.connect('roletas.db')
        cursor = conec.cursor()


        roleta = None
                
        try:
            roleta = cursor.execute(f'SELECT alternada FROM roletas WHERE name={name}').fetchone()[0]
        except:
            roleta = cursor.execute(f'SELECT alternada FROM roletas WHERE name={name}').fetchone()

        if roleta != None:
            numb = str(roleta).split(',')

            for i in range(len(numb)):

                if i%2 == 0:

                    if numb[i].find('black') == -1:
                        cursor.execute(f'UPDATE roletas SET alternada=Null WHERE name={name}')
                        conec.commit()
                        tm(0.2)
                        return None
                elif i%2 !=0:

                    if numb[i].find('red') == -1:
                        cursor.execute(f'UPDATE roletas SET alternada=Null WHERE name={name}')
                        conec.commit()
                        tm(0.2)
                        return None
                elif len(numb) == giros-1:
                    return name
    def init(self):

        self.entry_roletes()
        _thread.start_new_thread(self.check_updates_in_roletes,())
        
        


        self.verify_updates(4,12,12,12,12,12)




tete = Roll('luizrgfg',True)
tete.init()




            

        
        
        

        
        

        
           

        
        
            
            

                
rol = Roll('luizrgfg',True)
rol.entry_roletes()
rol.check_padroes()
