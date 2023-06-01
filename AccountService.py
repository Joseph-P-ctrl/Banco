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
        self.movimientos = pd.read_excel(movimientos) 
       
        if (len(self.movimientos.columns)<6):
            self.error.message = "Archivo Estado de Cuenta: Columnas no encontradas, elimine cabeceras innecesarias"
            return
        if "Monto" not in self.movimientos.columns:
            self.error.message = "Archivo Estado de Cuenta: Columnas no encontradas, elimine cabeceras innecesarias"
            return
        column_name = "Monto"        
        self.movimientos[column_name] = self.movimientos[column_name].astype(str).str.replace(",", "")
        self.movimientos["Monto"] = pd.to_numeric(self.movimientos["Monto"],errors='coerce')
        self.movimientos["Fecha"] = pd.to_datetime(self.movimientos["Fecha"], dayfirst=True)
        self.movimientos["Fecha"] = self.movimientos["Fecha"].dt.date

    