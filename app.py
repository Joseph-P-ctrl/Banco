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
import re
import logging
import traceback
from storage_paths import ensure_data_dirs, bootstrap_bd_from_source, files_path, logs_path, SESSION_DIR

# setup logging
ensure_data_dirs()
bootstrap_bd_from_source()
logging.basicConfig(filename=logs_path('error.log'), level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
app = Flask(__name__)
app.secret_key = 'AldoAbril1978'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = SESSION_DIR
Session(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

TRANSFER = "TRANSFER"
PROVIDERS = "PROVIDER"
INTERBANK = "INTERBAN"
CUENTA = "MOVIMIENT"
MOVIMIENTOS = "MOVIMIENTOS"
ASIENTO= "EXPORT"

def extract_emails_from_df(df):
    emails = set()
    email_regex = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    for col in df.columns:
        for val in df[col].dropna():
            for m in email_regex.findall(str(val)):
                emails.add(m)
    return sorted(emails)

def extract_emails_from_excel_upload(file_storage):
    emails = set()
    email_regex = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    try:
        file_storage.stream.seek(0)
        workbook = load_workbook(filename=BytesIO(file_storage.read()), data_only=True)
        file_storage.stream.seek(0)

        for ws in workbook.worksheets:
            for row in ws.iter_rows():
                for cell in row:
                    if cell.value is not None:
                        for m in email_regex.findall(str(cell.value)):
                            emails.add(m)
                    if cell.hyperlink and cell.hyperlink.target:
                        target = str(cell.hyperlink.target)
                        if target.lower().startswith('mailto:'):
                            target = target[7:]
                        target = target.split('?', 1)[0]
                        for m in email_regex.findall(target):
                            emails.add(m)
    except Exception:
        # If the file cannot be opened with openpyxl (e.g., unsupported format), fallback to df extraction only
        try:
            file_storage.stream.seek(0)
        except Exception:
            pass
    return sorted(emails)

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
                guardaMovimientos(accountService.movimientos)
                guardaRecaudos(accountService.recaudos)
                resumen = {"movements": accountService.error, "providers": providerService.error, "transfers": transferService.error, "interbanks": interbankService.error}
               
                return render_template("response.html", data= resumen) 
    
                #return redirect(url_for('upload'))
            except Exception as e:
                error_message = str(e)
                return render_template('home.html', error_message= error_message)
    else:
        return render_template('home.html')

def guardaMovimientos(movimientos):
    movimientos["Fecha"] = pd.to_datetime(movimientos["Fecha"], format="%d/%m/%Y").dt.strftime("%d/%m/%Y")
    excel_file = BytesIO()
    movimientos.to_excel(excel_file, index=False)
    excel_file.seek(0)
    workbook = openpyxl.load_workbook(excel_file)
    worksheet = workbook.active 
    worksheet.column_dimensions["A"].width = 20  
    worksheet.column_dimensions["C"].width = 30  
    worksheet.column_dimensions["K"].width = 40  
    worksheet.column_dimensions["L"].width = 40  
    worksheet.column_dimensions["M"].width = 35 
    worksheet.column_dimensions["N"].width = 40
    ruta_archivo = files_path('movimientos.xlsx')
    workbook.save(ruta_archivo)

def guardaRecaudos(recaudos):
    excel_file = BytesIO()
    recaudos.to_excel(excel_file, index=False)
    excel_file.seek(0)
    workbook = openpyxl.load_workbook(excel_file)
    worksheet = workbook.active 
    worksheet.column_dimensions["A"].width = 15  
    worksheet.column_dimensions["B"].width = 50  
    worksheet.column_dimensions["C"].width = 25  
    worksheet.column_dimensions["D"].width = 10  
    worksheet.column_dimensions["E"].width = 15 
    worksheet.column_dimensions["F"].width = 10 

    ruta_archivo = files_path('recaudos.xlsx')
    workbook.save(ruta_archivo)

@app.route('/basedatos', methods=['POST','GET'])
def basedatos():
    if request.method == 'POST':
        files    = request.files.getlist('file')
        
        try:
            filtered_files = [x for x in files if x.filename!=""]
                        
            if len(filtered_files) < 1:
                return render_template('base-datos.html', error_message= 'Debe subir por lo menos un archivo.')

            nombres = [f.filename.upper() for f in filtered_files]
            missing = []
            if not any('CLIENTE' in n for n in nombres):
                missing.append('CLIENTES')
            if not any('RECAUDO' in n for n in nombres):
                missing.append('CODIGO RECAUDO')
            if not any('PREPAGO' in n for n in nombres):
                missing.append('PREPAGOS')
            if not any('TRABAJADOR' in n for n in nombres):
                missing.append('TRABAJADORES')

            if missing:
                return render_template('base-datos.html', error_message='Faltan archivos obligatorios: ' + ', '.join(missing))

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
    
@app.route('/asiento', methods=['POST'])
def asiento_procesar():
    logging.error('asiento_procesar: start')
    files = request.files.getlist('file')
    logging.error('asiento_procesar: received %d files', len(files))
    filtered_files = [x for x in files if x.filename!=""]
    logging.error('asiento_procesar: filtered %d files', len(filtered_files))
    if len(filtered_files) <= 1:
        logging.error('asiento_procesar: not enough files, returning form')
        return render_template('asiento.html', error_message= 'Debe subir ambos archivo.')
    else:
        try:
            asientoService = AsientoService()    
            # detect files: movimientos, asientos, codigo (optional)
            movimientosfile = None
            asientosfile = None
            codigofile = None
            for file in files:
                nombre =  file.filename.upper()
                if (nombre != ""):
                    if MOVIMIENTOS in nombre or "MOVIMIENTO" in nombre:
                        movimientosfile = file
                    elif ASIENTO in nombre:
                        asientosfile = file
                    elif 'CODIG' in nombre or 'CODIGO' in nombre:
                        codigofile = file
                    else:
                        # ignore unknown files for now
                        pass

            if movimientosfile is None or asientosfile is None:
                raise Exception('Faltan archivos Movimientos o Asientos')

            asientoService.conciliar(movimientosfile, asientosfile)
            #solo si hay asientos se completa en el cache
            if asientoService.df_movimientos is not None:
                guardaAsientos(asientoService.df_movimientos)
                # extraer correos desde movimientos resultantes + export/asientos original
                emails = set(extract_emails_from_df(asientoService.df_movimientos))
                if getattr(asientoService, 'df_asientos', None) is not None:
                    emails.update(extract_emails_from_df(asientoService.df_asientos))
                emails.update(extract_emails_from_excel_upload(asientosfile))
                # guardar en session para uso posterior y redirigir al flujo de correos
                sorted_emails = sorted(emails)
                session['asiento_emails'] = sorted_emails
                if len(sorted_emails) == 0:
                    session['asiento_email_warning'] = 'No se encontraron correos en el archivo EXPORT. Verifique que existan direcciones con @ o hipervínculos mailto:.'
                else:
                    session.pop('asiento_email_warning', None)
                # guardaAsientos ya escribió files/asientos.xlsx, descargamos directamente
                ruta_archivo = files_path('asientos.xlsx')
                return send_file(ruta_archivo, as_attachment=True, download_name='asientos.xlsx')
            else: 
                #si hubiera error se pinta la misma pagina y no se redirecciona
                return render_template('asiento.html', error_message= 'No se encontro ningun asiento en el proceso')       
            
        except Exception as e:
            error_message = str(e)
            logging.error('asiento_procesar: exception: %s', error_message)
            return render_template('asiento.html', error_message= error_message)
    # Fallback: ensure the view always returns a response
    logging.error('asiento_procesar: reached end of function without explicit return')
    return render_template('asiento.html', error_message='Error inesperado en el procesamiento')



@app.route('/asiento', methods=['GET'])
def asiento_get():
    return render_template('asiento.html')


@app.route('/correos', methods=['GET','POST'])
def correos():
    if request.method == 'GET':
        # If emails are already in session (set by /asiento), show them immediately
        sess_emails = session.get('asiento_emails')
        warning_message = session.pop('asiento_email_warning', None)
        if sess_emails:
            return render_template('correos.html', emails=sess_emails, mensaje_exito=warning_message)
        # otherwise show the upload/process UI (and allow processing existing file)
        # If an existing asientos file exists, attempt to auto-extract and show
        existing_path = files_path('asientos.xlsx')
        if os.path.exists(existing_path):
            try:
                df = pd.read_excel(existing_path, header=0)
                emails = extract_emails_from_df(df)
                session['asiento_emails'] = emails
                if warning_message:
                    return render_template('correos.html', emails=emails, mensaje_exito=warning_message)
                return render_template('correos.html', emails=emails)
            except Exception:
                pass
        return render_template('correos.html', mensaje_exito=warning_message)
    try:
        # si el formulario pide usar el asientos.xlsx existente
        if request.form.get('use_existing'):
            existing_path = files_path('asientos.xlsx')
            if not os.path.exists(existing_path):
                return render_template('correos.html', emails=[], mensaje_exito='No se encontró asientos.xlsx')
            df = pd.read_excel(existing_path, header=0)
        else:
            file = request.files.get('file')
            if not file or file.filename == '':
                return render_template('correos.html', emails=[], mensaje_exito='No se seleccionó archivo')
            # leer archivo subido con pandas
            df = pd.read_excel(file, header=0)
            file.stream.seek(0)

        emails = extract_emails_from_df(df)
        if not request.form.get('use_existing'):
            emails = sorted(set(emails).union(set(extract_emails_from_excel_upload(file))))
        session['asiento_emails'] = emails
        return render_template('correos.html', emails=emails)
    except Exception as ex:
        return render_template('correos.html', emails=[], mensaje_exito=str(ex))

@app.route('/upload', methods=['POST','GET'])
def upload():
    
    if request.method == 'POST':
        ruta_archivo = files_path('movimientos.xlsx')
        return send_file(ruta_archivo, as_attachment=True, download_name="movimientos.xlsx")
   
    

@app.route('/download_recaudos', methods=['POST'])
def download_recaudos():
    ruta_archivo = files_path('recaudos.xlsx')
    return send_file(ruta_archivo, as_attachment=True, download_name="recaudos.xlsx")

def guardaAsientos(movimientosAsientos):
    movimientosAsientos["Fecha"] = pd.to_datetime(movimientosAsientos["Fecha"], format="%d/%m/%Y").dt.strftime("%d/%m/%Y")
    excel_file = BytesIO()
    movimientosAsientos.to_excel(excel_file, index=False)
    excel_file.seek(0)
    workbook = openpyxl.load_workbook(excel_file)
    worksheet = workbook.active 
    worksheet.column_dimensions["A"].width = 20  
    worksheet.column_dimensions["C"].width = 30  
    worksheet.column_dimensions["K"].width = 40  
    worksheet.column_dimensions["L"].width = 40  
    worksheet.column_dimensions["M"].width = 35 
    worksheet.column_dimensions["N"].width = 28 

    ruta_archivo = files_path('asientos.xlsx')
    workbook.save(ruta_archivo)


@app.route('/download_asientos', methods=['POST'])
def dowload_asientos():
    ruta_archivo = files_path('asientos.xlsx')
    return send_file(ruta_archivo, as_attachment=True, download_name="Asiento.xlsx")


@app.route('/send_emails', methods=['POST'])
def send_emails():
    emails = session.get('asiento_emails', [])
    if not emails:
        return render_template('correos.html', emails=[], mensaje_exito='No hay correos para enviar')
    # crear archivo CSV con los correos para descargar (simula envío)
    csv_path = files_path('emails_to_send.csv')
    try:
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write('email\n')
            for e in emails:
                f.write(e + '\n')
        return send_file(csv_path, as_attachment=True, download_name='emails_to_send.csv')
    except Exception as ex:
        return render_template('correos.html', emails=[], mensaje_exito=str(ex))



@app.errorhandler(Exception)
def handle_exception(e):
     # Log full traceback to file
     tb = traceback.format_exc()
     logging.error('Unhandled exception:\n%s', tb)
     # return a friendly error page
     return render_template('error.html', message=str(e)), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')

    