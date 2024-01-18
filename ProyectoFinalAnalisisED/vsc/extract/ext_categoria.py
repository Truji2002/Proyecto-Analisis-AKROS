import traceback
import pandas as pd

def extraer_categoria():
    try:
        filename = './csvs/Categoria.csv'
        cate = pd.read_csv(filename, delimiter=';')
        return cate

    except pd.errors.ParserError as e:
        print("Error al parsear el archivo CSV:", e)
        traceback.print_exc()
    except FileNotFoundError as e:
        print("Archivo no encontrado:", e)
        traceback.print_exc()
    except Exception as e:
        print("Ocurrió un error inesperado:", e)
        traceback.print_exc()
    except:
        traceback.print_exc()
    finally:
        pass

