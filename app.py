from flask import Flask, jsonify, render_template, request, send_file, session, redirect, url_for
from AccountService import AccountService
from InterbankService import InterbankService
from ProviderService import ProviderService
from TransferService import TransferService

from io import BytesIO
from flask_session import Session
from flask_caching import Cache

import pandas as pd
app = Flask(__name__)
app.secret_key = 'AldoAbril1978'
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the file system
Session(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

TRANSFER = "TRANSFER"
PROVIDERS = "PROVEEDOR"
INTERBANK = "INTERBAN"
CUENTA = "CUENTA"

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
                            raise Exception("Archivo no ubicado")    
                
                cache.set('movimientos', accountService.movimientos.to_json(), timeout=600)
                resumen = {"movements": accountService.error, "providers": providerService.error, "transfers": transferService.error, "interbanks": interbankService.error}
                cache.set('resumen', resumen)
                return redirect(url_for('upload'))
                
            except Exception as e:
                error_message = str(e)
                return render_template('home.html', error_message= error_message)

    else:
        return render_template('home.html')


@app.route('/upload', methods=['POST','GET'])
def upload():
    
    if request.method == 'POST':
        movimientos_json = cache.get("movimientos")
        movimientos = pd.read_json(movimientos_json)
        movimientos["Fecha"] = pd.to_datetime(movimientos['Fecha'])
        excel_file = BytesIO()
        
        #movimientos["Fecha"] = movimientos["Fecha"].dt.strftime('%d-%m-%Y')
        movimientos.to_excel(excel_file, index=False)
        excel_file.seek(0)
        # Send the file-like object as a response with appropriate headers
        return send_file(excel_file, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name="movimientos.xlsx")
    else:
        data = cache.get('resumen')  # Access the query parameter
        return render_template("response.html", data= data)



if __name__ == '__main__':
   #app.run(host='0.0.0.0')
   app.run(debug=True)

    