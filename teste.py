
import os

text = open('teste.txt','r').read()

def get_roulete(path):
    
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
        open(name_final[i]+'.txt','w').write(text_final)




        


    
    
get_roulete(os.getcwd()+'\\')