-- Esquema SQLite equivalente al modelo MySQL de la Fase II (CRM_BD.sql)
DROP TABLE IF EXISTS Actividad;
DROP TABLE IF EXISTS Interaccion;
DROP TABLE IF EXISTS DetallePedido;
DROP TABLE IF EXISTS Pedido;
DROP TABLE IF EXISTS Producto;
DROP TABLE IF EXISTS Cliente;
DROP TABLE IF EXISTS Usuario;

CREATE TABLE Usuario (
  id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  correo TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  rol TEXT NOT NULL CHECK (rol IN ('admin','editor','colaborador'))
);

CREATE TABLE Cliente (
  id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  telefono_wa TEXT UNIQUE NOT NULL,
  ig_user TEXT,
  email TEXT,
  fecha_alta TEXT DEFAULT (date('now')),
  segmento TEXT DEFAULT 'nuevo',
  ltv REAL DEFAULT 0
);

CREATE TABLE Producto (
  id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  tipo TEXT NOT NULL CHECK (tipo IN ('fisico','digital')),
  precio REAL NOT NULL
);

CREATE TABLE Pedido (
  id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cliente INTEGER NOT NULL REFERENCES Cliente(id_cliente),
  canal TEXT NOT NULL CHECK (canal IN ('IG','WA','WEB')),
  fecha TEXT NOT NULL DEFAULT (datetime('now')),
  total REAL NOT NULL,
  estado TEXT DEFAULT 'nuevo' CHECK (estado IN ('nuevo','pagado','enviado','entregado','cancelado')),
  id_usuario_registra INTEGER REFERENCES Usuario(id_usuario)
);

CREATE TABLE DetallePedido (
  id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
  id_pedido INTEGER NOT NULL REFERENCES Pedido(id_pedido),
  id_producto INTEGER NOT NULL REFERENCES Producto(id_producto),
  cantidad INTEGER NOT NULL DEFAULT 1,
  precio_unit REAL NOT NULL
);

CREATE TABLE Interaccion (
  id_interaccion INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cliente INTEGER NOT NULL REFERENCES Cliente(id_cliente),
  fecha TEXT NOT NULL DEFAULT (datetime('now')),
  tipo TEXT,
  mensaje TEXT,
  resultado TEXT
);

-- Nueva en Fase III: bitacora de actividades del equipo (Actividad 11)
CREATE TABLE Actividad (
  id_actividad INTEGER PRIMARY KEY AUTOINCREMENT,
  id_usuario INTEGER REFERENCES Usuario(id_usuario),
  fecha TEXT NOT NULL DEFAULT (datetime('now')),
  accion TEXT NOT NULL,
  detalle TEXT
);

CREATE INDEX idx_cliente_tel ON Cliente(telefono_wa);
CREATE INDEX idx_pedido_fecha ON Pedido(fecha);
CREATE INDEX idx_pedido_cliente ON Pedido(id_cliente);
