import traceback
from util.db_connection import Db_Connection
import pandas as pd

def cargar_Ciudad():

    try:
        # Conexión con la base de datos 'staging'
        con_db_stg = Db_Connection('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'staging')
        ses_db_stg = con_db_stg.start()
        if ses_db_stg == -1:
            raise Exception("El tipo de base de datos no es válido")
        elif ses_db_stg == -2:
            raise Exception("Error al establecer la conexión de pruebas")

        # Extraer datos de 'staging'
        sql_stmt = "SELECT idCiudad, nombre, provincia FROM ext_Ciudad"
        ciudades_tra = pd.read_sql(sql_stmt, ses_db_stg)

        # Conexión con la base de datos 'sor'
        con_db_sor = Db_Connection('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'sor')
        ses_db_sor = con_db_sor.start()
        if ses_db_sor == -1:
            raise Exception("El tipo de base de datos no es válido")
        elif ses_db_sor == -2:
            raise Exception("Error al establecer la conexión de pruebas") 

        # Crear diccionario para transformar los datos
        dim_ciudad_dict = {
            "ciudad_key": [],
            "idCiudad": [],
            "nombre": [],
            "provincia": []
        }

        # Llenar el diccionario con los datos
        if not ciudades_tra.empty:
            for key, id, nom, prov in zip(ciudades_tra['idCiudad'], ciudades_tra['idCiudad'], ciudades_tra['nombre'], ciudades_tra['provincia']):
                dim_ciudad_dict['ciudad_key'].append(key)
                dim_ciudad_dict['idCiudad'].append(id)
                dim_ciudad_dict['nombre'].append(nom)
                dim_ciudad_dict['provincia'].append(prov)

        # Convertir el diccionario en un DataFrame y cargarlo en 'sor'
        if dim_ciudad_dict['ciudad_key']:
            df_dim_ciudad = pd.DataFrame(dim_ciudad_dict)
            df_dim_ciudad.to_sql('dim_Ciudad', ses_db_sor, if_exists='append', index=False)

    except:
        traceback.print_exc()
    finally:
        pass

