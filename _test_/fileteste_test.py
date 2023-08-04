import unittest

import pandas as pd
# from AsientoService import AsientoService

from TransferService import TransferService
from ProviderService import ProviderService
from AccountService import AccountService

class TestReadExcel(unittest.TestCase):
    def test_proveedores(self):
        proveedores_teste = '_test_/data/PROVIDERS_RECEIVED_PAYMENTS.xlsx'
        movimientos = '_test_/data/MOVIMIENTOS-TESTER.xlsx'
        proveedoresService = ProviderService()
        accountService = AccountService()   
        accountService.process_movements(movimientos)
        proveedoresService.setMovimientos(accountService.movimientos)  
        proveedoresService.process_providers(proveedores_teste)  
    
    def test_tgransfee(self):
        traferencias = '_test_/data/TRANSFER_TESTER.xlsx'
        movimientos = '_test_/data/MOVIMIENTOS-TRAFES-TESTER.xlsx'
        inteService = TransferService()
        accountService = AccountService()   
        accountService.process_movements(movimientos)
        inteService.setMovimientos(accountService.movimientos)  
            
        inteService.process_transfers(traferencias)  
    # def test_read_excel(self):
    #     movimiento_teste = 'movimientos (68).xlsx'
    #     export_teste = 'export (2).xlsb'
    #     asientoService = AsientoService()
    #     asientoService.conciliar(movimiento_teste, export_teste)  
    # 
    
    # def test_al_decima(self):
    #     numero_asiento = '7000014929.0'
    #     asientoService = AsientoService()
    #     asientoService.convert_to_decimal(numero_asiento)    


if __name__ == '__main__':
    unittest.main()
