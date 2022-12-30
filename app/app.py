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


@app.route('/', methods = ["GET", "POST"])
def index():
    try:
        return render_template('index.html')
    except:
        return render_template('error.html')
    
    
    
    
@app.errorhandler(404)
def pageNotFount(error):
    return render_template('error.html', title="Страница не найдена")
    

if __name__ == '__main__':
   app.run(debug = True)
