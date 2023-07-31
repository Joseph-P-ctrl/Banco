from flask import Flask, jsonify, render_template, request, send_file, session, redirect, url_for
from AccountService import AccountService
from InterbankService import InterbankService
from ProviderService import ProviderService
from TransferService import TransferService
from BaseDatosService import BaseDatosService
from AsientoService import AsientoService
from io import BytesIO
from flask_session import Session
from flask_caching import Cache
from openpyxl import load_workbook
import pandas as pd
import os
import openpyxl
from openpyxl import Workbook
app = Flask(__name__)
app.secret_key = 'AldoAbril1978'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

TRANSFER = "TRANSFER"
PROVIDERS = "PROVIDER"
INTERBANK = "INTERBAN"
CUENTA = "MOVIMIENT"
MOVIMIENTOS = "MOVIMIENTOS"
ASIENTO= "EXPORT"

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        files = request.files.getlist('file')
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
                            raise Exception("Archivo no ubicado: "+nombre)    
                cache.set('movimientos', accountService.movimientos, timeout=600)
                resumen = {"movements": accountService.error, "providers": providerService.error, "transfers": transferService.error, "interbanks": interbankService.error}
                cache.set('resumen', resumen)
                return redirect(url_for('upload'))
            except Exception as e:
                error_message = str(e)
                return render_template('home.html', error_message= error_message)
    else:
        return render_template('home.html')
@app.route('/basedatos', methods=['POST','GET'])
def basedatos():
    if request.method == 'POST':
        files    = request.files.getlist('file')
        
        try:
            filtered_files = [x for x in files if x.filename!=""]
                        
            if len(filtered_files) < 1:
                return render_template('base-datos.html', error_message= 'Debe subir por lo menos un archivo.')
            mensaje_exito = 'Archivo subido correctamente.'
            
            base_datos_service = BaseDatosService()  
            base_datos_service.GuardarAchivos(files)  
            return render_template('base-datos.html',mensaje_exito=mensaje_exito)
                
        except Exception as e:
            error_message = str(e)
            return render_template('base-datos.html', error_message= error_message)

    else:
        nohay = 'Archivo subido correctamente.'
        return render_template('base-datos.html')
    
@app.route('/asiento', methods=['POST','GET'])

def asiento():
    if request.method == 'POST':
          files = request.files.getlist('file')
          filtered_files = [x for x in files if x.filename!=""]
          if len(filtered_files) <= 1:
            return render_template('asiento.html', error_message= 'Debe subir por lo menos un archivo.')
          else:
            try:
                asientoService = AsientoService()    
                for file in files:
                    nombre =  file.filename.upper() 
                 
                    if (nombre != ""):
                        if MOVIMIENTOS in nombre:
                            movimientosfile= file
                        elif   ASIENTO in nombre:
                            asientosfile = file
                        else:
                            raise Exception("Archivo no ubicado: "+nombre)    
                movimientosAsientos=asientoService.conciliar(movimientosfile, asientosfile)
                print(movimientosAsientos)
                cache.set('movimientosAsientos', asientoService.resultadosMovimiento, timeout=600)
                return redirect(url_for('respuestaasiento'))
            except Exception as e:
                error_message = str(e)
                return render_template('asiento.html', error_message= error_message)
    else:
        return render_template('asiento.html')




@app.route('/upload', methods=['POST','GET'])
def upload():
    
    if request.method == 'POST':
        movimientos = cache.get("movimientos")
        movimientos["Fecha"] = pd.to_datetime(movimientos["Fecha"], format="%d/%m/%Y").dt.strftime("%d/%m/%Y")
        
                
        excel_file = BytesIO()
        movimientos.to_excel(excel_file, index=False)

        workbook = openpyxl.load_workbook(excel_file)
        worksheet = workbook.active 

        worksheet.column_dimensions["A"].width = 20  
        worksheet.column_dimensions["C"].width = 30  
        worksheet.column_dimensions["K"].width = 40  
        worksheet.column_dimensions["L"].width = 40  
        worksheet.column_dimensions["M"].width = 35 

        ruta_archivo = 'files/movimientos.xlsx'
        workbook.save(ruta_archivo)

        return send_file(ruta_archivo, as_attachment=True, download_name="movimientos.xlsx")
    else:
        data = cache.get('resumen')  
        return render_template("response.html", data= data)
    
    
    
    
@app.route('/respuestaasiento', methods=['POST','GET'])
def respuestaasiento():
    
    if request.method == 'POST':
        movimientosAsientos = cache.get("movimientosAsientos")
        
        movimientosAsientos["Fecha"] = pd.to_datetime(movimientosAsientos["Fecha"], format="%d/%m/%Y").dt.strftime("%d/%m/%Y")
        excel_file = BytesIO()
        movimientosAsientos.to_excel(excel_file, index=False)
        workbook = openpyxl.load_workbook(excel_file)
        worksheet = workbook.active 
        worksheet.column_dimensions["A"].width = 20  
        worksheet.column_dimensions["C"].width = 30  
        worksheet.column_dimensions["K"].width = 40  
        worksheet.column_dimensions["L"].width = 40  
        worksheet.column_dimensions["M"].width = 35 
        worksheet.column_dimensions["N"].width = 28 

        ruta_archivo = 'files/movimientos.xlsx'
        workbook.save(ruta_archivo)

        return send_file(ruta_archivo, as_attachment=True, download_name="Asiento.xlsx")
    else:
        data = cache.get('movimientosAsientos')
        return render_template("responseasiento.html", data= data)



if __name__ == '__main__':
   app.run(host='0.0.0.0')
#    app.run(debug=True)

    