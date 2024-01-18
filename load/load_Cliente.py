import traceback
from util.db_connection import Db_Connection
import pandas as pd

def cargar_Cliente():

    try:
        # Conexión con la base de datos 'staging'
        con_db_stg = Db_Connection('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'staging')
        ses_db_stg = con_db_stg.start()
        if ses_db_stg == -1:
            raise Exception("El tipo de base de datos no es válido")
        elif ses_db_stg == -2:
            raise Exception("Error al establecer la conexión de pruebas")

        # Extraer datos de 'staging'
        sql_stmt = "SELECT idCliente, nombre FROM ext_Cliente"
        clientes_tra = pd.read_sql(sql_stmt, ses_db_stg)

        # Conexión con la base de datos 'sor'
        con_db_sor = Db_Connection('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'sor')
        ses_db_sor = con_db_sor.start()
        if ses_db_sor == -1:
            raise Exception("El tipo de base de datos no es válido")
        elif ses_db_sor == -2:
            raise Exception("Error al establecer la conexión de pruebas") 

        # Crear diccionario para transformar los datos
        dim_cliente_dict = {
            "cliente_key": [],
            "idCliente": [],
            "nombre": []
        }

        # Llenar el diccionario con los datos
        if not clientes_tra.empty:
            for key, id, nom in zip(clientes_tra['idCliente'], clientes_tra['idCliente'], clientes_tra['nombre']):
                dim_cliente_dict['cliente_key'].append(key)
                dim_cliente_dict['idCliente'].append(id)
                dim_cliente_dict['nombre'].append(nom)

        # Convertir el diccionario en un DataFrame y cargarlo en 'sor'
        if dim_cliente_dict['cliente_key']:
            df_dim_cliente = pd.DataFrame(dim_cliente_dict)
            df_dim_cliente.to_sql('dim_Cliente', ses_db_sor, if_exists='append', index=False)

    except:
        traceback.print_exc()
    finally:
        pass


