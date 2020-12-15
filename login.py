from selenium import webdriver
import pickle
import os
from selenium.webdriver.common.keys import Keys
import json
import undetected_chromedriver
from time import sleep as tm

class Login():
    
    def __init__(self,visible:bool,user:str,password:str):
        import platform
        
        path = ''
        sistema = platform.system()
        undetected_chromedriver.install()
        self.path = os.getcwd()+self.barra()+user
        self.user = user
        self.password = password
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
    def barra(self):
        
        import platform
        
        sistema = platform.system()
        
        if sistema == 'Linux':
            return '/'
        else:
            return '\\'
    def login(self):
        
        local_path = os.path.isfile(self.path+self.barra()+'cookie.pkl')
        
        if local_path == False:
            
        
            while True:
                
                try:
                    self.driver.find_element_by_xpath('/html/body/div[2]/div[4]/header/div/div[2]/div[4]/div[2]/button').click()
                    break
                except Exception as e:            
                    self.driver.find_element_by_xpath('/html/body/div[2]/div[4]/header/div/div[2]/div[4]/div[2]/button').click()
                    break
            tm(1)
            self.driver.find_element_by_id('txtUsername').send_keys(self.user)
            self.driver.find_element_by_id('txtPassword').send_keys(self.password)
            self.driver.find_element_by_xpath('/html/body/div[2]/div[4]/header/div/div[3]/div/form/button').click()
            tm(5)
            directory = self.path
            
            if os.path.isdir(directory):
                print()
            else:
                os.mkdir(directory)
            
            pickle.dump(self.driver.get_cookies(),open(self.path+self.barra()+'cookie.pkl','wb'))        
        else:
            
            cookies = pickle.load(open(self.path+self.barra()+'cookie.pkl','rb'))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.get('https://casino.bet365.com/home')
            tm(5)
            try:
                
                self.driver.find_element_by_class_name('members-dropdown-component__members-icon-container')
            except:
                os.remove(self.path+self.barra()+'cookie.pkl')
                
        self.driver.close()
login = Login(True,'luizrgfg','Mano010599')
login.login()
        
        
                
        
        