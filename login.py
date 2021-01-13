from selenium import webdriver
import pickle
import os
from selenium.webdriver.common.keys import Keys
import json
import undetected_chromedriver
from time import sleep as tm

class Login():
    
    def __init__(self,visible:bool,user:str,password:str,driver:webdriver):
        import platform
        

        self.path = os.getcwd()+self.barra()+user
        self.user = user
        self.password = password
        self.driver = driver
        self.driver.get('https://casino.bet365.com/home')              
    def barra(self):
        
        import platform
        
        sistema = platform.system()
        
        if sistema == 'Linux':
            return '/'
        else:
            return '\\'
    def login(self):
        

            
        
        while True:
            
            try:
                self.driver.find_element_by_xpath('/html/body/div[2]/div[4]/header/div/div[2]/div[4]/div[2]/button').click()
                break
            except:            
                self.driver.find_element_by_xpath('/html/body/div[2]/div[4]/header/div/div[2]/div[4]/div[2]/button').click()
                break
        tm(1)
        self.driver.find_element_by_id('txtUsername').send_keys(self.user)
        self.driver.find_element_by_id('txtPassword').send_keys(self.password)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[4]/header/div/div[3]/div/form/button').click()
        tm(10)
                
        try:
            self.driver.find_element_by_xpath('/html/body/div[2]/div[4]/header/div/div[2]/div[4]/div[2]/button')
            return 'falha'
        except:
            return 'sucesso'
        
