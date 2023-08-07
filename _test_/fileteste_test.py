import unittest

import pandas as pd
from AsientoService import AsientoService
from TransferService import TransferService
from ProviderService import ProviderService
from AccountService import AccountService

class TestReadExcel(unittest.TestCase):
    def test_proveedores(self):
        proveedores = {
            'nombre': ['KALLPA GENERACION SA'],
            'ruc_dni': ['RUC'],
            'numero': ['20538810682'],
            'tipo_documento': ['Factura del proveedor'],
            'numero_documento': ['00F061-00013868'],
            'fecha_pago': ['27/07/2023'],
            'cuenta_destino_t': ['C'],
            'cuenta_destino_m': ['S/'],
            'cuenta_destino_numero': ['305-0037523-0-27'],
            'monto_abonado_moneda': ['S/'],
            'monto_abonado': ['12430.97'],
            'estado': ['Procesada'],
            'observacion': ['Ninguna']
        }
        movimientoProveedores = {
            'Fecha': ['27/07/2023'],
            'Fecha valuta': [''],
            'Descripción operación': ['VARIOS KALLPA GENERACI'],
            'Monto': ['234,421.78'],
            'Saldo': ['2,672,535.72'],
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
        proveedoresService._process_providers(proveedores_teste)  
    
    def test_tgransfee(self):
        traferedatos =   {
            "Ordenante": ["CONSORCIO ELECTRICO DE VILLACURI S.A.C."],
            "Fecha de abono": ["27/07/2023"],
            "Cuenta - T": ["C"],
            "Cuenta - M": ["S/"],
            "Cuenta - Número": ["305-0037523-0-27"],
            "Monto de operación - Moneda": ["S/"],
            "Monto de operación": ["166,916.42"],
            "Monto de operación T/C": ["0.00"],
            "Monto abonado - Moneda": ["S/"],
            "Monto abonado": ["166,916.42"]
        }
        movimientosTraferencias = {
            "Fecha": ["27/07/2023"],
            "Fecha valuta": [""],
            "Descripción operación": ["DE CONSORCIO ELECTRICO"],
            "Monto": ["166,916.42"],
            "Saldo": ["2,438,113.94"],
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
    
    
    def test_read_excel(self):
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
        export_teste =  {
            "Documento compras": [""],
            "Icono part.abiertas/comp.": [""],
            "Acreedor": [""],
            "Cuenta": ["6500004868"],
            "Fecha de documento": ["26/07/2023"],
            "Fe.contabilización": ["26/07/2023"],
            "Nº documento": ["F061-13822"],
            "Clase de documento": ["DZ"],
            "Referencia": ["230726"],
            "Doc.compensación": [""],
            "Texto": [""],
            "Moneda del documento": ["PEN"],
            "Importe en moneda local": ["13170.07"],
            "División": ["0212"],
            "Ejercicio / mes": ["2023/07"],
            "Nombre del usuario": ["JEREFI200-2"],
            "Clave contabiliz.": ["40"],
            "Asignación": ["0371937"],
            "Indicador Debe/Haber": ["S"],
            "Importe en ML2": ["3654.29"],
            "Centro de coste": [""],
            "Centro de beneficio": [""]
        }


        
        movimiento_teste = pd.DataFrame(movimientosAsientos)
        export_teste = pd.DataFrame(export_teste)
        asientoService = AsientoService()
        asientoService._conciliar_df(movimiento_teste, export_teste)


if __name__ == '__main__':
    unittest.main()
