import os
import pandas as pd
from datetime import datetime

class MyCustomException(Exception):
        pass



class Error:
    def __init__(self):
        self.message = ""
        self.items = []
    def addItem(self, item):
        self.items.append(item)    
        

class AccountService:
    def __init__(self):
        self.error = Error()
     
    def process_movements(self, movimientos):
        # self.movimientos = pd.read_excel(movimientos)
        self.movimientos= pd.read_excel(movimientos,  header=4)
        # self.movimientos = pd.read_excel(movimientos, header=2, skiprows=2)

        # self.interrupciones = pd.read_excel(interrupciones, header=2)
    
        # print("si estoy", movimientos)
      
        if (len(self.movimientos.columns)<11):
            self.error.message = "Archivo movimientos: Columnas no encontradas, elimine cabeceras innecesarias de movimientos"
            return
        if "Fecha" not in self.movimientos.columns:
            self.error.message = "esty en las columnas : Columnas no encontradas, eliminemmmmmmmmmmm cabeceras innecesarias"
            return
 
        column_name = "Fecha"        
       
        self.movimientos[column_name] = self.movimientos[column_name].astype(str).str.replace(",", "")
        self.movimientos["Monto"] = pd.to_numeric(self.movimientos["Monto"],errors='coerce')
        self.movimientos["Fecha"] = pd.to_datetime(self.movimientos["Fecha"], dayfirst=True)
        self.movimientos["Fecha"] = self.movimientos["Fecha"].dt.date
   

    