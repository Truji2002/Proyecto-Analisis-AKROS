import traceback
from util.db_connection import Db_Connection
import pandas as pd

def transformar_producto():

    try:
        type = 'mysql'
        host = '10.10.10.2'
        port = '3306'
        user = 'dwh'
        pwd = 'Analisis_1124'
        db = 'staging'

        con_db = Db_Connection(type, host, port, user, pwd, db)
        ses_db = con_db.start()
        if ses_db == -1:
            raise Exception(f"El tipo de base de datos {type} no es válido")
        elif ses_db == -2:
            raise Exception("Error al establecer la conexión de pruebas")     

        sql_stmt = """
        SELECT 
            p.idCategoria,
            p.idProducto,
            p.nombre AS nombreProducto,
            c.nombre AS nombreCategoria
        FROM 
            ext_Producto p
        JOIN 
            ext_Categoria c ON p.idCategoria = c.idCategoria;
        """
        productos_transformados = pd.read_sql(sql_stmt, ses_db)
        
        return productos_transformados

    except:
        traceback.print_exc()
    finally:
        pass
