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
    def __process_interbanks_df(self, df_interbancarias):
        try:
            if (len(df_interbancarias.columns)<7):
                raise MyCustomException("Archivo Interbanks: Columnas no encontradas, elimine cabeceras innecesarias")
                
            
            if "Tipo de Operación" not in df_interbancarias.columns:
                raise MyCustomException("Archivo Interbanks: Columnas no encontradas, elimine cabeceras innecesarias")
            
            df_interbancarias["Monto abonado"] = df_interbancarias["Monto abonado"].astype(str).str.replace(",", "")
            df_interbancarias["Monto abonado"] = pd.to_numeric(df_interbancarias["Monto abonado"],errors='coerce')
            df_interbancarias = df_interbancarias.loc[df_interbancarias["Monto abonado - Moneda"]=="S/ "].copy()
            print(df_interbancarias.dtypes)
            for index, row in df_interbancarias.iterrows():
                num_operacion = str(row["N° Operación"])
                reg = self.movimientos.loc[(self.movimientos["Monto"].apply(lambda x: round(x, 2))==round(row["Monto abonado"],2)) &
                                           (self.movimientos["Operación - Número"].astype(str).str[-4:]==num_operacion[-4:])].copy()
                
                if len(reg)>1:
                    self.error.message = "Mas de una coincidencia"
                    self.error.addItem({"ordenante": row["Ordenante"], "monto": row["Monto abonado"], "operacion":num_operacion})
                elif(len(reg)==1):
                        self.movimientos.loc[(self.movimientos["Monto"].apply(lambda x: round(x, 2))==round(row["Monto abonado"],2)) &
                                             (self.movimientos["Operación - Número"].astype(str).str[-4:]==num_operacion[-4:]), "Referencia"] = row["Ordenante"]
                else:
                    self.error.addItem({"ordenante": row["Ordenante"], "monto": row["Monto abonado"], "operacion":num_operacion})          
        except Exception as ex:
            self.error.message =str(ex)

    def process_interbanks( self,interbankFile):
        try:
            interbancarias = pd.read_excel(interbankFile, header=2)
            self.__process_interbanks_df(interbancarias)
        except Exception as ex:
            self.error.message =str(ex)
 



