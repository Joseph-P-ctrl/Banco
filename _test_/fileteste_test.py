import unittest

import pandas as pd
from AsientoService import AsientoService
from TransferService import TransferService
from ProviderService import ProviderService
from AccountService import AccountService

class TestReadExcel(unittest.TestCase):
    def test_proveedores(self):
        proveedores = {
            "Ordenante - Nombre o Razón Social": ["KALLPA GENERACION SA"] * 20,
            "Ordenante - RUC/DNI": ["RUC"] * 20,
            "Ordenante - Número": [20538810682] * 20,
            "Documento - Tipo": ["Factura del proveedor"] * 20,
            "Nº de documento": [
                "00F061-00013868", "00F061-00013870", "00F061-00013865", "00F061-00013872",
                "00F061-00013862", "00F061-00013860", "00F061-00013859", "00F061-00013855",
                "00F061-00013866", "00F061-00013863", "00F061-00013852", "00F061-00013858",
                "00F061-00013861", "00F061-00013853", "00F061-00013857", "00F061-00013871",
                "00F061-00013869", "00F061-00013856", "00F061-00013864", "00F061-00013854"
            ],
            "Fecha de pago": ['27/07/2023'] * 20,
            "Cuenta, crédito o tarjeta de crédito de destino - T": ["C"] * 20,
            "Cuenta, crédito o tarjeta de crédito de destino - M": ["S/"] * 20,
            "Cuenta, crédito o tarjeta de crédito de destino - Número": ["305-0037523-0-27"] * 20,
            "Monto abonado - Moneda": ["S/"] * 20,
            "Monto abonado": [
                12430.97, 11263.82, 9945.67, 15475.77, 3714.89, 1489.25, 14072.47, 4540.68,
                3308.18, 17776.66, 27077.20, 3273.67, 5731.50, 74744.11, 19755.35, 2170.02,
                2833.84, 3083.79, 1690.70, 43.24
            ],
            "Estado": ["Procesada"] * 20,
            "Observación": ["Ninguna"] * 20
        }
        movimientoProveedores = {
            'Fecha': ['27/07/2023'],
            'Fecha valuta': [''],
            'Descripción operación': ['VARIOS KALLPA GENERACI'],
            'Monto': [234421.78],
            'Saldo': [2672535.72],
            'Sucursal - agencia': ['111-008'],
            'Operación - Número': ['09789286'],
            'Operación - Hora': ['13:32:02'],
            'Usuario': ['TNP101'],
            'UTC': ['2401'],
            'Referencia2': ['0000010041']
        }
        proveedores_teste = pd.DataFrame(proveedores)    
        movimientos =  pd.DataFrame(movimientoProveedores)
        proveedoresService = ProviderService()
        accountService = AccountService()   
        accountService._process_movements_df(movimientos)
        proveedoresService.setMovimientos(accountService.movimientos)  
        proveedoresService._process_providers_df(proveedores_teste) 
        
          # Realiza las aserciones correspondientes para verificar los resultados
        self.assertEqual( proveedoresService.movimientos["Referencia"][0],"KALLPA GENERACION SA")  # Aserciones de prueba según lo que esperas
 
    def test_proveedores_06(self):
        proveedores = {
            "Ordenante - Nombre o Razón Social": ["CELEPSA RENOVABLES SRL"],
            "Ordenante - RUC/DNI": ["RUC"],
            "Ordenante - Número": ["20422764136"],
            "Documento - Tipo": ["Factura del proveedor"],
            "Nº de documento": ["000000000014007"],
            "Fecha de pago": ["01/08/2023"],
            "Cuenta, crédito o tarjeta de crédito de destino - T": ["C"],
            "Cuenta, crédito o tarjeta de crédito de destino - M": ["S/"],
            "Cuenta, crédito o tarjeta de crédito de destino - Número": ["305-0037523-0-27"],
            "Monto abonado - Moneda": ["S/"],
            "Monto abonado": [0.06],
            "Estado": ["Procesada"],
            "Observación": ["Ninguna"]
        }

        movimientoProveedores = {
            "Fecha": ["01/08/2023"],
            "Fecha valuta": [""],  # This field appears to be empty in the given data
            "Descripción operación": ["0000014007 CELEPSA REN"],
            "Monto": [0.06],
            "Saldo": ["11,834,790.39"],  # You might want to represent this as a float or integer based on use-case
            "Sucursal - agencia": ["111-008"],
            "Operación - Número": ["01248993"],
            "Operación - Hora": ["16:55:55"],
            "Usuario": ["TNP100"],
            "UTC": ["2401"],
            "Referencia2": ["Pago Fact.14007"]
        }
        proveedores_teste = pd.DataFrame(proveedores)    
        movimientos =  pd.DataFrame(movimientoProveedores)
        proveedoresService = ProviderService()
        accountService = AccountService()   
        accountService._process_movements_df(movimientos)
        proveedoresService.setMovimientos(accountService.movimientos)  
        proveedoresService._process_providers_df(proveedores_teste) 
        
          # Realiza las aserciones correspondientes para verificar los resultados
        self.assertEqual( proveedoresService.movimientos["Referencia"][0],"CELEPSA RENOVABLES SRL")  # Aserciones de prueba según lo que esperas
 
    def test_recaudos_EFECTIVO(self):
        
        movimientoProveedores = {
            "Fecha": ["09/08/2023"],
            "Fecha valuta": [""],  # This field appears to be empty in the given data
            "Descripción operación": ["EFECTIVO00000027149820"],
            "Monto": [2832.16],
            "Saldo": ["2,597,597.93"],  # You might want to represent this as a float or integer based on use-case
            "Sucursal - agencia": ["111-008"],
            "Operación - Número": ["01248993"],
            "Operación - Hora": ["16:55:55"],
            "Usuario": ["TNP100"],
            "UTC": ["2401"],
            "Referencia2": ["Pago Fact.14007"]
        }
        movimientos = pd.DataFrame(movimientoProveedores)
        accountService = AccountService()   
        accountService._process_movements_df(movimientos)
        self.assertEqual( accountService.movimientos["Procendecias"][0],"COD.RECAUDO")  # Aserciones de prueba según lo que esperas
        
        # Realiza las aserciones correspondientes para verificar los resultados
 
    def test_transferencias_consorcio_electrico_villacuri(self):
        
        traferedatos =   {
            "Ordenante": ["CONSORCIO ELECTRICO DE VILLACURI S.A.C."],
            "Fecha de abono": ["27/07/2023"],
            "Cuenta - T": ["C"],
            "Cuenta - M": ["S/"],
            "Cuenta - Número": ["305-0037523-0-27"],
            "Monto de operación - Moneda": ["S/"],
            "Monto de operación": [166916.42],
            "Monto de operación T/C": ["0.00"],
            "Monto abonado - Moneda": ["S/"],
            "Monto abonado": [166916.42]
        }
        movimientosTraferencias = {
            "Fecha": ["27/07/2023"],
            "Fecha valuta": [""],
            "Descripción operación": ["DE CONSORCIO ELECTRICO"],
            "Monto": [166916.42],
            "Saldo": [2438113.94],
            "Sucursal - agencia": ["111-008"],
            "Operación - Número": ["03070075"],
            "Operación - Hora": ["16:11:01"],
            "Usuario": ["TNP0UA"],
            "UTC": ["2401"],
            "Referencia2": [""]
        }
        traferencias =pd.DataFrame(traferedatos)
        
        movimientos = pd.DataFrame(movimientosTraferencias)
        inteService = TransferService()
        accountService = AccountService()   
        accountService._process_movements_df(movimientos)
        inteService.setMovimientos(accountService.movimientos)  
            
        inteService._process_transfers_df(traferencias)  
        self.assertEqual( inteService.movimientos["Referencia"][0],"CONSORCIO ELECTRICO DE VILLACURI S.A.C.")
    
    def test_emp_regional_serv_publico(self):
        
        transfer =   {
    "Ordenante": ["EMPRESA REGIONAL DE SERVICIO PUBLICO DE ELECTRICIDAD DEL NORTE S.A."],
    "Fecha de abono": ["09/08/2023"],
    "Cuenta - T": ["C"],
    "Cuenta - M": ["S/"],
    "Cuenta - Número": ["305-0037523-0-27"],
    "Monto de operación - Moneda": ["S/"],
    "Monto de operación": ["1,180,000.00"],
    "T/C": ["0.00"],
    "Monto abonado - Moneda": ["S/"],
    "Monto abonado": ["1,180,000.00"]
}
        movimientos = {
    "Fecha": ["09/08/2023"],
    "Fecha valuta": [""],
    "Descripción operación": ["DE EMP.REG.DE SERV.PUB"],
    "Monto": ["1,180,000.00"],
    "Saldo": ["4398085"],
    "Sucursal - agencia": ["111-008"],
    "Operación - Número": ["03026831"],
    "Operación - Hora": ["12:51:58"],
    "Usuario": ["TNP131"],
    "UTC": ["2406"],
    "Referencia2": [""],
    "Referencia": [""],
    "Procendecias": [""]
}
        df_transfer =pd.DataFrame(transfer)
        
        df_movimientos = pd.DataFrame(movimientos)
        transferService = TransferService()
        accountService = AccountService()   
        accountService._process_movements_df(df_movimientos)
        transferService.setMovimientos(accountService.movimientos)  
            
        transferService._process_transfers_df(df_transfer)  
        self.assertEqual( transferService.movimientos["Referencia"][0],"EMPRESA REGIONAL DE SERVICIO PUBLICO DE ELECTRICIDAD DEL NORTE S.A.")
    

    def test_cable_nortetv(self):
        
        transfer =   {
    "Ordenante": ["CABLENORTV SAC"],
    "Fecha de abono": ["04/08/2023"],
    "Cuenta - T": ["C"],
    "Cuenta - M": ["S/"],
    "Cuenta - Número": ["305-0037523-0-27"],
    "Monto de operación - Moneda": ["S/"],
    "Monto de operación": ["2,390.37"],
    "T/C": ["0.00"],
    "Monto abonado - Moneda": ["S/"],
    "Monto abonado": ["2,390.37"]
}
        movimientos =  {
    "Fecha": ["04/08/2023"],
    "Fecha valuta": [""],
    "Descripción operación": ["DE CABLENORTV SAC"],
    "Monto": ["2,390.37"],
    "Saldo": ["1660931.09"],
    "Sucursal - agencia": ["111-008"],
    "Operación - Número": ["03032687"],
    "Operación - Hora": ["12:45:53"],
    "Usuario": ["TNP0R4"],
    "UTC": ["2401"],
    "Referencia2": [""],
    "Referencia": [""]
}
        df_transfer =pd.DataFrame(transfer)
        
        df_movimientos = pd.DataFrame(movimientos)
        transferService = TransferService()
        accountService = AccountService()   
        accountService._process_movements_df(df_movimientos)
        transferService.setMovimientos(accountService.movimientos)  
            
        transferService._process_transfers_df(df_transfer)  
        self.assertEqual( transferService.movimientos["Referencia"][0],"CABLENORTV SAC")
    
    def test_asiento(self):
        movimientosAsientos ={
            "Fecha": ["04/07/2023"],
            "Fecha valuta": [""],
            "Descripción operación": ["BCO.NACI0000"],
            "Monto": ["5723.2"],
            "Saldo": ["4426163.58"],
            "Sucursal - agencia": ["191-000"],
            "Operación - Número": ["08555500"],
            "Operación - Hora": ["16:39:14"],
            "Usuario": ["RCJN"],
            "UTC": ["2014"],
            "Referencia2": [""],
            "Referencia": ["CONTRALORIA GRAL DE LA REPUBLICA 03"],
            "Procendecias": [""]
        }
        export_teste = {
            "Documento compras": [1041032011],
            "Icono part.abiertas/comp.": [""],
            "Acreedor": [""],
            "Cuenta": [7000013520],
            "Fecha de documento": ["4/07/2023"],
            "Fe.contabilización": ["6/07/2023"],
            "Nº documento": [7000013520],
            "Clase de documento": ["DI"],
            "Referencia": [600737402],
            "Doc.compensación": ["230707"],
            "Texto": [0.00],
            "Moneda del documento": ["PEN"],
            "Importe en moneda local": [5723.2],
            "División": [212],
            "Ejercicio / mes": ["2023/07"],
            "Nombre del usuario": ["INT-OPTIMUS"],
            "Clave contabiliz.": [40],
            "Asignación": ["555500"],
            "Indicador Debe/Haber": ["S"],
            "Importe en ML2": [1576.64],
            "Centro de coste": [""],
            "Centro de beneficio": [""]
        }



        
        movimiento_teste = pd.DataFrame(movimientosAsientos)
        export_teste = pd.DataFrame(export_teste)
        asientoService = AsientoService()
        asientoService._conciliar_df(movimiento_teste, export_teste)
        self.assertEqual(asientoService.df_movimientos["Asientos"][0],7000013520)
    


if __name__ == '__main__':
    unittest.main()
