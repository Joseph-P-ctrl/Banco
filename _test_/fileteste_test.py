import unittest

import pandas as pd
# from AsientoService import AsientoService

from TransferService import TransferService
from ProviderService import ProviderService
from AccountService import AccountService

class TestReadExcel(unittest.TestCase):
    def test_read_excel(self):
        movimiento_teste = '_test_/data/movimientos-tester.xlsx'
        export_teste = '_test_/data//export-tester.xlsb'
        asientoService = AsientoService()
        # create data frame
        data = {[{
                        "Fecha": "30/07/2023",
                        "Fecha valuta": "",
                        "Descripción operación": "COMIS.RECAUDACION",
                        "Monto": -13,
                        "Saldo": "2659520,87",
                        "Sucursal - agencia": "305-000",
                        "Operación - Número": "00804290",
                        "Operación - Hora": "00:00:00",
                        "Usuario": "BATCH",
                        "UTC": 4983,
                        "Referencia2": "",
                        "Referencia": "",
                        "Procendecias": ""
        }]}
        df_movimientos = pd.DataFrame(data)
        asientoService.conciliar(movimiento_teste, export_teste)

    # def test_al_decima(self):
    #     numero_asiento = '7000014929.0'
    #     asientoService = AsientoService()
    #     asientoService.convert_to_decimal(numero_asiento)


if __name__ == '__main__':
    unittest.main()
