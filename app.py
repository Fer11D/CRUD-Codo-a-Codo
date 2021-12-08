from flask import Flask, render_template,request,redirect
from flaskext.mysql import MySQL
from pymysql import cursors
from datetime import datetime

from werkzeug.utils import redirect



app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = "localhost"
app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = ""
app.config['MYSQL_DATABASE_DB'] = "sistema 2170"
mysql.init_app(app)

@app.route("/")
def index():
    sql = "SELECT * FROM empleados;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit()
    
    return render_template("empleados/index.html", empleados=empleados)

@app.route("/destroy/<int:id>")
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id=%s", (id))
    conn.commit()
    return redirect("/")

@app.route("/juancarlos")
def juanca():
    return render_template("empleados/indexjuan.html")


@app.route("/create")
def create():
    return render_template("empleados/create.html")


@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto   = request.files['txtFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    nuevoNombreFoto = tiempo + _foto.filename

    #Fix me, si no sube foto, rompe todo.
    if _foto.filename!="":
        _foto.save("uploads/"+nuevoNombreFoto)

    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos = [_nombre,_correo,nuevoNombreFoto]

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return render_template('empleados/index.html')









if __name__ == '__main__':
    app.run(debug=True)