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
        

class TransferService:
     
    def __init__(self):
        self.error = Error()
        
    def setMovimientos(self,movimientos):
        self.movimientos = movimientos
        

    def _process_transfers_df(self, transferencias):
        if len(transferencias.columns) < 10:
            self.error.message = "Archivo Transferencias: Columnas no ubicadas, elimine cabeceras innecesarias"
            return
        
        if "Ordenante" not in transferencias.columns:
            self.error.message = "Archivo Transferencias: Columnas no encontradas, elimine cabeceras innecesarias"
            return
        transferencias["Monto abonado"] = transferencias["Monto abonado"].astype(str).str.replace(",", "")
        transferencias["Fecha de abono"] =  pd.to_datetime(transferencias["Fecha de abono"], dayfirst=True, errors='coerce')
        transferencias["Monto abonado"] = pd.to_numeric(transferencias["Monto abonado"],errors='coerce')
        transferencias = transferencias.loc[transferencias["Monto abonado - Moneda"]=="S/ "].copy()
        self.movimientos["Fecha"] = pd.to_datetime(self.movimientos["Fecha"], dayfirst=True)
        

        for index, row in transferencias.iterrows():
            fecha = row["Fecha de abono"]
            reg = self.movimientos.loc[(self.movimientos["Monto"]==row["Monto abonado"]) & (self.movimientos["Fecha"]==fecha)]
            
            print('los resultadops',reg)
            if len(reg)>1:
                self.error.message= "Mas de una coincidencia"
                self.error.addItem({"ordenante": row["Ordenante"], "monto": row["Monto abonado"], "fecha":row["Fecha de abono"]})   
            elif(len(reg)==1):
                self.movimientos.loc[(self.movimientos["Monto"]==row["Monto abonado"]) & (self.movimientos["Fecha"]==fecha), "Referencia"] = row["Ordenante"]
            else:
                 self.error.message = "Registros no ubicados"
                 self.error.addItem({"ordenante": row["Ordenante"], "monto": row["Monto abonado"], "fecha":row["Fecha de abono"]})   
    
    def process_transfers(self, transferFile):
        transferencias = pd.read_excel(transferFile, header=2)
        self._process_transfers_df(transferencias)