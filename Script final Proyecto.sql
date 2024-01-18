
USE oltp;
 
CREATE TABLE Cliente (
    idCliente INT AUTO_INCREMENT NOT NULL,
    nombre VARCHAR(100) NOT NULL CHECK (nombre NOT LIKE '%[^a-zA-Z0-9]%'),
    telefono CHAR(9) NOT NULL CHECK (telefono NOT LIKE '%[^0-9]%'),
    ruc CHAR(13) NOT NULL CHECK (ruc NOT LIKE '%[^0-9]%'),
    direccion VARCHAR(150),
	correoElectronico VARCHAR(255) NOT NULL CHECK (correoElectronico LIKE '%@%' AND correoElectronico 
	LIKE '%.%' AND correoElectronico NOT LIKE '%@%@%' AND correoElectronico NOT LIKE '%..%'),
    area VARCHAR(20) CHECK (area NOT LIKE '%[^a-zA-Z]%'),
    fechaRegistro DATE NOT NULL,
	CONSTRAINT PK_Cliente PRIMARY KEY (idCliente),
    CONSTRAINT UQ_Cliente_nombre UNIQUE (nombre),
    CONSTRAINT UQ_Cliente_telefono UNIQUE (telefono),
    CONSTRAINT UQ_Cliente_ruc UNIQUE (ruc),
    CONSTRAINT UQ_Cliente_correoElectronico UNIQUE (correoElectronico)
);
 
 
CREATE TABLE Ciudad (
    idCiudad TINYINT AUTO_INCREMENT NOT NULL,
    nombre VARCHAR(15) NOT NULL CHECK (nombre NOT LIKE '%[^a-zA-Z]%'),
    provincia VARCHAR(50) NOT NULL CHECK (provincia NOT LIKE '%[^a-zA-Z]%'),
    codigoPostal CHAR(6) NOT NULL CHECK (codigoPostal NOT LIKE '%[^0-9]%'),
    region VARCHAR(10) NOT NULL CHECK (region NOT LIKE '%[^a-zA-Z]%'),
	CONSTRAINT PK_Ciudad PRIMARY KEY (idCiudad),
    CONSTRAINT UQ_Ciudad_nombre UNIQUE (nombre),
    CONSTRAINT UQ_Ciudad_codigoPostal UNIQUE (codigoPostal)
);
 
CREATE TABLE Categoria (
    idCategoria TINYINT AUTO_INCREMENT NOT NULL,
    nombre VARCHAR(100) NOT NULL CHECK (nombre NOT LIKE '%[^a-zA-Z]%'),
	descripcion VARCHAR(150),
	estado BIT NOT NULL,
	fechaCreacion DATE NOT NULL,
	CONSTRAINT PK_Categoria PRIMARY KEY (idCategoria),
    CONSTRAINT UQ_Categoria_nombre UNIQUE (nombre)
);
 
 
CREATE TABLE Vendedor (
    idVendedor TINYINT UNSIGNED AUTO_INCREMENT NOT NULL,
	idCiudad TINYINT NOT NULL,
    nombreCompleto VARCHAR(90) NOT NULL CHECK (nombreCompleto NOT LIKE '%[^a-zA-Z ]%'),
    apellidoCompleto VARCHAR(90) NOT NULL CHECK (apellidoCompleto NOT LIKE '%[^a-zA-Z ]%'),
    cedula CHAR(10) NOT NULL CHECK (cedula NOT LIKE '%[^0-9]%'),
    telefono CHAR(10) NOT NULL CHECK (telefono NOT LIKE '%[^0-9]%'),
    correoElectronico VARCHAR(255) NOT NULL CHECK (correoElectronico LIKE '%@%' AND correoElectronico 
	LIKE '%.%' AND correoElectronico NOT LIKE '%@%@%' AND correoElectronico NOT LIKE '%..%'),
    direccion VARCHAR(150),
    fechaInicio DATE NOT NULL,
    estadoEmpleado BIT NOT NULL,
	CONSTRAINT PK_Vendedor PRIMARY KEY (idVendedor),
    CONSTRAINT FK_Vendedor_Ciudad FOREIGN KEY (idCiudad) REFERENCES Ciudad(idCiudad),
    CONSTRAINT UQ_Vendedor_cedula UNIQUE (cedula),
    CONSTRAINT UQ_Vendedor_telefono UNIQUE (telefono),
    CONSTRAINT UQ_Vendedor_correoElectronico UNIQUE (correoElectronico)
);
 
