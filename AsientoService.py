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
        try:
            if (len(self.df_movimientos.columns)<10):
                self.error.message = "Archivo moviento: Columnas no encontradas, elimine cabeceras innecesarias provecios "
                return
            if "Fecha" not in self.df_movimientos.columns:
                self.error.message = "Archivo Estado de Cuenta: Columnas no encontradas"
                return
            if (len(self.df_asientos.columns)<21):
                self.error.message = "Archivo asiento: Columnas no encontradas, elimine  cabeceras innecesarias "
                return
            if "Documento compras" not in self.df_asientos.columns:
                self.error.message = "Archivo Estado de Cuenta: Columnas no encontradas, elimine cabeceras innecesarias"
                return
            df1m = self.df_movimientos[["Monto","Saldo" ,"Sucursal - agencia" ,"Operación - Número" ,"Operación - Hora" ,"Usuario" ,"UTC" ,"Referencia2" ,"Referencia" ,"Procendecias"]].copy()
            df_asientos = self.df_asientos[["Documento compras","Icono part.abiertas/comp." ,"Acreedor" ,"Cuenta" ,"Fecha de documento" ,"Fe.contabilización" ,"Nº documento" ,"Clase de documento" ,"Referencia" ,"Doc.compensación" ,"Texto" ,"Moneda del documento" ,"Importe en moneda local" ,"División" ,"Ejercicio / mes" ,"Nombre del usuario" ,"Clave contabiliz." ,"Asignación" ,"Indicador Debe/Haber" ,"Importe en ML2" ,"Centro de coste"]].copy()
            df_asientos_filtrado = df_asientos.dropna(subset=["Asignación"])

            df_asientos_filtrado_7 = df_asientos_filtrado[df_asientos_filtrado['Nº documento'].astype(str).str.startswith('7')]
            print('df_asientos_filtrado_7', df_asientos_filtrado_7)
            df_asientos_filtrado_7['Asignacion_new'] = df_asientos_filtrado_7['Asignación'].astype(int).astype(str).str.zfill(7).str[-6:]
            df1m['Operacion_new'] = df1m['Operación - Número'].astype(str).str[-6:]

            for index, row in df1m.iterrows():
                reg = df_asientos_filtrado_7.loc[df_asientos_filtrado_7['Asignacion_new'] == row["Operacion_new"]]
                if len(reg) == 1:
                    print('los reg', reg['Nº documento'].iloc[0])
                    self.df_movimientos.loc[index, "Asientos"] = reg['Nº documento'].iloc[0]

               
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
            
    