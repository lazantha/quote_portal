from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "mysecretkey"
db = SQLAlchemy(app)
migrate=Migrate(app,db)
csrf = CSRFProtect(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')



from forms import UserLoginForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=UserLoginForm()
    return render_template('login.html',form=form)


from forms import UserRegisterForm
@app.route('/register', methods=['GET', 'POST'])
def register():
    form=UserRegisterForm()

    return render_template('register.html',form=form)





if __name__ == '__main__':
    app.run(debug=True)