from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Datos de ejemplo para los vendedores
datos_vendedores = [
    {'nombre': 'Juan'},
    {'nombre': 'María'},
    {'nombre': 'Pedro'},
    {'nombre': 'Luis'},
    {'nombre': 'Ana'}
]

# Datos de ejemplo para las ventas
datos_ventas = [
    {'vendedor': 'Juan', 'fecha': '2023-06-25', 'descripcion': 'Venta 1', 'monto_total': 100.50},
    {'vendedor': 'María', 'fecha': '2023-06-26', 'descripcion': 'Venta 2', 'monto_total': 75.20},
    {'vendedor': 'Pedro', 'fecha': '2023-06-27', 'descripcion': 'Venta 3', 'monto_total': 200.10},
    {'vendedor': 'Luis', 'fecha': '2023-06-28', 'descripcion': 'Venta 4', 'monto_total': 50.75},
    {'vendedor': 'Ana', 'fecha': '2023-06-28', 'descripcion': 'Venta 5', 'monto_total': 120.30},
    {'vendedor': 'Juan', 'fecha': '2023-06-29', 'descripcion': 'Venta 6', 'monto_total': 300.00},
    {'vendedor': 'María', 'fecha': '2023-06-29', 'descripcion': 'Venta 7', 'monto_total': 85.50},
    {'vendedor': 'Pedro', 'fecha': '2023-06-30', 'descripcion': 'Venta 8', 'monto_total': 70.00},
    {'vendedor': 'Luis', 'fecha': '2023-06-30', 'descripcion': 'Venta 9', 'monto_total': 250.80},
    {'vendedor': 'Ana', 'fecha': '2023-06-30', 'descripcion': 'Venta 10', 'monto_total': 180.10},
    {'vendedor': 'Juan', 'fecha': '2023-07-01', 'descripcion': 'Venta 11', 'monto_total': 90.20},
    {'vendedor': 'María', 'fecha': '2023-07-01', 'descripcion': 'Venta 12', 'monto_total': 105.70},
    {'vendedor': 'Pedro', 'fecha': '2023-07-02', 'descripcion': 'Venta 13', 'monto_total': 310.50},
    {'vendedor': 'Luis', 'fecha': '2023-07-02', 'descripcion': 'Venta 14', 'monto_total': 40.60},
    {'vendedor': 'Ana', 'fecha': '2023-07-02', 'descripcion': 'Venta 15', 'monto_total': 75.30},
    {'vendedor': 'Juan', 'fecha': '2023-07-03', 'descripcion': 'Venta 16', 'monto_total': 200.25},
    {'vendedor': 'María', 'fecha': '2023-07-03', 'descripcion': 'Venta 17', 'monto_total': 180.00},
    {'vendedor': 'Pedro', 'fecha': '2023-07-04', 'descripcion': 'Venta 18', 'monto_total': 50.00},
    {'vendedor': 'Luis', 'fecha': '2023-07-04', 'descripcion': 'Venta 19', 'monto_total': 110.80},
    {'vendedor': 'Ana', 'fecha': '2023-07-04', 'descripcion': 'Venta 20', 'monto_total': 95.40},
]


app = Flask(__name__)

# Configura la conexión a la base de datos PostgreSQL.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Felixpro2510@localhost/minicore_flask_db'
db = SQLAlchemy(app)


# Modelo para la tabla de Vendedores
class Vendedor(db.Model):
    idvendedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)


# Modelo para la tabla de Ventas
class Venta(db.Model):
    idventa = db.Column(db.Integer, primary_key=True)
    vendedor = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    monto_total = db.Column(db.Float, nullable=False)

# Ruta para mostrar los vendedores y sus ventas
@app.route('/')
def mostrar_ventas():
    vendedores = Vendedor.query.all()
    ventas = Venta.query.all()
    return render_template('mostrar_ventas.html', vendedores=vendedores, ventas=ventas)

# Ruta para filtrar por fechas y encontrar el vendedor con mayor monto total
@app.route('/filtrar', methods=['POST'])
def filtrar_ventas():
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']

    # Consulta a la base de datos para obtener el vendedor con mayor monto total entre las fechas seleccionadas
    resultado = db.session.query(Venta.vendedor, db.func.sum(Venta.monto_total).label('total_monto')) \
        .filter(Venta.fecha.between(fecha_inicio, fecha_fin)) \
        .group_by(Venta.vendedor) \
        .order_by(db.desc('total_monto')) \
        .first()

    if resultado:
        vendedor, total_monto = resultado
    else:
        vendedor, total_monto = None, None

    vendedores = Vendedor.query.all()
    ventas = Venta.query.all()
    return render_template('mostrar_ventas.html', vendedores=vendedores, ventas=ventas, vendedor_mayor_monto=vendedor, total_monto=total_monto)


if __name__ == '__main__':
    with app.app_context():
        # Crear las tablas en la base de datos
        db.create_all()

        # Verificar si hay datos existentes en la tabla Vendedor
        if not db.session.query(Vendedor).count():
            # Poblar la base de datos con datos de ejemplo
            for vendedor_data in datos_vendedores:
                vendedor = Vendedor(**vendedor_data)
                db.session.add(vendedor)

        # Verificar si hay datos existentes en la tabla Venta
        if not db.session.query(Venta).count():
            # Poblar la base de datos con datos de ejemplo
            for venta_data in datos_ventas:
                venta = Venta(**venta_data)
                db.session.add(venta)

        # Confirmar los cambios (hacer commit) en la base de datos
        db.session.commit()

    app.run(debug=True)
