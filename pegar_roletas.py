from selenium import webdriver
import pickle
import os
from selenium.webdriver.common.keys import Keys
import json
import undetected_chromedriver
from time import sleep as tm

class Roll():
    
    def __init__(self,user:str,visible:bool):
        
        import platform
        
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
        self.driver.get('https://casino.bet365.com/home')
        tm(10)
        self.confirm_ident()      
    def barra(self):
        
        import platform
        
        sistema = platform.system()
        
        if sistema == 'Linux':
            return '/'
        else:
            return '\\'
    def entry_roletes(self):
        self.driver.get('https://casino.bet365.com/Play/LiveRoulette')
        tm(10)
        
        
        link = 'https://dl-com.c365play.com/casinoclient.html?game=rol&preferedmode=real&language=en&cashierdomain=www.sgla365.com&ngm=1&wmode=opaque&gametableid=1021&tableid=1021'
        
        self.driver.get(link)
        
        tm(3)
        
        
        element = None
        
            
        tm(30)        
        element = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/ul/li[1]')
               

        element.click()
        tm(1)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div[4]/div/div/div[1]/div/div/ul[1]/li[1]/span').click()
        tm(1)
    def get_roulete(self,name_roulete:str):
        num_roletes = len(self.driver.find_elements_by_class_name('lobby-tables__item'))
        names_roletes = self.driver.find_elements_by_class_name('lobby-table__name-container')
        numbers_of_roulete = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')
        
        tm(5)
        roulete = []
        digits = []
        for i in range(num_roletes):
            if names_roletes[i].text.find(name_roulete) != -1:
                name = names_roletes[i].text
                color = ''
                number = 0
                numeros = numbers_of_roulete[i].find_elements_by_class_name('lobby-table-rol-round-result__item-number')
                
                for numero in numeros:
                    number = int(numero.text)
                    color = numero.find_element_by_xpath('./..').get_attribute('class')
                    print
                    if color.find('red') != -1:
                        color = 'red'
                    elif color.find('black') != -1:
                        color='black'
                    else:
                        color = 'green'
                    print(name,color,number)
                    file_reader = ''
                    try:
                        file_reader = open(name+'.txt','r').read()
                    except:
                        print()
                    
                    if len(file_reader) == 0:
                        file_reader = str(number)+','+color
                    else:
                        file_reader = file_reader+'\n'+str(number)+','+color
                    
                    open(name+'.txt','w').write(file_reader)           
        try:
            file_reader = open(name+'.txt','r').read()
            file_reader = file_reader+'\n'+'exit'
            open(name+'.txt','w').write(file_reader)   
        except:
            print('Não foi encntrada a roleta!')
                    

        
                #digits.append({'name':name_rolete[i],'color':color,'number':base.find_element_by_class_name('lobby-table-rol-round-result__item-number')})
    def confirm_ident(self):
        
        try:
            self.driver.find_element_by_id('remindLater').click()                                
        except Exception as e:
            print(e)
        try:
            self.driver.find_element_by_class_name('regulatory-last-login-modal__button').click()
        except Exception as e:
            print(e)
rol = Roll('luizrgfg',True)
rol.entry_roletes()
rol.get_roulete('bet365 Premium Roulette')