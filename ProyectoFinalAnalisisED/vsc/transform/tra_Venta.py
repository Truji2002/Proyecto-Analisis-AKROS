import traceback
from util.db_connection import Db_Connection
import pandas as pd

def transformar_venta():

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
                v.idVenta,
                MAX(v.idCliente) AS idCliente, 
                MAX(v.idProducto) AS idProducto,
                MAX(v.fechaCompra) AS fechaCompra,
                MAX(ve.idVendedor) AS idVendedor,
                MAX(c.idCiudad) AS idCiudad,
                MAX(p.precio) AS precio,
                MAX(v.cantidad) AS cantidad,
                MAX(v.metodoPago) AS metodoPago,
                SUM(p.precio * v.cantidad) AS Total
            FROM 
                ext_Venta v
            LEFT JOIN 
                ext_Producto p ON v.idProducto = p.idProducto
            LEFT JOIN 
                ext_Cliente cl ON v.idCliente = cl.idCliente
            LEFT JOIN 
                ext_Orden o ON p.idProducto = o.idProducto
            LEFT JOIN 
                ext_Vendedor ve ON o.idVendedor = ve.idVendedor
            LEFT JOIN 
                ext_Ciudad c ON ve.idCiudad = c.idCiudad
            GROUP BY 
                v.idVenta;

           
        """
        ventas_productos_transformados = pd.read_sql(sql_stmt, ses_db)
        
        return ventas_productos_transformados

    except:
        traceback.print_exc()
    finally:
        pass
