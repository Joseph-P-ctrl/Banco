import os
import pandas as pd
from datetime import datetime
from flask_session import Session
from flask_caching import Cache
import json

class MyCustomException(Exception):
        pass

class BaseDatosService:
    def removeFiles(self, fileName):
        directory_path = "BD"  # Current directory
        
        # List all files in the directory that contain the substring
        matching_files = [f for f in os.listdir(directory_path) if fileName in f and os.path.isfile(os.path.join(directory_path, f))]
        # Print the matching files
        for file_name in matching_files:
            path_file = os.path.join(directory_path, file_name)
            if os.path.exists(path_file):
                os.remove(path_file)
    def GuardarAchivos(self, files):
        RECAUDO = "RECAUDO"
        PREPAGO = "PREPAGO"
        TRABAJADOR = "TRABAJADOR"
        config = {
            "RECAUDOS": "CODIGO RECAUDO.xlsx",
            "PREPAGOS": "PREPAGOS.xlsx",
            "TRABAJADORES": "TRABAJADORES.xlsx"
        }
        try:
            for file in files:
                if file:
                    filename = file.filename.upper()
                    if RECAUDO in filename:
                         config["RECAUDOS"] = filename
                         self.removeFiles(RECAUDO)
                    elif PREPAGO in filename:  
                        config["PREPAGOS"] = filename   
                        self.removeFiles(PREPAGO)
                    elif TRABAJADOR in filename : 
                        config["TRABAJADORES"] = filename   
                        self.removeFiles(TRABAJADOR)
                    file_path = os.path.join('BD', filename)

                    file.save(file_path)
            
            # Save to a JSON file
            config_path = os.path.join('BD', 'config.json')
            with open(config_path, 'w') as myfile:
                json.dump(config, myfile, indent=4)  # The `indent` parameter makes the output more readable
              
        except Exception as ex:
            raise ex


