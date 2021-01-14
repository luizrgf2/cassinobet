from selenium import webdriver
import pickle
import os
from selenium.webdriver.common.keys import Keys
import json
import undetected_chromedriver
from time import sleep as tm
from login import Login
from get_roletas import Roll
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

driver = webdriver_complete(True)

@app.route('/iniciar',methods=['POST'])
def init():
    
    json_file = request.get_json()
    print(json_file)
    file = json.loads(json_file)
    print(file)
    user = file['user']
    visible = file['visible']
    giro_alternada = file['alternada']
    giro_dupla_alternada = file['dupla_alternada']
    giro_tripla_alternada = file['tripla_alternada']
    giro_bloco_unico = file['bloco_unico']
    giro_bloco_duplo = file['bloco_duplo']
    giro_bloco_alternada = file['bloco_alternada']
    auth_alternada = file['auth_alternada']
    auth_dalternada = file['auth_dalternada']
    auth_talternada = file['auth_talternada']
    auth_bunico = file['auth_bunico']
    auth_balternada = file['auth_balternada']
    auth_bduplo = file['auth_bduplo']
    


    
    try:

        
        roll = Roll(user,visible,driver)
        
        _thread.start_new_thread(roll.init,(giro_alternada,giro_dupla_alternada,giro_tripla_alternada,giro_bloco_unico,giro_bloco_alternada,giro_bloco_duplo,auth_alternada,auth_dalternada,auth_talternada,auth_bunico,auth_balternada,auth_bduplo))
        
        
        return 'Iniciado com sucesso'
    except Exception as e:
        return e
def init_sound(sound:bool,text:str,name_file:str):

    if len(text) > 2:
        if sound == True:
            _thread.start_new_thread(playsound,('alert.mp3',))
            tm(0.4)
        open(name_file+'.txt','w').write('')

        return text 
@app.route('/pegarinfo',methods=['POST'])
def pegar_infos():
    
    padrao = ''

    
    
    
    
    json_file = json.loads(request.get_json())
    
    print(json_file)
    try:
        padrao = open('padrao.txt','r',encoding='utf8').read()
    except Exception as e:
        print(e)
   


    text_actual = init_sound(json_file['sound'],padrao,'padrao')
    if text_actual != None:
        
        file_reader = open('aux_padrao.txt','r').read()

        if len(file_reader) == 0:

            open('aux_padrao.txt','w').write(text_actual)
        else:
            open('aux_padrao.txt','w').write(file_reader+'\n'+text_actual)
            
        file_reader = open('aux_padrao.txt','r').read()



        return file_reader
    else:
        file_reader = open('aux_padrao.txt','r').read()
        return file_reader   
@app.route('/login',methods=['POST'])
def login():
    json_file = request.get_json()
    
    jsonn = json.loads(json_file)
    print(type(jsonn))
    visible = jsonn['visible']
    user = jsonn['user']
    password = jsonn['password']
    login = Login(visible,user,password,driver)
    open('aux_padrao.txt','w').write('')

    return login.login()
        
app.run()
    
    
