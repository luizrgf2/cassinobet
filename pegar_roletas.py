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
    def get_rouletes(self):
        num_roletes = len(self.driver.find_elements_by_class_name('lobby-tables__item'))
        tm(5)
        roulete = []
        digits = []

        
        for i in range(1,num_roletes+1):

            try:
                name_rolete = self.driver.find_element_by_xpath(f'/html/body/div[1]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div/div/div[{i}]/div/div/div[2]/div[5]/div[1]').text
            except:
                name_rolete = self.driver.find_element_by_xpath(f'/html/body/div[1]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div/div/div[{i}]/div/div/div[3]/div[5]/div[1]').text
            color = ''
            for k in range(1,13):
                
                base = None
                try:
                    base = self.driver.find_element_by_xpath(f'/html/body/div[1]/div/div[3]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div[{i}]/div/div/div[2]/div[4]/div/div[{k}]')
                except:
                                                                                /html/body/div[1]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/div/div[3]/div[4]/div/div[11]
                                                            /html/body/div[1]/div/div[3]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div[1]/div/div/div[2]/div[4]/div/div[9]
                                                            /html/body/div[1]/div/div[3]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div[1]/div/div/div[2]/div[4]/div/div[5]
                                                            /html/body/div[1]/div/div[3]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div[1]/div/div/div[2]/div[4]/div/div[11]
                color = base.get_attribute('class')
                if color.find('red') != -1:
                    color = 'red'
                elif color.find('black') != -1:
                    color = 'black'
                else:
                    color = 'green'
                print(name_rolete[i],color)
                #digits.append({'name':name_rolete[i],'color':color,'number':base.find_element_by_class_name('lobby-table-rol-round-result__item-number')})
                                             
                
rol = Roll('luizrgfg',True)
rol.entry_roletes()
rol.get_rouletes()