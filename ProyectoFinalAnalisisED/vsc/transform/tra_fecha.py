import traceback
from util.db_connection import Db_Connection
import pandas as pd

def transformar_fecha():

    try:
        # Conexión con la base de datos 'staging'
        con_db = Db_Connection('mysql', '10.10.10.2', '3306', 'dwh', 'Analisis_1124', 'staging')
        ses_db = con_db.start()
        if ses_db == -1:
            raise Exception("El tipo de base de datos no es válido")
        elif ses_db == -2:
            raise Exception("Error al establecer la conexión de pruebas")

        # Extraer datos de 'staging'
        sql_stmt = "SELECT fechaCompra FROM ext_Venta"
        ventas_df = pd.read_sql(sql_stmt, ses_db)

        # Transformar la columna 'fechaCompra' a 'anio', 'mes' y 'trimestre'
        ventas_df['fechaCompra'] = pd.to_datetime(ventas_df['fechaCompra'])
        ventas_df['anio'] = ventas_df['fechaCompra'].dt.year
        ventas_df['mes'] = ventas_df['fechaCompra'].dt.month
        ventas_df['trimestre'] = ventas_df['fechaCompra'].dt.to_period('Q').dt.strftime('Q%q')

        # Crear 'idFecha' como un identificador único comenzando en 1
        ventas_df.reset_index(inplace=True)
        ventas_df['index'] += 1  # Aumentar en 1 para comenzar el índice desde 1
        ventas_df.rename(columns={'index': 'idFecha'}, inplace=True)

        # Seleccionar solo las columnas necesarias
        fechas_transformadas = ventas_df[['idFecha', 'anio', 'mes', 'trimestre']]

        return fechas_transformadas

    except:
        traceback.print_exc()
    finally:
        pass


# Luego puedes llamar a la función para
