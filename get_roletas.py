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
        while True:
            try:

                link = self.driver.find_element_by_id('gamecontent').get_attribute('src')
                self.driver.get(link)
                break
            except:
                pass

        
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
        while True:
            try:
                self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div[4]/div/div/div[1]/div/div/ul[1]/li[1]/span').click()
                break
            except:
                pass
        
        tm(5)
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
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[6]/div/div[2]/div[2]/button')
            self.entry_roletes()
            self.create_jsons()
            open('aux_padrao.txt')
        except:
            pass
    def veryfying_updates(self):

        self.bet365_Premium_Roulette()
        self.bet365_Roulette()

        self.Roulette()

        self.Football_Roulette()
        self.Hindi_Roulette()
        self.Speed_Roulette()
        self.Greek_Roulette()
        self.Turkish_Roulette()
        self.Roleta_Brasileira()

        self.Prestige_Roulette()

        self.Spread_Bet_Roulette()
        self.Deutsches_Roulette()

        self.UK_Roulette()


        self.Triumph_Roulette()

        self.Roulette_Italiana()

        

        verificar_roleta_fechada = self.driver.execute_script('''function detect_close_roulete(){


        let button = document.getElementsByClassName('modal-footer-btn modal-footer-btn_resolve modal-footer-btn_full')
        let result = false

        for(let i =0 ; i <button.length;i++){
            if (button[i] != undefined){


                if(button[i].innerHTML == "Ok"){


                    button[i].click()
                    
                    
                }else if (button[i].innerHTML == "Close" || button[i].innerHTML == "Fechar"){
                    
                    
                    button[i].click()
                    result =  true


                }

            }
        }
        return result



        } return detect_close_roulete()''')


        print('Estado da roleta',verificar_roleta_fechada)

        if verificar_roleta_fechada == True:

            self.entry_roletes()
            self.create_jsons()


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
            self.veryfying_updates()
            if auth_alternada == True:
                self.alternada(giro_alternada)
            if auth_dalternada == True:
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
            roleta_final = ''

            if len(roleta) >=giro-1:
                roleta.reverse()
                
                for k in range(giro-1):
                    
                    
                    if len(roleta_final) ==0:

                        roleta_final = roleta[k]
                        
                    else:
                        roleta_final= roleta_final+','+roleta[k]
                    
                    if k % 2 == 0:
                        
                        if roleta[k].find('black') == -1:

                            seguir_roleta = False
                    elif k % 2 != 0:

                        if roleta[k].find('red') == -1:

                            seguir_roleta = False
                
                self.reiniciar_roleta(roleta,names[i],'alternada')

                print(seguir_roleta,roleta)
                if seguir_roleta == True and self.indentificar_repeticoes(f'Alternada({names[i]}) '+str(roleta_final)):

                    file_reader = open('padrao.txt','r').read()

                    if len(file_reader) == 0:
                        
                        f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'
                        open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Alternada({names[i]}) '+str(roleta_final))
                    else:
                        open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Alternada({names[i]}) '+str(roleta_final))
    def dupla_alternada(self,giro:int):

        names = self.get_names()

        for k in range(len(names)):

            json_file_dupla_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'dupla_alternada.json','r').read())
            

            roleta = str(json_file_dupla_alternada[names[k]][0]['dupla_alternada']).split(',')
            
            seguir_roleta = True
            change_state = False
            roleta_final = ''

            if len(roleta) >=giro-1:
                roleta.reverse()
                for i in range(giro -1):

                    if len(roleta_final) == 0:
                        roleta_final = roleta[i]
                    else:
                        roleta_final = roleta_final+','+roleta[i]


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
                
                self.reiniciar_roleta(roleta,names[k],'dupla_alternada')

                print(roleta,seguir_roleta)
                if seguir_roleta == True and self.indentificar_repeticoes(f'Dupla Alternada({names[k]}) '+str(roleta)):

                    file_reader = open('padrao.txt','r').read()

                    if len(file_reader) == 0:

                        open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Dupla Alternada({names[k]}) '+str(roleta_final))
                    else:
                        open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Dupla Alternada({names[k]}) '+str(roleta_final))
    def tripla_alternada(self,giro:int):
        names = self.get_names()

        for k in range(len(names)):

            json_file_tripla_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'tripla_alternada.json','r').read())
            roleta = str(json_file_tripla_alternada[names[k]][0]['tripla_alternada']).split(',')
            init_red = False
            
            counter_checker = 0
            seguir_roleta = True
            

            if roleta[0].find('red') != -1:
                init_red = True
                
            roleta_final = ''

            if len(roleta) >=giro-1:
                roleta.reverse()




                for i in range(giro -1):
                    if len(roleta_final) == 0:
                        roleta_final = roleta[i]
                    else:
                        roleta_final = roleta_final+","+roleta[i]
                    
                    if init_red == True:

                        if counter_checker <2:
                            counter_checker+=1

                            if roleta[i].find('red') == -1:
                                seguir_roleta = False

                        else:

                            counter_checker = 0
                            if roleta[i].find('black') == -1:
                                seguir_roleta = False
                    else:
                        if counter_checker <2:
                            counter_checker+=1

                            if roleta[i].find('black') == -1:
                                seguir_roleta = False

                        else:

                            counter_checker = 0
                            if roleta[i].find('red') == -1:
                                seguir_roleta = False

                            
                    




                print(names[k],roleta)
                self.reiniciar_roleta(roleta,names[k],'tripla_alternada')
                
                if seguir_roleta == True and self.indentificar_repeticoes(f'Tripla Alternada({names[k]}) '+str(roleta)):

                    file_reader = open('padrao.txt','r').read()

                    if len(file_reader) == 0:

                        open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Tripla Alternada({names[k]}) '+str(roleta_final))
                    else:
                        open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Tripla Alternada({names[k]}) '+str(roleta_final))
    def bloco_unico(self,giro:int):
        names = self.get_names()
        try:
            for k in range(len(names)):
                json_file_bloco_unico = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_unico.json','r').read())
                roleta = str(json_file_bloco_unico[names[k]][0]['bloco_unico']).split(',')



                seguir_roleta = True
                roleta_final = ''
                if len(roleta) >= giro -1:

                    roleta.reverse()
                    
                    
                    bloco = self.indentificar_bloco(roleta[0])
                    self.reiniciar_roleta(roleta,names[k],'bloco_unico')
                    for i in range(giro -1):
                        

                        if len(roleta_final) == 0:
                            roleta_final = roleta[i]
                        else:
                            roleta_final = roleta_final+','+roleta[i]

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
                

                    if seguir_roleta == True and self.indentificar_repeticoes(f'Bloco Unico({names[k]}) '+str(roleta_final)):

                        file_reader = open('padrao.txt','r').read()

                        if len(file_reader) == 0:

                            open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Unico({names[k]}) '+str(roleta_final))
                        else:
                            open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Unico({names[k]}) '+str(roleta_final))
        except Exception as e:
            print(e)
    def bloco_alternada(self,giro:int):
        names = self.get_names()
        try:
            for k in range(len(names)):
                json_file_bloco_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_alternada.json','r').read())
                roleta = str(json_file_bloco_alternada[names[k]][0]['bloco_alternada']).split(',')

                seguir_roleta = True
                roleta_final = ''

                if len(roleta) >= giro -1:
                    
                    roleta.reverse()
                    self.reiniciar_roleta(roleta,names[k],'bloco_alternada')
                    
                    bloco_1 = self.indentificar_bloco(roleta[0])
                    bloco_2 = self.indentificar_bloco(roleta[1])

                    for i in range(giro -1):

                        if len(roleta_final) == 0:
                            roleta_final = roleta[i]
                        else:
                            roleta_final = roleta_final+","+roleta[i]


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
                        


                    

                    if seguir_roleta == True and self.indentificar_repeticoes(f'Bloco Alternado({names[k]}) '+str(roleta_final)):

                        file_reader = open('padrao.txt','r').read()

                        if len(file_reader) == 0:

                            open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Alternado({names[k]}) '+str(roleta_final))
                        else:
                            open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Alternado({names[k]}) '+str(roleta_final))
        except Exception as e:
            print(e)
    def bloco_duplo(self,giro:int):
        names = self.get_names()
        try:
            for k in range(len(names)):
                json_file_bloco_duplo = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_duplo.json','r').read())
                roleta = str(json_file_bloco_duplo[names[k]][0]['bloco_duplo']).split(',')
  

                seguir_roleta = True
                roleta_final = ''

                if len(roleta) >= giro -1:
                    roleta.reverse()
                    
                    self.reiniciar_roleta(roleta,names[k],'bloco_duplo')
                    
                    bloco_1 = self.indentificar_bloco(roleta[0])
                    bloco_2 = self.indentificar_bloco(roleta[2])
                    change_state = False
                    for i in range(giro -1):

                        if len(roleta_final) == 0:
                            roleta_final = roleta[i]
                        else:
                            roleta_final = roleta_final+','+roleta[i]

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
                        


                    

                    if seguir_roleta == True and self.indentificar_repeticoes(f'Bloco Duplo({names[k]}) '+str(roleta_final)):
                        file_reader = open('padrao.txt','r').read()

                        if len(file_reader) == 0:

                            open('padrao.txt','w').write(f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Duplo({names[k]}) '+str(roleta_final))
                        else:
                            open('padrao.txt','w').write(file_reader+'\n'+f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}-{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'+f'Bloco Duplo({names[k]}) '+str(roleta_final))
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
    def update_json_files(self,name_roulete:str,text_tripla:str,text_roulete:str):
        
        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        json_file_dupla_alternada = json.loads(open(path+'dupla_alternada.json','r').read())
        json_file_tripla_alternada = json.loads(open(path+'tripla_alternada.json','r').read())
        json_file_bloco_unico = json.loads(open(path+'bloco_unico.json','r').read())
        json_file_bloco_alternada = json.loads(open(path+'bloco_alternada.json','r').read())
        json_file_bloco_duplo = json.loads(open(path+'bloco_duplo.json','r').read())

        if len(text_tripla) > 0:
            json_file_alternada[name_roulete][1]['tripla_roleta'] = text_tripla
            json_file_dupla_alternada[name_roulete][1]['tripla_roleta'] = text_tripla
            json_file_tripla_alternada[name_roulete][1]['tripla_roleta'] = text_tripla
            json_file_bloco_unico[name_roulete][1]['tripla_roleta'] = text_tripla
            json_file_bloco_alternada[name_roulete][1]['tripla_roleta'] = text_tripla
            json_file_bloco_duplo[name_roulete][1]['tripla_roleta'] = text_tripla
            open(path+'alternada.json','w').write(json.dumps(json_file_alternada,indent=4))
            open(path+'dupla_alternada.json','w').write(json.dumps(json_file_dupla_alternada,indent=4))
            open(path+'tripla_alternada.json','w').write(json.dumps(json_file_tripla_alternada,indent=4))
            open(path+'bloco_unico.json','w').write(json.dumps(json_file_bloco_unico,indent=4))
            open(path+'bloco_alternada.json','w').write(json.dumps(json_file_bloco_alternada,indent=4))
            open(path+'bloco_duplo.json','w').write(json.dumps(json_file_bloco_duplo,indent=4))


        if len(text_roulete) > 0:
            
            if len(json_file_alternada[name_roulete][0]['alternada']) == 0:
                json_file_alternada[name_roulete][0]['alternada'] = text_roulete
            else:
                json_file_alternada[name_roulete][0]['alternada'] = json_file_alternada[name_roulete][0]['alternada']+','+text_roulete

            if len(json_file_dupla_alternada[name_roulete][0]['dupla_alternada']) == 0:
                json_file_dupla_alternada[name_roulete][0]['dupla_alternada'] = text_roulete
            else:
                json_file_dupla_alternada[name_roulete][0]['dupla_alternada'] = json_file_dupla_alternada[name_roulete][0]['dupla_alternada']+','+text_roulete
            
            if len(json_file_tripla_alternada[name_roulete][0]['tripla_alternada']) == 0:
                json_file_tripla_alternada[name_roulete][0]['tripla_alternada'] = text_roulete
            else:
                json_file_tripla_alternada[name_roulete][0]['tripla_alternada'] = json_file_tripla_alternada[name_roulete][0]['tripla_alternada']+','+text_roulete

            if len(json_file_bloco_unico[name_roulete][0]['bloco_unico']) == 0:
                json_file_bloco_unico[name_roulete][0]['bloco_unico'] = text_roulete
            else:
                json_file_bloco_unico[name_roulete][0]['bloco_unico'] = json_file_bloco_unico[name_roulete][0]['bloco_unico']+','+text_roulete
            
            if len(json_file_bloco_alternada[name_roulete][0]['bloco_alternada']) == 0:
                json_file_bloco_alternada[name_roulete][0]['bloco_alternada'] = text_roulete
            else:
                json_file_bloco_alternada[name_roulete][0]['bloco_alternada'] = json_file_bloco_alternada[name_roulete][0]['bloco_alternada']+','+text_roulete
            
            if len(json_file_bloco_duplo[name_roulete][0]['bloco_duplo']) == 0:
                json_file_bloco_duplo[name_roulete][0]['bloco_duplo'] = text_roulete
            else:
                json_file_bloco_duplo[name_roulete][0]['bloco_duplo'] = json_file_bloco_duplo[name_roulete][0]['bloco_duplo']+','+text_roulete

            
            open(path+'alternada.json','w').write(json.dumps(json_file_alternada,indent=4))
            open(path+'dupla_alternada.json','w').write(json.dumps(json_file_dupla_alternada,indent=4))
            open(path+'tripla_alternada.json','w').write(json.dumps(json_file_tripla_alternada,indent=4))
            open(path+'bloco_unico.json','w').write(json.dumps(json_file_bloco_unico,indent=4))
            open(path+'bloco_alternada.json','w').write(json.dumps(json_file_bloco_alternada,indent=4))
            open(path+'bloco_duplo.json','w').write(json.dumps(json_file_bloco_duplo,indent=4))
    def get_indicie_roulete(self,name_roulete:str):

        names = self.get_names()
        result = None
        for i in range(len(names)):

            if str(names[i]) == name_roulete:

                
                result =  i
        return result
    def indentificar_repeticoes(self,text:str):
        file_reader = open('repeticao.txt','r').read()

        if len(file_reader.split('\n')) > 200:

            open('repeticao.txt','w').write('')

        if file_reader.find(text) == -1:
            if len(file_reader) == 0:
                file_reader = text
            else:
                file_reader = file_reader+'\n'+text
            open('repeticao.txt','w').write(file_reader)
            return True
        else:
            return False           
    def reiniciar_roleta(self,roleta:list,name_roleta:str,padrao_roleta:str):

        if padrao_roleta == 'alternada':

            json_file_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'alternada.json','r').read())
            lista_numbers = json_file_alternada[name_roleta][0]['alternada'].split(',')
            roleta_renovada = ''
            if len(lista_numbers) >=30:

                for i in range(15,30):

                    if len(roleta_renovada) == 0:
                        roleta_renovada = lista_numbers[i]
                    else:
                        roleta_renovada = roleta_renovada+','+lista_numbers[i]
                json_file_alternada[name_roleta][0]['alternada'] = roleta_renovada
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'alternada.json','w').write(json.dumps(json_file_alternada,indent=4))
        elif padrao_roleta == 'dupla_alternada':

            json_file_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'dupla_alternada.json','r').read())
            lista_numbers = json_file_alternada[name_roleta][0]['dupla_alternada'].split(',')
            roleta_renovada = ''
            if len(lista_numbers) >=30:

                for i in range(15,30):

                    if len(roleta_renovada) == 0:
                        roleta_renovada = lista_numbers[i]
                    else:
                        roleta_renovada = roleta_renovada+','+lista_numbers[i]
                json_file_alternada[name_roleta][0]['dupla_alternada'] = roleta_renovada
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'dupla_alternada.json','w').write(json.dumps(json_file_alternada,indent=4))
        elif padrao_roleta == 'tripla_alternada':

            json_file_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'tripla_alternada.json','r').read())
            lista_numbers = json_file_alternada[name_roleta][0]['tripla_alternada'].split(',')
            roleta_renovada = ''
            if len(lista_numbers) >=30:

                for i in range(15,30):

                    if len(roleta_renovada) == 0:
                        roleta_renovada = lista_numbers[i]
                    else:
                        roleta_renovada = roleta_renovada+','+lista_numbers[i]
                json_file_alternada[name_roleta][0]['tripla_alternada'] = roleta_renovada
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'tripla_alternada.json','w').write(json.dumps(json_file_alternada,indent=4))
        elif padrao_roleta == 'bloco_unico':

            json_file_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_unico.json','r').read())
            lista_numbers = json_file_alternada[name_roleta][0]['bloco_unico'].split(',')
            roleta_renovada = ''
            if len(lista_numbers) >=30:

                for i in range(15,30):

                    if len(roleta_renovada) == 0:
                        roleta_renovada = lista_numbers[i]
                    else:
                        roleta_renovada = roleta_renovada+','+lista_numbers[i]
                json_file_alternada[name_roleta][0]['bloco_unico'] = roleta_renovada
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_unico.json','w').write(json.dumps(json_file_alternada,indent=4))
        elif padrao_roleta == 'bloco_alternada':

            json_file_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_alternada.json','r').read())
            lista_numbers = json_file_alternada[name_roleta][0]['bloco_alternada'].split(',')
            roleta_renovada = ''
            if len(lista_numbers) >=30:

                for i in range(15,30):

                    if len(roleta_renovada) == 0:
                        roleta_renovada = lista_numbers[i]
                    else:
                        roleta_renovada = roleta_renovada+','+lista_numbers[i]
                json_file_alternada[name_roleta][0]['bloco_alternada'] = roleta_renovada
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_alternada.json','w').write(json.dumps(json_file_alternada,indent=4))
        elif padrao_roleta == 'bloco_duplo':

            json_file_alternada = json.loads(open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_duplo.json','r').read())
            lista_numbers = json_file_alternada[name_roleta][0]['bloco_duplo'].split(',')
            roleta_renovada = ''
            if len(lista_numbers) >=30:

                for i in range(15,30):

                    if len(roleta_renovada) == 0:
                        roleta_renovada = lista_numbers[i]
                    else:
                        roleta_renovada = roleta_renovada+','+lista_numbers[i]
                json_file_alternada[name_roleta][0]['bloco_duplo'] = roleta_renovada
                open(os.getcwd()+self.barra()+'padroes'+self.barra()+'bloco_duplo.json','w').write(json.dumps(json_file_alternada,indent=4))
    def bet365_Premium_Roulette(self):

        index = self.get_indicie_roulete('bet365 Premium Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['bet365 Premium Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('bet365 Premium Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')     
    def bet365_Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        


        index = self.get_indicie_roulete('bet365 Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['bet365 Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('bet365 Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')  
    def Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        



        index = self.get_indicie_roulete('Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')   
    def Football_Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        


        index = self.get_indicie_roulete('Football Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Football Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Football Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')    
    def Hindi_Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        


        index = self.get_indicie_roulete('Hindi Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Hindi Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Hindi Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')   
    def Speed_Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        



        index = self.get_indicie_roulete('Speed Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Speed Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Speed Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')
    def Greek_Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        



        index = self.get_indicie_roulete('Greek  Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Greek  Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Greek  Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')   
    def Turkish_Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        



        index = self.get_indicie_roulete('Turkish Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Turkish Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Turkish Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')   
    def Roleta_Brasileira(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        



        index = self.get_indicie_roulete('Roleta Brasileira')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Roleta Brasileira'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Roleta Brasileira',tripla_rolete_atual,f'{num_1.text} {color_1}')    
    def Prestige_Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        

        index = self.get_indicie_roulete('Prestige Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Prestige Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Prestige Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')
    def Spread_Bet_Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        



        index = self.get_indicie_roulete('Spread Bet Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Spread Bet Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Spread Bet Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')
    def Deutsches_Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        


        index = self.get_indicie_roulete('Deutsches Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Deutsches Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Deutsches Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')
    def UK_Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        



        index = self.get_indicie_roulete('UK Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['UK Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('UK Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')
    def Triumph_Roulette(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        



        index = self.get_indicie_roulete('Triumph Roulette')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Triumph Roulette'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Triumph Roulette',tripla_rolete_atual,f'{num_1.text} {color_1}')   
    def Roulette_Italiana(self):

        path = os.getcwd()+self.barra()+'padroes'+self.barra()
        

        index = self.get_indicie_roulete('Roulette Italiana')


        if index == None:
            return

        path = os.getcwd()+self.barra()+'padroes'+self.barra()

        roleta = self.driver.find_elements_by_class_name('lobby-table-rol-round-result__container')[index]
        num_1 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-1]
        color_1 = num_1.find_element_by_xpath('..').get_attribute('class')
        num_2 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-2]
        color_2 = num_2.find_element_by_xpath('..').get_attribute('class')
        num_3 = roleta.find_elements_by_class_name('lobby-table-rol-round-result__item-number')[-3]
        color_3 = num_3.find_element_by_xpath('..').get_attribute('class')

        if color_1.find('red') != -1:
        
            color_1 = 'red'
        
        elif color_1.find('black') != -1:
            
            color_1 = 'black'
        
        else:
        
            color_1 = 'green'
        
        
        
        if color_2.find('red') != -1:
        
            color_2 = 'red'
        
        elif color_2.find('black') != -1:
            
            color_2 = 'black'
        
        else:
        
            color_2 = 'green'
        
        
        
        
        if color_3.find('red') != -1:
        
            color_3 = 'red'
        
        elif color_3.find('black') != -1:
            
            color_3 = 'black'
        
        else:
        
            color_3 = 'green'

        json_file_alternada = json.loads(open(path+'alternada.json','r').read())
        tripla_rolete = json_file_alternada['Roulette Italiana'][1]['tripla_roleta']
        tripla_rolete_atual = f'{num_1.text} {color_1},{num_2.text} {color_2},{num_3.text} {color_3}'

        if tripla_rolete != tripla_rolete_atual and num_1.text !='0':

            self.update_json_files('Roulette Italiana',tripla_rolete_atual,f'{num_1.text} {color_1}')  