CREATE TABLE Producto (
    idProducto TINYINT UNSIGNED AUTO_INCREMENT NOT NULL,
	idCategoria TINYINT NOT NULL,
    nombre VARCHAR(45) NOT NULL CHECK (nombre NOT LIKE '%[^a-zA-Z0-9]%'),
    precio DECIMAL(7,2) NOT NULL CHECK (precio >= 0 AND precio NOT LIKE ' %[^0-9]%'),
    stock SMALLINT NOT NULL CHECK (stock >= 0 AND stock NOT LIKE ' %[^0-9]%'),
    estado BIT NOT NULL,
    costo DECIMAL(7,2) NOT NULL CHECK (costo >= 0 AND costo NOT LIKE ' %[^0-9]%'),
    requerimiento VARCHAR(50),
    fechaLanzamiento DATE NOT NULL,
	CONSTRAINT PK_Producto PRIMARY KEY (idProducto),
    CONSTRAINT FK_Producto_Categoria FOREIGN KEY (idCategoria) REFERENCES Categoria(idCategoria),
    CONSTRAINT UQ_Producto_nombre UNIQUE (nombre)
);
 
CREATE TABLE Orden (
    idOrden INT AUTO_INCREMENT NOT NULL,
	idProducto TINYINT UNSIGNED NOT NULL,
	idVendedor TINYINT UNSIGNED NOT NULL,
    fechaOrden DATE NOT NULL,
    estado BIT NOT NULL,
    comentario VARCHAR(50),
	CONSTRAINT PK_Orden PRIMARY KEY (idOrden),
	CONSTRAINT FK_Orden_Producto FOREIGN KEY (idProducto) REFERENCES Producto(idProducto),
	CONSTRAINT FK_Orden_Vendedor FOREIGN KEY (idVendedor) REFERENCES Vendedor(idVendedor)
);
 
CREATE TABLE Venta (
    idVenta INT AUTO_INCREMENT NOT NULL,
	idCliente INT NOT NULL,
	idProducto TINYINT UNSIGNED NOT NULL,
    fechaCompra DATE NOT NULL,
    cantidad SMALLINT NOT NULL CHECK (cantidad > 0 AND cantidad NOT LIKE ' %[^0-9]%'),
    metodoPago VARCHAR(15) NOT NULL CHECK (metodoPago NOT LIKE '%[^a-zA-Z]%'),
	CONSTRAINT PK_Venta PRIMARY KEY (idVenta),
	CONSTRAINT FK_Venta_Cliente FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente),
	CONSTRAINT FK_Venta_Producto FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
);


USE staging;
CREATE TABLE ext_Categoria AS SELECT * FROM oltp.Categoria WHERE 1=2;
CREATE TABLE ext_Ciudad AS SELECT * FROM oltp.Ciudad WHERE 1=2;
CREATE TABLE ext_Cliente AS SELECT * FROM oltp.Cliente WHERE 1=2;
CREATE TABLE ext_Producto AS SELECT * FROM oltp.Producto WHERE 1=2;
CREATE TABLE ext_Vendedor AS SELECT * FROM oltp.Vendedor WHERE 1=2;
CREATE TABLE ext_Venta AS SELECT * FROM oltp.Venta WHERE 1=2;
CREATE TABLE ext_Orden AS SELECT * FROM oltp.Orden WHERE 1=2;

USE sor;
 
CREATE TABLE dim_Ciudad (
    ciudad_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    idCiudad BIGINT,
    nombre TEXT,
    provincia TEXT
);
CREATE TABLE dim_Cliente (
    cliente_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    idCliente BIGINT,
    nombre TEXT
);
CREATE TABLE dim_Fecha (
    idFecha BIGINT AUTO_INCREMENT PRIMARY KEY,
    anio BIGINT,
    mes BIGINT,
    trimestre TEXT
);
CREATE TABLE dim_Producto (
    producto_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_Producto BIGINT,
    nombreProducto TEXT,
    nombreCategoria TEXT
);
CREATE TABLE dim_Vendedor (
    vendedor_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    idVendedor BIGINT,
    nombreCompleto TEXT,
    apellidoCompleto TEXT,
    cedula TEXT
);
 




 