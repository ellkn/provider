from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import db as db
import user as u
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
import logging


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOPSECRETKEY'
login_manager = LoginManager()
login_manager.init_app(app)

logging.basicConfig(filename="logs/info.log", filemode='a', level=logging.INFO, format='%(asctime)s | %(message)s')
logging.basicConfig(filename="logs/error.log", filemode='a', level=logging.ERROR)

@login_manager.user_loader
def load_user(user_id):
    return u.UserLogin().dbi(user_id)


@app.route('/')
def index():
    try:
        return render_template('index.html')
    except:
        return render_template('error.html')
    


@app.route('/menu')
def menu():
    try:
        return render_template('menu.html')
    except:
        return render_template('error.html')


@app.route('/content', methods = ["GET", "POST"])
def content():
    try:
        return render_template('content.html')
    except:
        return render_template('error.html')


@app.route('/login', methods = ["GET", "POST"])
def login():
    try:
        if not current_user.get_id():
            if request.method == 'POST':
                user = db.getUserByEmail(request.form.get("email"))
                if user:
                    if db.checkUser(user['password'], request.form.get("password")):
                        login_user(u.UserLogin().create(user))
                        flash("Успешный вход")
                        return redirect("/")
                    else:
                        flash("Неверный логин или пароль")
                        return render_template('login.html')
                return render_template('login.html')
            
            return render_template('login.html')
        else:
            return redirect("/")
    except:
        return render_template('error.html')
    
    
@app.route('/logout')
@login_required
def logout():
    if current_user.get_id():
        logout_user()
        return redirect("/")
    else:
        return redirect("/") 
    
    
@app.route('/registration', methods = ["GET", "POST"])
def registration():
    try:
        if current_user.is_authenticated:
            return redirect('/')
        else:
            if request.method == 'POST':
                db.createUser(request.form.get('email'), request.form.get('password'), request.form.get('lastname'), request.form.get('name'), request.form.get('phone'))
                return redirect('/login')
            return render_template('registration.html')
    except:
        return render_template('error.html')


@app.route('/banks')
def banks():
    try:
        bank = db.getBanks()
        return render_template('banks.html', bank = bank)
    except:
        return render_template('error.html')
        
    
@app.route('/createOrder',  methods = ["GET", "POST"])
def createOrder():
    try:
        if current_user.is_authenticated:
            users = db.getUsersU() 
            goods = db.getGoods()
            goddtypes = db.getGoodTypes()
            if request.method == 'POST':
                if current_user.get_role() == 'ADMIN'  or current_user.get_role() == 'PROVIDER':
                    if request.form.get("good") == "-1" or request.form.get("user") == "-1":
                        flash("Введите корректные данные")
                    else:
                        db.createOrder(request.form.get("user"), request.form.get("good"))
                        flash('Заказ создан')
                        return redirect('/orders')
                elif current_user.get_role() == 'USER':
                    if request.form.get("good") == "-1":
                        flash("Введите корректные данные")
                    else:
                        db.createOrder(current_user.get_id(), request.form.get("good"))
                        flash('Заказ создан')
                        return redirect('/orders')
            return render_template('createOrder.html', users = users, good = goods, goddtypes = goddtypes)
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/content')  
    except:
        return render_template('error.html')    


@app.route('/providers')
def providers():
    try:
        prov = db.getProviders()
        goods = db.getGoods()
        types = db.getGoodTypes()
        return render_template('providers.html', providers = prov, goods = goods, types = types)
    except:
        return render_template('error.html')


@app.route('/users')
def users():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN':
            users = db.getUsers()
            return render_template('user.html', users = users)
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/content')
    except:
        return render_template('error.html')
    

