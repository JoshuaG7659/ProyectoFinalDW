import email
from traceback import print_tb
from urllib import response
from wsgiref import headers
from xml.dom import INVALID_MODIFICATION_ERR
import requests
from cgitb import html
from http.client import NOT_FOUND
import re
from bson import json_util
from flask import Flask, render_template, request,jsonify,Response,redirect,url_for,flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash



app=Flask(__name__)



@app.route('/')
def home():
    return redirect(url_for('login'))

#@app.route('/api/login',methods=["GET"])    
#def login():
#    print("hola mundo")
#    users=user.find()
#    response =json_util.dumps(users)
#    return Response(response, mimetype="application/json")


@app.route('/login',methods=['POST','GET'])    
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
        urlbase="http://localhost:5000/api/Cliente/usuario"
        datos={
                    "nombre":username,
                    "contrasena":password
                }
        headers={'Content-Type':'application/json'}
        response =json_util.dumps(datos)
        r=requests.request("POST",urlbase,headers=headers,data=response)
        if username :
            if password:
                print('usuario logeado correctamente')
                return render_template('/menu.html')
            else:
                print("Contraseña Invalida")
                return render_template('/login.html')
        else:
            print("Usuario incorrecto")
            return render_template('/login.html')            
    else:
        return render_template('/login.html')

@app.route('/menu')
def menu():
    return render_template('/menu.html')

@app.route('/consultacliente',methods=['POST','GET'])  
def formcliente():
    if request.method=='POST':
        Nit=request.form['nit']
        urlbase="http://localhost:5000/api/Cliente/Cliente,"
        url=urlbase+Nit
        r=requests.get(url,params=Nit)
        data=r.json()
        for a in data:
            return (a['nombre']+" "+a['apellido'])
    else:
        return render_template('/consulta.html')       

@app.route('/Registrocliente',methods=['POST','GET'])
def regcliente():
    print('hola')

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


@app.route('/Registropago',methods=['POST','GET'])
def regpago():
    if request.method=='POST':
        idfactura= request.form['idfactura']
        idcliente= request.form['idcliente']
        correlativo= request.form['correlativo']
        transaccion= request.form['transaccion']
        nomtarj= request.form['nom_tarj']
        fecha= request.form['fecha']
        auditoria= request.form['auditoria']
        autorizacion= request.form['autorizacion']
        referencia= request.form['referencia']
        reftarj= request.form['reftarj']
        deposito=request.form['deposito']
        banco=request.form['banco']
        if correlativo and idfactura and transaccion and nomtarj and fecha and auditoria and autorizacion and referencia and reftarj and idcliente:
            urlbase="http://localhost:5000/api/Cliente/pagos"
            datospago={
                "correlativo": correlativo,
                "Id_factura": idfactura,
                "metodo": {
                    "No_transaccion": transaccion,
                    "Nombre_tarjeta": nomtarj,
                    "Fecha": fecha,
                    "No_Auditoria": auditoria,
                    "No_Autorizacion": autorizacion,
                    "No_Referencia": referencia,
                    "Referencia_tarjeta": reftarj,
                    },
                "Id_cliente": idcliente,
                    }
            headers={'Content-Type':'application/json'}
            response =json_util.dumps(datospago)
            r=requests.request("POST",urlbase,headers=headers,data=response)
            print(r.text)
            return("Pago Registrado")
        else:
            if correlativo and idfactura and deposito and banco and idcliente:
                urlbase="http://localhost:5000/api/Cliente/pagos"
                datospago={
                "correlativo": correlativo,
                "Id_factura": idfactura,
                "metodo": {
                    "Deposito": deposito,
                    "Banco": banco,
                    "Fecha": fecha
                    },
                "Id_cliente": idcliente,
                    }
                headers={'Content-Type':'application/json'}
                response =json_util.dumps(datospago)
                r=requests.request("POST",urlbase,headers=headers,data=response)
                print(r.text)
                return("Pago Registrado")
            else:
                print("No hay datos")
                return("No hay datos")
    else:
        return render_template('/registropago.html')

@app.route('/Anularpago')
def anular():
    correlativo= request.form['correlativo']
    razon= request.form['razon']
    return render_template('/anularpago.html') 

@app.route('/Factura',methods=['POST','GET'])
def emitirfac():
    if request.method=='POST':
        Id_factura= request.form['Id_factura']
        fecha= request.form['fecha']
        Nit= request.form['Nit']
        Id_producto= request.form['Id_Producto']
        valoru= request.form['valoru']
        motivo= request.form['motivo']
        cantidad= request.form['cantidad']
        total= request.form['total']
        observaciones= request.form['observaciones']
        if Id_factura and Nit and fecha and motivo and total and observaciones:
            urlbase="http://localhost:5000/api/Cliente/factura"
            datosfac={
                "Id_factura":Id_factura,
                "fecha":fecha,
                "NIT":Nit,
                "motivo":motivo,
                "total":total,
                "observaciones":observaciones
            }
            headers={'Content-Type':'application/json'}
            response =json_util.dumps(datosfac)
            r=requests.request("POST",urlbase,headers=headers,data=response)
            print(r.text)
            #flash('Factura Registrada Exitosamente')
            if Id_producto and Id_factura and valoru and cantidad:
                urlbase1="http://localhost:5000/api/Cliente/detallefactura"
                datosdetfac={
                    "Id_factura":Id_factura,
                    "Id_producto":Id_producto,
                    "valorunitario":valoru,
                    "cantidad":cantidad
                }
                headers={'Content-Type':'application/json'}
                response =json_util.dumps(datosdetfac)
                r2=requests.request("POST",urlbase1,headers=headers,data=response)
                print(r2.text)
                print('Factura registrada exitosamente')
                return render_template('/emitirfactura.html')
            else:
                print("Falta llenar campos")
                return render_template('/emitirfactura.html') 
        else:
            print('Faltan llenar campos')
            return render_template('/emitirfactura.html')     
    else:
        return render_template('/emitirfactura.html')        

@app.route('/Estadocuenta',methods=['GET','POST'])
def estadocuenta():
    if request.method=='POST':
        Nit=request.form['nit']
        urlbase="http://localhost:5000/api/Cliente/Cliente,"
        url=urlbase+Nit
        r=requests.get(url,params=Nit)
        data2=r.json()
        return(data2)
    else:
        return render_template('/estadocuenta.html')    

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
    app.run(port=2000)