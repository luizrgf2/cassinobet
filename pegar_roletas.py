
from sqlite3.dbapi2 import Cursor
from selenium import webdriver
import pickle
import os
from selenium.webdriver.common.keys import Keys
import json
import undetected_chromedriver
from time import sleep as tm
import sqlite3
import _thread
from datetime import datetime
from playsound import playsound



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

        
        tm(1)   
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
        
        
        corte_principal_name = text.split('class="lobby-table__name-container"')
        corte_principal_name.pop(0)
        names = []
        
        
        for i in range(len(corte_principal_name)):
            
            names.append(corte_principal_name[i].split('">')[1].split('</div><div')[0])



        
        
        return names
    def check_updates_in_roletes(self):
        text = ''
        print('Verificando por atualização!')
            
        while True:
            try:
                file_json = json.loads(open('database.json','r').read())
                break
            except Exception as e:
                print(e)
                if str(e).find('Extra data: line') != -1:
                    text_aux = ''
                    file = open('database.json','r').read().split('\n')
                    for i in range(502):
                        if i != 501:
                            if len(text_aux) ==  0:
                                text_aux = file[i]
                            else:
                                text_aux = text_aux+'\n'+file[i]
                        else:

                            if len(file[i]) >=2:

                                text_aux = text_aux+'\n'+'}'

                    open('database.json','w').write(text_aux)
                    

        text = str(self.driver.page_source) #pegando html da roleta
        
        corte_principal = text.split('class="lobby-table-rol-round-result__container"') #separando onde estao os ultimos numeros
        corte_principal.pop(0)
        
        
        
            
        names = self.get_names()
            
        for i in range(len(corte_principal)):

            
            name = names[i]
            num_atual = 0
            try:
                num_atual = str(corte_principal[i].split('last"')[1].split('number">')[1].split('</div>')[0])+' '+str(corte_principal[i].split('__item_last"')[0].split('_item_')[-1].split(' ')[0])
                
            except:
                print('O Html da dessa tabela está temporariamente modificado!...')
                file_json[name][0]['alternada'] = None
                file_json[name][1]['dalternada'] = None
                file_json[name][2]['talternada'] = None
                file_json[name][3]['bunico'] = None
                file_json[name][4]['balternada'] = None
                file_json[name][5]['bduplo'] = None

            
            
            
            

            
            alternada = file_json[name][0]['alternada']
            
            dalternada = file_json[name][1]['dalternada']
            
            talternada = file_json[name][2]['talternada']
            
            bunico = file_json[name][3]['bunico']
            
            balternada = file_json[name][4]['balternada']
            
            bduplo = file_json[name][5]['bduplo']
            

            


            if alternada == None:

                file_json[name][0]['alternada'] = num_atual      
            


            else:
                numero = num_atual
                try:
                    numero = alternada.split(',')[-1]
                except:
                    print('Valor errado!')
                
                if numero != num_atual:
                    insert = alternada+','+num_atual
                    file_json[name][0]['alternada'] = insert      


            if dalternada == None:
                file_json[name][1]['dalternada'] = num_atual      

            else:
                numero = num_atual
                try:
                    numero = dalternada.split(',')[-1]
                except:
                    print('Valor errado!')

                if numero != num_atual:
                    insert = dalternada+','+num_atual
                    file_json[name][1]['dalternada'] = insert      


            
            if talternada == None:
                
                file_json[name][2]['talternada'] = num_atual      

            else:
                numero = num_atual
                try:

                    numero = talternada.split(',')[-1]
                except:
                    print('Valor errado!')
                if numero != num_atual:
                    insert = talternada+','+num_atual
                    file_json[name][2]['talternada'] = insert      



            
            if bunico == None:

                file_json[name][3]['bunico'] = num_atual      

                
            else:
                numero = num_atual
                try:
                    numero = bunico.split(',')[-1]
                except:
                    print('Valor errado!')
                if numero != num_atual:
                    
                    insert = bunico+','+num_atual

                    file_json[name][3]['bunico'] = insert      

                
            if balternada == None:


                file_json[name][4]['balternada'] = num_atual      

            
            else:
                numero = num_atual
                try:
                    numero = balternada.split(',')[-1]
                except:
                    print('Valor errado!')
                if numero != num_atual:
                    
                    insert = balternada+','+num_atual
                    file_json[name][4]['balternada'] = insert      

            
            
            if bduplo == None:

                file_json[name][5]['bduplo'] = num_atual      

            else:
                numero = num_atual
                
                try:
                    numero = bduplo.split(',')[-1]
                except:
                    print('Valor errado!')
                if numero != num_atual:
                    
                    insert = bduplo+','+num_atual

                    file_json[name][5]['bduplo'] = insert
            
            open('database.json','w').write(json.dumps(file_json,indent=4))  

        try:
            self.driver.execute_script('var a = document.getElementsByClassName("modal-footer-btn modal-footer-btn_resolve modal-footer-btn_full"); a[0].click();')
        except:

            pass
    def alternada(self,giro,sound:bool):
        

        names = self.get_names()
        

        
        for name in names:
            
            while True:
                try:
                    file_json = json.loads(open('database.json','r').read())
                    break
                except Exception as e:
                    print(e)
                    if str(e).find('Extra data: line')!= -1:
                        text_aux = ''
                        file = open('database.json','r').read().split('\n')
                        
                        for i in range(502):
                            if i != 501:
                                if len(text_aux) ==  0:
                                    text_aux = file[i]
                                else:
                                    
                                    text_aux = text_aux+'\n'+file[i]
                            else:

                                if len(file[i]) >=2:

                                    text_aux = text_aux+'\n'+'}'

                        open('database.json','w').write(text_aux)
                    
            roleta = file_json[name][0]['alternada']
            alternada_encontrado = True
            #print('Alternada('+name+')',roleta)
            if roleta != None:
                roll = []
                try:
                    roll = roleta.split(',')
                except Exception as e:
                    print(e)
                    roll = []
                
                roll.reverse()
                if len(roll) == giro-1:

                    for i in range(giro-1):
                        #(roll[i])
                        
                        if i%2 == 0:

                            if roll[i].find('black') == -1:

                                alternada_encontrado = False

                        if i%2 !=0:

                            if roll[i].find('red') == -1:

                                alternada_encontrado = False
                    file_json[name][0]['alternada'] = None
                    
                    

                    
                    if alternada_encontrado == True:
                        text_from_file = open('padrao.txt','r',encoding='utf8').read()
                        if len(text_from_file) == 0:

                            open('padrao.txt','w',encoding='utf8').write(str(datetime.now())+' '+'Alternada('+name+')'+' '+str(roll))

                        else:
                            open('padrao.txt','w',encoding='utf8').write(text_from_file+'\n'+str(datetime.now())+' '+'Alternada('+name+')'+' '+str(roll))


                        
                        file_json[name][0]['alternada'] = None
                    
                        

                    open('database.json','w').write(json.dumps(file_json,indent=4))
    def duplo_alternada(self,giro,sound:bool):
       

        names = self.get_names()
        
        for name in names:

            while True:
                try:
                    file_json = json.loads(open('database.json','r').read())
                    break
                except Exception as e:
                    print(e)
                    if str(e).find('Extra data: line')!= -1:
                        text_aux = ''
                        file = open('database.json','r').read().split('\n')
                        for i in range(502):
                            if i != 501:
                                if len(text_aux) ==  0:
                                    text_aux = file[i]
                                else:
                                    text_aux = text_aux+'\n'+file[i]
                            else:

                                if len(file[i]) >=2:

                                    text_aux = text_aux+'\n'+'}'

                        open('database.json','w').write(text_aux)

            roleta = file_json[name][1]['dalternada']
            
            
            controler = False
            alternada_encontrado = True
            #print('Dupla_Alternada('+name+')',roleta)
            if roleta != None:

                roll = []
                try:
                    roll = roleta.split(',')
                except Exception as e:
                    print(e)
                    roll = []
                roll.reverse()

                if len(roll) ==giro-1:

                    for i in range(giro-1):

                        if controler == False:
                            #print('black')
                            if roll[i].find('black') == -1:

                                alternada_encontrado = False

                            if i%2 != 0:

                                controler = True
                        elif controler == True:
                            #print('red')
                            if roll[i].find('red') == -1:

                                alternada_encontrado = False

                            if i%2 != 0:

                                controler = False


                        


                    
                    if roll[0].find('red') != -1:

                        alternada_encontrado = False
                    
                    file_json[name][0]['dalternada'] = None
                    #print(file_json)
                    

                    
                    if alternada_encontrado == True:
                        text_from_file = open('padrao.txt','r',encoding='utf8').read()
                        if len(text_from_file) == 0:

                            open('padrao.txt','w',encoding='utf8').write(str(datetime.now())+' '+'Dupla Alternada('+name+')'+' '+str(roll))

                        else:
                            open('padrao.txt','w',encoding='utf8').write(text_from_file+'\n'+str(datetime.now())+' '+'Dupla Alternada('+name+')'+' '+str(roll))


                        
                        file_json[name][0]['dalternada'] = None
                    
                        

                    open('database.json','w').write(json.dumps(file_json,indent=4))                          
    def tripla_alternada(self,giro,sound:bool):
        
        

        names = self.get_names()
        
        

       
        for name in names:

            ini_controll = 2
            controll = True
            
            while True:
                try:
                    file_json = json.loads(open('database.json','r').read())
                    break
                except Exception as e:
                    print(e)
                    if str(e).find('Extra data: line')!= -1:
                        text_aux = ''
                        file = open('database.json','r').read().split('\n')
                        for i in range(502):
                            if i != 501:
                                if len(text_aux) ==  0:
                                    text_aux = file[i]
                                else:
                                    text_aux = text_aux+'\n'+file[i]
                            else:

                                if len(file[i]) >=2:

                                    text_aux = text_aux+'\n'+'}'

                        open('database.json','w').write(text_aux)

            roleta = file_json[name][2]['talternada']
            
            
            alternada_encontrado = True
            #print('Tripla_Alternada('+name+')',roleta)
            if roleta != None:

                roll = []
                try:
                    roll = roleta.split(',')
                except Exception as e:
                    print(e)
                    roll = []
                roll.reverse()

                if len(roll) == giro -1:

                    for i in range(giro-1):
                        
                        if i == 0:

                            if roll[i].find('red') != -1:

                                #print('red')

                                controll = True
                            else:
                                controll = False
                                #print('black')
                        if i == ini_controll:

                            ini_controll = ini_controll + 3

                            if controll == False:

                                if roll[i].find('red') == -1:

                                    alternada_encontrado = False

                                

                            else:

                                if roll[i].find('black') == -1:
                                    
                                    alternada_encontrado = False
                        else:
                    
                            if controll == True:

                                if roll[i].find('red') == -1:

                                    alternada_encontrado = False

                                

                            else:

                                if roll[i].find('black') == -1:
                                    
                                    alternada_encontrado = False




                        
                    
                    file_json[name][0]['talternada'] = None
                    #print(file_json)
                    

                    
                    if alternada_encontrado == True:
                        text_from_file = open('padrao.txt','r',encoding='utf8').read()
                        if len(text_from_file) == 0:

                            open('padrao.txt','w',encoding='utf8').write(str(datetime.now())+' '+'Tripla Alternada('+name+')'+' '+str(roll))

                        else:
                            open('padrao.txt','w',encoding='utf8').write(text_from_file+'\n'+str(datetime.now())+' '+'Tripla Alternada('+name+')'+' '+str(roll))


                        
                        file_json[name][0]['talternada'] = None
                    
                        

                    open('database.json','w').write(json.dumps(file_json,indent=4))
    def bloco_unico(self,giro,sound:bool):
        

        names = self.get_names()
        
        

        
        for name in names:

            ini_controll = 0

            controll = True
            
            while True:
                try:
                    file_json = json.loads(open('database.json','r').read())
                    break
                except Exception as e:
                    print(e)
                    if str(e).find('Extra data: line')!= -1:
                        text_aux = ''
                        file = open('database.json','r').read().split('\n')
                        for i in range(502):
                            if i != 501:
                                if len(text_aux) ==  0:
                                    text_aux = file[i]
                                else:
                                    text_aux = text_aux+'\n'+file[i]
                            else:

                                if len(file[i]) >=2:

                                    text_aux = text_aux+'\n'+'}'

                        open('database.json','w').write(text_aux)

            roleta = file_json[name][3]['bunico']

            #print('Bloco_Unico('+name+')',roleta)
            if roleta != None:
                roll = []
                try:
                    roll = roleta.split(',')
                except Exception as e:
                    print(e)
                    roll = []
                roll.reverse()

                if len(roll) ==giro -1:

                    for i in range(giro-1):
                        
                        number = int(roll[i].split(' ')[0])

                        if i == 0:
                            if number >= 1 and number <= 12:
                                #print('bloco 1')
                                ini_controll = 0

                            elif number >=13 and number <= 24:

                                #print('bloco 2')
                                ini_controll = 1

                            elif number >= 25 and number <= 36:

                                #print('bloco 3')
                                ini_controll = 2

                        else:

                            if ini_controll == 0:

                                if number >= 1 and number <= 12:

                                    

                                    print('bloco 1')
                                else:

                                    controll = False
                            elif ini_controll == 1:

                                if number >=13 and number <= 24:
                                    print('bloco 2')
                                    

                                else:

                                    controll = False
                            elif ini_controll ==2:
                                if number >= 25 and number <= 36:

                                    
                                    print('bloco 3')

                                else:

                                    controll = False
                            else:

                                controll = False

                    
                    
                    

                    file_json[name][3]['bunico'] = None
                    open('database.json','w').write(json.dumps(file_json,indent=4))  

                    if controll == True:
                        text_from_file = open('padrao.txt','r',encoding='utf8').read()
                        if len(text_from_file) == 0:

                            open('padrao.txt','w',encoding='utf8').write(str(datetime.now())+' '+'Bloco Unico('+name+')'+' '+str(roll))

                        else:
                            open('padrao.txt','w',encoding='utf8').write(text_from_file+'\n'+str(datetime.now())+' '+'Bloco Unico('+name+')'+' '+str(roll))

                        file_json[name][3]['bunico'] = None

                    
                    open('database.json','w').write(json.dumps(file_json,indent=4)) 
    def bloco_alternado(self,giro,sound:bool):

        names = self.get_names()
            
        for name in names:

            ini_controll = 0
            init_controll = 0

            controll = True
            
            while True:
                try:
                    file_json = json.loads(open('database.json','r').read())
                    break
                except Exception as e:
                    print(e)
                    if str(e).find('Extra data: line')!= -1:
                        text_aux = ''
                        file = open('database.json','r').read().split('\n')
                        for i in range(502):
                            if i != 501:
                                if len(text_aux) ==  0:
                                    text_aux = file[i]
                                else:
                                    text_aux = text_aux+'\n'+file[i]
                            else:

                                if len(file[i]) >=2:

                                    text_aux = text_aux+'\n'+'}'

                        open('database.json','w').write(text_aux)

            roleta = file_json[name][4]['balternada']
            
            #print('Bloco_Alternada('+name+')',roleta)
            if roleta != None:

                roll = []
                try:
                    roll = roleta.split(',')
                except Exception as e:
                    print(e)
                    roll = []
                roll.reverse()

                
                if len(roll) ==giro -1:
                    # descobrir qual bloco pertence o primeiro numero
                    
                    
                    if int(roll[0].split(' ')[0]) >= 1 and int(roll[0].split(' ')[0]) <= 12:

                        ini_controll = 0

                    elif int(roll[0].split(' ')[0]) >=13 and int(roll[0].split(' ')[0]) <= 24:

                        ini_controll = 1

                    elif int(roll[0].split(' ')[0]) >= 25 and int(roll[0].split(' ')[0]) <= 36:

                        ini_controll = 2
                    
                    
                    
                    #descobrir qual bloco pertence o numero 2

                    if int(roll[1].split(' ')[0]) >= 1 and int(roll[1].split(' ')[0]) <= 12:

                        init_controll = 0

                    elif int(roll[1].split(' ')[0]) >=13 and int(roll[1].split(' ')[0]) <= 24:

                        init_controll = 1

                    elif int(roll[1].split(' ')[0]) >= 25 and int(roll[1].split(' ')[0]) <= 36:

                        init_controll = 2

                    ###################

                    for i in range(giro-1):
                        
                        if i % 2 == 0:

                            controller = 0

                            if int(roll[i].split(' ')[0]) >= 1 and int(roll[i].split(' ')[0]) <= 12:
                                #print('bloco 1')
                                controller = 0

                            elif int(roll[i].split(' ')[0]) >=13 and int(roll[i].split(' ')[0]) <= 24:
                                #print('bloco 2')
                                controller = 1

                            elif int(roll[i].split(' ')[0]) >= 25 and int(roll[i].split(' ')[0]) <= 36:
                                #print('bloco 3')
                                controller = 2

                            if controller != ini_controll:

                                controll = False
                            
                        if i % 2 != 0:

                            controller = 0

                            if int(roll[i].split(' ')[0]) >= 1 and int(roll[i].split(' ')[0]) <= 12:
                                #print('bloco 1')
                                controller = 0

                            elif int(roll[i].split(' ')[0]) >=13 and int(roll[i].split(' ')[0]) <= 24:
                                #print('bloco 2')
                                controller = 1

                            elif int(roll[i].split(' ')[0]) >= 25 and int(roll[i].split(' ')[0]) <= 36:
                                #print('bloco 3')
                                controller = 2

                            if controller != init_controll or ini_controll == init_controll:

                                controll = False
                    

                    file_json[name][4]['balternada'] = None
                    open('database.json','w').write(json.dumps(file_json,indent=4))  

                    if controll == True:
                        text_from_file = open('padrao.txt','r',encoding='utf8').read()
                        if len(text_from_file) == 0:

                            open('padrao.txt','w',encoding='utf8').write(str(datetime.now())+' '+'Bloco Alternado('+name+')'+' '+str(roll))

                        else:
                            open('padrao.txt','w',encoding='utf8').write(text_from_file+'\n'+str(datetime.now())+' '+'Bloco Alternado('+name+')'+' '+str(roll))


                        file_json[name][4]['balternada'] = None

                    
                    open('database.json','w').write(json.dumps(file_json,indent=4)) 
    def bloco_duplo(self,giro,sound:bool):
        

        names = self.get_names()
            
        
        for name in names:

            ini_controll = 0
            init_controll = 0
            check_bloco_actual = False
            controll = True
            while True:
                try:
                    file_json = json.loads(open('database.json','r').read())
                    break
                except Exception as e:
                    print(e)
                    if str(e).find('Extra data: line')!= -1:
                        text_aux = ''
                        file = open('database.json','r').read().split('\n')
                        for i in range(502):
                            if i != 501:
                                if len(text_aux) ==  0:
                                    text_aux = file[i]
                                else:
                                    text_aux = text_aux+'\n'+file[i]
                            else:

                                if len(file[i]) >=2:

                                    text_aux = text_aux+'\n'+'}'

                        open('database.json','w').write(text_aux)

            roleta = file_json[name][5]['bduplo']
            
            #print('Bloco_Duplo('+name+')',roleta)
            if roleta != None:
                roll = []
                try:
                    roll = roleta.split(',')
                except Exception as e:
                    print(e)
                    roll = []

                roll.reverse()

                
                if len(roll) ==giro -1:
                    # descobrir qual bloco pertence o primeiro numero
                    
                    
                    if int(roll[0].split(' ')[0]) >= 1 and int(roll[0].split(' ')[0]) <= 12:

                        ini_controll = 0

                    elif int(roll[0].split(' ')[0]) >=13 and int(roll[0].split(' ')[0]) <= 24:

                        ini_controll = 1

                    elif int(roll[0].split(' ')[0]) >= 25 and int(roll[0].split(' ')[0]) <= 36:

                        ini_controll = 2
                    
                    
                    
                    #descobrir qual bloco pertence o numero 2

                    if int(roll[2].split(' ')[0]) >= 1 and int(roll[2].split(' ')[0]) <= 12:

                        init_controll = 0

                    elif int(roll[2].split(' ')[0]) >=13 and int(roll[2].split(' ')[0]) <= 24:

                        init_controll = 1

                    elif int(roll[2].split(' ')[0]) >= 25 and int(roll[2].split(' ')[0]) <= 36:

                        init_controll = 2

                    ###################

                    for i in range(giro-1):

                        controller = 0

                        if check_bloco_actual == False:

                            if ini_controll == 0:
                                
                                controller = 0

                                if int(roll[i].split(' ')[0]) >= 1 and int(roll[i].split(' ')[0]) <= 12:

                                    print('bloco 1')
                                    

                                else:

                                    controll = False
                                
                            elif ini_controll == 1:

                                controller = 1

                                if int(roll[i].split(' ')[0]) >=13 and int(roll[i].split(' ')[0]) <= 24:

                                    print('bloco 2')
                                
                                else:

                                    controll = False

                            elif ini_controll == 2:

                                controller = 2

                                if int(roll[i].split(' ')[0]) >= 25 and int(roll[i].split(' ')[0]) <= 36:

                                    print('bloco 3')

                                else:

                                    controll = False

                            if i % 2 != 0:

                                check_bloco_actual = True
                            
                            if controller != ini_controll:

                                controll = False
                        
                        if check_bloco_actual == True:

                            if init_controll == 0:
                                
                                controller = 0

                                if int(roll[i].split(' ')[0]) >= 1 and int(roll[i].split(' ')[0]) <= 12:

                                    print('bloco 1')
                                    

                                else:

                                    controll = False
                                
                            elif init_controll == 1:

                                controller = 1

                                if int(roll[i].split(' ')[0]) >=13 and int(roll[i].split(' ')[0]) <= 24:

                                    print('bloco 2')
                                
                                else:

                                    controll = False

                            elif init_controll == 2:

                                controller = 2

                                if int(roll[i].split(' ')[0]) >= 25 and int(roll[i].split(' ')[0]) <= 36:

                                    print('bloco 3')

                                else:

                                    controll = False

                            if i % 2 != 0:

                                check_bloco_actual = False
                            
                            if controller != ini_controll or ini_controll == init_controll:

                                controll = False
                    
                    file_json[name][5]['bduplo'] = None
                    open('database.json','w').write(json.dumps(file_json,indent=4)) 

                    if controll == True:
                        text_from_file = open('padrao.txt','r',encoding='utf8').read()
                        if len(text_from_file) == 0:

                            open('padrao.txt','w',encoding='utf8').write(str(datetime.now())+' '+'Bloco Duplo('+name+')'+' '+str(roll))

                        else:
                            open('padrao.txt','w',encoding='utf8').write(text_from_file+'\n'+str(datetime.now())+' '+'Bloco Duplo('+name+')'+' '+str(roll))

                        
                        file_json[name][5]['bduplo'] = None
                    

                    open('database.json','w').write(json.dumps(file_json,indent=4))            
    def init(self,giro_alternada:int,giro_dupla_alternada:int,giro_tripla_alternada:int,giro_bloco_unico:int,giro_bloco_alternada:int,giro_bloco_duplo:int,auth_alternada:bool,auth_dalternada:bool,auth_talternada:bool,auth_bunico:bool,auth_balternada:bool,auth_bduplo:bool,sound:bool):

        self.entry_roletes()
        self.create_json()
        

        os.remove(os.getcwd()+self.barra()+self.user+self.barra()+'cookie.pkl')

        while True:
            
            self.check_updates_in_roletes()

            print('Termino de verificação!')
            if auth_alternada == True:
            
                self.alternada(giro_alternada,sound)
            
            if auth_dalternada == True:

                self.duplo_alternada(giro_dupla_alternada,sound)
            
            if auth_talternada == True:

                self.tripla_alternada(giro_tripla_alternada,sound)
            
            if auth_bunico == True:
            
                self.bloco_unico(giro_bloco_unico,sound)
            if auth_balternada == True:
            
                self.bloco_alternado(giro_bloco_alternada,sound)
            
            if auth_bduplo == True:
            
                self.bloco_duplo(giro_bloco_duplo,sound)
            
            #self.duplo_alternada(giro_dupla_alternada)
            #self.tripla_alternada(giro_tripla_alternada)
            #self.bloco_unico(giro_bloco_unico)
            #self.bloco_alternado(giro_bloco_alternada)
            #self.bloco_duplo(giro_bloco_duplo)
    def create_json(self):
        nomes = self.get_names()

        lista = [{"alternada":None},{"dalternada":None},{"talternada":None},{"bunico":None},{"balternada":None},{"bduplo":None}]
        dicionario = {}
        for name in nomes:
            dicionario[name] = lista
        
        open('database.json','w').write(json.dumps(dicionario,indent=4))

roll = Roll('luizrgfg',True)
roll.init(4,5,5,5,5,5,True,False,True,False,False,False,True)