@app.route('/edit/<id>', methods = ["GET", "POST"])
def edit(id):
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN':
            user = db.getUserById(id)
            role = db.getRoles()
            if request.method == "POST":
                if request.form.get("role") == "-1":
                    flash("Введите корректные данные")
                else:
                    if db.getAdminsCount()[0][0] == 1 and request.form.get("role") ==2 or db.getAdminsCount()[0][0] == 1 and request.form.get("role") == 3:
                        flash("Вы не можете изменить роль у единственного пользователя с ролью ADMIN")
                    else:
                        db.editUser(request.form.get("email"), request.form.get("lastname"), request.form.get("firstname"), request.form.get("phone"), request.form.get("role"), id)
                    return render_template('edit.html', user = user, role = role)  
                
            return render_template('edit.html', user = user, role = role)   
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/content')  
    except:
        return render_template('error.html')
    
    
@app.route('/orders')
def orders():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN':
            orders = db.getOrders()
            return render_template('orders.html', orders = orders)
        elif current_user.is_authenticated and current_user.get_role() == 'USER' or current_user.get_role() == 'PROVIDER':
            orders = db.getUserOrders(current_user.get_id())
            return render_template('orders.html', orders = orders)
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/content')
    except:
        return render_template('error.html')    
    
    
@app.route('/editOrder/<id>', methods = ["GET", "POST"])
def editOrder(id):
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN' or current_user.get_role() == 'PROVIDER':
            status = db.getStatus()
            order = db.getOrder(id)
            if request.method == "POST":
                print(request.form.get("status") )
                if request.form.get("status") == "-1":
                    flash("Введите корректные данные")
                else:
                    db.editOrder(id, request.form.get("status"))
                    return redirect('/orders')
                
            return render_template('editOrder.html', status = status, tr = order)   
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/content')  
    except:
        return render_template('error.html')
    
    
@app.route('/addCategory', methods = ["GET", "POST"])
def addCategory():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN' or current_user.get_role() == 'PROVIDER':
            if request.method == 'POST':
                db.addTypeGood(request.form.get("name"))
                flash('Категория товара добавлена')
                return redirect('/providers')
            return render_template("addCategory.html")
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/content')  
    except:
        return render_template('error.html')
    
    
@app.route('/addGood', methods = ["GET", "POST"])
def addGood():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN' or current_user.get_role() == 'PROVIDER':
            goodtypes = db.getGoodTypes()
            provs = db.getProviders()
            if request.method == 'POST':
                if request.form.get("type") == "-1" :
                    flash("Введите корректные данные")
                else:
                    db.addGood(request.form.get("name"), request.form.get("price"), request.form.get("type"), request.form.get("prov"))
                    flash('Товар добавлен')
                    return redirect('/providers')
            return render_template("addGood.html", type = goodtypes, provs = provs)
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/content')  
    except:
        return render_template('error.html')


@app.route('/addBank', methods = ["GET", "POST"])
def addBank():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN':
            if request.method == 'POST':
                db.addBank(request.form.get("name"))
                return redirect('/banks')
            return render_template("addBank.html")
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/content')  
    except:
        return render_template('error.html')
    
    
@app.route('/addBankRelation', methods = ["GET", "POST"])
def addBankRelation():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN' :
            bank = db.getBanks()
            users = db.getUsers()
            if request.method == 'POST':
                if request.form.get("banks") == "-1" or request.form.get("user") == "-1":
                    flash("Введите корректные данные")
                else:
                    db.addBankRelation(request.form.get("banks"), request.form.get("user"))
                    return redirect('/banks')
            return render_template("addBankRelation.html", users = users, bank = bank)
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/content')  
    except:
        return render_template('error.html')


@app.route('/relations')
def relations():
    try:
        relationsProvider = db.getBankRelationForProv()
        relationsUser = db.getBankRelationForUser()
        return render_template('relations.html', relationsProvider = relationsProvider, relationsUser = relationsUser)
    except:
        return render_template('error.html')


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('error.html', title="Страница не найдена")
    

if __name__ == '__main__':
   app.run(debug = True)
