import traceback
from util.db_connection import Db_Connection
import pandas as pd

def cargar_Fecha():

    try:
        # Conexión con la base de datos 'staging'
        con_db_stg = Db_Connection('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'staging')
        ses_db_stg = con_db_stg.start()
        if ses_db_stg == -1:
            raise Exception("El tipo de base de datos no es válido")
        elif ses_db_stg == -2:
            raise Exception("Error al establecer la conexión de pruebas")

        # Extraer datos de 'staging'
        sql_stmt = "SELECT idFecha, anio, mes, trimestre FROM tra_Fecha"
        fechas_tra = pd.read_sql(sql_stmt, ses_db_stg)

        # Conexión con la base de datos 'sor'
        con_db_sor = Db_Connection('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'sor')
        ses_db_sor = con_db_sor.start()
        if ses_db_sor == -1:
            raise Exception("El tipo de base de datos no es válido")
        elif ses_db_sor == -2:
            raise Exception("Error al establecer la conexión de pruebas") 

        # Crear diccionario para transformar los datos
        dim_fecha_dict = {
            "idFecha": [],
            "anio": [],
            "mes": [],
            "trimestre": []
        }

        # Llenar el diccionario con los datos
        if not fechas_tra.empty:
            for idFecha, anio, mes, trimestre in zip(fechas_tra['idFecha'], fechas_tra['anio'], fechas_tra['mes'], fechas_tra['trimestre']):
                dim_fecha_dict['idFecha'].append(idFecha)
                dim_fecha_dict['anio'].append(anio)
                dim_fecha_dict['mes'].append(mes)
                dim_fecha_dict['trimestre'].append(trimestre)

        # Convertir el diccionario en un DataFrame y cargarlo en 'sor'
        if dim_fecha_dict['anio']:
            df_dim_fecha = pd.DataFrame(dim_fecha_dict)
            df_dim_fecha.to_sql('dim_Fecha', ses_db_sor, if_exists='append', index=False)

    except:
        traceback.print_exc()
    finally:
        # Opcionalmente, aquí podrías cerrar las conexiones a la base de datos
        pass

# Luego puedes llamar a la función cargar_Fecha para realizar la operación
