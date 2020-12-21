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
        
        text = str(self.driver.page_source)
        open('tete.txt','w').write(text)
        corte_principal = text.split('lobby-table-rol-round-result__container"><div')
        corte_principal.pop(0)
        nums = []
        
        
        
            
            
        
        for i in range(len(corte_principal)):
            
            nums.append(str(corte_principal[i].split('item-number">')[1].split('</')[0])+' '+str(corte_principal[i].split('lobby-table-rol-round-result__item_')[1].split('">')[0]))
        print(nums)
        
    def alternada(self,item:str):
        
        
        
        
        
        

        
        

        
           

        
        
            
            

                
rol = Roll('luizrgfg',True)
rol.entry_roletes()
rol.check_padroes(14)

