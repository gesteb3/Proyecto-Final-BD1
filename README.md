# 🧠 Mini IDE de Bases de Datos (PostgreSQL + MongoDB)

Este proyecto es una aplicación de escritorio desarrollada en **Python** utilizando **Tkinter**, que permite conectarse, consultar y administrar bases de datos **PostgreSQL** y **MongoDB** desde una sola interfaz visual.

---

## 📋 Descripción del Proyecto

El **Mini IDE de Bases de Datos** busca ofrecer una herramienta ligera e intuitiva para ejecutar comandos SQL y operaciones básicas en MongoDB sin depender de herramientas externas como pgAdmin o Compass.

Incluye:
- Conexión directa a **PostgreSQL** y **MongoDB**.  
- Ejecución de sentencias **DDL/DML** (SELECT, INSERT, UPDATE, DELETE, CREATE, etc.) en PostgreSQL.  
- Ejecución de comandos Mongo como `insertOne()`, `insertMany()`, y `find()`.  
- Visualización de resultados en una consola integrada.  
- Interfaz gráfica amigable desarrollada con **Tkinter** y **ttk**.  

---

## ⚙️ Instrucciones de Instalación y Ejecución

### 🧩 Requisitos previos

1. Tener instalado **Python 3.10+**  
2. Tener instalados y corriendo:
   - **PostgreSQL** (versión 14 o superior)
   - **MongoDB** (versión 5.0 o superior)

### 📦 Librerías necesarias

Instala las dependencias usando pip:

```bash
pip install psycopg2 pymongo pandas
```

> Tkinter viene incluido con Python en la mayoría de instalaciones.  
> Si no, puede instalarse con:
> ```bash
> sudo apt install python3-tk
> ```

---

### ▶️ Ejecución del programa

1. Guarda el archivo del proyecto como `mini_db_ide.py`.
2. Ejecuta el programa desde la terminal o entorno IDE con:

```bash
python mini_db_ide.py
```

3. Se abrirá la ventana principal del programa con dos secciones:
   - **PostgreSQL:** para ejecutar comandos SQL.
   - **MongoDB:** para ejecutar operaciones básicas en colecciones.

---

## 🗄️ Bases de Datos Utilizadas

### 🐘 PostgreSQL
- **Tipo:** Relacional  
- **Versión recomendada:** 14 o superior  
- **Conexión:**
  - Host: `localhost`
  - Puerto: `5432`
  - Base de datos por defecto: `testdb`
  - Usuario: `postgres`
  - Contraseña: `1234` *(editable desde la interfaz)*

La conexión se realiza mediante la librería `psycopg2`:
```python
psycopg2.connect(
    host="localhost",
    port="5432",
    database="testdb",
    user="postgres",
    password="1234"
)
```

### 🍃 MongoDB
- **Tipo:** NoSQL orientado a documentos  
- **Versión recomendada:** 5.0 o superior  
- **Conexión:**
  - URI por defecto: `mongodb://localhost:27017`
  - Base de datos por defecto: `testdb`

La conexión se realiza con la librería `pymongo`:
```python
client = MongoClient("mongodb://localhost:27017")
db = client["testdb"]
```

---

## 💡 Ejemplos de uso

### PostgreSQL
```sql
CREATE TABLE empleados (id SERIAL PRIMARY KEY, nombre VARCHAR(50), salario NUMERIC);
INSERT INTO empleados (nombre, salario) VALUES ('Carlos', 3500);
SELECT * FROM empleados;
```

### MongoDB
```js
db.empleados.insertMany([
  {"nombre": "Ana", "salario": 3000},
  {"nombre": "Luis", "salario": 4500}
])

db.empleados.find()
```

---

## 🧭 Reflexión Personal

Durante el desarrollo de este proyecto enfrenté varios **retos técnicos**, entre ellos:

- Comprender cómo manejar **dos tipos de bases de datos** (relacional y no relacional) desde una misma interfaz.
- Gestionar las conexiones y errores de **PostgreSQL y MongoDB** de forma simultánea sin que el programa se bloquee.
- Formatear y mostrar los resultados de manera legible usando **pandas** dentro del entorno gráfico de Tkinter.

Gracias a este proyecto aprendí a:
- Implementar conexiones seguras con distintos motores de base de datos.
- Diseñar interfaces con **Tkinter** y mejorar la interacción con el usuario.
- Aplicar buenas prácticas de manejo de errores y modularización del código.

En resumen, esta aplicación me permitió **consolidar conocimientos de programación, bases de datos y diseño de interfaces gráficas**, integrando lo aprendido en un proyecto funcional y educativo.

---
