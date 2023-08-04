import unittest
from InterbankService import InterbankService
from ProviderService import ProviderService
    
class Calculos(unittest.TestCase):
    def TransferService(self):
        movimiento_teste = 'movimientos (68).xlsx'
        export_teste = 'export (2).xlsb'
        inteService = InterbankService()
            
        inteService.process_interbanks(movimiento_teste, export_teste)  
    def provedores(self):
        proveedores_teste = 'PROVIDERS_RECEIVED_PAYMENTS1690842415432 (1).xls'
        proveedoresService = ProviderService()
            
        proveedoresService.process_providers(self, proveedores_teste)  
         

if __name__ == '__main__':
    unittest.main()
