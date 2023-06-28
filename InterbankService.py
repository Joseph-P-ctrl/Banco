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
        

class InterbankService:
     
    def __init__(self):
        self.error=Error()

    def setMovimientos(self,movimientos):
        self.movimientos = movimientos

    def process_interbanks( self,interbankFile):
        try:
            interbancarias = pd.read_excel(interbankFile, header=2)
            if (len(interbancarias.columns)<7):
                self.error.message = "Archivo Interbanks: Columnas no encontradas, elimine cabeceras innecesarias"
                return
            
            if "Tipo de Operación" not in interbancarias.columns:
                self.error.message = "Archivo Interbanks: Columnas no encontradas, elimine cabeceras innecesarias"
                return
            interbancarias["Monto abonado"] = interbancarias["Monto abonado"].astype(str).str.replace(",", "")
            interbancarias["Monto abonado"] = pd.to_numeric(interbancarias["Monto abonado"],errors='coerce')
            interbancarias = interbancarias.loc[interbancarias["Monto abonado - Moneda"]=="S/ "].copy()
            
            for index, row in interbancarias.iterrows():
                num_operacion = str(row["N° Operación"])
                reg = self.movimientos.loc[(self.movimientos["Monto"].apply(lambda x: round(x, 2))==round(row["Monto abonado"],2)) & (self.movimientos["Operación - Número"].astype(str).str[-4:]==num_operacion[-4:])].copy()
                if len(reg)>1:
                    self.error.message = "Mas de una coincidencia"
                    self.error.addItem({"ordenante": row["Ordenante"], "monto": row["Monto abonado"], "operacion":num_operacion})
                elif(len(reg)==1):
                        self.movimientos.loc[(self.movimientos["Monto"].apply(lambda x: round(x, 2))==round(row["Monto abonado"],2)) & (self.movimientos["Operación - Número"].astype(str).str[-4:]==num_operacion[-4:]), "Referencia"] = row["Ordenante"]
                else:
                    self.error.addItem({"ordenante": row["Ordenante"], "monto": row["Monto abonado"], "operacion":num_operacion})   
             
            

        except Exception as ex:
            self.error.message =str(ex)


