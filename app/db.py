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