-- Esquema MySQL 8 del CRM (equivalente a app/schema.sql de SQLite)
CREATE DATABASE IF NOT EXISTS crm_ecommerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE crm_ecommerce;

CREATE TABLE Usuario (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  correo VARCHAR(150) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  rol ENUM('admin','editor','colaborador') NOT NULL
);

CREATE TABLE Cliente (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  telefono_wa VARCHAR(20) NOT NULL UNIQUE,
  ig_user VARCHAR(60),
  email VARCHAR(150),
  fecha_alta DATE DEFAULT (CURRENT_DATE),
  segmento ENUM('nuevo','frecuente','inactivo') DEFAULT 'nuevo',
  ltv DECIMAL(12,2) DEFAULT 0,
  INDEX idx_cliente_segmento_ltv (segmento, ltv)
);

CREATE TABLE Producto (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  tipo ENUM('fisico','digital') NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  activo TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE Pedido (
  id_pedido INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT NOT NULL,
  canal ENUM('IG','WA','WEB') NOT NULL,
  fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total DECIMAL(12,2) NOT NULL,
  estado ENUM('nuevo','pagado','enviado','entregado','cancelado') DEFAULT 'nuevo',
  id_usuario_registra INT,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
  FOREIGN KEY (id_usuario_registra) REFERENCES Usuario(id_usuario),
  INDEX idx_pedido_fecha (fecha), INDEX idx_pedido_cliente (id_cliente),
  INDEX idx_pedido_estado (estado), INDEX idx_pedido_canal (canal)
);

CREATE TABLE DetallePedido (
  id_detalle INT AUTO_INCREMENT PRIMARY KEY,
  id_pedido INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL DEFAULT 1,
  precio_unit DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido),
  FOREIGN KEY (id_producto) REFERENCES Producto(id_producto)
);

CREATE TABLE Interaccion (
  id_interaccion INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT NOT NULL,
  fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tipo VARCHAR(30),
  mensaje TEXT,
  resultado VARCHAR(30),
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
  INDEX idx_interaccion_cliente (id_cliente, fecha)
);

CREATE TABLE Actividad (
  id_actividad INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT,
  fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  accion VARCHAR(60) NOT NULL,
  detalle TEXT,
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Plantilla (
  id_plantilla INT AUTO_INCREMENT PRIMARY KEY,
  clave VARCHAR(60) NOT NULL UNIQUE,
  texto VARCHAR(500) NOT NULL
);
