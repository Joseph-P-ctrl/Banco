import unittest
from AsientoService import AsientoService

class TestReadExcel(unittest.TestCase):
    def test_read_excel(self):
        movimiento_teste = '_test_/data/movimientos-tester.xlsx'
        export_teste = '_test_/data//export-tester.xlsb'
        asientoService = AsientoService()
            
        asientoService.conciliar(movimiento_teste, export_teste)  
        
    # def test_al_decima(self):
    #     numero_asiento = '7000014929.0'
    #     asientoService = AsientoService()
    #     asientoService.convert_to_decimal(numero_asiento)    


if __name__ == '__main__':
    unittest.main()
