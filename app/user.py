from flask_login import UserMixin
import db as db

class User:
    def __init__(self, id, email, password, lastname, firstname, phone, role):
        self.id = id
        self.email = email
        self.password = password
        self.lastname = lastname
        self.firstname = firstname
        self.phone = phone
        self.role = role
        
        
class Role:
    def __init__(self, role):
        self.id = id
        self.role = role


class UserLogin(UserMixin):
       
    def dbi(self, user_id):
        self.__user = db.getUserById(user_id)
        return self
    
    def create(self, user):
        self.__user = user
        return self
     
    def is_authenticated():
        return True
    
    def is_active():
        return True
    
    def is_anonymous():
        return False
    
    def get_id(self):
        if self.__user:
            return self.__user['id']
        else:
            return False
        
    def get_role(self):
        if self.__user:
            return self.__user['role']
        else:
            return False
