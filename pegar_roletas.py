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
        tm(5)
        
        frame = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/main/div[1]/iframe')

        self.driver.switch_to_frame(frame)

        url = self.driver.find_element_by_id('gamecontent').get_attribute('src')

        self.driver.get(url)

        
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
        tm(5)
    def get_roulete(self,path):
        

        text =str(self.driver.page_source)
        open('teste.txt','w').write(text)


        name_aux = text.split('class="lobby-table__name-container" data-theme="tableNamesColor_color">')
        get_nums_aux = text.split('class="lobby-table__features"><div class="lobby-table-features"></div>')
        area_numbs = []
        text_final = ''
        final_text = ''
        last_item = ''
        numbs = []
        colors = []
        
        name_final = []
        for i in range(1,len(name_aux)):
            
            name_final.append(name_aux[i].split('</div>')[0])
            area_numbs.append(get_nums_aux[i].split('class="lobby-table__name-container" data-theme="tableNamesColor_color">')[0])
        
        for i in range(len(area_numbs)):
            aux = area_numbs[i].split('class="lobby-table-rol-round-result__item-number">')
            for au in aux:
                numero = au.split('</')[0]
                if len(numero) >0:
                    numbs.append(au.split('</')[0])
                    
            aux = area_numbs[i].split('class="lobby-table-rol-round-result__item lobby-table-rol-round-result__item_') 
        

            for au in aux:
                
                color = au
                
                if color.find('red') != -1:
                    colors.append('red')
                if color.find('black') != -1:
                    colors.append('black')
                if color.find('green') != -1:
                    colors.append('green')
            text_final =''
            print(len(colors))
            print(len(numbs))
            for k in range(0,12):

                if len(text_final) == 0:
                    text_final = numbs[k]+','+colors[k]
                else:
                    text_final = text_final+'\n'+numbs[k]+','+colors[k]
            colors =[]
            numbs = []
            open(path+name_final[i]+'.txt','w').write(text_final)
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
