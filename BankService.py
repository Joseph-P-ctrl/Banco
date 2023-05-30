import os
import pandas as pd
from datetime import datetime

class MyCustomException(Exception):
        pass

TRANSFER = "TRANSFER"
PROVIDERS = "PROVIDERS"
INTERBANK = "INTERBANK"
MOVIMIENTOS = "MOVIMIENTOS"

class Error:
    def __init__(self, category):
        self.message = ""
        self.category = category
        self.items = []
    def addItem(self, item):
        self.items.append(item)    
        

class BankService:
     
    def __init__(self):
        self.errors = []

    def process_movements(self, movimientos):
        self.movimientos = pd.read_excel(movimientos) 
        error = Error(MOVIMIENTOS)
        if (len(self.movimientos.columns)<6):
            error.message = "Columnas no encontradas, verifique archivo movimientos"
        column_name = "Monto"        
        self.movimientos[column_name] = self.movimientos[column_name].astype(str).str.replace(",", "")
        self.movimientos["Monto"] = pd.to_numeric(self.movimientos["Monto"],errors='coerce')
        if (error.message!=""):
            self.errors.append(error)
    

    def process_transfers(self, transferFile):
        
        transferencias = pd.read_excel(transferFile)
        error = Error(TRANSFER)
        if len(transferencias.columns) == 0:
            error.message = "Columnas no ubicadas, verifique archivo transfers"
            return error
        transferencias["Monto abonado"] = transferencias["Monto abonado"].astype(str).str.replace(",", "")
        transferencias["Monto abonado"] = pd.to_numeric(transferencias["Monto abonado"],errors='coerce')
        transferencias = transferencias.loc[transferencias["Monto abonado - Moneda"]=="S/ "].copy()

        
        for index, row in transferencias.iterrows():
            #buscar en movimientos
            #print("Monto abonado...", row["Monto abonado"])
            #print("Fecha...", row["Fecha de abono"])
            fecha = datetime.strptime(row["Fecha de abono"], "%d/%m/%Y")
            reg = self.movimientos.loc[(self.movimientos["Monto"]==row["Monto abonado"]) & (self.movimientos["Fecha"]==fecha)].copy()
            
            if len(reg)>1:
                error.message= "Mas de una coincidencia"
                error.addItem({"ordenante": row["Ordenante"], "monto": row["Monto abonado"], "fecha":row["Fecha de abono"]})   
            elif(len(reg)==1):
                #print("reg",row["Ordenante"])
                reg["Referencia"] = row["Ordenante"]
                self.movimientos.update(reg)
            else:
                 error.message = "Registros no ubicados"
                 error.addItem({"ordenante": row["Ordenante"], "monto": row["Monto abonado"], "fecha":row["Fecha de abono"]})   
        if (error.message!=""):
            self.errors.append(error)
             
    def process_providers( self,providersFile):
        try:
            proveedores = pd.read_excel(providersFile)
            proveedores["Monto abonado"] = proveedores["Monto abonado"].astype(str).str.replace(",", "")
            proveedores["Monto abonado"] = pd.to_numeric(proveedores["Monto abonado"],errors='coerce')
            proveedores["Ordenante - Nombre o Razón Social"]=proveedores["Ordenante - Nombre o Razón Social"].str.strip()
            new_proveedores = proveedores[["Monto abonado", "Ordenante - Nombre o Razón Social","Fecha de pago"]].copy()
            group_proveedores = new_proveedores.groupby(["Ordenante - Nombre o Razón Social","Fecha de pago"]).sum()
            error = Error(PROVIDERS)
            
            for index, row in group_proveedores.iterrows():
                fecha = datetime.strptime(index[1], "%d/%m/%Y")
                reg = self.movimientos.loc[(self.movimientos["Monto"]==row["Monto abonado"]) & (self.movimientos["Fecha"]==fecha)].copy()
        
                if len(reg)>1:
                    error.message = "Mas de una coincidencia"
                    error.addItem({"ordenante": index[0], "monto": row["Monto abonado"], "fecha":fecha})
                elif(len(reg)==1):
                    #print("reg",index[0])
                    reg["Referencia"] = index[0]
                    self.movimientos.update(reg)
                else:
                    error.message = "Registros no ubicados"
                    error.addItem({"ordenante": index[0], "monto": row["Monto abonado"], "fecha":fecha})   
            if (error.message!=""):
                self.errors.append(error)
        except Exception as ex:
            error.message = str(ex)
            error.addItem(str(ex))
            self.errors.append(error)

    def process_interbanks( self,interbankFile):
        try:
            interbancarias = pd.read_excel(interbankFile)
            interbancarias["Monto abonado"] = interbancarias["Monto abonado"].astype(str).str.replace(",", "")
            interbancarias["Monto abonado"] = pd.to_numeric(interbancarias["Monto abonado"],errors='coerce')
            interbancarias = interbancarias.loc[interbancarias["Monto abonado - Moneda"]=="S/ "].copy()
            error = Error(INTERBANK)
            for index, row in interbancarias.iterrows():
                #buscar en movimientos
                #print("Monto abonado...", row["Monto abonado"])
                #print("Fecha...", row["Fecha de abono"])
                num_operacion = str(row["N° Operación"])
                reg = self.movimientos.loc[(self.movimientos["Monto"]==row["Monto abonado"]) & (self.movimientos["Operación - Número"].astype(str).str[-4:]==num_operacion[-4:])].copy()
                
                if len(reg)>1:
                    error.message = "Mas de una coincidencia"
                    error.addItem({"ordenante": row["Ordenante"], "monto": row["Monto abonado"], "operacion":num_operacion})
                elif(len(reg)==1):
                    #print("reg",row["Ordenante"])
                    reg["Referencia"] = row["Ordenante"]
                    self.movimientos.update(reg)
                else:
                    error.addItem({"ordenante": row["Ordenante"], "monto": row["Monto abonado"], "operacion":num_operacion})   
            if (error.message!=""):
                self.errors.append(error)
             
        except Exception as ex:
            self.errors.append(str(ex))

    def search_strings(self, array, search_query):
        """This function searches for a string within an array and returns the matching items."""
        matching_item = ""
        for item in array:
            if search_query in item.upper():
                matching_item = item.upper()
        return matching_item

    