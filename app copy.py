from flask import Flask, jsonify, render_template, request, send_file, session, redirect, url_for
from AccountService import AccountService
from InterbankService import InterbankService
from ProviderService import ProviderService
from TransferService import TransferService

from io import BytesIO
from flask_session import Session
from flask_caching import Cache
from openpyxl import load_workbook
import openpyxl


import pandas as pd
app = Flask(__name__)
app.secret_key = 'AldoAbril1978'
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the file system
Session(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

TRANSFER = "TRANSFER"
PROVIDERS = "PROVIDER"
INTERBANK = "INTERBAN"
CUENTA = "MOVIMIENT"

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        files = request.files.getlist('file')
        # Check if at least one file was uploaded
        filtered_files = [x for x in files if x.filename!=""]
                    
        if len(filtered_files) <= 1:
            return render_template('home.html', error_message= 'Debe subir por lo menos un archivo.')
        else:
            try:
                accountService = AccountService()    
                transferService = TransferService()
                interbankService = InterbankService()
                providerService = ProviderService()
                for file in files:
                    # Read the content of each file
                    #content = file.read().decode().strip()
                    
                    nombre =  file.filename.upper() 
                 
                    if (nombre != ""):
                        if CUENTA in nombre:
                            accountService.process_movements(file)
                            # movimientosServicios = AccountService()
                            # resutadoMovimiento= movimientosServicios.process_movements(file)
                        elif TRANSFER in nombre:  
                            transferService.setMovimientos(accountService.movimientos)
                            transferService.process_transfers(file)
                        elif INTERBANK in nombre:
                            interbankService.setMovimientos(accountService.movimientos)
                            interbankService.process_interbanks(file)
                        elif PROVIDERS in nombre:
                            providerService.setMovimientos(accountService.movimientos)
                            providerService.process_providers(file)    
                            
                        else:
                            raise Exception("Archivo no ubicado"+nombre)    
                
                cache.set('movimientos', accountService.movimientos.to_json(), timeout=600)
                
                # cache.set('resutadoMovimiento',  resutadoMovimiento.to_json(), timeout=600)
                # resumen = {"movements": accountService.error, "providers": providerService.error, "transfers": transferService.error, "interbanks": interbankService.error}
                # cache.set('resumen', resumen)
                return redirect(url_for('upload'))
                
            except Exception as e:
                error_message = str(e)
                return render_template('home.html', error_message= error_message)

    else:
        return render_template('home.html')


@app.route('/upload', methods=['POST','GET'])
def upload():
    
    if request.method == 'POST':
        resutadoMovimiento_json = cache.get("resutadoMovimiento")
        resutadoMovimientocon = pd.read_json(resutadoMovimiento_json)
        # movimientos["Fecha"] = pd.to_datetime(movimientos['Fecha'])
        excel_file = BytesIO()
        
        #movimientos["Fecha"] = movimientos["Fecha"].dt.strftime('%d-%m-%Y')
        resutadoMovimientocon.to_excel(excel_file, index=False)
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active
        sheet.column_dimensions['A'].width = 15  # Ajusta el ancho de la columna A a 15
        sheet.column_dimensions['B'].width = 15  # Ajusta el ancho de la columna B a 20
        sheet.column_dimensions['C'].width = 20  # Ajusta el ancho de la columna B a 20
        sheet.column_dimensions['D'].width = 20  # Ajusta el ancho de la columna B a 20
        
        
        
        excel_file.seek(0)
        # Send the file-like object as a response with appropriate headers
        return send_file(excel_file, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name="movimientos.xlsx")
    else:
        data = cache.get('resutadoMovimientocon')  # Access the query parameter
        data = pd.read_json(data)
        arr = []
        for  row in data.iterrows():
            # print("aqui esta los datos ")
            # print(row[1]["Fecha"])
            # print(row["Fecha valuta"])
            arr.append({
                "Fecha": row[1]["Fecha"],
                "Fecha valuta": row[1]["Fecha valuta"], 
                "Descripción operación": row[1]["Descripción operación"],
                "Saldo": row[1]["Saldo"],
                "Sucursal - agencia": row[1]["Sucursal - agencia"],
                "Operación - Número": row[1]["Operación - Número"],
                "Operación - Hora": row[1]["Operación - Hora"],
                "Usuario": row[1]["Usuario"],
                "UTC": row[1]["UTC"],
                "Referencia2": row[1]["Referencia2"],
                "Referencia": row[1]["Referencia"],
                })
       
        return render_template("response.html", data= data)



if __name__ == '__main__':
   #app.run(host='0.0.0.0')
   app.run(debug=True)

    