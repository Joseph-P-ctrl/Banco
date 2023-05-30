from flask import Flask, jsonify, render_template, request
from BankService import BankService

import pandas as pd
app = Flask(__name__)

TRANSFER = "TRANSFER"
PROVIDERS = "PROVIDERS"
INTERBANK = "INTERBANK"
MOVIMIENTOS = "MOVIMIENTOS"

@app.route('/')
def home():
    return render_template('upload_movements.html')

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message='Hello, World!')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        
        files = request.files.getlist('file')
        bankService = BankService()    
        for file in files:
            # Read the content of each file
            #content = file.read().decode().strip()
            nombre =  file.filename.upper() 
            
            if (nombre != ""):
                if MOVIMIENTOS in nombre:
                    bankService.process_movements(file)
                elif TRANSFER in nombre:  
                    bankService.process_transfers(file)
                elif INTERBANK in nombre:
                     bankService.process_interbanks(file)
                elif PROVIDERS in nombre:
                    bankService.process_providers(file)    
                    
                else:
                    raise Exception("Archivo no ubicado")    
        movements =     [project for project in bankService.errors if project.category == MOVIMIENTOS]
        transfers =  [project for project in bankService.errors if project.category == TRANSFER]
        interbanks = [project for project in bankService.errors if project.category == INTERBANK]
        providers = [project for project in bankService.errors if project.category == PROVIDERS]
        return render_template("response.html", data= {"movements": movements, "providers": providers, "transfers": transfers, "interbanks": interbanks})
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500

@app.route('/process', methods=['POST'])
def process():
    try:
        files = request.files.getlist('file')

        # Check if at least one file was uploaded
        if len(files) <= 1:
            return 'Debe subir por lo menos un archivo.'

        file_contents = []
        for file in files:
            # Read the content of each file
            #content = file.read().decode().strip()
             bankService = BankService.process_file(file)
            #file_contents.append(content)
    except Exception as e:
        return jsonify({'error': str(e)})     
if __name__ == '__main__':
    app.run(debug=True)


    