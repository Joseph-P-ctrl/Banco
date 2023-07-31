import os
import pandas as pd
from datetime import datetime
from flask_session import Session
from flask_caching import Cache


class MyCustomException(Exception):
        pass

class BaseDatosService:
     
    def GuardarAchivos(self, files):
        try:
            for file in files:
                if file:
                    filename = file.filename
                    file_path = os.path.join('BD', filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    file.save(file_path)
            
        except Exception as ex:
            raise ex


