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

    def conciliar( self, movimientosfile, asientosfile):
        try:
            self.resultadosMovimiento = pd.read_excel(movimientosfile,   header=0 )
            
            self.asientos = pd.read_excel(asientosfile,   header=0 )
        
            if (len(self.resultadosMovimiento.columns)<10):
                self.error.message = "Archivo moviento: Columnas no encontradas, elimine cabeceras innecesarias provecios "
                return
            
            if "Fecha" not in self.resultadosMovimiento.columns:
                self.error.message = "Archivo Estado de Cuenta: Columnas no encontradas"
                return
           
            if (len(self.asientos.columns)<21):
                self.error.message = "Archivo asiento: Columnas no encontradas, elimine  cabeceras innecesarias "
                return
            
            if "Documento compras" not in self.asientos.columns:
                self.error.message = "Archivo Estado de Cuenta: Columnas no encontradas, elimine cabeceras innecesarias"
                return
            df1m = self.resultadosMovimiento[["Monto","Saldo" ,"Sucursal - agencia" ,"Operación - Número" ,"Operación - Hora" ,"Usuario" ,"UTC" ,"Referencia2" ,"Referencia" ,"Procendecias"]].copy()
            df1a = self.asientos[["Documento compras","Icono part.abiertas/comp." ,"Acreedor" ,"Cuenta" ,"Fecha de documento" ,"Fe.contabilización" ,"Nº documento" ,"Clase de documento" ,"Referencia" ,"Doc.compensación" ,"Texto" ,"Moneda del documento" ,"Importe en moneda local" ,"División" ,"Ejercicio / mes" ,"Nombre del usuario" ,"Clave contabiliz." ,"Asignación" ,"Indicador Debe/Haber" ,"Importe en ML2" ,"Centro de coste"]].copy()
          
            
            df1aa = pd.DataFrame(df1a, columns=['Asignación'])
            df1aa_filtrado = df1aa.dropna()
            asignaciones= df1aa_filtrado['Asignación'].astype(int).astype(str).str.zfill(7).str[-6:]
            movimientos_op= df1m['Operación - Número'].str[-6:]
          
            df1a = df1a.dropna(subset=['Nº documento'])
            documentos = df1a['Nº documento'].astype(str)

            numeros_con_7 = documentos[documentos.str.startswith('7')]
          
                                
            for valo1 in movimientos_op:
                if valo1 in asignaciones.values:
                    indice = asignaciones[asignaciones == valo1].index[0]
                    
                    num = round(float(numeros_con_7.loc[indice]))
                    num_str = str(num)
                
                    self.resultadosMovimiento.at[indice, "Asientos"] = num_str



        except Exception as ex:
            self.error.message = str(ex)
            
    