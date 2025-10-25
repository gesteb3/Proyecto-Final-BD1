import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import psycopg2
from pymongo import MongoClient
import json
import pandas as pd

APP_TITLE = "Mini IDE de Bases de Datos (PostgreSQL + MongoDB)"

class MiniDBIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1000x700")
        self.create_widgets()
        self.pg_conn = None
        self.mongo_client = None
        self.mongo_db = None

    def create_widgets(self):
        # Frame de PostgreSQL
        pg_frame = ttk.LabelFrame(self, text="PostgreSQL")
        pg_frame.pack(fill='x', padx=8, pady=6)

        ttk.Label(pg_frame, text="Host").grid(row=0, column=0)
        self.pg_host = tk.StringVar(value="localhost")
        ttk.Entry(pg_frame, textvariable=self.pg_host).grid(row=0, column=1)

        ttk.Label(pg_frame, text="Puerto").grid(row=0, column=2)
        self.pg_port = tk.StringVar(value="5432")
        ttk.Entry(pg_frame, textvariable=self.pg_port).grid(row=0, column=3)

        ttk.Label(pg_frame, text="Base de Datos").grid(row=1, column=0)
        self.pg_db = tk.StringVar(value="testdb")
        ttk.Entry(pg_frame, textvariable=self.pg_db).grid(row=1, column=1)

        ttk.Label(pg_frame, text="Usuario").grid(row=1, column=2)
        self.pg_user = tk.StringVar(value="postgres")
        ttk.Entry(pg_frame, textvariable=self.pg_user).grid(row=1, column=3)

        ttk.Label(pg_frame, text="Contraseña").grid(row=2, column=0)
        self.pg_pass = tk.StringVar(value="1234")
        ttk.Entry(pg_frame, textvariable=self.pg_pass, show="*").grid(row=2, column=1)

        ttk.Button(pg_frame, text="Conectar", command=self.connect_postgres).grid(row=2, column=2)
        ttk.Label(pg_frame, text="Consulta SQL (DDL/DML)").grid(row=3, column=0, columnspan=4, sticky='w')

        self.pg_text = scrolledtext.ScrolledText(pg_frame, height=8)
        self.pg_text.grid(row=4, column=0, columnspan=4, sticky='nsew')

        ttk.Button(pg_frame, text="Ejecutar SQL", command=self.run_sql).grid(row=5, column=0, pady=6)

        # Frame de MongoDB
        mongo_frame = ttk.LabelFrame(self, text="MongoDB")
        mongo_frame.pack(fill='x', padx=8, pady=6)

        ttk.Label(mongo_frame, text="URI").grid(row=0, column=0)
        self.mongo_uri = tk.StringVar(value="mongodb://localhost:27017")
        ttk.Entry(mongo_frame, textvariable=self.mongo_uri, width=40).grid(row=0, column=1, columnspan=3, sticky='w')

        ttk.Label(mongo_frame, text="Base de Datos").grid(row=1, column=0)
        self.mongo_db_name = tk.StringVar(value="testdb")
        ttk.Entry(mongo_frame, textvariable=self.mongo_db_name).grid(row=1, column=1)

        ttk.Button(mongo_frame, text="Conectar", command=self.connect_mongo).grid(row=1, column=2)

        ttk.Label(mongo_frame, text="Comandos Mongo (insertar/buscar/mostrar)").grid(row=2, column=0, columnspan=4, sticky='w')
        self.mongo_text = scrolledtext.ScrolledText(mongo_frame, height=8)
        self.mongo_text.grid(row=3, column=0, columnspan=4, sticky='nsew')

        ttk.Button(mongo_frame, text="Ejecutar Mongo", command=self.run_mongo).grid(row=4, column=0, pady=6)

        # Frame de salida
        out_frame = ttk.LabelFrame(self, text="Salida / Resultados")
        out_frame.pack(fill='both', expand=True, padx=8, pady=6)
        self.output = scrolledtext.ScrolledText(out_frame)
        self.output.pack(fill='both', expand=True)

    def log(self, text):
        self.output.insert("end", str(text) + "\n\n")
        self.output.see("end")

    # PostgreSQL
    def connect_postgres(self):
        try:
            self.pg_conn = psycopg2.connect(
                host=self.pg_host.get(),
                port=self.pg_port.get(),
                database=self.pg_db.get(),
                user=self.pg_user.get(),
                password=self.pg_pass.get()
            )
            self.log(f"Conectado a PostgreSQL ({self.pg_db.get()})")
        except Exception as e:
            self.log(f"Error al conectar con PostgreSQL: {e}")

    def run_sql(self):
        if self.pg_conn is None:
            self.connect_postgres()
            if self.pg_conn is None:
                return
        sql = self.pg_text.get("1.0", "end").strip()
        if not sql:
            return
        try:
            cur = self.pg_conn.cursor()
            cur.execute(sql)
            if sql.lower().startswith("select"):
                rows = cur.fetchall()
                cols = [desc[0] for desc in cur.description]
                df = pd.DataFrame(rows, columns=cols)
                self.log(df.to_string(index=False))
            else:
                self.pg_conn.commit()
                self.log(f"Consulta SQL ejecutada correctamente. Filas afectadas: {cur.rowcount}")
        except Exception as e:
            self.log(f"Error en SQL: {e}")

    # MongoDB
    def connect_mongo(self):
        try:
            self.mongo_client = MongoClient(self.mongo_uri.get())
            self.mongo_db = self.mongo_client[self.mongo_db_name.get()]
            self.log(f"Conectado a MongoDB ({self.mongo_db_name.get()})")
        except Exception as e:
            self.log(f"Error al conectar con MongoDB: {e}")

    def run_mongo(self):
        if self.mongo_db is None:
            self.connect_mongo()
            if self.mongo_db is None:
                return
        cmd = self.mongo_text.get("1.0", "end").strip()
        if not cmd:
            return
        try:
            # Ejecutar código JS/Mongo directamente usando eval en Python
            # Soporta db.<coleccion>.insertOne(...), insertMany(...), find(), etc.
            # Solo permitimos llamadas simples para no romper seguridad
            if cmd.startswith("db."):
                # Extraer colección
                coll_name = cmd.split(".")[1]
                coll = self.mongo_db[coll_name]

                if ".insertMany(" in cmd:
                    json_text = cmd.split(".insertMany(", 1)[1].rsplit(")", 1)[0]
                    data = json.loads(json_text)
                    coll.insert_many(data)
                    self.log(f"{len(data)} documentos insertados en {coll_name}")
                elif ".insertOne(" in cmd:
                    json_text = cmd.split(".insertOne(", 1)[1].rsplit(")", 1)[0]
                    data = json.loads(json_text)
                    coll.insert_one(data)
                    self.log(f"Documento insertado en {coll_name}")
                elif ".find(" in cmd:
                    docs = list(coll.find({}, {"_id": 0}))
                    self.log(f"Documentos encontrados ({len(docs)}):\n{docs}")
                else:
                    self.log("Comando Mongo no soportado aún.")
            else:
                self.log("Comando Mongo no reconocido. Debe iniciar con db.<coleccion>.")
        except Exception as e:
            self.log(f"Error en comando Mongo: {e}")


if __name__ == "__main__":
    app = MiniDBIDE()
    app.mainloop()
