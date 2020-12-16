from selenium import webdriver
import pickle
import os
from selenium.webdriver.common.keys import Keys
import json
import undetected_chromedriver
from time import sleep as tm
from login import Login
from pegar_roletas import Roll
import _thread
import platform

def barra():
        
    
        
    sistema = platform.system()
        
    if sistema == 'Linux':
        return '/'
    else:
        return '\\'
def webdriver_complete(visible:bool):
    sistema = platform.system()
    undetected_chromedriver.install()
        
    if sistema == 'Linux':
        path = os.getcwd()+barra()+'chromedriver'
    else:
        path = os.getcwd()+barra()+'chromedriver.exe'
        
    options = webdriver.ChromeOptions()
    if visible == False:
            
        options.add_argument("--headless")
    options.add_argument('ignore-certificate-errors')
    options.add_argument('--no-sandbox')
        
    driver = webdriver.Chrome(executable_path=path,chrome_options=options)
    return driver  
def get_roulete(name_roulete:str,driver:webdriver,path:str):
        
    num_roletes = len(driver.find_elements_by_class_name('lobby-tables__item'))
    names_roletes = driver.find_elements_by_class_name('lobby-table__name-container')
    numbers_of_roulete = driver.find_elements_by_class_name('lobby-table-rol-round-result__container')
        
    open('teste.txt','w').write(str(driver.page_source))
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
def init(visible:bool,user:str,password:str):
    driver = webdriver_complete(True)
    login = Login(visible,user,password,driver)
    login.login()
    path = os.getcwd()+barra()+'roletas'+barra()
    
    roll = Roll(user,visible,driver)
    roll.entry_roletes()
    
    
    roll.get_roulete(path)


                

        
init(True,'luizrgfg','Mano010599')
    
    
