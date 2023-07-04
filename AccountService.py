import os
import pandas as pd
import re
import numpy as np

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
        self.movimientos= pd.read_excel(movimientos,  header=4)
        
        
        movimientos_efectivo = self.movimientos.loc[self.movimientos["Descripción operación"].str.contains('EFECTIVO', na=False)]

        for index, row in movimientos_efectivo.iterrows():
            cod_recaudo = re.findall(r'\d+', row["Descripción operación"])
            
            # if cod_recaudo:
            #     cod_recaudo_entero = [int(digito) for digito in cod_recaudo]
            #     print(cod_recaudo_entero[0])
            recaudos = "BD/CODIGO RECAUDO.xls"
            prepagos = "BD/PREPAGOS.xls"
            trabajores = "BD/TRABAJORES.xls"

            # Leer el archivo Excel
            df_recaudos = pd.read_excel(recaudos, header=None)
            df_prepagos = pd.read_excel(prepagos, header=None)
            df_trabajores = pd.read_excel(trabajores, header=None)

            # Obtener la columna A y la columna B
            col_codigos_recaudo     = df_recaudos[0]
            col_codigos_prepagos    = df_prepagos[0]
            col_codigos_trabajores  =  df_trabajores[0]
            col_descripcion_recaudo     = df_recaudos[1]
            col_descripcion_prepagos    = df_prepagos[1]
            col_descripcion_trabajores  =  df_trabajores[1]
            if cod_recaudo:
                cod_recaudo_entero = [int(digito) for digito in cod_recaudo]
                
                if cod_recaudo_entero[0] in col_codigos_recaudo.values:
                    indice = np.where(col_codigos_recaudo == cod_recaudo_entero[0])[0][0]
                    descripcion = col_descripcion_recaudo[indice]
                    self.movimientos.at[index, "Referencia"] = descripcion

                    # print(cod_recaudo_entero[0], descripcion)
                
                if cod_recaudo_entero[0] in col_codigos_prepagos.values:
                    indice = np.where(col_codigos_prepagos == cod_recaudo_entero[0])[0][0]
                    descripcion = col_descripcion_prepagos[indice]
                    self.movimientos.at[index, "Referencia"] = descripcion

                    # print(cod_recaudo_entero[0], descripcion)
                
                if cod_recaudo_entero[0] in col_codigos_trabajores.values:
                    indice = np.where(col_codigos_trabajores == cod_recaudo_entero[0])[0][0]
                    descripcion = col_descripcion_trabajores[indice]
                    self.movimientos.at[index, "Referencia"] = descripcion

                    # print(cod_recaudo_entero[0], descripcion)
        # Guardar el DataFrame con la nueva columna "Referencia" en un nuevo archivo de Excel
                    
        # if len(descripcion)>1:
            
        #     self.movimientos.loc[(self.movimientos[cod_recaudo_entero[0]]."Referencia")] = row["descripcion"]
        if (len(self.movimientos.columns)<11):
            self.error.message = "Archivo movimientos: Columnas no encontradas, elimine cabeceras innecesarias de movimientos"
            return
        if "Fecha" not in self.movimientos.columns:
            self.error.message = "esty en las columnas : Columnas no encontradas, eliminemmmmmmmmmmm cabeceras innecesarias"
            return
 
        # column_name = "Fecha"        
       
        # self.movimientos[column_name] = self.movimientos[column_name].astype(str).str.replace(",", "")
        # self.movimientos["Monto"] = pd.to_numeric(self.movimientos["Monto"],errors='coerce')
        # self.movimientos["Fecha"] = pd.to_datetime(self.movimientos["Fecha"], dayfirst=True)
        # self.movimientos["Fecha"] = self.movimientos["Fecha"].dt.date
        

   


   

    