import psycopg2
from flask import flash
import user as u
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import logging

def getData(query):
    try:
        connection = psycopg2.connect(host='localhost', user='postgres', password='1606', dbname='provider', port=5432)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except (Exception, psycopg2.DatabaseError) as ex:
        logging.ERROR(ex)
        print(ex)
    finally:
        connection.close()


def setData(query):
    try:
        connection = psycopg2.connect(host='localhost', user='postgres', password='1606', dbname='provider', port=5432)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as ex:
        logging.ERROR(ex)
        print(ex)
    finally:
        connection.close()
        
        
def getUserById(id):
    try:
        user = getData(f"SELECT u.id, u.email, u.password, u.lastname, u.firstname, u.phone, r.role from users u join roles r on u.role = r.id and u.id = {id}")
        if user != []:
            person = u.User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][5], user[0][6])
            return {'id': person.id, 'email': person.email, 'password': person.password, 'lastname': person.lastname, 'firstname': person.firstname, 'phone': person.phone,'role': person.role}
        else:
            return False
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getUserByEmail(email):
    try:
        user = getData(f"SELECT u.id, u.email, u.password, u.lastname, u.firstname, u.phone, r.role from users u join roles r on u.role = r.id and  u.email = '{email}'")
        if user != []:
            person = u.User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][5],  user[0][6])
            return  {'id': person.id, 'email': person.email, 'password': person.password, 'lastname': person.lastname, 'firstname': person.firstname, 'phone': person.phone,'role': person.role}
        else: 
            return False
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def createUser(login, password, firstname, lastname, phone ):
    password_hash = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
    try:
        setData(f'INSERT INTO users ( email, password, lastname, firstname, phone, role) VALUES { login, password_hash, lastname, firstname, phone, 3}')
        flash('Пользователь успешно добавлен!')
    except Exception as error:
        logging.error(error)
        flash('Пользователь с таким email существует!')
        print(error)
        
        
def checkUser(password_hash, password):
    try:
        return check_password_hash(password_hash, password)
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getUsers():
    try:
        return getData("select u.id, u.email, u.lastname, u.firstname, u.phone, r.role from users u join roles r on r.id = u.role")
    except Exception as ex:
        logging.error(ex)
        print(ex)
    
    
def getProviders():
    try:
        return getData("select u.id, u.email, u.lastname, u.firstname, u.phone, r.role from users u join roles r on r.id = u.role where u.role = 2")
    except Exception as ex:
        logging.error(ex)
        print(ex)
        

def getRoles():
    try:
        return getData(f'SELECT * FROM roles')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getAdminsCount():
    try:
        return getData(f'SELECT count(*) FROM users WHERE role = 1')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getStatus():
    try:
        return getData("select * from status")
    except Exception as ex:
        logging.error(ex)
        print(ex)    
        

def addTypeGood(type):
    try:
        setData(f"INSERT INTO categorys (type) VALUES ('{type}')")
    except Exception as ex:
        print(ex)
        logging.error(ex)
        

def addGood(name, price, type_id, user_id):
    try:
        setData(f"INSERT INTO goods (name, price, category, prov) VALUES {name, price, type_id, user_id}")
    except Exception as ex:
        print(ex)
        logging.error(ex)
        

def getOrders():
    try:
        return getData("select o.id, u.email, u.lastname, u.firstname, u.phone, g.name, g.price, c.category, o.datetime from orders o join users u on u.id = o.user_id join goods g on o.good_id = g.\"id \" join category c on g.category = c.id")
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getUserOrders(user_id):
    try:
        return getData(f"select o.id, u.email, u.lastname, u.firstname, u.phone, g.name, g.price, c.category, o.datetime from orders o join users u on u.id = o.user_id join goods g on o.good_id = g.\"id \" join category c on g.category = c.id WHERE o.user_id = {user_id}")
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getOrder(id):
    try:
        return getData(f"select o.*, st.status from orders o join status st on st.id = o.status where o.id = {id}")
    except Exception as ex:
        logging.error(ex)
        print(ex)
        

def editUser(email, lastname, firstname, phone, role, id):
    try:
        setData(f"UPDATE users SET email = '{email}',  lastname = '{lastname}', firstname = '{firstname}', phone = '{phone}', role = {role} WHERE id = {id}")
    except Exception as ex:
        print(ex)
        logging.error(ex)
