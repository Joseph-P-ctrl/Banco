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
class AsientoService:
        
    def __init__(self):
        self.error= Error()
        
    def _conciliar_df( self, df_movimientos, df_asientos):
        self.df_movimientos = df_movimientos
        self.df_asientos = df_asientos
        print(df_movimientos.columns)
        print('columnas',len(df_movimientos.columns))
        print('asiento cols',len(df_asientos.columns))
        try:
            if (len(self.df_movimientos.columns)<10):
               raise MyCustomException("Archivo movimientos: Columnas no encontradas, elimine cabeceras innecesarias provecios ")
            if "Fecha" not in self.df_movimientos.columns:
                raise MyCustomException( "Archivo movimientos: Columnas no encontradas")
            if (len(self.df_asientos.columns)<17):
                raise MyCustomException("Archivo asiento: Columnas no encontradas, elimine  cabeceras innecesarias ")
            if "Nº documento" not in self.df_asientos.columns:
                raise MyCustomException("Archivo Asientos: Columna Nro Documento no encontrada")
            
            df1m = self.df_movimientos[["Monto","Saldo" ,"Sucursal - agencia" ,"Operación - Número" ,"Operación - Hora" ,"Usuario" ,"UTC"  ,"Referencia" ,"Procedencia"]].copy()
            
            df_asientos_filtrado = df_asientos.dropna(subset=["Asignación"])
        
            #df_asientos_filtrado_7 = df_asientos_filtrado[df_asientos_filtrado['Nº documento'].astype(str).str.startswith('7')]
            df_asientos_filtrado['Asignacion_new'] = df_asientos_filtrado['Asignación'].astype(str).str.zfill(7).str[-6:]
            df1m['Operacion_new'] = df1m['Operación - Número'].astype(str).str[-6:]
            for index, row in df1m.iterrows():
                print('dentro de for')
                reg = df_asientos_filtrado.loc[df_asientos_filtrado['Asignacion_new'] == row["Operacion_new"]]
                print(reg)
                if len(reg) == 1:
                    self.df_movimientos.loc[index, "Asientos"] = reg['Nº documento'].iloc[0]
                    print('encontro')

               
        except Exception as ex:
            self.error.message = str(ex)
            raise ex
            
    
    def conciliar( self, movimientosfile, asientosfile):
        try:
            df_movimientos = pd.read_excel(movimientosfile,   header=0 )
            df_asientos = pd.read_excel(asientosfile,   header=0 )
            self._conciliar_df(df_movimientos, df_asientos)

               
        except Exception as ex:
            self.error.message = str(ex)
            raise ex
            
    