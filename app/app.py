import os
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esta-clave")

def connect_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "postgres"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "inventario"),
        user=os.environ.get("DB_USER", "inventario"),
        password=os.environ.get("DB_PASSWORD", "inventario123"),
        connect_timeout=5
    )

def init_db():
    # Espera breve a que PostgreSQL esté disponible durante el arranque.
    import time
    for attempt in range(30):
        try:
            with connect_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS productos (
                            id SERIAL PRIMARY KEY,
                            nombre VARCHAR(120) NOT NULL,
                            descripcion TEXT DEFAULT '',
                            precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
                            cantidad INTEGER NOT NULL DEFAULT 0 CHECK (cantidad >= 0)
                        )
                    """)
            return
        except Exception:
            if attempt == 29:
                raise
            time.sleep(2)

@app.route("/")
def index():
    with connect_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM productos ORDER BY id DESC")
            productos = cur.fetchall()
    return render_template("index.html", productos=productos)

@app.route("/crear", methods=["POST"])
def crear():
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    try:
        precio = float(request.form.get("precio", ""))
        cantidad = int(request.form.get("cantidad", ""))
        if not nombre or precio < 0 or cantidad < 0:
            raise ValueError()
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO productos (nombre, descripcion, precio, cantidad) VALUES (%s,%s,%s,%s)",
                    (nombre, descripcion, precio, cantidad)
                )
        flash("Producto registrado correctamente.", "success")
    except (ValueError, TypeError):
        flash("Revisa los datos: nombre requerido, precio y cantidad no negativos.", "error")
    return redirect(url_for("index"))

@app.route("/editar/<int:producto_id>", methods=["POST"])
def editar(producto_id):
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    try:
        precio = float(request.form.get("precio", ""))
        cantidad = int(request.form.get("cantidad", ""))
        if not nombre or precio < 0 or cantidad < 0:
            raise ValueError()
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, cantidad=%s WHERE id=%s",
                    (nombre, descripcion, precio, cantidad, producto_id)
                )
        flash("Producto actualizado.", "success")
    except (ValueError, TypeError):
        flash("Datos inválidos; no se actualizó el producto.", "error")
    return redirect(url_for("index"))

@app.route("/eliminar/<int:producto_id>", methods=["POST"])
def eliminar(producto_id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM productos WHERE id=%s", (producto_id,))
    flash("Producto eliminado.", "success")
    return redirect(url_for("index"))

@app.get("/health")
def health():
    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"status": "ok"}, 200
    except Exception:
        return {"status": "database unavailable"}, 503

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
else:
    # Gunicorn carga el módulo; crear tabla al arrancar el worker.
    init_db()
