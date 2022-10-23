from cgitb import html
from http.client import NOT_FOUND
import re
from bson import json_util
from flask import Flask, render_template, request,jsonify,Response,redirect,url_for,flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash


app=Flask(__name__)
client = MongoClient("mongodb+srv://Joshua:hS3XtG1QFLTWGPnu@cluster1.fdgfgb1.mongodb.net/?retryWrites=true&w=majority")
#app.config["MONGO_HOST"] = DB_URI
#mongo = PyMongo(app)
db= client.CuentasPorCobrar1
#print(db.list_collection_names())
#print(client.list_database_names())
#todo1={"usuario":"joshua","contraseña":"1234"}

user=db.usuarios
#result= usuarios.insert_one(todo1)
@app.route('/')
def home():
    return redirect(url_for('login'))

#@app.route('/api/login',methods=["GET"])    
#def login():
#    print("hola mundo")
#    users=user.find()
#    response =json_util.dumps(users)
#    return Response(response, mimetype="application/json")


@app.route('/login',methods=["POST",'GET'])    
def login():
    #username=request.json['usuario']
    #password=request.json['contraseña']
    #if username and password:
    #    hashed=generate_password_hash(password)
    #    user.find_one(
    #        {'usuario':username,
    #        'contraseña':hashed})
    #    return {'mesage':'acceso autorizado'}
    #else:
    #    return not_found()
    if request.method=='POST':
        username= request.form['usuario']
        password= request.form['contraseña']
        if username =="josh":
            if password=="1234":
                return redirect(url_for('menu'))
            else:
                print("Contraseña invalida") 
                return render_template('/login.html')
        else:       
            print("Usuario no existe....") 
            return render_template('/login.html')
    else:
        return render_template('/login.html')

@app.route('/menu')
def menu():
    return render_template('/menu.html')

@app.route('/consultacliente',methods=['GET'])  
def conscliente():   
    Id=request.json['Id']
    if Id:
        users=user.find_one(
            {'Id':Id
            })
        response =json_util.dumps(users)
        return Response(response, mimetype="application/json")
    else:
        return render_template('/consulta.html')

@app.route('/Registrocliente')
def regcliente():
    id_cliente= request.form['id_cliente']
    nombres= request.form['nombres']
    apellidos= request.form['apellidos']
    NIT= request.form['NIT']
    telefono= request.form['telefono']
    direccion= request.form['direccion']
    correo= request.form['correo']
    return render_template('/registrocliente.html')

@app.route('/BajaCliente')
def bajacliente():
    id_cliente= request.form['id_cliente']
    razon= request.form['razon']
    return render_template('/bajacliente.html')

@app.route('/Modificarcliente')
def modificar():
    nombres= request.form['nombres']
    apellidos= request.form['apellidos']
    NIT= request.form['NIT']
    telefono= request.form['telefono']
    direccion= request.form['direccion']
    correo= request.form['correo']
    return render_template('/modcliente.html')         


@app.route('/Registropago')
def regpago():
    idcliente= request.form['idcliente']
    correlativo= request.form['correlativo']
    fecha= request.form['fecha']
    concepto= request.form['concepto']
    return render_template('/registropago.html')

@app.route('/Anularpago')
def anular():
    correlativo= request.form['correlativo']
    razon= request.form['razon']
    return render_template('/anularpago.html') 

@app.route('/Factura')
def emitirfac():
    factura= request.form['factura']
    fecha= request.form['fecha']
    NIT= request.form['NIT']
    direccion= request.form['direccion']
    concepto= request.form['concepto']
    cantidad= request.form['cantidad']
    IVA= request.form['IVA']
    total= request.form['total']
    return render_template('/emitirfactura.html')        

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)