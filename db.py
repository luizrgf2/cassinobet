import sqlite3

cone = sqlite3.connect('roletas.db')


cursor = cone.cursor()



#cursor.execute('CREATE TABLE teste1(id INTEGER AUTO_INCREMENT PRIMARY KEY, nome TEXT)')
#cursor.execute('INSERT INTO teste1(nome) VALUES("luz fellipe")')
#cursor.execute('CREATE TABLE roletas(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), value VARCHAR(255))')
cursor.execute('UPDATE roletas SET roleta = Null')
cursor.execute(f'SELECT value FROM roletas')

xy = cursor.fetchall()

for x in xy:
    
    

    print(x)
