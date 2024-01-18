import traceback
from util.db_connection import Db_Connection
import pandas as pd

def cargar_Producto():

    try:
        # Establecer conexión con la base de datos 'staging'
        con_db_stg = Db_Connection('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'staging')
        ses_db_stg = con_db_stg.start()
        if ses_db_stg == -1:
            raise Exception("El tipo de base de datos no es válido")
        elif ses_db_stg == -2:
            raise Exception("Error al establecer la conexión de pruebas")

        # Extraer datos de 'staging'
        sql_stmt = "SELECT idCategoria, idProducto, nombreProducto, nombreCategoria FROM tra_Producto"
        productos_tra = pd.read_sql(sql_stmt, ses_db_stg)

        # Conexión con la base de datos 'sor'
        con_db_sor = Db_Connection('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'sor')
        ses_db_sor = con_db_sor.start()
        if ses_db_sor == -1:
            raise Exception("El tipo de base de datos no es válido")
        elif ses_db_sor == -2:
            raise Exception("Error al establecer la conexión de pruebas") 

        # Crear diccionario para transformar los datos
        dim_producto_dict = {
            "producto_key": [],
            "id_Producto": [],
            "nombreProducto": [],
            "nombreCategoria": []
        }

        # Llenar el diccionario con los datos
        if not productos_tra.empty:
            for key, id, nombre, categoria in zip(productos_tra['idProducto'], productos_tra['idProducto'], productos_tra['nombreProducto'], productos_tra['nombreCategoria']):
                dim_producto_dict['producto_key'].append(key)
                dim_producto_dict['id_Producto'].append(id)
                dim_producto_dict['nombreProducto'].append(nombre)
                dim_producto_dict['nombreCategoria'].append(categoria)

        # Convertir el diccionario en un DataFrame y cargarlo en 'sor'
        if dim_producto_dict['producto_key']:
            df_dim_producto = pd.DataFrame(dim_producto_dict)
            df_dim_producto.to_sql('dim_Producto', ses_db_sor, if_exists='append', index=False)

    except:
        traceback.print_exc()
    finally:
        # Opcionalmente, aquí podrías cerrar las conexiones a la base de datos
        pass


