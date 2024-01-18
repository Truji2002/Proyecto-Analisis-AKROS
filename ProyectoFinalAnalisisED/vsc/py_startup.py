from util.db_connection import Db_Connection
import traceback
import pandas as pd

from extract.ext_categoria import extraer_categoria
from extract.per_oltp import persistir_oltp
from extract.per_staging import persistir_staging
from extract.ext_ciudad import extraer_ciudad
from extract.faker import generar_cliente
from extract.faker import generar_vendedor
from extract.faker import generar_producto
from extract.faker import generar_orden
from extract.faker import base_nombres
from extract.extr import extraer_general
from extract.faker import generar_venta
from transform.tra_Producto import transformar_producto
from transform.tra_fecha import transformar_fecha
from transform.tra_Venta import transformar_venta
from load.load_Producto import cargar_Producto
from load.load_Cliente import cargar_Cliente
from load.load_Vendedor import cargar_Vendedor
from load.load_Ciudad import cargar_Ciudad
from load.load_Fecha import cargar_Fecha
from load.load_Venta import cargar_Venta

try:

    #DATOS OLTP

    #Categoria
    cat = extraer_categoria()
    persistir_oltp(cat, 'Categoria')
    #Ciudad
    ciu = extraer_ciudad()
    persistir_oltp(ciu, 'Ciudad')

    #Cliente
    cliente=[generar_cliente() for _ in range(1000)]
    clientes_df = pd.DataFrame(cliente)
    persistir_oltp(clientes_df, 'Cliente')

    #Vendedor
    ciudades_disponibles = [1, 2, 3, 4, 5,6,7,8,9,10,11,12]
    vendedor = [generar_vendedor(ciudades_disponibles) for _ in range(250)]
    vendedor_df = pd.DataFrame(vendedor)
    persistir_oltp(vendedor_df, 'Vendedor')

    ##Producto
    productos = []
    for idCategoria, categoria in enumerate(base_nombres, start=1):
        for _ in range(8):
            productos.append(generar_producto(idCategoria, categoria))

    productos_df=pd.DataFrame(productos)
    persistir_oltp(productos_df, 'Producto')

    ventas = [generar_venta() for _ in range(1000)]
 
    ventas_df=pd.DataFrame(ventas)
 
    persistir_oltp(ventas_df, 'Venta')

    #Orden
    ordenes = [generar_orden() for _ in range(1000)]
 
    ordenes_df=pd.DataFrame(ordenes)
 
    persistir_oltp(ordenes_df, 'Orden')
    #DATOS STAGING


    #Cliente
    ClienteOl = extraer_general('Cliente')
    persistir_staging(ClienteOl, 'ext_Cliente')

    Orden = extraer_general('Orden')
    persistir_staging(Orden,'ext_Orden')

    #Categoria
    cat = extraer_categoria()
    persistir_staging(cat, 'ext_Categoria')

    #Ciudad
    ciu = extraer_ciudad()
    persistir_staging(ciu, 'ext_Ciudad')

    #Vendedor
    ven = extraer_general('Vendedor')
    persistir_staging(ven, 'ext_Vendedor')

    #Producto
    pro = extraer_general('Producto')
    persistir_staging(pro, 'ext_Producto')


    vent = extraer_general('Venta')
    persistir_staging(vent,'ext_Venta')

    

    #Orden
    #Venta

#Transformación de datos
    
  
    producto_tra = transformar_producto()
    persistir_staging(producto_tra, 'tra_Producto')

    venta_tra=transformar_venta()
    persistir_staging(venta_tra, 'tra_Venta')

    fecha_tra=transformar_fecha()
    persistir_staging(fecha_tra,'tra_Fecha')



    cargar_Producto()
    cargar_Cliente()
    cargar_Vendedor()
    cargar_Ciudad()
    cargar_Fecha()
    cargar_Venta()

    
except:
    traceback.print_exc()
finally:
    pass