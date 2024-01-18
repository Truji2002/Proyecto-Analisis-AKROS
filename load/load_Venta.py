import traceback
from util.db_connection import Db_Connection
import pandas as pd

def cargar_Venta():
    def conectar_bd(tipo, host, port, user, pwd, db):
        con_db = Db_Connection(tipo, host, port, user, pwd, db)
        ses_db = con_db.start()
        if ses_db == -1:
            raise Exception(f"El tipo de base de datos {tipo} no es válido")
        elif ses_db == -2:
            raise Exception("Error al establecer la conexión de pruebas")
        return ses_db

    try:
        # Parámetros de conexión para las bases de datos
        parametros_staging = ('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'staging')
        parametros_sor = ('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'sor')

        # Conexiones a las bases de datos
        conexion_staging = conectar_bd(*parametros_staging)
        conexion_sor = conectar_bd(*parametros_sor)

        # Consulta a la tabla tra_Venta y dim_Fecha
        consulta_tra_venta = "SELECT * FROM tra_Venta"
        datos_tra_venta = pd.read_sql(consulta_tra_venta, conexion_staging)
        
        consulta_dim_fecha = "SELECT * FROM dim_Fecha"
        datos_dim_fecha = pd.read_sql(consulta_dim_fecha, conexion_sor)

        # Asegúrate de que 'fechaCompra' en datos_tra_venta es un objeto datetime
        datos_tra_venta['fechaCompra'] = pd.to_datetime(datos_tra_venta['fechaCompra'])
        
        # Agregar campos de año, mes y trimestre a datos_tra_venta para el merge
        datos_tra_venta['anio'] = datos_tra_venta['fechaCompra'].dt.year
        datos_tra_venta['mes'] = datos_tra_venta['fechaCompra'].dt.month
        datos_tra_venta['trimestre'] = datos_tra_venta['fechaCompra'].dt.to_period('Q').dt.strftime('Q%q')

        # Merge con dim_Fecha para obtener idFecha
        datos_tra_venta = datos_tra_venta.merge(datos_dim_fecha, on=['anio', 'mes', 'trimestre'], how='left')
        datos_tra_venta.drop_duplicates(subset=['idVenta'], keep='first', inplace=True)

        # Seleccionar las columnas relevantes para fact_Venta, incluido idFecha
        datos_fact_venta = datos_tra_venta[['idVenta', 'idCliente', 'idProducto', 'idVendedor', 'idCiudad', 'precio', 'cantidad', 'metodoPago', 'Total', 'idFecha']]

        # Cargar los datos en fact_Venta
        datos_fact_venta.to_sql('fact_Venta', conexion_sor, if_exists='append', index=False)

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        pass


