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
from flask import Flask,request
from playsound import playsound


app = Flask('app')


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
@app.route('/iniciar',methods=['POST'])
def init():
    
    json_file = request.get_json()
    
    visible = json_file['visible']
    user = json_file['user']
    password = json_file['password']

    open('alternada.txt','w').truncate(0)
    open('dupla_alternada.txt','w').truncate(0)
    open('tripla_alternada.txt','w').truncate(0)
    open('bloco_unico.txt','w').truncate(0)
    open('bloco_alternada.txt','w').truncate(0)
    open('bloco_duplo.txt','w').truncate(0)

    try:
        driver = webdriver_complete(visible)
        login = Login(visible,user,password)
        login.login()
        
        roll = Roll(user,visible)
        roll.init()
        
        
        
        return 'Iniciado com sucesso'
    except Exception as e:
        return e
@app.route('/pegarinfo',methods=['GET'])
def pegar_infos():

    alternada_reader = ''
    dupla_alternada_reader = ''
    tripla_alternada_reader = ''
    bunico_reader = ''
    balternada_reaader = ''
    bduplo_reader = ''





    try:
        alternada_reader = open('alternada.txt','r').read()
    except:
        print('alternada.txt não encontrada!')
    
    try:
        dupla_alternada_reader = open('dupla_alternada.txt','r').read()
    except:
        print('dupla_alternada.txt não encontrada!')
    
    
    try:
        tripla_alternada_reader = open('tripla_alternada.txt','r').read()
    except:
        print('tripla_alternada.txt não encontrada!')

    try:
        bunico_reader = open('bloco_unico.txt','r').read()
    except:
        print('bloco_unico.txt não encontrada!')

    try:
        balternada_reaader = open('bloco_alternada.txt','r').read()
    except:
        print('bloco_alternada.txt não encontrada!')

    try:
        bduplo_reader = open('bloco_duplo.txt','r').read()
    except:
        print('bloco_duplo.txt não encontrada!')

    if len(alternada_reader) != 0:

        print(alternada_reader,'Altenada encontaada')
        open('alternada.txt','w').truncate(0)
        playsound('alert.mp3')
        tm(6)
        return alternada_reader + ' Altenada encontaada'
    if len(dupla_alternada_reader) != 0:

            print(dupla_alternada_reader,'dupla_alternada encontrado')
            open('dupla_alternada.txt','w').truncate(0)
            playsound('alert.mp3')
            tm(6)
            return dupla_alternada_reader+' dupla_alternada encontrado'
    if len(tripla_alternada_reader) != 0:

         
            print(tripla_alternada_reader,'tripla_alternada encontrado')
            open('tripla_alternada.txt','w').truncate(0)
            playsound('alert.mp3')
            tm(6)
            return tripla_alternada_reader+' tripla_alternada encontrado'
    if len(bunico_reader) != 0:

            print(bunico_reader,'bloco unico encontrado')
            open('loco_unico.txt','w').truncate(0)
            playsound('alert.mp3')
            tm(6)
            return bunico_reader+' bloco unico encontrado'
    if len(balternada_reaader) != 0:

            print(balternada_reaader,'bloco alternada encontrado')
            open('bloco_alternada.txt','w').truncate(0)
            playsound('alert.mp3')
            tm(6)
            return balternada_reaader+' bloco alternada encontrado'
    if len(bduplo_reader) != 0:

            print(bduplo_reader,'bloco duplo encontrado')
            open('bloco_alternada.txt','w').truncate(0)
            playsound('alert.mp3')
            tm(6)
            return bduplo_reader+' bloco duplo encontrado'
        
    return None

        
app.run()
    
    
