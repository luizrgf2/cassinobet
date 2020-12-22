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
    def check_padroes(self):
        
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
                



                cursor.execute(f'SELECT value FROM roletas WHERE name="{names[i]}"')

                value_actual = str(cursor.fetchall())
                value_actual = value_actual[3:len(value_actual)-4]
                print(value_actual)
                if value_actual != 'None':
                    print(nums[i], value_actual, len(nums[i]), len(value_actual))
                    if nums[i].find(value_actual) == -1 :
                        

                        cursor.execute(f'UPDATE roletas SET value="{nums[i]}" WHERE name="{names[i]}"')
                        conec.commit()
                        cursor.close()
                        conec.close()

                    else:
                        cursor.execute(f'UPDATE roletas SET value="None" WHERE name="{names[i]}"')
                        conec.commit()
                        cursor.close()
                        conec.close()
                
            
    def alternada(self,giro:int):

         while True:

            
            names = self.get_names()

            for name in names:

                self.cursor.execute(f'SELECT value FROM roletas WHERE name="{name}"')

                value = str(self.cursor.fetchall())

                value = value[3:len(value)-4]

                if value != 'None':

                    
                    self.cursor.execute(f'SELECT roleta FROM roletas WHERE name="{name}"')
                    roleta = str(self.cursor.fetchall())
                    roleta = roleta[3:len(roleta)-4]
                    rolete_final = ''
                    if roleta == 'None':
                        rolete_final = value
                    else:
                        rolete_final = roleta+','+value
                    self.cursor.execute(f"UPDATE roletas SET roleta='{rolete_final}' WHERE name='{name}'")
                
                    self.conec.commit()

                    self.cursor.execute(f'SELECT roleta FROM roletas WHERE name="{name}"')
                    

                    tm(0.3)            
    def init(self):

        self.entry_roletes()

        _thread.start_new_thread(self.check_padroes,())
        _thread.start_new_thread(self.detele_values,())

        self.alternada(15)
    def detele_values(self):

        names = self.get_names()
        conec = sqlite3.connect('roletas.db')
        cursor = conec.cursor()

        for name in names:
            cursor.execute(f'SELECT roleta FROM roletas WHERE name="{name}"')
            roleta = str(cursor.fetchall())
            roleta = roleta[2:len(roleta)-3]

            if roleta.find('None') == -1:


                tamanho = len(roleta.split(','))-1

                if tamanho >=20:

            
                    cursor.execute(f'UPDATE roletas SET roleta=Null WHERE name="{name}"')
                    conec.commit()
        





tete = Roll('luizrgfg',True)
tete.init()




            

        
        
        

        
        

        
           

        
        
            
            

                
rol = Roll('luizrgfg',True)
rol.entry_roletes()
rol.check_padroes()
