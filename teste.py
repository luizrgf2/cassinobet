


text = open('teste.txt','r').read()

def get_roulete():
    
    name_aux = text.split('class="lobby-table__name-container" data-theme="tableNamesColor_color">')
    area_numbers = name_aux[0]
    name_final = []
    for i in range(1,len(name_aux)):
        name_final.append(name_aux[i].split('</div>')[0])
    print(name_final)
get_roulete()