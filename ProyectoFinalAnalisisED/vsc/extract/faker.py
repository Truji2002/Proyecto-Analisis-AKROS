from faker import Faker
import pandas as pd
 
from util.db_connection import Db_Connection
 
 
 
try:
    fake = Faker('es_EC')  
except AttributeError:
    fake = Faker('es')
 
##Cliente
   
areas_posibles = [
    'Marketing', 'Finanzas', 'Operaciones', 'RecursosHumanos', 'Ventas', 'IT',
    'Salud', 'Investigación', 'AtenciónCliente', 'Logística', 'Producción', 'Calidad',
    'Compras', 'Legal', 'Seguridad', 'Ingeniería', 'Tecnología', 'Administración',
    'Educación', 'MedioAmbiente', 'Comunicaciones', 'Diseño', 'ServiciosTécnicos',
    'Planificación', 'GestiónProyectos', 'DesarrolloNegocios',
    'Consultoría', 'ControlGestión', 'Auditoría',
]
 
def generar_cliente():
 
    nombre = fake.unique.company()
   
    telefono = fake.unique.numerify(text="#########")
   
    ruc = fake.unique.numerify(text="#############")
   
    correoElectronico = fake.unique.ascii_free_email()
   
    direccion = fake.address()
    area = fake.random_element(elements=areas_posibles)
   
    fechaRegistro = fake.date_between(start_date='-15y', end_date='today').strftime("%Y-%m-%d")
   
    return {
        'nombre': nombre,
        'telefono': telefono,
        'ruc': ruc,
        'direccion': direccion,
        'correoElectronico': correoElectronico,
        'area': area,
        'fechaRegistro': fechaRegistro
    }
 
 
 
##Vendedor
def generar_vendedor(ciudades_disponibles):
    """
    Genera datos para un vendedor considerando restricciones y unicidad.
    :param ciudades_disponibles: Lista de IDs de ciudades disponibles.
    :return: Un diccionario con datos de un vendedor.
    """
    nombre_completo = fake.first_name()
    apellido_completo = fake.last_name()
 
    cedula = fake.unique.numerify(text="##########")
   
    telefono = fake.unique.numerify(text="##########")
 
    correoElectronico = fake.unique.ascii_free_email()
 
    direccion = fake.address()
   
    fechaInicio = fake.date_between(start_date='-15y', end_date='today').strftime("%Y-%m-%d")
    estadoEmpleado = fake.random_element(elements=[0, 1])
   
    idCiudad = fake.random_element(elements=ciudades_disponibles)
 
    return {
        'idCiudad': idCiudad,
        'nombreCompleto': nombre_completo,
        'apellidoCompleto': apellido_completo,
        'cedula': cedula,
        'telefono': telefono,
        'correoElectronico': correoElectronico,
        'direccion': direccion,
        'fechaInicio': fechaInicio,
        'estadoEmpleado': estadoEmpleado
    }
 
 
 
 
 #Producto      
 
base_nombres = {
        "Empresa Digital": ["CloudPlatform", "BizNet", "DigitalFlow"],
        "Akros as a Service": ["SaaSManager", "ServiceFlow", "CloudService"],
        "Infraestructura Digital": ["DataCenter", "DigitalCore", "NetFrame"],
        "Ciberseguridad": ["SecureGate", "CyberShield", "DataProtector"],
        "Akros Cloud": ["CloudSpace", "SkyStorage", "CloudStream"],
        "Hardware y Equipamiento Tecnológico": ["TechGear", "GadgetPro", "HardwareHub"],
        "Consultoría y Estrategia Digital": ["DigitalConsult", "StrategyAdvisor", "BizTechGuide"],
        "Gestión de Datos y Almacenamiento": ["DataSaver", "StorageKing", "InfoKeeper"],
        "Soluciones Móviles y Desarrollo de Apps": ["AppBuilder", "MobileSuite", "AppFactory"],
        "Plataformas de Comercio Electrónico": ["EcomPlatform", "OnlineStore", "TradeNet"],
        "Servicios de Virtualización": ["VirtualSpace", "VirtuDesk", "CloudVirtual"],
        "Gestión de Redes y Comunicaciones": ["NetManager", "CommuLink", "NetworkPro"],
        "Soluciones de Inteligencia Artificial": ["AISolution", "SmartAI", "IntellectBot"],
        "Servicios de Automatización y Robótica": ["AutoBot", "RoboWorks", "TaskAutomator"],
        "Capacitación y Formación Tecnológica": ["TechEdu", "SkillTech", "LearnIT"]
    }
nombres_generados = set()
 
def generar_producto(idCategoria, categoria_nombre):
    producto = {
        "idCategoria": idCategoria,
        "nombre": generar_nombre_producto(categoria_nombre),
        "precio": fake.pydecimal(left_digits=4, right_digits=2, positive=True, min_value=0.01, max_value=10000.00),
        "stock": fake.random_int(min=0, max=1000),
        "estado": fake.random_element(elements=[0, 1]),
        "costo": fake.pydecimal(left_digits=4, right_digits=2, positive=True, min_value=0.01, max_value=5000.00),
        "requerimiento": fake.text(max_nb_chars=50) if fake.boolean(chance_of_getting_true=50) else None,
        "fechaLanzamiento": fake.date_between(start_date="-10y", end_date="today")
    }
    return producto
 
def generar_nombre_producto(categoria):
    while True:
        nombre = fake.random.choice(base_nombres[categoria]) + "_" + fake.lexify("???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        if nombre not in nombres_generados:
            nombres_generados.add(nombre)
            return nombre
       
 
 
##Orden
       
def generar_orden():
    idProducto = fake.random_int(min=1, max=120)  
    idVendedor = fake.random_int(min=1, max=250)  
    fechaOrden = fake.date_between(start_date='-15y', end_date='today')
    estado = fake.random_element(elements=[0, 1])  
    comentario = fake.text(max_nb_chars=50) if fake.random.choice([True, False]) else ""
 
    return {
        "idProducto": idProducto,
        "idVendedor": idVendedor,
        "fechaOrden": fechaOrden,
        "estado": estado,
        "comentario": comentario
    }
 
 
 
##Ventas
 
   
def generar_venta():
   
    idCliente = fake.random_int(min=1, max=1000)
    idProducto = fake.random_int(min=1, max=120)
    fechaCompra = fake.date_between(start_date='-15y', end_date='today')
    cantidad = fake.random_int(min=1, max=15)
 
   
 
   
    metodos_pago = ['Efectivo', 'Tarjeta', 'Transferencia', 'Cheque']
    metodoPago = fake.random_element(elements=metodos_pago)
 
    return {
        "idCliente": idCliente,
        "idProducto": idProducto,
        "fechaCompra": fechaCompra,
        "cantidad": cantidad,
        "metodoPago": metodoPago
    }