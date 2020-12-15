from selenium import webdriver
import pickle
import os
from selenium.webdriver.common.keys import Keys
import json
import undetected_chromedriver
from time import sleep as tm

class Roll():
    
    def __init__(self,user:str,visible:bool,driver:webdriver):
        
        import platform
        
        path = ''
        
        self.path = os.getcwd()+self.barra()+user
        self.user = user
        
        self.driver = driver
        
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
    def get_roulete(self,name_roulete:str,path:str):
        
        num_roletes = len(self.driver.find_elements_by_class_name('lobby-tables__item'))
        names_roletes = self.driver.find_elements_by_class_name('lobby-table__name-container')
        numbers_of_roulete = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')
        
        
        roulete = []
        digits = []
        for i in range(num_roletes):
            
            if names_roletes[i].text == name_roulete:
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
                        file_reader = open(path+name+'.txt','r').read()
                    except:
                        print()
                    
                    if len(file_reader) == 0:
                        file_reader = str(number)+','+color
                    else:
                        file_reader = file_reader+'\n'+str(number)+','+color
                    
                    open(path+name+'.txt','w').write(file_reader)           

                    

        
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
    def get_name_roletes(self):
        tm(10)
        names = self.driver.find_elements_by_class_name('lobby-table__name-container')
        text_final = ''
        for name in names:
            if len(text_final) == 0:
                text_final = name.text
            else:
                text_final = text_final+'\n'+name.text
        print(text_final.split('\n'))
        return text_final.split('\n')
