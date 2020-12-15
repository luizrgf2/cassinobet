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

def init(visible:bool,user:str,password:str):
    
    login = Login(visible,user,password)
    login.login()
    
    roll = Roll(user,visible)
    roll.entry_roletes()
    nomes_roletas = roll.get_name_roletes()
    for roleta in nomes_roletas:
        print(roleta+' ACTUAL')
        try:
            open(roleta+'.txt','w').truncate(0)
        except:
            print()
        roll.get_roulete(roleta)

        
init(True,'luizrgfg','Mano010599')
    
    
