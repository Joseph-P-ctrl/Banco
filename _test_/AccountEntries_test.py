import unittest

import pandas as pd
from AsientoService import AsientoService

class AccountEntries_test(unittest.TestCase):
    def test_contraloria_gral_republica(self):
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
                "Procedencia": [""]
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


    def test_asiento_guivar_silva(self):
                movimientos_data ={
        'Fecha': ['15/08/2023'],
        'Fecha valuta': [None],
        'Descripción operación': ['EFECTIVO00000025788302'],
        'Monto': [50],
        'Saldo': [4202405.12],
        'Sucursal - agencia': ['111-017'],
        'Operación - Número': [555716],
        'Operación - Hora': ['14:36:02'],
        'Usuario': [988379],
        'UTC': [1013],
        'Referencia2': [None],
        'Referencia': ['GUIVAR SILVA, MARIA CONSUELO'],
        'Procedencia': ['PREPAGO']
    }
                export_data = {
                    "Documento compras": [1041032011],
                    "Icono part.abiertas/comp.": [""],
                    "Acreedor": [""],
                    "Cuenta": [7000017736],
                    "Fecha de documento": ["4/07/2023"],
                    "Fe.contabilización": ["6/07/2023"],
                    "Nº documento": [7000017736],
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
                    "Asignación": ["0555716"],
                    "Indicador Debe/Haber": ["S"],
                    "Importe en ML2": [1576.64],
                    "Centro de coste": [""],
                    "Centro de beneficio": [""]
                }
                
                movimiento_teste = pd.DataFrame(movimientos_data)
                export_teste = pd.DataFrame(export_data)
                asientoService = AsientoService()
                asientoService._conciliar_df(movimiento_teste, export_teste)
                self.assertEqual(asientoService.df_movimientos["Asientos"][0],7000017736)
