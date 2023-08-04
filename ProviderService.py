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
        
class ProviderService:
     
    def __init__(self):
        self.error= Error()

    def setMovimientos(self,movimientos):
        self.movimientos = movimientos

    def process_providers_df( self,df_proveedores):
        try:
            if (len(df_proveedores.columns)<13):
                self.error.message = "Archivo Providers: Columnas no encontradas, elimine cabeceras innecesarias provecios "
                return
            if "Ordenante - Nombre o Razón Social" not in df_proveedores.columns:
                self.error.message = "Archivo Estado de Cuenta: Columnas no encontradas, eliminepppppppp cabeceras innecesarias"
                return
            df_proveedores["Monto abonado"] = df_proveedores["Monto abonado"].astype(str).str.replace(",", "")
            df_proveedores["Monto abonado"] = pd.to_numeric(df_proveedores["Monto abonado"],errors='coerce')
            df_proveedores["Ordenante - Nombre o Razón Social"]=df_proveedores["Ordenante - Nombre o Razón Social"].str.strip()
            new_proveedores = df_proveedores[["Monto abonado", "Ordenante - Nombre o Razón Social","Fecha de pago"]].copy()
            df_proveedores["Fecha de pago"] = pd.to_datetime(df_proveedores["Fecha de pago"], dayfirst=True)

            group_proveedores = new_proveedores.groupby(["Ordenante - Nombre o Razón Social","Fecha de pago"]).sum().round(2)
            print('los grupos de proveedores',group_proveedores)
            self.movimientos["Fecha"] = pd.to_datetime(self.movimientos["Fecha"], dayfirst=True)
            
            for index, row in group_proveedores.iterrows():
                #fecha = datetime.strptime(index[1], "%d/%m/%Y").date()
                fecha = index[1]
                monto_abonado = float(row["Monto abonado"])
                # self.movimientos["Monto"] = pd.to_numeric(self.movimientos["Monto"], errors='coerce')
                
                reg = self.movimientos.loc[(self.movimientos["Monto"]==monto_abonado) & (self.movimientos["Fecha"]==fecha)]
               
                if len(reg)>1:
                    self.error.message = "Mas de una coincidencia"
                    self.error.addItem({"ordenante": index[0], "monto": monto_abonado, "fecha":fecha})
                elif(len(reg)==1):
                    self.movimientos.loc[(self.movimientos["Monto"]==monto_abonado) & (self.movimientos["Fecha"]==fecha), "Referencia"] = index[0]
                else:
                    self.error.message = "Registros no ubicados"
                    self.error.addItem({"ordenante": index[0], "monto": monto_abonado, "fecha":fecha})   
            
        except Exception as ex:
            self.error.message = str(ex)
            
    def process_providers( self,providersFile):
        try:
            df_proveedores = pd.read_excel(providersFile,   header=2 )
            self.process_providers_df(df_proveedores)
            
        except Exception as ex:
            self.error.message = str(ex)
            