import traceback
from util.db_connection import Db_Connection
import pandas as pd

def cargar_Vendedor():

    try:
        # Conexión con la base de datos 'staging'
        con_db_stg = Db_Connection('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'staging')
        ses_db_stg = con_db_stg.start()
        if ses_db_stg == -1:
            raise Exception("El tipo de base de datos no es válido")
        elif ses_db_stg == -2:
            raise Exception("Error al establecer la conexión de pruebas")

        # Extraer datos de 'staging'
        sql_stmt = "SELECT idVendedor, nombreCompleto, apellidoCompleto, cedula FROM ext_Vendedor"
        vendedores_tra = pd.read_sql(sql_stmt, ses_db_stg)

        # Conexión con la base de datos 'sor'
        con_db_sor = Db_Connection('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'sor')
        ses_db_sor = con_db_sor.start()
        if ses_db_sor == -1:
            raise Exception("El tipo de base de datos no es válido")
        elif ses_db_sor == -2:
            raise Exception("Error al establecer la conexión de pruebas") 

        # Crear diccionario para transformar los datos
        dim_vendedor_dict = {
            "vendedor_key": [],
            "idVendedor": [],
            "nombreCompleto": [],
            "apellidoCompleto": [],
            "cedula": []
        }

        # Llenar el diccionario con los datos
        if not vendedores_tra.empty:
            for key, id, nombre, apellido, ced in zip(vendedores_tra['idVendedor'], vendedores_tra['idVendedor'], vendedores_tra['nombreCompleto'], vendedores_tra['apellidoCompleto'], vendedores_tra['cedula']):
                dim_vendedor_dict['vendedor_key'].append(key)
                dim_vendedor_dict['idVendedor'].append(id)
                dim_vendedor_dict['nombreCompleto'].append(nombre)
                dim_vendedor_dict['apellidoCompleto'].append(apellido)
                dim_vendedor_dict['cedula'].append(ced)

        # Convertir el diccionario en un DataFrame y cargarlo en 'sor'
        if dim_vendedor_dict['vendedor_key']:
            df_dim_vendedor = pd.DataFrame(dim_vendedor_dict)
            df_dim_vendedor.to_sql('dim_Vendedor', ses_db_sor, if_exists='append', index=False)

    except:
        traceback.print_exc()
    finally:
        # Opcionalmente, aquí podrías cerrar las conexiones a la base de datos
        pass


