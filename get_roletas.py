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
from selenium import webdriver
from datetime import datetime

class Roll():
    
   
    def __init__(self,user:str,visible:bool,driver:webdriver):

        
        self.driver = driver
        
        self.driver.get('https://casino.bet365.com/home')
        
        
        
        tm(5)   
    def barra(self):
        
        import platform
        
        sistema = platform.system()
        
        if sistema == 'Linux':
            return '/'
        else:
            return '\\'
    def entry_roletes(self):
        tm(5)
        self.driver.get('https://casino.bet365.com/Play/LiveRoulette')
        link = ''
        
        while True:
            try:
                self.driver.switch_to_frame(self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/main/div[1]/iframe'))
                break
            except Exception as e:
                print(e)
        tm(3)
        link = self.driver.find_element_by_id('gamecontent').get_attribute('src')
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
        
        
        corte_principal_name = text.split('class="lobby-table__name-container" data-theme="tableNamesColor_color">')
        corte_principal_name.pop(0)
        names = []
        
        
        for i in range(len(corte_principal_name)):
            
            names.append(corte_principal_name[i].split('</div>')[0])



        
        
        return names
    def check_updates(self):

        tm(2)
        page_text = str(self.driver.page_source)

        aux_roletes = page_text.split('class="lobby-tables__item">') #pegando blocos de informaçao atraves do pagesouse
        aux_roletes.pop(0)
        names = self.get_names()
        last_num = '' #guardara o valor do ultimo giro
        penultimo_numero = '' #guardara o valor do penultimo giro
        antpenultimo_numero = ''#guardara o valor do antpnultimo giro


        for i in range(len(aux_roletes)): # percorrendo blocos e armazenando nas variaveis last_num, penultimo_numero, antpenultimo_numero

            
            open('texto.txt','w',encoding='utf8').write(page_text)
            
            last_num = ''
            penultimo_numero = ''
            antpenultimo_numero = ''
            
            while True:
                try:
                    last_num = aux_roletes[i].split('item_last">')[1].split('item-number">')[1].split('</div>')[0]+' '+aux_roletes[i].split('item_last">')[0].split('result__item_')[-1].split('class')[0].split(' ')[0]
                    penultimo_numero = aux_roletes[i].split('item_last">')[0].split('round-result__item-number">')[-1].split('</div>')[0]+' '+aux_roletes[i].split('item_last">')[0].split('class="lobby-table-rol-round-result__item lobby-table-rol-round-result__item_')[-2].split('"><div')[0]
                    antpenultimo_numero = aux_roletes[i].split('item_last">')[0].split('round-result__item-number">')[-2].split('</div>')[0]+' '+aux_roletes[i].split('item_last">')[0].split('class="lobby-table-rol-round-result__item lobby-table-rol-round-result__item_')[-3].split('"><div')[0]
                    break
                except:
                    return


            tripla_roleta_atual = f'{last_num},{penultimo_numero},{antpenultimo_numero}'
            
            json_alternada =json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'alternada.json','r').read()) 
            json_dupla_alternada =json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'dupla_alternada.json','r').read()) 
            json_tripla_alternada =json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'tripla_alternada.json','r').read()) 
            json_bloco_unico =json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_unico.json','r').read()) 
            json_bloco_alternada =json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_alternada.json','r').read()) 
            json_bloco_dupla =json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_duplo.json','r').read())

            while True:
                try:
                    roleta_alternada = json_alternada[names[i]][1]['tripla_roleta']
                    break
                except:
                    names = self.get_names()
            roleta_dupla_alternada = json_dupla_alternada[names[i]][1]['tripla_roleta']
            roleta_tripla_alternada = json_tripla_alternada[names[i]][1]['tripla_roleta']
            roleta_bloco_unico = json_bloco_unico[names[i]][1]['tripla_roleta']
            roleta_bloco_alternada = json_bloco_alternada[names[i]][1]['tripla_roleta']
            roleta_bloco_dupla = json_bloco_dupla[names[i]][1]['tripla_roleta']
            

            if roleta_alternada != tripla_roleta_atual and last_num.split(' ')[0] !='0': #verificar se os novos numeros no bet cassino são novos padrao alternada

                json_alternada[names[i]][1]['tripla_roleta'] = tripla_roleta_atual
                check_is_empty = 0
                
                
                check_is_empty = len(json_alternada[names[i]][0]['alternada'])


                if check_is_empty == 0:
                    json_alternada[names[i]][0]['alternada'] = last_num
                    
                    
                else:
                    json_alternada[names[i]][0]['alternada'] = json_alternada[names[i]][0]['alternada']+','+last_num
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'alternada.json','w').write(json.dumps(json_alternada,indent=4))
            #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
            if roleta_dupla_alternada != tripla_roleta_atual and last_num.split(' ')[0] !='0':   #verificar se os novos numeros no bet cassino são novos padrao dupla alternada

                json_dupla_alternada[names[i]][1]['tripla_roleta'] = tripla_roleta_atual
                check_is_empty = 0
                try:
                    check_is_empty = len(json_dupla_alternada[names[i]][0]['dupla_alternada'])
                except:
                    pass
                if check_is_empty == 0:
                    json_dupla_alternada[names[i]][0]['dupla_alternada'] = last_num
                else:
                    json_dupla_alternada[names[i]][0]['dupla_alternada'] = json_dupla_alternada[names[i]][0]['dupla_alternada']+','+last_num
                
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'dupla_alternada.json','w').write(json.dumps(json_dupla_alternada,indent=4))
            #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

            if roleta_tripla_alternada != tripla_roleta_atual and last_num.split(' ')[0] !='0':  #verificar se os novos numeros no bet cassino são novos padrao tripla alternada

                json_tripla_alternada[names[i]][1]['tripla_roleta'] = tripla_roleta_atual
                check_is_empty = 0
                try:
                    check_is_empty = len(json_tripla_alternada[names[i]][0]['tripla_alternada'])
                except:
                    pass
                if check_is_empty == 0:
                    json_tripla_alternada[names[i]][0]['tripla_alternada'] = last_num
                else:
                    json_tripla_alternada[names[i]][0]['tripla_alternada'] = json_tripla_alternada[names[i]][0]['tripla_alternada']+','+last_num
            
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'tripla_alternada.json','w').write(json.dumps(json_tripla_alternada,indent=4))
            
            #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
            if roleta_bloco_unico != tripla_roleta_atual and last_num.split(' ')[0] !='0':   #verificar se os novos numeros no bet cassino são novos padrao bloco unico

                json_bloco_unico[names[i]][1]['tripla_roleta'] = tripla_roleta_atual
                check_is_empty = 0
                try:
                    check_is_empty = len(json_bloco_unico[names[i]][0]['bloco_unico'])
                except:
                    pass
                if check_is_empty == 0:
                    json_bloco_unico[names[i]][0]['bloco_unico'] = last_num
                else:
                    json_bloco_unico[names[i]][0]['bloco_unico'] = json_bloco_unico[names[i]][0]['bloco_unico']+','+last_num
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_unico.json','w').write(json.dumps(json_bloco_unico,indent=4))
            #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
            if roleta_bloco_alternada != tripla_roleta_atual and last_num.split(' ')[0] !='0': #verificar se os novos numeros no bet cassino são novos padrao bloco alternada

                json_bloco_alternada[names[i]][1]['tripla_roleta'] = tripla_roleta_atual
                check_is_empty = 0

                try:
                    check_is_empty = len(json_bloco_alternada[names[i]][0]['bloco_alternada'])
                except:
                    pass
                if check_is_empty == 0:
                    json_bloco_alternada[names[i]][0]['bloco_alternada'] = last_num
                else:
                    json_bloco_alternada[names[i]][0]['bloco_alternada'] = json_bloco_alternada[names[i]][0]['bloco_alternada']+','+last_num
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_alternada.json','w').write(json.dumps(json_bloco_alternada,indent=4))
            
            #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
            
            if roleta_bloco_dupla != tripla_roleta_atual and last_num.split(' ')[0] !='0':   #verificar se os novos numeros no bet cassino são novos padrao bloco dupla

                json_bloco_dupla[names[i]][1]['tripla_roleta'] = tripla_roleta_atual
                check_is_empty = 0
                try:
                    check_is_empty = len(json_bloco_dupla[names[i]][0]['bloco_duplo'])
                except:
                    pass
                if check_is_empty == 0:
                    json_bloco_dupla[names[i]][0]['bloco_duplo'] = last_num
                else:
                    json_bloco_dupla[names[i]][0]['bloco_duplo'] = json_bloco_dupla[names[i]][0]['bloco_duplo']+','+last_num
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_duplo.json','w').write(json.dumps(json_bloco_dupla,indent=4))
            #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def create_json(self,name_file):
        nomes = self.get_names()

        lista = [{name_file:""},{"tripla_roleta":""}]
        dicionario = {}
        for name in nomes:
            dicionario[name] = lista
        
        open(os.getcwd()+self.barra()+'padroes'+self.barra()+name_file+".json",'w').write(json.dumps(dicionario,indent=4))
    def create_jsons(self):

        self.create_json('alternada')
        self.create_json('dupla_alternada')
        self.create_json('tripla_alternada')
        self.create_json('bloco_unico')
        self.create_json('bloco_alternada')
        self.create_json('bloco_duplo')
    def init(self,giro_alternada:int,giro_dupla_alternada:int,giro_tripla_alternada:int,giro_bloco_unico:int,giro_bloco_alternada:int,giro_bloco_duplo:int,auth_alternada:bool,auth_dalternada:bool,auth_talternada:bool,auth_bunico:bool,auth_balternada:bool,auth_bduplo:bool):
        self.entry_roletes()
        self.create_jsons()
        while True:
            self.check_updates()
            if auth_alternada == True:
                self.alternada(giro_alternada)
            if auth_balternada == True:
                self.dupla_alternada(giro_dupla_alternada)
            if auth_talternada == True:
                self.tripla_alternada(giro_tripla_alternada)
            if auth_bunico == True:
                self.bloco_unico(giro_bloco_unico)
            if auth_balternada == True:
                self.bloco_alternada(giro_bloco_alternada)
            if auth_bduplo == True:
                self.bloco_duplo(giro_bloco_alternada)
    def alternada(self,giro:int):

        names = self.get_names()

        for i in range(len(names)):

            json_file_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'alternada.json','r').read())
            roleta = str(json_file_alternada[names[i]][0]['alternada']).split(',')
            seguir_roleta = True

            if len(roleta) >=giro-1:
                roleta.reverse()
                for k in range(giro-1):

                    if k % 2 == 0:

                        if roleta[k].find('black') == -1:

                            seguir_roleta = False
                    elif k % 2 != 0:

                        if roleta[k].find('red') == -1:

                            seguir_roleta = False
                json_file_alternada[names[i]][0]['alternada'] = ''
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'alternada.json','w').write(json.dumps(json_file_alternada,indent=4))


                print(seguir_roleta,roleta)
                file_block = open('nomes_proibidos.txt','r').read()
                if seguir_roleta == True and file_block.find(names[i]) == -1:

                    file_reader = open('padrao.txt','r').read()

                    if len(file_reader) == 0:
                        print('oi')
                        
                        f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'
                        open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Alternada({names[i]})'+str(roleta))
                    else:
                        open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Alternada({names[i]})'+str(roleta))
    def dupla_alternada(self,giro:int):

        names = self.get_names()

        for k in range(len(names)):

            json_file_dupla_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'dupla_alternada.json','r').read())
            

            roleta = str(json_file_dupla_alternada[names[k]][0]['dupla_alternada']).split(',')
            
            seguir_roleta = True
            change_state = False

            if len(roleta) >=giro-1:
                roleta.reverse()
                for i in range(giro -1):
                    
                    if change_state == False:

                        if roleta[i].find('black') == -1:
                            
                            seguir_roleta =False
                        
                        if i % 2 != 0:

                            change_state = True                    

                    else:

                        if roleta[i].find('red') == -1:

                            seguir_roleta =False

                        if i % 2 != 0:

                            change_state = False                    
                print(names[k],roleta)
                json_file_dupla_alternada[names[k]][0]['dupla_alternada'] = ''
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'dupla_alternada.json','w').write(json.dumps(json_file_dupla_alternada,indent=4))

                file_block = open('nomes_proibidos.txt','r').read()
                if seguir_roleta == True and file_block.find(names[i]) == -1:

                    file_reader = open('padrao.txt','r').read()

                    if len(file_reader) == 0:

                        open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Dupla Alternada({names[k]})'+str(roleta))
                    else:
                        open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Dupla Alternada({names[k]})'+str(roleta))
    def tripla_alternada(self,giro:int):
        names = self.get_names()

        for k in range(len(names)):

            json_file_tripla_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'tripla_alternada.json','r').read())
            roleta = str(json_file_tripla_alternada[names[k]][0]['tripla_alternada']).split(',')
            init_red = False
            init_black = False
            
            seguir_roleta = True
            change_state = False

            if roleta[0].find('red') != -1:
                change_state=True
                init_black = True

            else:
                change_state=False
                init_red = True

            if len(roleta) >=giro-1:
                
                for i in range(giro -1):
                    
                    if change_state == False:

                        if roleta[i].find('black') == -1:
                            
                            seguir_roleta =False
                        
                        if i % 2 != 0 or init_black == True:

                            change_state = True                    

                    else:

                        if roleta[i].find('red') == -1:

                            seguir_roleta =False

                        if i % 2 != 0 or init_red == True:

                            change_state = False                    
                print(names[k],roleta)
                json_file_tripla_alternada[names[k]][0]['tripla_alternada'] = ''
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'tripla_alternada.json','w').write(json.dumps(json_file_tripla_alternada,indent=4))

                
                file_block = open('nomes_proibidos.txt','r').read()
                if seguir_roleta == True and file_block.find(names[i]) == -1:

                    file_reader = open('padrao.txt','r').read()

                    if len(file_reader) == 0:

                        open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Tripla Alternada({names[k]})'+str(roleta.reverse()))
                    else:
                        open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Tripla Alternada({names[k]})'+str(roleta.reverse()))
    def bloco_unico(self,giro:int):
        names = self.get_names()
        try:
            for k in range(len(names)):
                json_file_bloco_unico = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_unico.json','r').read())
                roleta = str(json_file_bloco_unico[names[k]][0]['bloco_unico']).split(',')



                seguir_roleta = True

                if len(roleta) >= giro -1:

                    roleta.reverse()
                    json_file_bloco_unico[names[k]][0]['bloco_unico'] = ''
                    open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_unico.json','w').write(json.dumps(json_file_bloco_unico,indent=4))
                    bloco = self.indentificar_bloco(roleta[0])
                    for i in range(giro -1):

                        bloco_atual = self.indentificar_bloco(roleta[i])

                        if bloco_atual == 1:
                            print('____________________________________________________________________________________________________________________________')
                            print('bloco atual 1 de 1 a 12')
                            print(roleta,roleta[i])
                            print('____________________________________________________________________________________________________________________________')

                        elif bloco_atual == 2:

                            print('____________________________________________________________________________________________________________________________')
                            print('bloco atual 2 de 13 a 24')
                            print(roleta,roleta[i])
                            print('____________________________________________________________________________________________________________________________')
                        
                        else:
                            print('____________________________________________________________________________________________________________________________')
                            print('bloco 3 de 25 a 36')
                            print(roleta,roleta[i])
                            print('____________________________________________________________________________________________________________________________')
                        

                        
                        if bloco_atual != bloco:
                            seguir_roleta = False
                

                    file_block = open('nomes_proibidos.txt','r').read()
                    if seguir_roleta == True and file_block.find(names[i]) == -1:

                        file_reader = open('padrao.txt','r').read()

                        if len(file_reader) == 0:

                            open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Unico({names[k]})'+str(roleta))
                        else:
                            open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Unico({names[k]})'+str(roleta))
        except Exception as e:
            print(e)
    def bloco_alternada(self,giro:int):
        names = self.get_names()
        try:
            for k in range(len(names)):
                json_file_bloco_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_alternada.json','r').read())
                roleta = str(json_file_bloco_alternada[names[k]][0]['bloco_alternada']).split(',')

                seguir_roleta = True

                if len(roleta) >= giro -1:
                    
                    roleta.reverse()
                    json_file_bloco_alternada[names[k]][0]['bloco_alternada'] = ''
                    open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_alternada.json','w').write(json.dumps(json_file_bloco_alternada,indent=4))
                    bloco_1 = self.indentificar_bloco(roleta[0])
                    bloco_2 = self.indentificar_bloco(roleta[1])
    

                    for i in range(giro -1):

                        bloco_atual = self.indentificar_bloco(roleta[i])
                        if i % 2 == 0:


                            if bloco_1 != bloco_atual or bloco_1 == bloco_2:

                                seguir_roleta = False
                        else:

                            if bloco_2 != bloco_atual or bloco_1 == bloco_2:

                                seguir_roleta = False

                        if bloco_atual == 1:
                            print('____________________________________________________________________________________________________________________________')
                            print('bloco atual 1 de 1 a 12')
                            print(roleta,roleta[i])
                            print('____________________________________________________________________________________________________________________________')

                        elif bloco_atual == 2:

                            print('____________________________________________________________________________________________________________________________')
                            print('bloco atual 2 de 13 a 24')
                            print(roleta,roleta[i])
                            print('____________________________________________________________________________________________________________________________')
                        
                        else:
                            print('____________________________________________________________________________________________________________________________')
                            print('bloco 3 de 25 a 36')
                            print(roleta,roleta[i])
                            print('____________________________________________________________________________________________________________________________')
                        


                    

                    file_block = open('nomes_proibidos.txt','r').read()
                    if seguir_roleta == True and file_block.find(names[i]) == -1:

                        file_reader = open('padrao.txt','r').read()

                        if len(file_reader) == 0:

                            open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Alternado({names[k]})'+str(roleta))
                        else:
                            open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Alternado({names[k]})'+str(roleta))
        except Exception as e:
            print(e)
    def bloco_duplo(self,giro:int):
        names = self.get_names()
        try:
            for k in range(len(names)):
                json_file_bloco_duplo = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_duplo.json','r').read())
                roleta = str(json_file_bloco_duplo[names[k]][0]['bloco_duplo']).split(',')
  

                seguir_roleta = True

                if len(roleta) >= giro -1:
                    roleta.reverse()
                    json_file_bloco_duplo[names[k]][0]['bloco_duplo'] = ''
                    open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_duplo.json','w').write(json.dumps(json_file_bloco_duplo,indent=4))
                    bloco_1 = self.indentificar_bloco(roleta[0])
                    bloco_2 = self.indentificar_bloco(roleta[2])
                    change_state = False
                    for i in range(giro -1):

                        bloco_atual = self.indentificar_bloco(roleta[i])
                        if change_state == False:


                            if bloco_1 != bloco_atual or bloco_1 == bloco_2:

                                seguir_roleta = False
                            if i % 2 != 0:

                                change_state = True
                        else:

                            if bloco_2 != bloco_atual or bloco_1 == bloco_2:

                                seguir_roleta = False
                            
                            if i % 2 != 0:

                                change_state = False

                        if bloco_atual == 1:
                            print('____________________________________________________________________________________________________________________________')
                            print('bloco atual 1 de 1 a 12')
                            print(roleta,roleta[i])
                            print('____________________________________________________________________________________________________________________________')

                        elif bloco_atual == 2:

                            print('____________________________________________________________________________________________________________________________')
                            print('bloco atual 2 de 13 a 24')
                            print(roleta,roleta[i])
                            print('____________________________________________________________________________________________________________________________')
                        
                        else:
                            print('____________________________________________________________________________________________________________________________')
                            print('bloco 3 de 25 a 36')
                            print(roleta,roleta[i])
                            print('____________________________________________________________________________________________________________________________')
                        


                    

                    file_block = open('nomes_proibidos.txt','r').read()
                    if seguir_roleta == True and file_block.find(names[i]) == -1:
                        file_reader = open('padrao.txt','r').read()

                        if len(file_reader) == 0:

                            open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Duplo({names[k]})'+str(roleta))
                        else:
                            open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Duplo({names[k]})'+str(roleta))
        except Exception as e:
            print(e)
    def indentificar_bloco(self,element:str):

        bloco = 0
        
        number = int(element.split(' ')[0])
        
        if number >=1 and number <=12:

            bloco = 1
        
        elif number >=13 and number <=24:

            bloco = 2
        
        elif number >=25 and number <=36:

            bloco = 3

        return bloco
        

        

